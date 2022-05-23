import datetime
from pyexpat import model
import django
from django.forms.widgets import DateInput, TimeInput
from django.http import JsonResponse
from django.http.response import Http404, HttpResponse

import users
from eventify.ViewExtentions import OverRideDeleteView
from .models import  Post, Comment, RegisterService,Service,ServiceComment,RegisterEvent,Approved
from users.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm, ServiceForm
from django.http import JsonResponse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import date
from actstream.actions import follow, unfollow, action
from actstream.models import user_stream, Action, following, followers
from datetime import date, timezone
from datetime import timedelta
from notifications.signals import notify
from notifications.models import Notification
import requests
import operator
import functools

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.http import JsonResponse

class PostListView(ListView):
    model = Post
    template_name = 'eventify/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        my_list = []
        try:
            keyword = self.request.GET['q']
            cat = self.request.GET['cat']
            km=self.request.GET['km']
        except:
            keyword = ''
            cat='all'
            km='all'

        if keyword != '' and cat=="all":
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
            wiki_items = search(keyword)
            condition = functools.reduce(operator.or_, [Q(content__icontains=wiki_item) | Q(title__icontains=wiki_item) for wiki_item in wiki_items])
            object_list2 = self.model.objects.filter(condition)
            object_list=object_list|object_list2
        elif keyword == '' and cat!="all":
            object_list = self.model.objects.filter(category=cat)
                    
        elif keyword != '' and cat!="all":
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword) & Q(category__icontains=cat))
            wiki_items = search(keyword)
            condition = functools.reduce(operator.or_, [Q(content__icontains=wiki_item) | Q(title__icontains=wiki_item) for wiki_item in wiki_items])
            object_list2 = self.model.objects.filter(condition)
            object_list=object_list|object_list2
                
        elif keyword=='' and cat=='all':
            object_list = self.model.objects.all()

        for item in object_list:
            try:
                item.tempLocation=round(geodesic(item.location, self.request.user.profile.location).km,2)
            except:
                item.tempLocation="Not calculated yet"     

        if km!='all':
            for item in object_list:
                if item.tempLocation<float(km):
                    my_list.append(item)
            return my_list
        else:
            return object_list

class FeedView(LoginRequiredMixin,ListView):
    model = Action
    template_name = 'eventify/feed.html'
    context_object_name = 'stream'
    paginate_by = 10

    def get_queryset(self):
        stream = user_stream(self.request.user)
        my_list = []
        for stream_item in stream:
            my_list.append(stream_item)
        return my_list

class NotificationsListView(ListView):
    model = Notification
    template_name = 'eventify/notifications_list.html'
    context_object_name = 'instance'

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user.id)
        qs.mark_all_as_read()
        return qs
        
class ServiceListView(ListView):
    model = Service
    template_name = 'eventify/services.html'
    context_object_name = 'services'
    paginate_by = 4

    def get_queryset(self):
        my_list = []
        try:
            keyword = self.request.GET['q']
            cat = self.request.GET['cat']
            km=self.request.GET['km']
        except:
            keyword = ''
            cat='all'
            km='all'

        if keyword != '' and cat=="all":
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword),IsCancelled=False)
            wiki_items = search(keyword)
            condition = functools.reduce(operator.or_, [Q(content__icontains=wiki_item) | Q(title__icontains=wiki_item) for wiki_item in wiki_items])
            object_list2 = self.model.objects.filter(condition)
            object_list=object_list|object_list2
        elif keyword == '' and cat!="all":
            object_list = self.model.objects.filter(category=cat,IsCancelled=False)
                    
        elif keyword != '' and cat!="all":
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword)) & Q(category__icontains=cat,IsCancelled=False,)
            wiki_items = search(keyword)
            condition = functools.reduce(operator.or_, [Q(content__icontains=wiki_item) | Q(title__icontains=wiki_item) for wiki_item in wiki_items])
            object_list2 = self.model.objects.filter(condition)
            object_list=object_list|object_list2

        elif keyword=='' and cat=='all':
            object_list = self.model.objects.filter(IsCancelled=False)

        for item in object_list:
            try:
                item.tempLocation=round(geodesic(item.location, self.request.user.profile.location).km,2)
            except:
                item.tempLocation="Not calculated yet"    
            
        if km!='all':
            for item in object_list:
                if item.tempLocation<float(km):
                    my_list.append(item)
            return my_list
        else:
            return object_list

def search(keyword):
    result = []

    url = 'https://query.wikidata.org/sparql'
    query = '''
    SELECT distinct ?itemLabel ?linkcount #?classLabel ?typeLabel
    WHERE {
      {
        SELECT ?class ?searched_item
        WHERE {
          {
            SELECT ?searched_item {
              SERVICE wikibase:mwapi {
                bd:serviceParam wikibase:api "EntitySearch".
                bd:serviceParam wikibase:endpoint "www.wikidata.org".
                bd:serviceParam mwapi:search "''' + keyword + '''".
                bd:serviceParam mwapi:language "en".
                ?searched_item wikibase:apiOutputItem mwapi:item.
                ?num wikibase:apiOrdinal true.
              }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
            }
            LIMIT 5
          }
          hint:Prior hint:runFirst true .
          ?searched_item wdt:P279 ?class .
          ?searched_item wdt:P31 ?type .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
      }
      hint:Prior hint:runFirst true .
      ?item wdt:P279 ?class .
      ?item wdt:P31 ?type .
      ?item wikibase:sitelinks ?linkcount .
      FILTER(?linkcount > 50).
      FILTER(?item != ?searched_item).
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    ORDER BY ASC(?class) ASC(?type) DESC(?linkcount)
    '''
    
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()
    for r in data["results"]["bindings"]:
        result.append(r["itemLabel"]["value"])

    return result

class UserListView(ListView):
    model = User
    template_name = 'eventify/profiledetail.html'
    context_object_name = 'object'


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return User.objects.get(id=user.id)

# class UserServiceListView(ListView):
#     model = Service
#     template_name = 'eventify/user_services.html'
#     context_object_name = 'services'
#     paginate_by = 5

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Service.objects.filter(author=user).order_by('-date_posted')
    

class PostDetailView(LoginRequiredMixin,DetailView):
    context_object_name = 'object'
    model = Post

    def get_context_data(self, **kwargs):
        geolocator = Nominatim(user_agent="arcan")
        pk=self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        event=Post.objects.get(id=pk)
        if event.eventdate < date.today():
            event.isLate=True
        location = geolocator.reverse(event.location,timeout=20)
        context['registerevent'] = RegisterEvent.objects.filter(post_id=pk,approved_register=True)
        context['unRegister'] = RegisterEvent.objects.filter(post_id=pk,author_id=self.request.user.id,approved_register=True)
        context['address']=location.address
        context['isLate']=event.isLate
        return context


class ServiceDetailView(LoginRequiredMixin,DetailView):
    context_object_name = 'object'
    model = Service

    def get_context_data(self, **kwargs):
        pk=self.kwargs['pk']
        geolocator = Nominatim(user_agent="arcan")
        service=Service.objects.get(id=pk)
        if service.eventdate < date.today():
           service.isLate=True
        elif service.eventdate == date.today() and service.eventtime < (datetime.datetime.now()+datetime.timedelta(hours=1)).time():
            service.isLate=True

        location = geolocator.reverse(service.location,timeout=20)
        context = super().get_context_data(**kwargs)
        context['registerservice'] = RegisterService.objects.filter(service_id=pk,approved_register=True)
        service.currentAtt= RegisterService.objects.filter(service_id=pk,approved_register=True).count()
        service.save()
        context['unRegister'] =RegisterService.objects.filter(service_id=pk,author_id=self.request.user.id,approved_register=False)
        context['approved'] =RegisterService.objects.filter(service_id=pk,author_id=self.request.user.id,approved_register=True)
        context['address']=location.address
        context['isLate']=service.isLate
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        event = form.save()
        action.send(self.request.user, verb="created an event", target=event)
        return super().form_valid(form)

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        service = form.save()
        action.send(self.request.user, verb="created a service", target=service)
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','duration','eventdate','eventtime','capacity','location','content','picture']
    widgets = {
            'eventdate':DateInput(attrs={'type': 'date'}),
            'eventtime':TimeInput(attrs={'type': 'time'}),
        }

    def form_valid(self, form):
        form.instance.author = self.request.user
        action.send(self.request.user, verb="updated an event", target=form.instance)
        attendees_ids = RegisterEvent.objects.filter(post_id=form.instance.id).values('author_id')
        if attendees_ids is not None:
            attendees = User.objects.filter(id__in=attendees_ids)
            sender = self.request.user
            receiver = attendees
            notify.send(sender, recipient=receiver, verb='updated by', target=form.instance)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    fields = ['title','duration','eventdate','category','eventtime','capacity','location','content','picture']
    widgets = {
            'eventdate':DateInput(attrs={'type': 'date'}),
            'eventtime':TimeInput(attrs={'type': 'time'}),
        }

    def form_valid(self, form):
        form.instance.author = self.request.user
        action.send(self.request.user, verb="updated service", target=form.instance)
        attendees_ids = RegisterService.objects.filter(service_id=form.instance.id).values('author_id')
        if attendees_ids is not None:
            attendees = User.objects.filter(id__in=attendees_ids)
            sender = self.request.user
            receiver = attendees
            notify.send(sender, recipient=receiver, verb='updated by', target=form.instance)
        return super().form_valid(form)

    def test_func(self):
        service = self.get_object()
        if self.request.user == service.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'eventify/about.html', {'title': 'About'})

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, OverRideDeleteView):
    model = Service
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user_id'))
        text = request.POST.get('text')
        Comment(author=user, post=post, text=text).save()
        messages.success(request, "Your comment has been added successfully.")
    else:
        return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)

@login_required
def approved(request, pk):
    app=None
    count=None
    service = get_object_or_404(Service, pk=pk)
    user = User.objects.get(id=request.POST.get('user_id'))
    if request.method == 'POST' and service.author_id==user.id:
        if service.author_id==user.id and service.isGiven==False:
            service.isGiven=True
            service.save()
            appr=Approved.objects.filter(service_id=service.id,isOk=False)
            if appr.exists():
                for item in appr:
                    senderUser=User.objects.get(id=item.author_id)
                    xowner=User.objects.get(id=service.author_id)
                    if item.isOk==False:
                        senderUser.profile.reserved-=service.duration
                        senderUser.save()
                        item.isOk=True
                        item.save()
                        if service.paid==False:
                            xowner.profile.credits+=service.duration
                            service.paid=True
                            service.save()
                            xowner.save()


            messages.success(request, "Successfully confirmed")
        else:
            service.isGiven=False
            service.save()
            messages.success(request, "Successfully Cancelled")


    elif  request.method == 'POST':

        try:
            app=Approved.objects.get(author_id=user.id,service_id=service.id)
            count=1
        except:
            app=Approved(author=user, service=service).save()
            approved(request, pk)

        if app and app.isOk==False and service.isGiven==True:
            user.profile.reserved-=service.duration
            user.save()
            app.isOk=True
            app.save()
            owner=User.objects.get(id=service.author_id)
            if service.paid==False:
                 owner.profile.credits+=service.duration
                 owner.save()
                 service.paid=True
                 service.save()
                 return redirect('service_detail', pk=pk)  

    else:    
        messages.warning(request, "You already confirmed") 
        return redirect('service_detail', pk=pk)
    if count==1:
         messages.warning(request, "You already confirmed")   
    return redirect('service_detail', pk=pk)

@login_required
def add_servicecomment(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user_id'))
        text = request.POST.get('text')
        ServiceComment(author=user, service=service, text=text).save()
        messages.success(request, "Your comment has been added successfully.")
    else:
        return redirect('service_detail', pk=pk)
    return redirect('service_detail', pk=pk)

@login_required
def register_event(request, pk):
    post= get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        ids=request.POST.get('user_id')
        post_id=request.POST.get('post_id')
        user = User.objects.get(id=request.POST.get('user_id'))
        try:
            event=RegisterEvent.objects.filter(author_id=ids,post_id=post_id)
            if event:
                messages.warning(request, "You already registered event")
                return redirect('post_detail', pk=pk)

        except:
            pass
        RegisterEvent(author=user, post=post,title=post.title,username=user.username).save()
        # action.send(request.user, verb="registered event", target=event)
        messages.success(request, "You register event successfully")
        return redirect('post_detail', pk=pk) 
       
    else:
        return redirect('post_detail', pk=pk)

@login_required
def unregister_event(request, pk):
    post= get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        ids=request.POST.get('user_id')
        post_id=request.POST.get('post_id')
        event = RegisterEvent.objects.filter(author_id=ids,post_id=post_id)
        event.delete()
        # action.send(request.user, verb="unregistered event", target=event)
        messages.success(request, "Successfully cancelled application")    
        return redirect('post_detail', pk=pk)
    else:
        return redirect('post_detail', pk=pk)

@login_required
def follow_unfollow_user(request, username):
    other_user = get_object_or_404(User, username=username)
    if request.method == 'POST': 
        if 'unfollow' in request.POST:
            unfollow(request.user, other_user)
        elif 'follow' in request.POST:
            follow(request.user, other_user, actor_only=False)
        return redirect('profiledetail', username=username)
    else:
        return redirect('profiledetail', username=username)

@login_required
def register_service(request, pk):
    service= get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        ids=request.POST.get('user_id')
        service_id=request.POST.get('service_id')
        user = User.objects.get(id=request.POST.get('user_id'))
        try:
            event=RegisterService.objects.filter(author_id=ids,service_id=service_id)
            if event:
                messages.warning(request, "You already registered service")
                return redirect('service_detail', pk=pk)
        except:
            pass
        profile=Profile.objects.get(user_id=user.id)
        credit=profile.credits-service.duration
        capacityControl=RegisterService.objects.filter(service_id=service_id).count()
        if service.capacity <= capacityControl:
            messages.warning(request, "The service reached enough participants")
            return redirect('service_detail', pk=pk)
        else:    
            if credit<0:
                messages.warning(request, "Not enough credits")
                return redirect('service_detail', pk=pk)
            else:
                RegisterService(author=user, service=service,title=service.title,owner=service.author.id, username=user.username).save()
                user.profile.credits-=service.duration
                user.profile.reserved+=service.duration
                user.save()
                action.send(request.user, verb="sent registration request", target=service)
                messages.success(request, "Registration request sent successfully")
                return redirect('service_detail', pk=pk) 
       
    else:
        return redirect('service_detail', pk=pk)

@login_required
def unregister_service(request, pk):
    service= get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        ids=request.POST.get('user_id')
        service_id=request.POST.get('service_id')
        RegisterService.objects.filter(author_id=ids,service_id=service_id).delete()
        user=User.objects.get(id=ids)
        user.profile.credits+=service.duration
        user.profile.reserved-=service.duration
        user.save()
        action.send(request.user, verb="unregistered", target=service)
        messages.success(request, "Successfully cancelled application")    
        return redirect('service_detail', pk=pk)
    else:
        return redirect('service_detail', pk=pk)

# @login_required
# def addfriend(request, pk):
#     if request.method == 'POST':
#         ids=request.POST.get('user_id')
#         AddFriend(user=pk,friend=ids).save()
#         messages.success(request, "Successfully cancelled application")    
#         return redirect('service_detail', pk=pk)
#     else:
#         return redirect('service_detail', pk=pk)     


# @login_required
# def follower_list_view(request, username):
#     followers_list = followers(request.user)
#     print(followers_list)
    
#     return redirect('followers_list', username=username)

# @login_required
# def following_list_view(request, username):
#     following_list = following(request.user)
#     print(following_list)
    
#     return redirect('following_list', username=username)




class FollowersView(ListView):
    model = Action
    template_name = 'users/followers_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username=self.kwargs.get('username')
        if(username == ''):
            followers_var = followers(self.request.user)
        else:
            followers_var = followers(User.objects.get(username=username))

        followers_var = followers(User.objects.get(username=username))
        followers_list = []
        for stream_item in followers_var:
            followers_list.append(stream_item)
        context = {
            'username': username,
            'followers_list' : followers_list

        }
       
        return context


class FollowingView(ListView):
    model = Action
    template_name = 'users/following_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username=self.kwargs.get('username')
        if(username == ''):
            following_var = following(self.request.user)
        else:
            following_var = following(User.objects.get(username=username))

        following_list = []
        for stream_item in following_var:
            following_list.append(stream_item)
        context = {
            'username': username,
            'following_list' : following_list

        }
       
        return context

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
   
    def get(self, request, format = None):
        labels = [
            'January',
            'February', 
            'March', 
            'April', 
            'May', 
            'June', 
            'July'
            ]
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45]
        data ={
                     "labels":labels,
                     "chartLabel":chartLabel,
                     "chartdata":chartdata,
             }
        return render (request, 'eventify/index_chart.html', {})



def pie_chart_category_active_render(request):
     return render(request, 'eventify/index_chart_2.html')
     
def pie_chart_category_active(request):
    labels = []
    data = []

    #queryset = Service.objects.order_by('-currentAtt')[:5]
    queryset = Service.objects.values('category').annotate(attendee_sum = Sum('currentAtt')).order_by('-attendee_sum')
    print("I am here",queryset)
    for service_loop in queryset:
        labels.append(service_loop['category'])
        data.append(service_loop['attendee_sum'])

    return JsonResponse(data= {
        'labels': labels,
        'data': data,
    })

import datetime
from itertools import count
from multiprocessing import context
from pyexpat import model
from tracemalloc import start
from unicodedata import category
import django
from django.forms.widgets import DateInput, TimeInput
from django.http import JsonResponse, QueryDict
from django.http.response import Http404, HttpResponse

import users
from eventify.ViewExtentions import OverRideDeleteView
from .models import  Post, Comment, RegisterService,Service, ServiceChart,ServiceComment,RegisterEvent,Approved, UserChart
from users.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import EventChartForm, PostForm, ServiceChartForm, ServiceForm,EventChartForm, UserChartForm

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

from django.db.models import Count

class PostListView(ListView):
    model = Post
    template_name = 'eventify/index.html'
    # context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        my_list = []
        object_list2 = []
        try:
            keyword = self.request.GET['q']
            cat = self.request.GET['cat']
            km=self.request.GET['km']
        except:
            keyword = ''
            cat='all'
            km='all'
        
        if keyword != '':
            wiki_items = search(keyword)
            if wiki_items:
                condition = functools.reduce(operator.or_, [Q(content__icontains=wiki_item) | Q(title__icontains=wiki_item) for wiki_item in wiki_items])
                object_list2 = self.model.objects.filter(condition)

        if keyword != '' and cat=="all":
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))            

        elif keyword == '' and cat!="all":
            object_list = self.model.objects.filter(category=cat)
                    
        elif keyword != '' and cat!="all":
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword) & Q(category__icontains=cat))
                
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
            sortedList = sorted(my_list, key=lambda x: x.tempLocation)
            context['posts'] = sortedList
            context['paginate_by'] = 5
            context['wikiresult'] = object_list2
            return context
        else:
            sortedList = sorted(object_list, key=lambda x: x.tempLocation)
            context['posts'] = sortedList
            context['paginate_by'] = 5
            context['wikiresult'] = object_list2      
            return context

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
    # context_object_name = 'services'
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        my_list = []
        object_list2 = []
        try:
            
            keyword = self.request.GET['q']
            cat = self.request.GET['cat']
            km=self.request.GET['km']
        except:
            keyword = ''
            cat='all'
            km='all'
        
        # get promoted services
        all_objects = self.model.objects.filter(IsCancelled=False)
        promoted_objects=all_objects.filter(isPromoted=True)

        if keyword != '':
            wiki_items = search(keyword)
            if wiki_items:
                condition = functools.reduce(operator.or_, [Q(content__icontains=wiki_item) | Q(title__icontains=wiki_item) for wiki_item in wiki_items])
                object_list2 = self.model.objects.filter(condition, IsCancelled=False, isPromoted=False)

        if keyword != '' and cat=="all":
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword),IsCancelled=False, isPromoted=False)
           
        elif keyword == '' and cat!="all":
            object_list = self.model.objects.filter(category=cat,IsCancelled=False, isPromoted=False)
                    
        elif keyword != '' and cat!="all":
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword) & Q(category__icontains=cat),IsCancelled=False, isPromoted=False)

        elif keyword=='' and cat=='all':
            object_list = self.model.objects.filter(IsCancelled=False, isPromoted=False)

        for item in object_list:
            try:
                item.tempLocation=round(geodesic(item.location, self.request.user.profile.location).km,2)
            except:
                item.tempLocation="Not calculated yet"    
        #  <QuerySet [<Service: Badminton>, <Service: test>]>
        #     [<Service: Badminton>, <Service: test>]

        if km!='all':
            for item in object_list:
                if item.tempLocation<float(km):
                    my_list.append(item)
            sortedList = sorted(my_list, key=lambda x: x.tempLocation)            
            context['services'] = my_list
            context['paginate_by'] = 4
            context['promotedservices'] = promoted_objects      
            context['wikiresult'] = object_list2    
            return context
        else:
            sortedList = sorted(object_list, key=lambda x: x.tempLocation)
            context['services'] = sortedList
            context['paginate_by'] = 4
            context['promotedservices'] = promoted_objects      
            context['wikiresult'] = object_list2
            return context

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
@login_required    
def manager(request):
    return render(request, 'eventify/manager.html', {'title': 'manager'})

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
def follow_unfollow_user(request, username, abc, activeuser):
    other_user = get_object_or_404(User, username=username)
    if request.method == 'POST': 
        if 'unfollow' in request.POST:
            unfollow(request.user, other_user)
        elif 'follow' in request.POST:
            follow(request.user, other_user, actor_only=False)

        if abc == 'True':
            return redirect('followers_list', username=activeuser)
            
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

                sender = request.user
                receiver = service.author
                notify.send(sender, recipient=receiver, verb='service is applied by', target=service)

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

class ServicePromoteListView(LoginRequiredMixin,ListView):
    context_object_name = 'object'
    model = Service
    template_name = 'eventify/service_promote_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            keyword=self.request.GET['a']
        except:
            keyword=100  
        if not keyword :
            context['services'] =Service.objects.filter(currentAtt__lte=5)
            return context
        context['services'] =Service.objects.filter(currentAtt__lte=keyword)
        return context

@login_required
def promote(request):

    if request.method == 'POST': 
        id=request.POST.get("q")
        print(id)
        service=Service.objects.get(id=id)
        service.isPromoted=True
        service.save()

        return redirect("service_promote_list")

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



def service_chart_filter(request):
     return render(request, 'eventify/service_chart_filter.html')

def event_chart_filter(request):
     return render(request, 'eventify/event_chart_filter.html')
def user_chart_filter(request):
     return render(request, 'eventify/user_chart_filter.html')     
def service_chart_data(request):
    labels = []
    data = []

    #Filters for date
    q1 = ServiceChart.objects.values('start_date').last()
    q2 = ServiceChart.objects.values('end_date').last()
    q3 = ServiceChart.objects.values('isLate').last()['isLate']
    q4 = ServiceChart.objects.values('isGiven').last()['isGiven']
    q5 = ServiceChart.objects.values('IsCancelled').last()['IsCancelled']
    q6 = ServiceChart.objects.values('paid').last()['paid']
    q7 = ServiceChart.objects.values('location').last()['location']
    q8 = ServiceChart.objects.values('range').last()['range']
 
   
    filterlist =[]
    date1 = q1['start_date']
    date2 = q2['end_date']

    #Filters for attendee numbers
    q9 = ServiceChart.objects.values('min_attendee').last()
    q10 = ServiceChart.objects.values('max_attendee').last()
    attendeeMin = q9['min_attendee']
    attendeeMax = q10['max_attendee']

    fieldname = 'created'
    prequery=Service.objects.all()
    for item in prequery:
        x=round(geodesic(item.location, q7).km,2)
        if x<q8:
            filterlist.append(item.location)
    print(filterlist)
    queryset = Service.objects.values(fieldname).filter(location__in=filterlist).filter(isLate=q3).filter(isGiven=q4).filter(IsCancelled=q5).filter(paid=q6).filter(eventdate__range=[date1,date2]).filter(currentAtt__range=[attendeeMin,attendeeMax]).order_by(fieldname).annotate(the_count=Count(fieldname))
    print(queryset)

        
    for service_loop in queryset:
        labels.append(service_loop[fieldname])
        data.append(service_loop['the_count'])

    return JsonResponse(data= {
        'labels': labels,
        'data': data,
    })
def event_chart_data(request):
    labels = []
    data = []

    #Filters for date
    q1 = ServiceChart.objects.values('start_date').last()
    q2 = ServiceChart.objects.values('end_date').last()
    q3 = ServiceChart.objects.values('isLate').last()['isLate']
    q5 = ServiceChart.objects.values('IsCancelled').last()['IsCancelled']
    q7 = ServiceChart.objects.values('location').last()['location']
    q8 = ServiceChart.objects.values('range').last()['range']
 
   
    filterlist =[]
    date1 = q1['start_date']
    date2 = q2['end_date']

    fieldname = 'created'
    prequery=Post.objects.all()
    for item in prequery:
        x=round(geodesic(item.location, q7).km,2)
        if x<q8:
            filterlist.append(item.location)
    print(filterlist)
    queryset = Post.objects.values(fieldname).filter(location__in=filterlist).filter(isLate=q3).filter(IsCancelled=q5).filter(eventdate__range=[date1,date2]).order_by(fieldname).annotate(the_count=Count(fieldname))
    print(queryset)

        
    for service_loop in queryset:
        labels.append(service_loop[fieldname])
        data.append(service_loop['the_count'])

    return JsonResponse(data= {
        'labels': labels,
        'data': data,
    })

def user_chart_data(request):
    labels = []
    data = []

    #Filters for date
    q1 = UserChart.objects.values('start_date').last()
    q2 = UserChart.objects.values('end_date').last()
    q3 = UserChart.objects.values('is_active').last()['is_active']
    q5 = UserChart.objects.values('credits').last()['credits']
    q7 = UserChart.objects.values('location').last()['location']
    q8 = UserChart.objects.values('range').last()['range']
 
   
    filterlist =[]
    date1 = q1['start_date']
    date2 = q2['end_date']

    fieldname = 'created'
    prequery=Profile.objects.all()
    for item in prequery:
        x=round(geodesic(item.location, q7).km,2)
        if x<q8:
            filterlist.append(item.location)
    print(filterlist)
    queryset = Profile.objects.values(fieldname).filter(location__in=filterlist).filter(created__range=[date1,date2]).order_by(fieldname).annotate(the_count=Count(fieldname))
    print(queryset)

        
    for service_loop in queryset:
        labels.append(service_loop[fieldname])
        data.append(service_loop['the_count'])

    return JsonResponse(data= {
        'labels': labels,
        'data': data,
    })


def service_chart(request):
    form = ServiceChartForm()

    if request.method == 'POST':
        form = ServiceChartForm(request.POST)
        if form.is_valid():
            selection = form.save(commit=False)
            selection.save()
            return redirect('service_chart_filter')

    context = {'form':form}
    return render(request, 'eventify/service_chart.html', context)

def event_chart(request):
    form = EventChartForm()

    if request.method == 'POST':
        form = EventChartForm(request.POST)
        if form.is_valid():
            selection = form.save(commit=False)
            selection.save()
            return redirect('event_chart_filter')

    context = {'form':form}
    return render(request, 'eventify/event_chart.html', context)

def user_chart(request):
    form = UserChartForm()

    if request.method == 'POST':
        form = UserChartForm(request.POST)
        if form.is_valid():
            selection = form.save(commit=False)
            selection.save()
            return redirect('user_chart_filter')

    context = {'form':form}
    return render(request, 'eventify/user_chart.html', context)
    
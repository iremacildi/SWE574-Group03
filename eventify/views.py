import django
from django.forms.widgets import DateInput, TimeInput
from django.http.response import Http404, HttpResponse
from .models import  Post, Comment, RegisterService,Service,ServiceComment,RegisterEvent,Approved
from users.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm, ServiceForm
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
            return my_list
        else:
            return object_list

class ServiceListView(ListView):
    model = Service
    template_name = 'eventify/services.html'
    context_object_name = 'services'
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
      
        elif keyword == '' and cat!="all":
            object_list = self.model.objects.filter(category=cat)
                    
        elif keyword != '' and cat!="all":
            object_list = self.model.objects.filter(
                (Q(content__icontains=keyword) | Q(title__icontains=keyword)) & Q(category__icontains=cat))

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
        location = geolocator.reverse(event.location)
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

        location = geolocator.reverse(service.location)
        context = super().get_context_data(**kwargs)
        context['registerservice'] = RegisterService.objects.filter(service_id=pk,approved_register=True)
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
        return super().form_valid(form)

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm

    def form_valid(self, form):
        form.instance.author = self.request.user
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

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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


            messages.success(request, "Successfully comfirmed")
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
        messages.warning(request, "You already comfirmed") 
        return redirect('service_detail', pk=pk)
    if count==1:
         messages.warning(request, "You already comfirmed")   
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
        RegisterEvent.objects.filter(author_id=ids,post_id=post_id).delete()
        messages.success(request, "Successfully cancelled application")    
        return redirect('post_detail', pk=pk)
    else:
        return redirect('post_detail', pk=pk)


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
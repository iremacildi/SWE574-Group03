from django.forms.widgets import DateInput, TimeInput
from django.http.response import Http404, HttpResponse
from .models import  Post, Comment, RegisterService,Service,ServiceComment,RegisterEvent
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

class PostListView(ListView):
    model = Post
    template_name = 'eventify/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword)|Q(category__icontains=keyword))
        else:
            object_list = self.model.objects.all()
        for item in object_list:
          item.tempLocation=round(geodesic(item.location, self.request.user.profile.address).km,2)    
        return object_list

class ServiceListView(ListView):
    model = Service
    template_name = 'eventify/services.html'
    context_object_name = 'services'
    paginate_by = 5
    geolocator = Nominatim(user_agent="arcan")
    location = geolocator.reverse("52.509669, 13.376294")
    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword)|Q(category__icontains=keyword))
        else:
            object_list = self.model.objects.all()

        for item in object_list:
            item.tempLocation=round(geodesic(item.location, self.request.user.profile.address).km,2)
            
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
        pk=self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['registerevent'] = RegisterEvent.objects.filter(post_id=pk,approved_register=True)
        context['unRegister'] = RegisterEvent.objects.filter(post_id=pk,author_id=self.request.user.id,approved_register=True)
        return context


class ServiceDetailView(LoginRequiredMixin,DetailView):
    context_object_name = 'object'
    model = Service

    def get_context_data(self, **kwargs):
        pk=self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['registerservice'] = RegisterService.objects.filter(service_id=pk,approved_register=True)
        context['unRegister'] =RegisterService.objects.filter(service_id=pk,author_id=self.request.user.id,approved_register=False)
        context['approved'] =RegisterService.objects.filter(service_id=pk,author_id=self.request.user.id,approved_register=True)
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
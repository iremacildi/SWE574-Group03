from django.http.response import Http404, HttpResponse
from .models import Post, Comment, RegisterService,Service,ServiceComment,RegisterEvent
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
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
        else:
            object_list = self.model.objects.all()
        return object_list

class ServiceListView(ListView):
    model = Service
    template_name = 'eventify/services.html'
    context_object_name = 'services'
    paginate_by = 5

    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
        else:
            object_list = self.model.objects.all()
        return object_list

class UserPostListView(ListView):
    model = Post
    template_name = 'eventify/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class UserServiceListView(ListView):
    model = Service
    template_name = 'eventify/user_services.html'
    context_object_name = 'services'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Service.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class ServiceDetailView(DetailView):
    model = Service

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
    fields = ['title', 'content','picture']

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
    fields = ['title', 'content','picture']

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
        RegisterEvent(author=user, post=post, username=user.username).save()
        messages.success(request, "You register event successfully")
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
                messages.warning(request, "You already registered event")
                return redirect('service_detail', pk=pk)

        except:
            pass
        RegisterService(author=user, service=service, username=user.username).save()
        messages.success(request, "You register event successfully")
        return redirect('service_detail', pk=pk) 
       
    else:
        return redirect('service_detail', pk=pk)
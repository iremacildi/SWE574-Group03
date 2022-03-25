from django.urls import path, include
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserListView,
    ServiceListView,
    ServiceDetailView,
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView,
    # UserServiceListView,
    add_comment,
    add_servicecomment,
    register_event,
    follow_unfollow_user,
    register_service,
    unregister_service,
    unregister_event,
    approved
)


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('services', ServiceListView.as_view(), name='services'),
    path('user/<str:username>/', UserListView.as_view(), name='profiledetail'),
    # path('user/<str:username>/', UserServiceListView.as_view(), name='user_services'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('service/new/', ServiceCreateView.as_view(), name='service_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('service/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('service/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    path('about/', views.about, name='about'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
    path('post/<int:pk>/postregister/', register_event, name='register_event'),
    path('post/<int:pk>/unpostregister/', unregister_event, name='unregister_event'),
    path('service/<int:pk>/serviceregister/', register_service, name='register_service'),
    path('user/<str:username>/follow-unfollow/', follow_unfollow_user, name='follow_unfollow_user'),
    path('service/<int:pk>/unserviceregister/', unregister_service, name='unregister_service'),
    path('service/<int:pk>/servicecomment/', add_servicecomment, name='add_servicecomment'),
    path('service/<int:pk>/approved/', approved, name='approved'),
]

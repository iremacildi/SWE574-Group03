from django.urls import path, include
from django.conf.urls import url
import notifications.urls
from . import views

from .views import (
    FollowersView,
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
    FeedView,
    FollowersView,
    NotificationsListView,
    # UserServiceListView,
    add_comment,
    add_servicecomment,
    # follower_list_view,
    # following_list_view,
    register_event,
    follow_unfollow_user,
    register_service,
    unregister_service,
    unregister_event,
    approved,
    pie_chart_category_active
)


urlpatterns = [

    # service
    path('services', ServiceListView.as_view(), name='services'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('service/new/', ServiceCreateView.as_view(), name='service_create'),
    path('service/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('service/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    path('notifications', NotificationsListView.as_view(), name='notifications'),
    path('about/', views.about, name='about'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
    path('post/<int:pk>/postregister/', register_event, name='register_event'),
    path('post/<int:pk>/unpostregister/', unregister_event, name='unregister_event'),
    path('service/<int:pk>/serviceregister/', register_service, name='register_service'),
    path('service/<int:pk>/unserviceregister/', unregister_service, name='unregister_service'),
    path('service/<int:pk>/servicecomment/', add_servicecomment, name='add_servicecomment'),
    path('service/<int:pk>/approved/', approved, name='approved'),
    # path('user/<str:username>/', UserServiceListView.as_view(), name='user_services'),
    

    # event
    path('', PostListView.as_view(), name='index'),
    path('post/<int:pk>/postregister/', register_event, name='register_event'),
    path('post/<int:pk>/unpostregister/', unregister_event, name='unregister_event'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),

    # user - feed
    path('user/<str:username>/', UserListView.as_view(), name='profiledetail'),
    path('about/', views.about, name='about'),
    path('user/<str:username>/follow-unfollow/', follow_unfollow_user, name='follow_unfollow_user'),
    path('feed', FeedView.as_view(), name='feed'),
    path('activity/', include('actstream.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    # charts
    path('api', views.ChartData.as_view(), name='api'),
    path('api2', views.pie_chart_category_active_render, name='api2'),
    path('api3', views.pie_chart_category_active, name='api3'),
    path('service_chart', views.service_chart, name='service_Chart')

]

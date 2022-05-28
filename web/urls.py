from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from eventify.views import FollowersView,FollowingView
from users import views as user_views

from django.conf import settings
from django.conf.urls.static import static
from controlcenter.views import controlcenter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/dashboard/', controlcenter.urls),
    #  urls
    path('', include('eventify.urls')),
    # Authentication Urls
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('profile', user_views.approve_service_register, name='approve_service_register'),
    # path('profile', user_views.delete_service_register, name='delete_service_register'),
 
  
    path('editprofile/', user_views.editprofile, name='editprofile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # Resete Password Urls
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    # Change Password Urls
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),    
    path('user/<str:username>/followers_list', FollowersView.as_view(), name='followers_list'),
    path('user/<str:username>/following_list', FollowingView.as_view(), name='following_list'),
    path('interests/<int:user_id>', user_views.interests, name='interests'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    path('', include('eventify.urls')),

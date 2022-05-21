from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import users
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,InterestsForm
from eventify.models import Post, RegisterEvent, RegisterService,Service
from .models import Profile
from geopy.geocoders import Nominatim
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, "Your account has been created! Your ar now able to login.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def interests(request):
    if request.method == 'POST':
        form = InterestsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "We understand your interests. Now enjoy with Eventify!")
            return redirect('login')
    else:
        form = InterestsForm()
    return render(request, 'users/interests.html', {'form': form})        


@login_required
def profile(request):
    geolocator = Nominatim(user_agent="arcan")
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        profile=Profile.objects.get(user_id=request.user.id)
        post_list=Post.objects.filter(author_id=request.user.id).order_by('-date_posted')
        service_list=Service.objects.filter(author_id=request.user.id).order_by('-date_posted')
        registerservice=RegisterService.objects.filter(owner=request.user.id,approved_register=False)
        myregisterservice=RegisterService.objects.filter(author_id=request.user.id)
        location = geolocator.reverse(profile.location,timeout=20)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'object_list':post_list,
        'service_list':service_list,
        'credits':profile.credits,
        'address':location.address,
        'registerservice':registerservice,
        'myregisterservice':myregisterservice
    }
    return render(request, 'users/profile.html', context)



@login_required
def editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/editprofile.html', context)
    
@login_required
def approve_service_register(request):
    if request.method == 'POST':
        user = request.POST.get('author')
        item = request.POST.get('item_id')
        answer = request.POST.get('answer')
        accept_delete=request.POST.get('type')
        if accept_delete=='Delete':
            RegisterService.objects.filter(author=user,id=item).delete()
            messages.success(request, "Successfully cancelled")
        else:    
            register=RegisterService.objects.get(author=user,id=item)
            register.approved_register=answer
            register.save()   
            messages.success(request, "Successfully accepted")
            return redirect('profile')
    else:
        return redirect('profile')
    return redirect('profile')

# @login_required
# def delete_service_register(request):
#     if request.method == 'POST':
#         user = request.POST.get('author')
#         item = request.POST.get('item_id')
        
#     else:
#         return redirect('profile/')
#     return redirect('profile/')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib.auth.views import LoginView
from django.contrib import messages
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_ratelimit.decorators import ratelimit

from .models import *
from .forms import CustomUserCreationForm, ProfileForm, ProfilePictureForm
from .serializers import UserProfileSerializer, ProfilePictureSerializer, UserSerializer


@ratelimit(key='user', rate='5/hour', method='POST', block=True)
def register(request):
    template = loader.get_template('register.html')
    if request.method == 'POST':
        # Check if the phone number is associated with less than two users
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            if CustomUser.objects.filter(phone_number=phone_number).count() >= 2:
                form.add_error('phone_number', 'Phone number registration limit reached')
            else:
                user = form.save()
                # group = Group.objects.get(name=clients)
                # user.groups.add()
                # CustomUser.objects.create_user(
                #     user=user,
                #     name=user.username,
                # )
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(
                    reverse('profile'))  # Redirect to a profile page or another view  #'userprofile-details', args=[user.pk]

    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        # Authenticate the user using the custom EmailOrUsernameModelBackend
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password,
                            backend='users.backends.EmailOrUsernameModelBackend')

        if user is not None:
            login(self.request, user)
            # Add success message
            messages.success(self.request, 'Login successful')
            return super().form_valid(form)
        else:
            # Add error message if authentication fails
            form.add_error(None, 'Login failed. Please check your credentials')
            messages.error(self.request, 'Login failed. Please check your credentials.')
            return super().form_valid(form)


def profile_view(request):
    template = loader.get_template('profile.html')
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where UserProfile doesn't exist for the user
        user_profile = None
    picture_form = None
    # if user_profile:
    #     try:
    #         picture_form = ProfilePictureForm(request.POST, request.FILE, instance=user_profile.profilepicture)
    #     except ProfilePicture.DoesNotExist:
    #
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user_profile)
        if user_profile:
            picture_form = ProfilePictureForm(request.POST, request.FILE, instance=user_profile.profilepicture)

            if picture_form.is_valid():
                # profile picture instance for the user
                profile_picture = picture_form.save(commit=False)
                profile_picture.user_profile = user_profile
                profile_picture.save()
        if profile_form.is_valid():
            profile_form.save()
            # Update the profile completeness score
            if user_profile:
                user_profile.update_profile_completeness()
            return HttpResponseRedirect('profile')
    else:
        profile_form = ProfileForm(instance=user_profile)
    context = {
        'user_profile': user_profile,
        'profile_form': profile_form,
        'picture_form': picture_form,
    }
    return HttpResponse(template.render(context, request))


class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__pk'
    template_name = 'profile.html'


class ProfilePictureDetail(generics.RetrieveUpdateAPIView):
    queryset = ProfilePicture.objects.all()
    serializer_class = ProfilePictureSerializer
    permission_classes = [IsAuthenticated]
    template_name = 'profile.html'


@api_view(['GET'])
def user_list(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    # return Response(serializer.data)
    return JsonResponse(serializer.data, safe= False) # Set safe to false for non-dict objects


@login_required
def onboarding_view(request):
    """
    This function is to show the new user how the website looks like and how it works
    """
    template = loader.get_template('')
    user_profile = UserProfile.objects.get(user=request.user)

    # Check if the user completed their profile
    if not user_profile.is_profile_complete():
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                # Redirect to the next fof onboarding or the dashboard
                return HttpResponseRedirect('/')
        else:
            profile_form = ProfileForm(instance=user_profile)
        context = {
            'user_profile': user_profile,
            'profile_form': profile_form,
        }
        return HttpResponse(template.render(context, request))
    else:
        # User has completed their profile; redirect to the dashboard
        return HttpResponseRedirect('/')

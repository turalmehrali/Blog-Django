
from .forms import SignUpForm, User, UserForm, ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from Blog.models import Article
#from django.views.generic.detail import DetailView
# Create your views here.



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            #if User.objects.filter(username=self.cleaned_data['username']).exists():

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile_view', username=user.username)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile_view', username=user.username)
            else:
                messages.error(request, 'İstifadəçi adı və ya şifrə yanlışdır')
        else:
            messages.error(request, 'İstifadəçi adı və ya şifrə yanlışdır')

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    else:
        return redirect('homepage')



def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)

    return render(request, 'profile.html', {'user_profile': user_profile})


@login_required(login_url='login')
def profile_edit(request):
    data = {'bio': request.user.userprofile.bio, 'profile_photo': request.user.userprofile.profile_photo}
    user_form = UserForm(request.POST or None, instance=request.user, initial=data)
    if user_form.is_valid():
        user_form.save()

        profile_form = ProfileForm(data=request.POST, instance=request.user.userprofile)
        profile_form.save()

        messages.success(request, 'Profiliniz yeniləndi')

        return redirect('profile_view', username=request.user.username)

    return render(request, 'profile_edit.html', context={'form': user_form})

def user_articles(request, username):
    article_list_user = get_object_or_404(User, username=username)
    article_list = Article.objects.all()
    return render(request, 'user_articles.html', {'article_list_user': article_list_user, 'article_list': article_list})
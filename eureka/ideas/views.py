from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from ideas.models import Idea
from django.utils import timezone
from ideas.forms import UserCreationForm
from ideas.forms import LoginForm
from ideas.forms import IdeaForm
import urllib, hashlib

import datetime

# Create your views here.
def index(request):
    return render(request, 'ideas/index.html')

def login(request):
    print request.GET
    if request.method == 'GET':
        return render(request, 'ideas/auth/login.html')
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if request.POST and login_form.is_valid():
            user = login_form.login(request)
            if user:
                auth_login(request, user)
                return redirect('ideas')
        return render(request, 'ideas/auth/login.html', 
            {'login_form': login_form})

def logout(request):
    auth_logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'GET':
        return render(request, 'ideas/auth/signup.html')
    elif request.method == 'POST':
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            email = user_form.clean_email()
            user_form.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'ideas/auth/signup.html',
                {'form': user_form})


@login_required(login_url='login')
def ideas(request, sort='latest'):
    # get the list of ideas and pass it to the context
    if (sort != 'latest' and sort != 'interesting' 
            and sort != 'approved' and sort != 'rejected'):
        sort = 'latest'

    if sort == 'latest':
        ideas = Idea.objects.order_by('created')
    elif sort == 'interesting':
        ideas = Idea.objects.all()[:1] # TODO temporary
    elif sort == 'approved':
        ideas = Idea.objects.filter(state='A') # TODO temporary
    else:
        ideas = Idea.objects.filter(state='R') # TODO temporary

    gravatars = {}

    for idea in ideas:
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(idea.user.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s':str(48)})
        gravatars[idea.user.username] = gravatar_url

    return render(request, 'ideas/ideas/list.html', {'idea_list': ideas, 'gravatars': gravatars, 'sort': sort})


@login_required(login_url='login')
def idea(request, idea_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
    except Idea.DoesNotExist:
        raise Http404

    return HttpResponse("This will show the idea with the id: %s" 
        % (idea_id)) 


@login_required(login_url='login')
def add_idea(request):
	if request.method == 'GET':	
		return render(request, 'ideas/ideas/add.html')
	elif request.method == 'POST':
		idea_form = IdeaForm(request.POST)

		if idea_form.is_valid():
			new_idea = idea_form.save(commit=False)
			new_idea.user = request.user
			new_idea.save()
			return HttpResponse("Ok, I hope!")
        else: # needs to show the form with the errors
		  pass

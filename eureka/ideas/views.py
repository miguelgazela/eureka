from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ideas.models import Idea
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from ideas.forms import UserCreationForm
from ideas.forms import LoginForm
from ideas.forms import IdeaForm
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
    valid_sorts = ['latest', 'interesting', 'approved', 'rejected']
    if sort not in valid_sorts:
        sort = 'latest'

    if sort == 'latest':
        ideas = Idea.objects.order_by('-created')
    elif sort == 'interesting':
        ideas = Idea.objects.annotate(num_interest=Count('interest')).filter(num_interest__gt=0)\
            .order_by('-created')
    elif sort == 'approved':
        ideas = Idea.objects.filter(state='A').order_by('-created')
    else:
        ideas = Idea.objects.filter(state='R').order_by('-created')

    return render(request, 'ideas/ideas/list.html',
        {'idea_list': ideas, 'sort': sort})


@login_required(login_url='login')
def idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)

    if request.method == 'GET':
        if(request.user == idea.user):
            return render(request, 'ideas/ideas/idea.html', {'idea': idea, 'owner': "yes"})
        else:
            return render(request, 'ideas/ideas/idea.html', {'idea': idea, 'owner': "no"})
        
    elif request.method == 'POST' and request.user == idea.user:
        if request.is_ajax():
            if(request.POST['data'] == "delete"):
                idea.delete()
                return
        else:
            idea_form = IdeaForm(request.POST)
        
            if idea_form.is_valid():      
                idea.title = request.POST['title']
                idea.text = request.POST['text']
                idea.save()
            
            return render(request, 'ideas/ideas/idea.html', {'idea': idea})
    else:
        return redirect("/eureka/ideas/%s" % idea.id)        
        
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
			return redirect("/eureka/ideas/%s" % new_idea.id)
        else: # needs to show the form with the errors
		  pass

@login_required(login_url='login')
def users(request, sort='latest'):
    valid_sorts = ['latest', 'commenters', 'thinkers']
    if sort not in valid_sorts:
        sort = 'latest'

    if sort == 'latest':
        users = User.objects.filter(date_joined__gte=datetime.date.today() - datetime.timedelta(days=7))
    elif sort == 'commenters':
        users = User.objects.annotate(num_comments=Count('comment')).filter(num_comments__gt=0).order_by('-num_comments')
    elif sort == 'thinkers':
        users = User.objects.annotate(num_ideas=Count('idea')).filter(num_ideas__gt=0).order_by('-num_ideas')

    # paginate the results
    paginator = Paginator(users, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'ideas/users/list.html',
        {'user_list': users, 'sort': sort})

@login_required(login_url='login')
def user(request, user_id):
    print "User here"

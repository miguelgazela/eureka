from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from ideas.models import Idea
from ideas.models import Interest
from ideas.models import Comment
from ideas.models import Like
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from ideas.forms import UserCreationForm
from ideas.forms import UserEditForm
from ideas.forms import LoginForm
from ideas.forms import IdeaForm
from ideas.forms import CommentForm
from taggit.models import Tag

import datetime
import json


def index(request):
    if request.user.is_authenticated():
        return redirect('ideas')
    return render(request, 'ideas/index.html')


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('user', user_id=request.user.id)
        return render(request, 'ideas/auth/login.html')
    elif request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)

        if request.POST and login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('index')

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
            user_form.clean_password2()
            user_form.clean_email()
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            return render(request, 'ideas/auth/signup.html',
                {'username': username, 'status': 'success'})
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
        ideas = Idea.objects.annotate(num_interest=Count('interest'))\
            .filter(num_interest__gt=0)\
            .order_by('-num_interest')
    elif sort == 'approved':
        ideas = Idea.objects.filter(state='A').order_by('-created')
    else:
        ideas = Idea.objects.filter(state='R').order_by('-created')

    return render(request, 'ideas/ideas/list.html',
        {'idea_list': ideas, 'sort': sort})


@login_required(login_url='login')
def idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)

    return render(request, 'ideas/ideas/view.html', {
        'idea': idea,
        'comments': idea.comment_set.all().order_by('-created'),
        'interested': request.user.interest_set.filter(idea=idea_id),
        'liked': request.user.like_set.filter(idea=idea_id),
    })
      

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
            idea_form.save_m2m()
            return redirect("idea", idea_id=new_idea.id)
        else: # needs to show the form with the errors
            return HttpResponse(idea_form.errors)


@login_required(login_url='login')
def edit_idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)

    if request.user.id == idea.user.id:
        if request.method == 'GET':
            return render(request, 'ideas/ideas/edit.html', {'idea': idea})
        elif request.method == 'POST':
            edit_form = IdeaForm(request.POST)
            if edit_form.is_valid():
                idea.title = request.POST['title']
                idea.text = request.POST['text']
                idea.updated = timezone.now()
                idea.save()
                return redirect('idea', idea_id=idea_id)
            else:
                return render(request, 'ideas/ideas/edit.html',
                {'idea': idea, 'form': edit_form})

    return HttpResponse("You don't have permission to edit this question")


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user.id == comment.user.id:
        if request.method == "POST":
            edit_form = CommentForm(request.POST)
            if edit_form.is_valid():
                comment.text = request.POST.get('text')
                comment.save()
                return redirect('idea', idea_id=comment.idea.id)
            else:
                return HttpResponse('This comment is not valid')
    
    return HttpResponse("You don't have permission to edit this comment")

def delete_idea(request, idea_id):
    response = {'status': 'fail'}
    response['data'] = None

    if request.is_ajax():
        if request.user.is_authenticated():
            try:
                idea = Idea.objects.get(pk=idea_id)
                if idea.user.id == request.user.id:
                    idea.delete()
                    response['status'] = 'success'
                else:
                    response['data'] = {'title': "This idea isn't yours"}
            except Idea.DoesNotExist:
                response['data'] = {'title': 'No idea with that id was found'}
        else:
            response['data'] = {'title': 'You must be logged in to delete an idea'}
    else:
        response['data'] = {'title': 'API can only be used with AJAX requests'}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(pk=comment_id)
            idea_id = comment.idea.id
            if comment.user == request.user:
                comment.delete()
                return redirect('idea', idea_id=idea_id)
            else:
                return HttpResponse("That comment isn't yours to delete.")
        except Comment.DoesNotExist:
            return HttpResponse('No comment with that id.')

def add_interest(request, idea_id):
    response = {'status': 'fail'}

    if request.is_ajax():
        if request.user.is_authenticated():
            if request.user.interest_set.filter(idea=idea_id):
                response['data'] = {
                    'title': "You're already interested in this question"}
            else:
                try:
                    idea = Idea.objects.get(pk=idea_id)
                    interest = Interest(user=request.user, idea=idea)
                    interest.save()
                    response['status'] = 'success'
                    response['data'] = {
                        'username': request.user.username,
                        'id': request.user.id,
                        'email': request.user.email,
                        'created': interest.created}
                except Idea.DoesNotExist:
                    response['data'] = {
                        'title': 'No idea with that id was found'}
        else:
            response['data'] = {
                'title': 'You must be logged in to be interested in an idea'}
    else:
        response['data'] = {'title': 'API can only be used with AJAX requests'}
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="application/json")


def remove_interest(request, idea_id):
    response = {'status': 'fail'}

    if request.is_ajax():
        if request.user.is_authenticated():
            if not request.user.interest_set.filter(idea=idea_id):
                response['data'] = {
                    'title': "You're not interested in this question"}
            else:
                interest = Interest.objects.filter(idea=idea_id, user=request.user.id)
                interest.delete()
                response['status'] = 'success'
                response['data'] = None
        else:
            response['data'] = {
                'title': 'You must be logged in to remove interest in an idea'}
    else:
        response['data'] = {'title': 'API can only be used with AJAX requests'}
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def add_comment(request, idea_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            try:
                idea = Idea.objects.get(pk=idea_id)
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.idea = idea
                new_comment.save()
                return redirect('idea', idea_id=idea_id)
            except Idea.DoesNotExist:
                pass
        else:
            return redirect('idea', idea_id=idea_id)


@login_required(login_url='login')
def users(request, sort='all'):
    valid_sorts = ['latest', 'commenters', 'thinkers', 'all']
    if sort not in valid_sorts:
        sort = 'all'

    if sort == 'latest':
        users = User.objects.filter(date_joined__gte=datetime.date.today()
            - datetime.timedelta(days=7))
    elif sort == 'commenters':
        users = User.objects.annotate(num_comments=Count('comment'))\
            .filter(num_comments__gt=0).order_by('-num_comments')
    elif sort == 'thinkers':
        users = User.objects.annotate(num_ideas=Count('idea'))\
            .filter(num_ideas__gt=0).order_by('-num_ideas')
    elif sort == 'all':
        users = User.objects.all().order_by('username')

    # paginate the results
    paginator = Paginator(users, 20)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    for user in users:
        user.num_comments = user.comment_set.count()
        user.num_ideas = user.idea_set.count()

    return render(request, 'ideas/users/list.html',
        {'user_list': users, 'sort': sort})


@login_required(login_url='login')
def user(request, user_id, tab="ideas"):
    user = get_object_or_404(User, pk=user_id)

    valid_tabs = ['ideas', 'comments', 'interests']
    if tab not in valid_tabs:
        tab = "ideas"

    if tab == 'ideas':
        list_items = Idea.objects.filter(user=user).order_by('-created')
    elif tab == 'comments':
        list_items = Comment.objects.filter(user=user).order_by('-created')

    return render(request, 'ideas/users/view.html', 
        {'user_': user, 'list_items': list_items, 'tab': tab})


@login_required(login_url='login')
def edit_user(request):
    if request.method == 'GET':
        return render(request, 'ideas/users/edit.html')
    elif request.method == 'POST':
        user_form = UserEditForm(request.POST)

        if user_form.is_valid():
            password = user_form.cleaned_data['password']
            newpassword = user_form.cleaned_data['newpassword2']
            
            if not check_password(password, request.user.password):
                return render(request, 'ideas/users/edit.html', {'form': user_form, 'errors': user_form.errors, 'wrong': 'true'})
            
            request.user.set_password(newpassword)
            request.user.save()
            
            if not check_password(newpassword, request.user.password):
                return HttpResponse("As ocurred an error! Your password was not changed.")                
                
            return render(request, 'ideas/users/edit.html', {'form': user_form, 'errors': user_form.errors, 'changed': 'true'})
        else:
            return render(request, 'ideas/users/edit.html', {'form': user_form, 'errors': user_form.errors})


@login_required
def tags(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        result = [tag.name for tag in tags]
        return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
def search(request):
    if request.method == 'GET':
        return render(request, 'ideas/search/search.html')

@login_required
def like(request, idea_id):
    response = {'status': 'fail', 'data': None}

    if request.is_ajax():
        if request.user.like_set.filter(idea=idea_id):
            response['data'] = {
                'title': "You already like this question"}
        else:
            idea = get_object_or_404(Idea, pk=idea_id)
            like = Like(user=request.user, idea=idea)
            like.save()
            response['status'] = 'success'
    else:
        response['data'] = {'title': 'API can only be used with AJAX requests'}
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def dislike(request, idea_id):
    response = {'status': 'fail', 'data': None}

    if request.is_ajax():
        if not request.user.like_set.filter(idea=idea_id):
            response['data'] = {
                'title': "You don't like this idea"
            }
        else:
            like = Like.objects.filter(idea=idea_id, user=request.user.id)
            like.delete()
            response['status'] = 'success'
    else:
        response['data'] = {'title': 'API can only be used with AJAX requests'}
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def change_state(request, idea_id, state):
    response = {'status': 'fail', 'data': None}

    if request.is_ajax():
        if not request.user.is_superuser:
            response['data'] = {
                'title': "You don't have permission to do this"
            }
        else:
            idea = get_object_or_404(Idea, pk=idea_id)
            idea.state = state.upper()
            idea.save()
            response['status'] = 'success'

    else:
        response['data'] = {'title': 'API can only be used with AJAX requests'}
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="application/json")


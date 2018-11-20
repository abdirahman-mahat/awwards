from django.shortcuts import HttpResponse, render, redirect, get_object_or_404, reverse, get_list_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import mail_admins
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .forms import *
from .models import *
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
# Create your views here.


def search_results(request):
    # check if the input field exists and that ic contains data
    if 'post' in request.GET and request.GET['post']:
        # get the data from the search input field
        explore_posts = Post.all_posts()
        search_term = request.GET.get('post')
        searched_posts = Post.filter_by_search_term(search_term)
        print(search_term)
        caption = f'Search results for {search_term}'

        if len(searched_posts) == 0:
            caption = f'Results for {search_term} Found'
        search_context = {
            'posts': searched_posts,
            'explore_posts': explore_posts,
            'caption': caption,
        }
        return render(request, 'search.html', search_context)
    else:
        explore_posts = Post.all_posts()
        search_context = {
            'explore_posts': explore_posts,
            'caption': 'Matches found for your search!! Discover More Posts'
        }
        return render(request, 'search.html', search_context)


def home(request):
    post = Post.objects.first()
    posts = Post.objects.all()
    print(posts)

    average_usability = Rating.average_usability(post)
    average_design = Rating.average_design(post)
    average_creativity = Rating.average_creativity(post)
    average_content = Rating.average_content(post)
    average_mobile = Rating.average_mobile(post)
    average_rating = Rating.average_rating(post)
    context = {
        'posts': posts,
        'post': post,
        'average_usability_w': stringify_rating(average_usability)[0],     'average_usability_d': stringify_rating(average_usability)[1],
        'average_design_w': stringify_rating(average_design)[0],           'average_design_d': stringify_rating(average_design)[1],
        'average_creativity_w': stringify_rating(average_creativity)[0],   'average_creativity_d': stringify_rating(average_creativity)[1],
        'average_content_w': stringify_rating(average_content)[0],         'average_content_d': stringify_rating(average_content)[1],
        'average_mobile_w': stringify_rating(average_mobile)[0],           'average_mobile_d': stringify_rating(average_mobile)[1],
        'average_rating': average_rating,
    }
    return render(request, 'index.html', context)


def login(request):
    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def profile(request,  username):
    projo = Post.objects.all()
    profile = User.objects.get(username=username)
    # print(profile.id)
    try:
        profile_details = Profile.objects.all()
    except:
        profile_details = Profile.objects.all()
    projo = Post.objects.all()
    title = f'@{profile.username} awwward projects and screenshots'

    return render(request, 'profile.html', locals())




def signup(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            print('here')
            form.save()
            return redirect('login')

    form = MyRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def post_website(request):
    if request.method == 'POST':
        uploadform = ProjectForm(request.POST, request.FILES)
        if uploadform.is_valid():
            upload = uploadform.save(commit=False)
            upload.profile = request.user.profile
            upload.save()
            return redirect('home')
    else:
        uploadform = ProjectForm()
    return render(request,'new_upload.html',locals())


def rate_website(request, post_id):
    user = request.user
    try:
        profile = user.profile
        posts = Post.objects.all()
        post = Post.objects.get(pk=post_id)
        post_reviews = post.ratings.all()
        judges = list(set([judge.user for judge in post_reviews]))
        if request.user.is_authenticated:
            print(post_id)
            p_user = post.uploaded_by
            if request.method == 'POST':
                rf = RatePostForm(request.POST)
                cf = ReviewCommentForm(request.POST)
                print(rf.is_valid())
                print(cf.is_valid())
                if rf.is_valid():
                    rf.save()
                    rating = Rating.objects.last()
                    rating.user = user
                    rating.post = post
                    rating.save()
                if cf.is_valid() and cf.cleaned_data['review'] != '':
                    cf.save()
                    review = Comment.objects.last()
                    review.author = user
                    review.post = post
                    review.save()
                return redirect(reverse('rate_website', args=(post_id,)))
            else:
                rf = RatePostForm()
                cf = ReviewCommentForm()
            print(judges)

            # user_rating = from
            average_usability = Rating.average_usability(post)
            average_design = Rating.average_design(post)
            average_creativity = Rating.average_creativity(post)
            average_content = Rating.average_content(post)
            average_mobile = Rating.average_mobile(post)
            average_rating = Rating.average_rating(post)
            context = {
                'average_usability_w': stringify_rating(average_usability)[0],       'average_usability_d': stringify_rating(average_usability)[1],
                'average_design_w': stringify_rating(average_design)[0],            'average_design_d': stringify_rating(average_design)[1],
                'average_creativity_w': stringify_rating(average_creativity)[0],     'average_creativity_d': stringify_rating(average_creativity)[1],
                'average_content_w': stringify_rating(average_content)[0],           'average_content_d': stringify_rating(average_content)[1],
                'average_mobile_w': stringify_rating(average_mobile)[0],            'average_mobile_d': stringify_rating(average_mobile)[1],
                'average_rating': average_rating,
                'rf_form': rf,
                'cf_form': cf,
                'p_user': p_user,
                'user': user,
                'post': post,
                'posts': posts,
                'judges': judges,
                'ratings': post_reviews
            }
            return render(request, 'rate.html', context)
    except:
        text = 'You need a profile before rating a website! Add One Now!'
        return render(request, 'profile_edit.html', {'text': text})


def dummy(request):
    return HttpResponse('dummy')


def edit_profile(request):
    profile = User.objects.get(username=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm()
    return render(request, 'profile_edit.html', locals())


def stringify_rating(rating):
    r = str(rating).split('.')
    x = r[1]
    if len(r[1]) < 2:
        x += '0'

    return [r[0], x]

class ProfileList(APIView):
    def get(self, request, format=None):
        all_profile = Profile.objects.all()
        serializers = ProfileSerializer(all_profile, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    permission_classes = (IsAdminOrReadOnly,)

class ProjectList(APIView):
    def get(self, request, format=None):
        all_post = Post.objects.all()
        serializers = ProjectSerializer(all_post, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (IsAdminOrReadOnly,)

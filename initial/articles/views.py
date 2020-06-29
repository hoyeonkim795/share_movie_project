from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model 
from . import views
from .models import Movie, Review, Comment, Genre
from .forms import ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import operator
from collections import Counter
# pagination
from django.core.paginator import Paginator
import requests
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('articles:home')
    # articles = Article.objects.all()
    
    context = {
        #'articles'가 html로 넘어가는 거.
        # 'articles': articles,
        
    }
    return render(request, 'articles/index.html', context)

@login_required
def home(request):
    # 추천 영화 알고리즘 
    # 비회원 & 리뷰를 남기지 않은 경우 => 인기순
    movies = Movie.objects.order_by('-popularity')
    if request.user.is_authenticated:
        # 리뷰를 남긴 경우 => 장르를 기준으로 평점의 평균을 구해서 장르 내림차순 
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        if len(user.review_set.all()): # 작성한 리뷰가 있는 경우
            scores = {
                '28': [0, 0], '12': [0, 0], '16': [0, 0], '35': [0, 0], '80': [0, 0], '99': [0, 0], '18': [0, 0], '10751': [0, 0], '14': [0, 0], '36': [0, 0], '27': [0, 0], '10402': [0, 0], '9648': [0, 0], '10749': [0, 0], '878': [0, 0], '10770': [0, 0], '53': [0, 0], '10752': [0, 0]
                } # genre : [cnt, sum]
            for review in user.review_set.all():
                score = review.score
                for genre in Genre.objects.filter(review=review.pk).values():
                    genre_id = str(genre['id'])
                    # cnt += 1, sum += 점수
                    scores[genre_id][0] = scores[genre_id][0] + 1
                    scores[genre_id][1] = scores[genre_id][1] + score
            
            # 평균 구하기
            for k, v in scores.items():
                if v[0]:
                    value = v[1] // v[0]
                    scores[k] = value
                else:
                    scores[k] = 0
            # 가장 큰 평균 평점 가지는 장르 구하기 => 값 기준 내림차순 정렬
            scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
            g_id = int(scores[0][0]) # 선호하는 장르를 찾았다
            
            # 유저가 본 영화 중 가장 많은 언어 선택 
            temp = []
            fin = [] # 유저가 작성한 리뷰 
            for review in user.review_set.all():
                l = Movie.objects.filter(review=review.id).values()[0]['original_language']
                temp.append(l)
                # 이미 본 영화 처리 = > 작성한 리뷰 아이디 저장
                fin.append(review.id)

            # 배열에서 data 개수 세기
            counter = Counter(temp)
            c = sorted(counter.items(), key=operator.itemgetter(1), reverse=True)
            lan = c[0][0] # 선호하는 언어를 찾았다

            # 선호하는 장르 + 언어 영화를 인기도를 기준으로 내림차순 정렬
            movies = Movie.objects.filter(genre_ids=g_id).exclude(review__in=fin).order_by('-popularity')[:5]
    
        # 유저가 가장 최근에 리뷰를 작성한 영화
        if len(user.review_set.all()):
            last_movie = user.review_set.last().movie
            # last_movie 에 대한 다른 유저의 리뷰 3개 들고오기
            other_reviews = last_movie.review_set.exclude(user=user).order_by('-created_at')[:3]

        else:
            last_movie = ''
            other_reviews = ''
        

    context = {
        'movies' : movies,
        'last_movie': last_movie,
        'other_reviews': other_reviews,
    }
    return render(request, 'articles/home.html', context)



def movie_list(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': movies,
        'page_obj': page_obj,
    }
    return render(request, 'articles/movie_list.html', context)

def last_movie_list(request):
    movies = Movie.objects.order_by('-release_date')
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': movies,
        'page_obj': page_obj,
    }
    return render(request, 'articles/movie_list.html', context)


def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    inputvalue = movie.title+'trailer'
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': '',
        'part': 'snippet',
        'type': 'video',
        'maxResults': '1',
        'q': inputvalue,
    }
    response = requests.get(url, params)
    response_dict = response.json()

    context = {
        'movie': movie,
        'reviews': reviews,
        'response_dict': response_dict,
        'youtube_items': response_dict['items']
    }
    return render(request, 'articles/movie_detail.html', context)

def community(request, movie_pk):
    # 해당하는 영화에 대한 reviews 들고오기 
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    paginator = Paginator(reviews, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'reviews': reviews,
        'movie': movie,
        'page_obj': page_obj,
    }
    return render(request, 'articles/community.html', context)

    
@login_required
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 해당하는 영화의 장르
    genres = Genre.objects.filter(genre_movies=movie_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            review.genre_ids.set(genres)
            return redirect('articles:community', movie_pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)

def review_list(request):
    movies = Movie.objects.all()
    reviews = Review.objects.all()
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'movies' : movies,

    }
    return render(request, 'articles/review_list.html', context)

def review_detail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    form = CommentForm()
    context = {
        'movie': movie,
        'review': review,
        'comments': comments,
        'form': form,
    }
    return render(request, 'articles/review_detail.html', context)



@login_required
def comment_create(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
        return redirect('articles:review_detail', movie.pk, review.pk)


@login_required
def review_delete(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        review.delete()
    return redirect('articles:community', movie_pk)


@login_required
def review_update(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('articles:review_detail', movie_pk, review_pk)
        else:
            form = ReviewForm(instance=review)
    else:
        return redirect('articles:review_detail', movie_pk, review_pk)
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)

@login_required
def comment_delete(request, movie_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('articles:review_detail', movie_pk, review_pk)

@login_required
def comment_update(request, movie_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if comment.user == request.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('articles:review_detail', movie_pk, review_pk)
        else:
            form = CommentForm(instance=comment)
    else:
        return redirect('articles:review_detail', movie_pk, review_pk)
    context = {
        'form': form,
        'comment': comment,
        'review': review,
    }
    return render(request, 'articles/review_detail.html', context)

def youtube(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    inputvalue = movie.orinal_title+'trailer'
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': '',
        'part': 'snippet',
        'type': 'video',
        'maxResults': '1',
        'order':'rating',
        'q': inputvalue,
        
    }
    response = requests.get(url, params)
    response_dict = response.json()

    context = {
        'youtube_items': response_dict['items']
        
    }
    return render(request, 'articles/youtube.html', context)
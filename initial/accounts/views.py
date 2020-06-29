from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from .forms import ProfileForm
from .forms import CustomUserCreationForm
from articles.models import Review
from django.views.decorators.csrf import csrf_exempt
# from .forms import CustomUserCreationForm

# Create your views here.
@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        # 사용자가 보낸 값 -> form
        form = AuthenticationForm(request, request.POST)
        # 검증
        if form.is_valid():
            # 검증 완료시 로그인!
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:home')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    # 조건식으로 직접 작성 해도 된다.
    auth_logout(request)
    return redirect('articles:index')

def signup(request):
    if request.user.is_authenticated:
            return redirect('articles:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # forms의 폼으로 바꿔줘야함
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:home')
    else:
        form = CustomUserCreationForm() # forms의 폼으로 바꿔줘야함
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def profile(request, username):
    User = get_user_model()
    user_id = User.objects.filter(username=username).values('id')[0]['id']
    person = get_object_or_404(User, username=username)
    # movie = get_object_or_404(Movie, pk=movie_pk)
    # review = get_object_or_404(Review, pk=review_pk)
    reviews = Review.objects.filter(user=user_id)
    # 사용자의 리뷰
    # 사용자의 최고 평점 영화
    context = {
        'person': person,
        'reviews' : reviews,

    }
    return render(request, 'accounts/profile.html', context)

def profile_edit(request, username):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # 현재 유저의 데이터 가져오고, 받은 값으로 갱신하기
            old_user = request.user
            if old_user.nickname :
                old_user.nickname = form.cleaned_data['nickname']
            old_user.image = form.cleaned_data['image']
            old_user.myinfo = form.cleaned_data['myinfo']
            old_user.save()
            return redirect('accounts:profile', old_user.username)
    else:
        form = ProfileForm()
    context = {
    'form':form,
    }
    return render(request, 'accounts/profile_edit.html', context)
    
def follow(request, username):
    User = get_user_model()
    # 팔로우 당하는 사람
    user = get_object_or_404(User, username=username)
    if user != request.user:
        # 팔로우를 요청한 사람 => request.user
        # 팔로우가 되어 있다면,
        if user.followers.filter(pk=request.user.pk).exists():
            # 삭제
            user.followers.remove(request.user)
        else:
            # 추가
            user.followers.add(request.user)
    return redirect('accounts:profile', username)
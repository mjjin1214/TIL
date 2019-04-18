accounts / models.py 수정

```python
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40, blank=True)
    introduction = models.TextField(blank=True)
    image = ProcessedImageField(
        blank=True,
            upload_to='profile/images', # 저장 위치
            processors=[ResizeToFill(300,300)], # 처리할 작업 목록
            format='JPEG', # 저장 포맷
            options={'quality':90}, # 옵션
        )
```

프로필 모델 생성



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
Migrations for 'accounts':
  accounts/migrations/0001_initial.py
    - Create model Profile
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying accounts.0001_initial... OK
```

모델 변경 부분 마이그레이트



accounts / admin.py 수정

```python
from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile)
```

admin 페이지에서 profile 모델을 수정할 수 있도록



accounts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from .models import Profile

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            Profile.objects.create(user=user) # User의 Profile 생성
            auth_login(request, user)
            return redirect('posts:list')
    else:
        signup_form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'signup_form':signup_form})
 
```

회원가입할 때 profile이 생성되도록



accounts / urls.py 수정

``` python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('password/', views.password, name='password'),
    path('profile/update', views.profile_update, name='profile_update'),
]
```

profile_updatae url 추가



accounts / forms.py 수정

```python
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'introduction', 'image',]
```

ProfileForm 폼 생성



accounts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, ProfileForm
from .models import Profile

def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('people', request.user.username)
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_update.html', {
        'profile_form':profile_form,
    })
```

profile_update 함수 생성



accounts / templates / accounts / profile_update.html 생성

```html
{% extends 'base.html' %}

{% load bootstrap4 %}

{% block container %}

<h1>Profile Edit</h1>

<form method='POST'>
    {% csrf_token %}
    {% bootstrap_form profile_form %}
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```



people.html 수정

```html
{% extends 'base.html' %}

{% block container %}

<div class="container">
    
    <div class="row">
        <div class="col-3">
            <h1>{{ people.username }}</h1>
        </div>
        <div class="col-9">
            <div>
                <strong>{{ people.profile.nickname }}</strong>
            </div>
            <div>
                {{ people.profile.introduction }}
            </div>
        </div>
    </div>
    {% if user == people %}
    <div>
        <a href="{% url 'accounts:profile_update' %}">프로필 수정</a>
        <a href="{% url 'accounts:update' %}">계정 정보 수정</a>
    </div>
    {% endif %}
    <div class="row">
        {% for post in people.post_set.all %}
        <div class="col-4">
            <img src="{{ post.image_set.first.file.url }}" class="img-fluid"/>
        </div>
        {% endfor %}
    </div>
</div>

{% endblock %}
```

people 페이지에 프로필 출력



accounts / models.py 수정

```python
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
```

models.Model -> class AbstractBaseUser -> class AbstractUser -> class User

User 클래스를 그대로 사용하지 않고 AbstractUser를 상속받아 새 클래스를 만들어 유저 커스텀화



settings.py 수정

```python
AUTH_USER_MODEL = 'accounts.User'
```

AUTH_USER_MODEL 을 accounts / models.py 의 User 클래스로 정의



db.sqlite3, accounts / migrations / pycache / init1~~ 삭제



``` bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
Migrations for 'accounts':
  accounts/migrations/0001_initial.py
    - Create model User
    - Create model Profile
    
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying posts.0001_initial... OK
  Applying posts.0002_post_image... OK
  Applying posts.0003_auto_20190409_0224... OK
  Applying posts.0004_auto_20190410_0510... OK
  Applying posts.0005_comment... OK
  Applying posts.0006_post_like_users... OK
  Applying posts.0007_auto_20190415_0042... OK
  Applying sessions.0001_initial... OK
```

새로운 User 모델을 마이그레이트



accounts / forms.py 수정

```python
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
```

UserCreationForm을 상속받아 새로운 User 모델의  CreationForm 생성



accounts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, ProfileForm, CustomUserCreationForm
from .models import Profile

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            Profile.objects.create(user=user) # User의 Profile 생성
            auth_login(request, user)
            return redirect('posts:list')
    else:
        signup_form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'signup_form':signup_form})
```

새로운 CustomUserCreationForm을 사용



accounts / urls.py 수정

```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('password/', views.password, name='password'),
    path('profile/update', views.profile_update, name='profile_update'),
    path('<int:user_id>/follow/', views.follow, name='follow'),
]
```

follow url 추가



accounts / views.py 수정

```python
def follow(request, user_id):
    people = get_object_or_404(get_user_model(), id=user_id)
    if request.user in people.followers.all():
        # 2. people을 unfollow 하기
        people.followers.remove(request.user)
    else:
        # 1. people을 follow하기
        people.followers.add(request.user)
    return redirect('people', people.username)
```

follow 함수 정의



people.html 수정

```html
{% extends 'base.html' %}

{% block container %}

<div class="container">
    
    <div class="row">
        <div class="col-3">
            <h1>{{ people.username }}</h1>
        </div>
        <div class="col-9">
            <div>
                <strong>{{ people.profile.nickname }}</strong>
                {% if user != people %}
                    {% if user in people.followers.all %}
                        <a href="{% url 'accounts:follow' people.id %}">UnFollow</a>
                    {% else %}
                        <a href="{% url 'accounts:follow' people.id %}">Follow</a>
                    {% endif %}
                {% endif %}
            </div>
            <div>
                <strong>Followers:</strong> {{ people.followers.count }}
                <strong>Followings:</strong> {{ people.followings.count }}
            </div>
            <div>
                {{ people.profile.introduction }}
            </div>
        </div>
    </div>
    {% if user == people %}
    <div>
        <a href="{% url 'accounts:profile_update' %}">프로필 수정</a>
        <a href="{% url 'accounts:update' %}">계정 정보 수정</a>
    </div>
    {% endif %}
    <div class="row">
        {% for post in people.post_set.all %}
        <div class="col-4">
            <img src="{{ post.image_set.first.file.url }}" class="img-fluid"/>
        </div>
        {% endfor %}
    </div>
</div>

{% endblock %}
```

followers followings people 페이지에 출력



posts / views.py 수정

```python
@login_required
def list(request):
    # posts = Post.objects.order_by('-id').all()
    # 1. 내가 follow하고 있는 사람들의 리스트
    followings = request.user.followings.all()
    # 2. 이 사람들이 작성한 Post들만 뽑아옴.
    posts = Post.objects.filter(user__in=followings)
    comment_form = CommentForm()
    return render(request, 'posts/list.html', {'posts': posts, 'comment_form': comment_form})
```

followings의 게시물 출력



profile_update.html 수정

```html
{% extends 'base.html' %}

{% load bootstrap4 %}

{% block container %}

<h1>Profile Edit</h1>

<form method='POST' enctype='multipart/form-data'>
    {% csrf_token %}
    {% bootstrap_form profile_form %}
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```

이미지 파일도 전달가능하게 enctype 수정



people.html 수정

```html
{% extends 'base.html' %}

{% block container %}

<div class="container">
    
    <div class="row">
        <div class="col-3">
            <h1>
                {% if people.profile.image %}
                <img src="{{ people.profile.image.url }}" width="50" alt="{{ people.profile.image }}">
                {% endif %}
                {{ people.username }}
            </h1>
        </div>
        <div class="col-9">
            <div>
                <strong>{{ people.profile.nickname }}</strong>
                {% if user != people %}
                    {% if user in people.followers.all %}
                        <a href="{% url 'accounts:follow' people.id %}">UnFollow</a>
                    {% else %}
                        <a href="{% url 'accounts:follow' people.id %}">Follow</a>
                    {% endif %}
                {% endif %}
            </div>
            <div>
                <strong>Followers:</strong> {{ people.followers.count }}
                <strong>Followings:</strong> {{ people.followings.count }}
            </div>
            <div>
                {{ people.profile.introduction }}
            </div>
        </div>
    </div>
    {% if user == people %}
    <div>
        <a href="{% url 'accounts:profile_update' %}">프로필 수정</a>
        <a href="{% url 'accounts:update' %}">계정 정보 수정</a>
    </div>
    {% endif %}
    <div class="row">
        {% for post in people.post_set.all %}
        <div class="col-4">
            <img src="{{ post.image_set.first.file.url }}" class="img-fluid"/>
        </div>
        {% endfor %}
    </div>
</div>

{% endblock %}
```

people 페이지에 프로필 사진 출력



post.html 수정

```html
<div class="card" style="width: 18rem;">
  <div class="card-header">
    {% if post.user.profile.image %}
    <img src="{{ post.user.profile.image.url }}" width="25" alt="{{ post.user.profile.image }}">
    {% endif %}
    <a href="{% url 'people' post.user.username %}">{{ post.user.username }}</a>
  </div>
  <div id="post_{{ post.id }}" class="carousel slide" data-ride="carousel">
    <div class="carousel-inner">
      {% for image in post.image_set.all %}
      <div class="carousel-item {% if forloop.counter == 1 %}active{% endif %}">
        <img src="{{ image.file.url }}" class="card-img-top" alt="{{ image.file }}">
      </div>
      {% endfor %}
    </div>
    <a class="carousel-control-prev" href="#post_{{ post.id }}" role="button" data-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="sr-only">Previous</span>
    </a>
    <a class="carousel-control-next" href="#post_{{ post.id }}" role="button" data-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="sr-only">Next</span>
    </a>
  </div>
  <div class="card-body">
    <a href="{% url 'posts:like' post.id %}">
      {% if user in post.like_users.all %}
        <i class="fas fa-heart" style="color:tomato;"></i>
      {% else %}
        <i class="far fa-heart" style="color:tomato;"></i>
      {% endif %}
    </a>
    <p class="card-text">
      {{ post.like_users.count }}명이 좋아합니다.
    </p>
  </div>
  <div class="card-body">
    <p class="card-text">{{ post.content }}</p>
    {% if post.user == user %}
    <a href="{% url 'posts:update' post.id %}" class="btn btn-info">Edit</a>
    <a href="{% url 'posts:delete' post.id %}" class="btn btn-danger">Delete</a>
    {% endif %}
  </div>
  <div class="card-body">
    {% for comment in post.comment_set.all %}
      <div class="card-text">
        <strong>{{ comment.user.username }}</strong> {{ comment.content }}
        {% if comment.user == user %}
        <a href="{% url 'posts:comment_delete' post.id comment.id %}">삭제</a>
        {% endif %}
      </div>
    {% empty %}
      <div class="card-text">댓글이 없습니다.</div>
    {% endfor %}
  </div>
  {% if user.is_authenticated %}
  <form action="{% url 'posts:comment_create' post.id %}" method="POST">
    {% csrf_token %}
    <div class="input-group">
      {{ comment_form }}
      <div class="input-group-append">
        <input type="submit" value="Submit" class="btn btn-primary"/>
      </div>
    </div>
  </form>
  {% endif %}
</div>
```

리스트 페이지에서 프로필 사진 출력



posts / views.py 수정

```python
@login_required
def list(request):
    # posts = Post.objects.order_by('-id').all()
    # 1. 내가 follow하고 있는 사람들의 리스트
    followings = request.user.followings.all()
    # 2. followings 변수와 나를 묶음
    followings = chain(followings, [request.user])
    # 2. 이 사람들이 작성한 Post들만 뽑아옴.
    posts = Post.objects.filter(user__in=followings).order_by('-id')
    comment_form = CommentForm()
    return render(request, 'posts/list.html', {'posts': posts, 'comment_form': comment_form})
```

유저가 작성한 글도 출력되도록 리스트 삽입과정 추가



posts / urls.py 수정

```python
urlpatterns = [
    path('', views.list, name='list'),
    path('explore/', views.explore, name='explore'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:post_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_id>/like/', views.like, name='like'),
]
```

explore url 추가



posts / views.py 수정

```python
def explore(request):
    posts = Post.objects.order_by('-id').all()
    comment_form = CommentForm()
    return render(request, 'posts/list.html', {'posts': posts, 'comment_form': comment_form})
```

팔로윙 외의 게시글 보는 함수 생성



base.html 수정

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="{% url 'posts:list' %}">
          <i class="fab fa-instagram fa-lg"></i> Instagram
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="{% url 'posts:explore' %}">Explore</a>
          </li>
          {% if user.is_authenticated %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'posts:create' %}">New Post</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'people' user.username %}">{{ user.username }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:logout' %}">Logout</a>
          </li>
          {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:login' %}">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:signup' %}">Signup</a>
          </li>
          {% endif %}
        </ul>
      </div>
    </nav>
    <div class='container'>
    {% block container %}
    {% endblock %}
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
```

nav bar에 explore 링크 추가




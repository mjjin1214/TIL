create.html을 form.html로 이름 변경

admin.py 수정

```python
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
```

admin 계정 생성

```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py createsuperuser
Username (leave blank to use 'ubuntu'): admin
Email address: admin@admin.com
Password: 
Password (again): 
The password is too similar to the email address.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
(insta-venv) minjaejin:~/worksp
```

views.py 수정

```python
def list(request):
    posts = Post.objects.order_by('-id')all()
    return render(request, 'posts/list.html', {'posts': posts})
```

base.html 수정

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">
          <i class="fab fa-instagram fa-lg"></i> Instagram
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link" href="{% url 'posts:create' %}">New Post</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Features</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Pricing</a>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
          </li>
        </ul>
      </div>
    </nav>
```

accounts app 생성

```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py startapp accounts
```

settings.py 수정

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'imagekit',
    'accounts',
    'posts',
]
```

accounts / urls.py 생성

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    
]
```

insta / urls.py 수정

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

accounts / views.py 수정

```python
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):
    signup_form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'signup_form':signup_form})
```

accounts /urls.py 수정

```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
```

accounts / templates / accounts / signup.html 생성

```html
{% extends 'base.html' %}


{% block container %}

<h1>회원 가입</h1>

<form method="POST">
    {% csrf_token %}
    {{ signup_form }}
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```

accounts / views.py 수정

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('posts:list')
    else:
        signup_form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'signup_form':signup_form})
```

accounts / view.py 수정

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('posts:list')
    else:
        login_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'login_form':login_form})
```

accounts / urls.py 수정

```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
```

login.html 생성

```html
{% extends 'base.html' %}

{% block container %}

<h1>로그인</h1>

<form method='POST'>
    {% csrf_token %}
    {{ login_form }}
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```

base.html 수정

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">
          <i class="fab fa-instagram fa-lg"></i> Instagram
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link" href="{% url 'posts:create' %}">New Post</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">{{ user.username }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Pricing</a>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
          </li>
        </ul>
      </div>
    </nav>
```

accounts / views.py  수정

``` python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('posts:list')
```

accounts / urls.py 수정

```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
```

base.html 수정

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">
          <i class="fab fa-instagram fa-lg"></i> Instagram
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          {% if user.is_authenticated %}
          <li class="nav-item active">
            <a class="nav-link" href="{% url 'posts:create' %}">New Post</a>
            </li>
          <li class="nav-item">
            <a class="nav-link" href="#">{{ user.username }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:logout' %}">Logout</a>
          </li>
          {% else %}
          <li class="nav-item">
            <a class="nav-linkd" href="{% url 'accounts:login' %}">Login</a>
          </li>
          {% endif %}
        </ul>
      </div>
    </nav>
```

accounts / views.py 수정

```python
def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('posts:list')
    else:
        signup_form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'signup_form':signup_form})
```

account / views.py 수정

```python
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('posts:list')
    else:
        signup_form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'signup_form':signup_form})
    

def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('posts:list')
    else:
        login_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'login_form':login_form})
```

post / views.py 수정

``` python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
    return render(request, 'posts/form.html', {'post_form':post_form})
```

accounts / views.py 수정

```python
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        login_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'login_form':login_form})
```

posts /models.py 수정

```python
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # image = models.ImageField(blank=True)
    image = ProcessedImageField(
            upload_to=post_image_path, # 저장 위치
            processors=[ResizeToFill(600,600)], # 처리할 작업 목록
            format='JPEG', # 저장 포맷
            options={'quality':90}, # 옵션
        )
```

on_delete=models.CASCADE : 유저가 삭제될 경우 게시물도 함께 삭제하는 옵션



migrations, migrate

```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
You are trying to add a non-nullable field 'user' to post without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> 1
Migrations for 'posts':
  posts/migrations/0004_auto_20190410_0510.py
    - Add field user to post
    - Alter field image on post

(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0004_auto_20190410_0510... OK
```

posts / views.py 수정

```python
@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save() # 실제 데이터베이스에 저장
            return redirect('posts:list')
    else:
        post_form = PostForm()
    return render(request, 'posts/form.html', {'post_form':post_form})
```

commit=False : 실제 데이터베이스에 저장 하지 않을 때



_post.html 수정

```html
<div class="card" style="width: 18rem;">
  <div class="card-header">
    <span>{{ post.user.username }}</span>
  </div>
  {% if post.image %}
  <img src="{{ post.image.url }}" class="card-img-top" alt="{{ post.image }}">
  {% endif %}
  <div class="card-body">
    {% if post.user == user %}
    <p class="card-text">{{ post.content }}</p>
    <a href="{% url 'posts:update' post.id %}" class="btn btn-info">Edit</a>
    <a href="{% url 'posts:delete' post.id %}" class="btn btn-danger">Delete</a>
    {% endif %}
  </div>
</div>
```



posts / views.py 수정

``` python
def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return redirect('posts:list')
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
    return render(request, 'posts/form.html', {'post_form':post_form})

    
def delete(request, post_id):
    # post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('posts:list')
```


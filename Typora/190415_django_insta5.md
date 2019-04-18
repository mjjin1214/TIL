posts / models.py 수정

```python
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # image = models.ImageField(blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
        

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # image = models.ImageField(blank=True)
    file = ProcessedImageField(
            upload_to=post_image_path, # 저장 위치
            processors=[ResizeToFill(600,600)], # 처리할 작업 목록
            format='JPEG', # 저장 포맷
            options={'quality':90}, # 옵션
        )
```

이미지 클래스 생성, 포스트 클래스의 image 필드 이동



forms.py 수정

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content',]
```

image field 삭제



```hash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0007_auto_20190415_0042.py
    - Create model Image
    - Remove field image from post
    - Add field post to image
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0007_auto_20190415_0042... OK
```

수정한 모델 마이그레이트



forms.py 수정

```python
from django import forms
from .models import Post, Comment, Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file', ]
        
ImageFormSet = forms.inlineformset_factory(Post, Image, form=Imageform, extra=3)
```

이미지 폼 생성

forms.inlineformset_factory(부모 모델, 모델, form=폼, extra= 폼 갯수)



posts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import PostForm, CommentForm, ImageFormSet
from .models import Post, Comment

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
        image_formset = ImageFormSet()
    return render(request, 'posts/form.html', {
        'post_form':post_form, 
        'image_formset':image_formset
    })
```

create 함수에 ImageFormSet 넘기는 기능 추가



form.html 수정

```html
{% extends 'base.html' %}

{% load bootstrap4 %}

{% block container %}

<h1>Post Form</h1>
<form action="" method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {% bootstrap_form post_form %}
    {{ image_formset.as_p }}
    {% buttons %}
        <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>

{% endblock %}
```

image_formset 출력



posts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import PostForm, CommentForm, ImageFormSet
from .models import Post, Comment
from django.db import transaction

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)
        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            
            with transaction.atomic():
                # 첫번째
                post.save() # 실제 데이터베이스에 저장
                # 두번째
                image_formset.instance = post
                image_formset.save() # 실제 데이터베이스에 저장
            
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_formset = ImageFormSet()
    return render(request, 'posts/form.html', {
        'post_form':post_form, 
        'image_formset':image_formset
    })
```

save는 db에 요청을 보내는 것으로 실제 db작업이 코드 순서대로 진행됨을 보장할 수 없음

그래서 transaction 사용



_post.html 수정

```html
<div class="card" style="width: 18rem;">
  <div class="card-header">
    <a href="{% url 'people' post.user.username %}">{{ post.user.username }}</a>
  </div>
  {% for image in post.image_set.all %}
  <img src="{{ image.file.url }}" class="card-img-top" alt="{{ image.file }}">
  {% endfor %}
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
    {% if post.user == user %}
    <p class="card-text">{{ post.content }}</p>
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

image 클래스에서 파일을 불러오는 for문 작성



_post.html 수정

``` html
<div class="card" style="width: 18rem;">
  <div class="card-header">
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
    {% if post.user == user %}
    <p class="card-text">{{ post.content }}</p>
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

bootstrap carousel 적용



people.html 수정

```html
{% extends 'base.html' %}

{% block container %}

<div class="container">
    <h1>{{ people.username }}</h1>
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



posts / views.py 수정

``` python
@login_required
def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return redirect('posts:list')
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=post)
        if post_form.is_valid() and image_formset.is_valid():
            post_form.save()
            image_formset.save()
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
        image_formset = ImageFormSet(instance=post)
    return render(request, 'posts/form.html', {
        'post_form':post_form, 
        'image_formset':image_formset
    })
```



accounts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

# User Edit(회원정보 수정) - User CRUD 중 U
def update(request):
    user_change_form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/update.html', {
        'user_change_form':user_change_form,
    })
```



accounts /urls.py 수정

```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
]
```



accounts / templates / accounts / update.html 생성

```html
{% extends 'base.html' %}

{% load bootstrap4 %}

{% block container %}

<h1>User Edit</h1>

<form method='POST'>
    {% csrf_token %}
    {% bootstrap_form user_change_form %}
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```



accounts / forms.py 생성

```python
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name',]
```

원하는 정보만 수정가능 하도록 클래스 생성



accounts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm

# User Edit(회원정보 수정) - User CRUD 중 U
def update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('people', request.user.username)
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/update.html', {
        'user_change_form':user_change_form,
    })
```

CustomUserChangeForm 반영



people.html 수정

```html
{% extends 'base.html' %}

{% block container %}

<div class="container">
    <h1>{{ people.username }}</h1>
    {% if user == people %}
    <div>
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

계정 정보 수정 링크 생성



accounts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

@login_required
def delete(request):
    if request.method == 'POST':
        requrest.user.delete()
        return redirect('posts:list')
    return render(request, 'accounts/delete.html')
```



accounts / urls.py 수정

```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
]
```



accounts / templates / accounts / delete.html 생성

```html
{% extends 'base.html' %}

{% block container %}

<h1>User Delete</h1>

<form method="POST">
    {% csrf_token %}
    <p>정말로 탈퇴하시겠습니까?</p>
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```



update.html 수정

```html
{% extends 'base.html' %}

{% load bootstrap4 %}

{% block container %}

<h1>User Edit</h1>

<form method='POST'>
    {% csrf_token %}
    {% bootstrap_form user_change_form %}
    <input type="submit" value="Submit"/>
</form>

<h3>User Delete</h3>

<a href="{% url 'accounts:delete' %}" class="btn btn-danger">회원 탈퇴하기</a>

{% endblock %}
```



accounts / urls.py 수정

```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('password/', views.password, name='password'),
]
```



accounts / templates / accounts / password.html 생성

```html
{% extends 'base.html' %}

{% load bootstrap4 %}

{% block container %}

<h1>Password Change</h1>

<form method='POST'>
    {% csrf_token %}
    {% bootstrap_form password_change_form %}
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```



accounts / views.py 수정

``` python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('people', request.user.username)
    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password.html', {
        'password_change_form':password_change_form,
    })
```

update_session_auth_hash : 비밀번호 변경후 로그인 유지하기 위해


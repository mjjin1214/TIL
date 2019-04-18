posts / models.py 수정

```python
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
```



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0005_comment.py
    - Create model Comment

(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0005_comment... OK
```

posts / forms.py 수정

```python
from django import forms
from .models import Post, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
```

posts / views.py 수정

```python
def comment_create(request, post_id):
    return redirect('posts:list')
```

posts / urls.py 수정

```python
urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create')
]
```

posts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post

def list(request):
    posts = Post.objects.order_by('-id').all()
    comment_form = CommentForm()
    return render(request, 'posts/list.html', {'posts': posts, 'comment_form': comment_form})
```

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
  <div class="card-body">
    {% for comment in post.comment_set.all %}
      <div class="card-text">
        <strong>{{ comment.user.username }}</strong> {{ comment.content }}
      </div>
    {% empty %}
      <div class="card-text">댓글이 없습니다.</div>
    {% endfor %}
  </div>
  <form action="{% url 'posts:comment_create' post.id %}" method="POST">
    {% csrf_token %}
    {{ comment_form }}
    <input type="submit" value="Submit"/>
  </form>
</div>
```

posts / views.py 수정

``` python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import PostForm, CommentForm
from .models import Post

@require_POST
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
    return redirect('posts:list')
```

@require_POST : POST method 만 함수 호출 허용



post_html  수정

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
  <div class="card-body">
    {% for comment in post.comment_set.all %}
      <div class="card-text">
        <strong>{{ comment.user.username }}</strong> {{ comment.content }}
      </div>
    {% empty %}
      <div class="card-text">댓글이 없습니다.</div>
    {% endfor %}
  </div>
  {% if user.is_authenticated %}
  <form action="{% url 'posts:comment_create' post.id %}" method="POST">
    {% csrf_token %}
    {{ comment_form }}
    <input type="submit" value="Submit"/>
  </form>
  {% endif %}
</div>
```

posts / views.py

```python
@login_required
```

로그인이 요구되는 함수 마다 적용해주기



posts / forms.py 수정

```python
class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'댓글을 작성하세요.'}))
    class Meta:
        model = Comment
        fields = ['content']
```

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
  <div class="card-body">
    {% for comment in post.comment_set.all %}
      <div class="card-text">
        <strong>{{ comment.user.username }}</strong> {{ comment.content }}
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

bootstrap 'Button addons' components 활용



posts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import PostForm, CommentForm
from .models import Post, Comment

@require_http_methods(['GET', 'POST'])
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('posts:list')
        
    comment.delete()
    return redirect('posts:list')
```

posts / urls.py 수정

```python
urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:post_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
```

_post.html / 수정

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

posts / models.py 수정

```python
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
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
 
```



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0006_post_like_users.py
    - Add field like_users to post

(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0006_post_like_users... OK
```

posts / views.py 수정

```python
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.like_users.all():
        # 2. 좋아요 취소
        post.like_users.remove(request.user)
    else:
        # 1. 좋아요!
        post.like_users.add(request.user)
    return redirect('posts:list')
```

posts / urls.py 수정

```python
urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:post_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_id>/like/', views.like, name='like'),
]
```

_post.html

```html
<div class="card" style="width: 18rem;">
  <div class="card-header">
    <span>{{ post.user.username }}</span>
  </div>
  {% if post.image %}
  <img src="{{ post.image.url }}" class="card-img-top" alt="{{ post.image }}">
  {% endif %}
  <div class="card-body">
    <a href="{% url 'posts:like' post.id %}">
      {% if user in post.like_users.all %}
        <i class="fas fa-heart"></i>
      {% else %}
        <i class="far fa-heart"></i>
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

accounts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contirb.auth import get_user_model

def people(request, username):
    # get_user_model() #=> User
    people = get_object_or_404(get_user_model(), username=username)
    return render(request, 'accounts/people.html', {'people':people})
```

insta / urls.py 수정

```python
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('<str:username>/', accounts_views.people, name='people'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

insta / templates / accounts / people.html 생성

``` html
{% extends 'base.html' %}

{% block container %}

<div class="container">
    <h1>{{ people.username }}</h1>
    <div class="row">
        {% for post in people.post_set.all %}
        <div class="col-4">
            <img src="{{ post.image.url }}" class="img-fluid"/>
        </div>
        {% endfor %}
    </div>
</div>

{% endblock %}
```


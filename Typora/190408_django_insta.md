```bash
minjaejin:~/workspace (master) $ cd django/insta
minjaejin:~/workspace/django/insta (master) $ \
> pyenv virtualenv 3.6.7 insta-venv
Looking in links: /tmp/tmp74jfmctv
Requirement already satisfied: setuptools in /home/ubuntu/.pyenv/versions/3.6.7/envs/insta-venv/lib/python3.6/site-packages (39.0.1)
Requirement already satisfied: pip in /home/ubuntu/.pyenv/versions/3.6.7/envs/insta-venv/lib/python3.6/site-packages (10.0.1)

minjaejin:~/workspace/django/insta (master) $ \
> pyenv local insta-venv
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> pip install django==2.1.8
Collecting django==2.1.8
  Downloading https://files.pythonhosted.org/packages/a9/e4/fb8f473fe8ee659859cb712e25222243bbd55ece7c319301eeb60ccddc46/Django-2.1.8-py3-none-any.whl (7.3MB)
    100% |████████████████████████████████| 7.3MB 5.3MB/s 
Collecting pytz (from django==2.1.8)
  Using cached https://files.pythonhosted.org/packages/61/28/1d3920e4d1d50b19bc5d24398a7cd85cc7b9a75a490570d5a30c57622d34/pytz-2018.9-py2.py3-none-any.whl
Installing collected packages: pytz, django
Successfully installed django-2.1.8 pytz-2018.9
You are using pip version 10.0.1, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> django-admin startproject insta .
(insta-venv) minjaejin:~/workspace/django/insta (master) $ ls
insta/  manage.py*
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py runserver $IP:$PORT
Performing system checks...

System check identified no issues (0 silenced).

You have 15 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

April 08, 2019 - 00:40:01
Django version 2.1.8, using settings 'insta.settings'
Starting development server at http://0.0.0.0:8080/
Quit the server with CONTROL-C.
```

settings.py 수정

```python
ALLOWED_HOSTS = ['playground-minjaejin.c9users.io']
```



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py startapp posts
(insta-venv) minjaejin:~/workspace/django/insta (master) $ ls
db.sqlite3  insta/  manage.py*  posts/
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
    'posts',
]
```

insta / posts / urls.py  생성

```python
from django.urls import path

app_name = 'posts'

urlpatterns = [
    
]
```

insta / insta / urls.py 수정

``` python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
]
```

models.py 수정

```python
class Post(models.Model):
    content = models.TextField()
```



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0001_initial.py
    - Create model Post
    
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying posts.0001_initial... OK
  Applying sessions.0001_initial... OK
```

insta / insta / templates / base.html 생성

``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    {% block container %}
    {% endblock %}
</body>
</html>
```

base.html에 bootstrap css js, fontawesome CDN 추가



views.py 수정

```python
def create(request):
    return render(request, 'posts/create.html')
```

posts / urls.py 수정

```python
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
]
```

posts / templates / posts / create.html 생성

```html
{% extends 'base.html' %}

{% block container %}

<h1>New Post</h1>

{% endblock %}
```

settings.py 수정

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'insta', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

posts / forms.py 생성

```python
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', ]
```

views.py 수정

```python
from django.shortcuts import render
from .forms import PostForm

# Create your views here.
def create(request):
    post_form = PostForm()
    return render(request, 'posts/create.html', {'post_form':post_form})
```



``` bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> pip install django-bootstrap4
Collecting django-bootstrap4
  Downloading https://files.pythonhosted.org/packages/02/5a/485d61f6dafa4e4d001a7880b04f40f04fe485a54b2756b0536ed2052342/django-bootstrap4-0.0.8.tar.gz
Installing collected packages: django-bootstrap4
  Running setup.py install for django-bootstrap4 ... done
Successfully installed django-bootstrap4-0.0.8
You are using pip version 10.0.1, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
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
    'posts',
]
```

create.html 수정

```html
{% extends 'base.html' %}

{% load bootstrap4 %}

{% block container %}

<h1>New Post</h1>
<form action="" method="post">
    {% csrf_token %}
    {% bootstrap_form post_form %}
    {% buttons %}
        <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>

{% endblock %}
```

views.py 수정

```python
from django.shortcuts import render, redirect
from .forms import PostForm

# Create your views here.
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
    return render(request, 'posts/create.html', {'post_form':post_form})
```

posts / urls.py 수정

```python
urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
]
```

views.py 수정

``` python
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post


def list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})
```

list.html 생성

```html
{% extends 'base.html' %}

{% block container %}

<h1>Post List</h1>
    
{% for post in posts %}

{% include 'posts/_post.html' %}
    
{% endfor %}

{% endblock %}
```

_post.html 생성

```html
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <p class="card-text">{{ post.content }}</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```

urls.py 수정

```python
urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
]
```

veiws.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post

def delete(request, post_id):
    # post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('posts:list')
```

_post.html 수정

```python
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <p class="card-text">{{ post.content }}</p>
    <a href="{% url 'posts:delete' post.id %}" class="btn btn-primary">Delete</a>
  </div>
</div>
```

!!! model을 수정했을 때 migrations 폴더 내의 __init__.py는 남기고 db.sqlite3 지우고 다시 마이그레이션 마이그레이트 크레이트수퍼유저 한다.


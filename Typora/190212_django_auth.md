190212_django_auth

```bash
(curd-venv) minjaejin:~/workspace/django/auth (master) $ ./manage.py startapp accounts
```

setting.py, INSTALLED_APPS에 추가

```python
'accounts.apps.AccountsConfig',
```

accounts폴더에 urls.py 생성

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    
]
```

crud 폴더 urls.py에  path 추가

```python
path('accounts/', include('accounts.urls')),
```

views.py에 signup함수 추가

```python
def signup(request):
    return render(request, 'signup.html')
```

urls.py에 path 추가

```python
path('signup/', views.signup, name='signup')
```

signup.html 생성

```html
{% extends 'base.html' %}

{% block container %}

<h1>회원가입</h1>

{% endblock %}
```

views.py 수정, import UserCreationForm 추가

```python
from django.shortcuts import render, redirect
from djnago.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('posts:list')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form':form})
```

signup.html 수정

```html
{% extends 'base.html' %}

{% block container %}

<h1>회원가입</h1>

<form method='post'>
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```

views.py에 login함수 추가

```python
def login(request):
    return render(request, 'login.html')
```

urls.py에 path 추가

```python
path('login/', views.login, name='login'),
```

login.html 생성

```html
{% extends 'base.html' %}

{% block container %}

<h1>로그인</h1>

{% endblock %}
```

views.py의 login 함수 수정, import AuthenticationForm, login as auth_login 추가

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:list')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form':form})
```

login.html 수정

```html
<h1>로그인</h1>

<form method='post'>
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit"/>
</form>

{% endblock %}
```

base.thml 수정

```html
<body>
    <h1>나는 {{ user.username }}</h1>
    {% block container %}
    {% endblock %}
    
</body>
```

views.py에 lougout 함수 추가, import logout as auth_logout  추가

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('posts:list')
```

urls.py에 path 추가

```python
path('logout/', views.logout, name='logout'),
```

base.html 수정

```html
<body>
    {% if user.is_authenticated %}
        <h1>
            나는 {{ user.username }}
            <a href="{% url 'accounts:logout' %}">로그아웃</a>
        </h1>
    {% else %}
        <h1>
            <a href="{% url 'accounts:login' %}">로그인</a>
            <a href="{% url 'accounts:signup' %}">회원가입</a>
        </h1>
    {% endif %}
    
    {% block container %}
    {% endblock %}
    
</body>
```

views.py의 signup 함수 수정

```python
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form':form})
```

views.py의 login 함수 수정

```python
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:list')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form':form})
```

posts 폴더 index.html 수정

```html
{% block container %}

    <img src="{% static 'scs.gif' %}"></img>
    <h1>Post Index</h1>
    
    {% if user.is_authenticated %}
        <a href="{% url 'posts:new' %}">New</a>
    {% endif %}
    
    <ul>
    {% for post in posts %}
        <li><a href="{% url 'posts:detail' post.pk %}">{{ post.title }}</a></li>    
    {% endfor %}
    </ul>

{% endblock %}
```

posts 폴더 views.py 수정, import login_required 추가, @login_required 추가

```python
from django.shortcuts import render, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
# views.py -> urls.py -> templates
@login_required
def new(request):
    if request.method == 'POST':
        # create
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # DB INSERT
        post = Post(title=title, content=content, image=image)
        post.save()
        
        return redirect('posts:detail', post.pk)
    
    else:
        #new
        return render(request, 'new.html')
    
```

accounts 폴더 views.py의 login 함수 수정

```python
# Session Create 
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')  # request.GET.get('next') => /posts/new/
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form':form})
```


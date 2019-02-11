190211_django_form

```bash
minjaejin:~/workspace/django/form (master) $ pyenv virtualenv 3.6.7 form-venv
Looking in links: /tmp/tmplf81_ood
Requirement already satisfied: setuptools in /home/ubuntu/.pyenv/versions/3.6.7/envs/form-venv/lib/python3.6/site-packages (39.0.1)
Requirement already satisfied: pip in /home/ubuntu/.pyenv/versions/3.6.7/envs/form-venv/lib/python3.6/site-packages (10.0.1)

minjaejin:~/workspace/django/form (master) $ pyenv local form-venv
(form-venv) minjaejin:~/workspace/django/form (master) $ pip install django
Collecting django
  Using cached https://files.pythonhosted.org/packages/36/50/078a42b4e9bedb94efd3e0278c0eb71650ed9672cdc91bd5542953bec17f/Django-2.1.5-py3-none-any.whl
Collecting pytz (from django)
  Using cached https://files.pythonhosted.org/packages/61/28/1d3920e4d1d50b19bc5d24398a7cd85cc7b9a75a490570d5a30c57622d34/pytz-2018.9-py2.py3-none-any.whl
Installing collected packages: pytz, django
Successfully installed django-2.1.5 pytz-2018.9
You are using pip version 10.0.1, however version 19.0.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(form-venv) minjaejin:~/workspace/django/form (master) $ \
django-admin startproject form .
(form-venv) minjaejin:~/workspace/django/form (master) $ ls
form/  manage.py*

(form-venv) minjaejin:~/workspace/django/form (master) $ \
./manage.py runserver $IP:$PORT
```

새 터미널

```bash
(form-venv) minjaejin:~/workspace/django/form (master) $ ./manage.py startapp articles
```

setting.py, INSTALLED_APPS 에 articles app 추가

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'articles.apps.ArticlesConfig',
]

```

articles 폴더에 urls.py 생성

```python
from django.urls import path

app_name = 'articles'

urlpatterns = [
    
]
```

from 폴더 urls.py 에 articles 폴더 urls 경로 추가, import include 추가

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('articles/', include('articles.urls')),
    path('admin/', admin.site.urls),
]
```

models.py 에 Article class 추가

```python
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

```bash
(form-venv) minjaejin:~/workspace/django/form (master) $ ./manage.py startapp articles
(form-venv) minjaejin:~/workspace/django/form (master) $ ./manage.py makemigrations
Migrations for 'articles':
  articles/migrations/0001_initial.py
    - Create model Article
    
(form-venv) minjaejin:~/workspace/django/form (master) $ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, articles, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying articles.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying sessions.0001_initial... OK    
```

views.py 에 create 함수 추가  **if 문 특별한 명령 없을 때 pass 필요!

```python
def create(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'create.html')
```

urls.py에 경로 추가, import views 추가

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('new/', views.create, name='create'),
]
```

articles 폴더에 templates 폴더 생성, 그 안에 create.html 생성  **post mehtod는 crsf_token 필수!

required 로 입력 오류 방지

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1>New Article</h1>
    
    <form method='post'>
        {% csrf_token %}
        <input type="text" name="title" required/>
        <input type="text" name="content" required/>
        <input type="submit" value="Submit"/>
    </form>
</body>
</html>
```

views.py의 create 함수 완성, import redirect, Article 추가, detail 함수 추가

```python
from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # article = Article(title=title, content=content)
        # article.save()
        article = Article.objects.create(title=title, content=content)
        return redirect('articles:detail', article.pk)
    else:
        return render(request, 'create.html')
        
def detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    return render(reqeust, 'detail.html', {'article':article})
```

urls.py에 detail path 추가

```python
path('<int:article_id>/', views.detail, name='detail')
```

detatil.html 생성

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1>Article Detail</h1>
    
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
</body>
</html>
```

articles 폴더에 forms.py 생성 **CharField의 max_length 필수 아님

```python
from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(label='제목')
    content = forms.CharField(label='내용', widget=forms.Textarea(attrs={
        'rows': 5,
        'cols': 50,
        'placeholder': '내용을 입력하세요.',
    }))
```

views.py에 create 함수 수정, import ArticleForm 추가

```python
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # article = Article(title=title, content=content)
        # article.save()
        article = Article.objects.create(title=title, content=content)
        return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
        return render(request, 'create.html', {'form':form})
```

create.html 수정

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1>New Article</h1>
    
    <form method='post'>
        {% csrf_token %}
        <!--<input type="text" name="title" required/>-->
        <!--<input type="text" name="content" required/>-->
        {{ form }}
        <input type="submit" value="Submit"/>
    </form>
</body>
</html>
```

views.py에 create 함수 수정 

```python
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            # article.save()
            article = Article.objects.create(title=title, content=content)
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
        
    return render(request, 'create.html', {'form':form})
```

forms.py에 ArticleModelFrom class 추가, import ARticle 추가

```python
from django import forms
from .models import Article

class ArticleForm(forms.Form):
    title = forms.CharField(label='제목')
    content = forms.CharField(label='내용', widget=forms.Textarea(attrs={
        'rows': 5,
        'cols': 50,
        'placeholder': '내용을 입력하세요.',
    }))
    
class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
```

views.py에 create 함수 수정, import ArticleModelForm 추가, update 함수 추가

```python
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleModelForm

# Create your views here.
def create(request):
    if request.method == 'POST':
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            article = form.save()
            # title = form.cleaned_data.get('title')
            # content = form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            # article.save()
            # article = Article.objects.create(title=title, content=content)
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleModelForm()
        
    return render(request, 'create.html', {'form':form})
        
        
def detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    return render(request, 'detail.html', {'article':article})
    

def update(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'POST':
        form = ArticleModelForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleModelForm(instance=article)
        
    return render(request, 'create.html', {'form':form})
```

urls.py에 path 추가

```python
path('<int:article_id>/edit/', views.update, name='update')
```

create.html 이름 form.html로 변경

form.html 수정

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1>New Article</h1>
    
    {{ form.non_field_errors }}
    <form method='post'>
        {% csrf_token %}
        <!--<input type="text" name="title" required/>-->
        <!--<input type="text" name="content" required/>-->
        <!-- 1.title -->
        <div>
            {{form.title.errors }} <!-- error messages (ul, li tag) -->
            {{ form.title.label_tag }} <!-- label tag -->
            {{ form.title }} <!-- input tag -->
        </div>
        <!-- 2.content -->
        <div>
            {{ form.content.errors }}
            {{ form.content.label_tag }}
            {{ form.content }}
        </div>
        
        <input type="submit" value="Submit"/>
    </form>
</body>
</html> 
```


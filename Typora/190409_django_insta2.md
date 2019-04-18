posts / urls.py 수정

```python
urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
]
```

views.py 수정

```python
def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
    return render(request, 'posts/create.html', {'post_form':post_form})
```

_posts.html 수정

```html
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <p class="card-text">{{ post.content }}</p>
    <a href="{% url 'posts:update' post.id %}" class="btn btn-info">Edit</a>
    <a href="{% url 'posts:delete' post.id %}" class="btn btn-danger">Delete</a>
  </div>
</div>
```



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> pip install pillow
Collecting pillow
  Downloading https://files.pythonhosted.org/packages/d2/c2/f84b1e57416755e967236468dcfb0fad7fd911f707185efc4ba8834a1a94/Pillow-6.0.0-cp36-cp36m-manylinux1_x86_64.whl (2.0MB)
    100% |████████████████████████████████| 2.0MB 13.5MB/s 
Installing collected packages: pillow
Successfully installed pillow-6.0.0
You are using pip version 10.0.1, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command
```

models.py 수정

```python
class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(blank=True)
```



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0002_post_image.py
    - Add field image to post

(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0002_post_image... OK
```

forms.py 수정

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image',]
```

create.html 수정

```html
<form action="" method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {% bootstrap_form post_form %}
    {% buttons %}
        <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>
```

views.py 수정

```python
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
    return render(request, 'posts/create.html', {'post_form':post_form})
```

setting.py 수정

```python
# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

insta / urls.py 수정

```python
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

_post.html 수정

```html
<div class="card" style="width: 18rem;">
  {% if post.image %}
  <img src="{{ post.image.url }}" class="card-img-top" alt="{{ post.image }}">
  {% endif %}
  <div class="card-body">
    <p class="card-text">{{ post.content }}</p>
    <a href="{% url 'posts:update' post.id %}" class="btn btn-info">Edit</a>
    <a href="{% url 'posts:delete' post.id %}" class="btn btn-danger">Delete</a>
  </div>
</div>
```

views.py 수정

```python
def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
    return render(request, 'posts/create.html', {'post_form':post_form})
```



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> pip install pilkit django-imagekit
Collecting pilkit
  Using cached https://files.pythonhosted.org/packages/c4/5c/318d9c20f309e6a79ea4d4605f86597d05f3e007d3d1925ff02474808659/pilkit-2.0.tar.gz
Collecting django-imagekit
  Using cached https://files.pythonhosted.org/packages/e5/2a/a5c62376e897c23d1ce21be86c18e68096cb8c83df7d010d24ca81139e9e/django_imagekit-4.0.2-py2.py3-none-any.whl
Collecting six (from django-imagekit)
  Using cached https://files.pythonhosted.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl
Collecting django-appconf>=0.5 (from django-imagekit)
  Downloading https://files.pythonhosted.org/packages/f6/b3/fcec63afcf323581c4919f21e90ef8c8200034108a6a0ab47a6bf6a9327b/django_appconf-1.0.3-py2.py3-none-any.whl
Requirement already satisfied: django in /home/ubuntu/.pyenv/versions/3.6.7/envs/insta-venv/lib/python3.6/site-packages (from django-appconf>=0.5->django-imagekit) (2.1.8)
Requirement already satisfied: pytz in /home/ubuntu/.pyenv/versions/3.6.7/envs/insta-venv/lib/python3.6/site-packages (from django->django-appconf>=0.5->django-imagekit) (2018.9)
Installing collected packages: pilkit, six, django-appconf, django-imagekit
  Running setup.py install for pilkit ... done
Successfully installed django-appconf-1.0.3 django-imagekit-4.0.2 pilkit-2.0 six-1.12.0
You are using pip version 10.0.1, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```

setting.py 수정

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
    'posts',
]
```

models.py 수정

```python
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    # image = models.ImageField(blank=True)
    image = ProcessedImageField(
            upload_to='posts/images', # 저장 위치
            processors=[ResizeToFill(600,600)], # 처리할 작업 목록
            format='JPEG', # 저장 포맷
            options={'quality':90}, # 옵션
        )
```



```bash
(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0003_auto_20190409_0224.py
    - Alter field image on post

(insta-venv) minjaejin:~/workspace/django/insta (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0003_auto_20190409_0224... OK
```

models.py 수정

```python
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


def post_image_path(instance, filename):
    return f'posts/images/{filename}'


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    # image = models.ImageField(blank=True)
    image = ProcessedImageField(
            upload_to=post_image_path, # 저장 위치
            processors=[ResizeToFill(600,600)], # 처리할 작업 목록
            format='JPEG', # 저장 포맷
            options={'quality':90}, # 옵션
        )
```


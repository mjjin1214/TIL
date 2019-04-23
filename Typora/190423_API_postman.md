```bash
minjaejin:~/workspace/django/api (master) $ pyenv virtualenv 3.6.7 api-venv
Looking in links: /tmp/tmpe7el9it9
Requirement already satisfied: setuptools in /home/ubuntu/.pyenv/versions/3.6.7/envs/api-venv/lib/python3.6/site-packages (39.0.1)
Requirement already satisfied: pip in /home/ubuntu/.pyenv/versions/3.6.7/envs/api-venv/lib/python3.6/site-packages (10.0.1)

minjaejin:~/workspace/django/api (master) $ pyenv local api-venv                
(api-venv) minjaejin:~/workspace/django/api (master) $ \
> pip install django==2.1.8
Collecting django==2.1.8
  Using cached https://files.pythonhosted.org/packages/a9/e4/fb8f473fe8ee659859cb712e25222243bbd55ece7c319301eeb60ccddc46/Django-2.1.8-py3-none-any.whl
Collecting pytz (from django==2.1.8)
  Using cached https://files.pythonhosted.org/packages/3d/73/fe30c2daaaa0713420d0382b16fbb761409f532c56bdcc514bf7b6262bb6/pytz-2019.1-py2.py3-none-any.whl
Installing collected packages: pytz, django
Successfully installed django-2.1.8 pytz-2019.1
You are using pip version 10.0.1, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(api-venv) minjaejin:~/workspace/django/api (master) $ \
> pip install djangorestframework
Collecting djangorestframework
  Downloading https://files.pythonhosted.org/packages/cc/6d/5f225f18d7978d8753c1861368efc62470947003c7f9f9a5cc425fc0689b/djangorestframework-3.9.2-py2.py3-none-any.whl (911kB)
    100% |████████████████████████████████| 921kB 9.5MB/s 
Installing collected packages: djangorestframework
Successfully installed djangorestframework-3.9.2
You are using pip version 10.0.1, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(api-venv) minjaejin:~/workspace/django/api (master) $ \
> django-admin startproject api .

(api-venv) minjaejin:~/workspace/django/api (master) $ \
> ./manage.py startapp musics
```



settings.py 수정

```python
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'musics',
]
```



musics / models.py 생성

```python
class Artist(models.Model):
    name = models.TextField()
    
    def __str__(self):
        return self.name
        
        
class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.TextField()
    
    def __str__(self):
        return self.title
        

class Comment(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    content = models.TextField()
```



```bash
(api-venv) minjaejin:~/workspace/django/api (master) $ ./manage.py makemigrations
Migrations for 'musics':
  musics/migrations/0001_initial.py
    - Create model Artist
    - Create model Comment
    - Create model Music
    - Add field music to comment
    
(api-venv) minjaejin:~/workspace/django/api (master) $ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, musics, sessions
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
  Applying musics.0001_initial... OK
  Applying sessions.0001_initial... OK
```



admin.py 수정

```python
from django.contrib import admin
from .models import Artist, Music, Comment

# Register your models here.
admin.site.register(Artist)
admin.site.register(Music)
admin.site.register(Comment)
```



```bash
(api-venv) minjaejin:~/workspace/django/api (master) $ \
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
```



musics / urls.py 생성

```python
from django.urls import path
from . import views

urlpatterns = [
    path('musics/', views.music_list),
]
```



api / urls.py 수정

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('musics.urls')),
]

```



musics / serializers.py 생성

```python
from rest_framework import serializers
from .models import Music

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'title', 'artist',]
```



views.py 수정

```python
from django.shortcuts import render
from .models import Music
from rest_framework.decorators import api_view
from .serializers import MusicSerializer
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def music_list(request):
    musics = Music.objects.all()
    serializer = MusicSerializer(musics, many=True)
    return Response(serializer.data)
```



musics / urls.py 수정

```python
urlpatterns = [
    path('musics/', views.music_list),
    path('musics/<int:music_id>/', views.music_detail),
]
```



views.py 수정

``` python
from django.shortcuts import render, get_object_or_404
from .models import Music
from rest_framework.decorators import api_view
from .serializers import MusicSerializer
from rest_framework.response import Response

@api_view(['GET'])
def music_detail(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    serializer = MusicSerializer(music)
    return Response(serializer.data)
```



```bash
(api-venv) minjaejin:~/workspace/django/api (master) $ \
> pip install django-rest-swagger
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
    'rest_framework',
    'rest_framework_swagger',
    'musics',
]
```



musics / urls.py 수정

```python
from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('docs/', get_swagger_view(title='API Docs')),
    path('musics/', views.music_list),
    path('musics/<int:music_id>/', views.music_detail),
]
```

swagger framework 활용하기 위해 url 추가



serializers.py 수정

``` python
from rest_framework import serializers
from .models import Music, Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name',]
```



musics / urls.py 수정

```python
urlpatterns = [
    path('docs/', get_swagger_view(title='API Docs')),
    path('musics/', views.music_list),
    path('musics/<int:music_id>/', views.music_detail),
    path('artists/', views.artist_list), 
]
```



views.py 수정

```python
from django.shortcuts import render, get_object_or_404
from .models import Music, Artist
from rest_framework.decorators import api_view
from .serializers import MusicSerializer, ArtistSerializer
from rest_framework.response import Response

def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)
```



musics / urls.py 수정

```python
urlpatterns = [
    path('docs/', get_swagger_view(title='API Docs')),
    path('musics/', views.music_list),
    path('musics/<int:music_id>/', views.music_detail),
    path('artists/', views.artist_list),
    path('artists/<int:artist_id>/', views.artist_detail),
]
```



serializers.py 수정

```python
class ArtistDetailSerializer(serializers.ModelSerializer):
    music_set = MusicSerializer(many=True)
    class Meta:
        model = Artist
        fields = ['id', 'name', 'music_set',]
```



views.py 수정

```python
from django.shortcuts import render, get_object_or_404
from .models import Music, Artist
from rest_framework.decorators import api_view
from .serializers import MusicSerializer, ArtistSerializer, ArtistDetailSerializer
from rest_framework.response import Response

@api_view(['GET'])
def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    serializer = ArtistDetailSerializer(artist)
    return Response(serializer.data)
```



musics / urls.py 수정

```python
urlpatterns = [
    path('docs/', get_swagger_view(title='API Docs')),
    path('musics/', views.music_list),
    path('musics/<int:music_id>/', views.music_detail),
    path('musics/<int:music_id>/comments/', views.comment_create),
    path('artists/', views.artist_list),
    path('artists/<int:artist_id>/', views.artist_detail),
]
```



serializers.py 수정

```python
from rest_framework import serializers
from .models import Music, Artist, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', ]
```



views.py 수정

```python
from django.shortcuts import render, get_object_or_404
from .models import Music, Artist
from rest_framework.decorators import api_view
from .serializers import MusicSerializer, ArtistSerializer, ArtistDetailSerializer, CommentSerializer
from rest_framework.response import Response

@api_view(['POST'])
def comment_create(request, music_id):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(music_id=music_id)
        return Response(serializer.data)
```

raise_exception=True 올바르지 않은 값이 들어왔을 때 코드에서 에러가 나는 것을 사용자가 알수있도록



musics / urls.py 수정

```python
urlpatterns = [
    path('docs/', get_swagger_view(title='API Docs')),
    path('musics/', views.music_list),
    path('musics/<int:music_id>/', views.music_detail),
    path('musics/<int:music_id>/comments/', views.comment_create),
    path('musics/<int:music_id>/comments/<int:comment_id>/', views.comment_update_and_delete),
    path('artists/', views.artist_list),
    path('artists/<int:artist_id>/', views.artist_detail),
]
```



views.py 수정

```python
@api_view(['PUT', 'DELETE'])    
def comment_update_and_delete(request, music_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Comment has been updated!'})
    else:
        comment.delete()
        return Response({'message':'Comment has been deleted!'})
```


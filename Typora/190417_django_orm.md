```bash
minjaejin:~/workspace/django/orm (master) $ \
> pyenv local orm-venv
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> pip freeze
alembic==1.0.6
Click==7.0
Flask==1.0.2
Flask-Migrate==2.3.1
Flask-SQLAlchemy==2.3.2
itsdangerous==1.1.0
Jinja2==2.10
Mako==1.0.7
MarkupSafe==1.1.0
python-dateutil==2.7.5
python-editor==1.0.3
six==1.12.0
SQLAlchemy==1.2.16
Werkzeug==0.14.1

(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> pip install django==2.1.8
Collecting django==2.1.8
  Using cached https://files.pythonhosted.org/packages/a9/e4/fb8f473fe8ee659859cb712e25222243bbd55ece7c319301eeb60ccddc46/Django-2.1.8-py3-none-any.whl
Collecting pytz (from django==2.1.8)
  Downloading https://files.pythonhosted.org/packages/3d/73/fe30c2daaaa0713420d0382b16fbb761409f532c56bdcc514bf7b6262bb6/pytz-2019.1-py2.py3-none-any.whl (510kB)
    100% |████████████████████████████████| 512kB 18.3MB/s 
Installing collected packages: pytz, django
Successfully installed django-2.1.8 pytz-2019.1
You are using pip version 19.0, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> django-admin startproject orm .
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py startapp crud
(orm-venv) minjaejin:~/workspace/django/orm (master) $ ls
crud/  manage.py*  orm/
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
    'crud',
]
```

crud 추가



models.py 수정

```python
from django.db import models

# Create your models here.
class Post(mdels.Model):
    title = models.TextField()
```

Post 모델 생성



```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py makemigrations
Migrations for 'crud':
  crud/migrations/0001_initial.py
    - Create model Post
    
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, crud, sessions
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
  Applying crud.0001_initial... OK
  Applying sessions.0001_initial... OK
  
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> pip install django_extensions
Collecting django_extensions
  Downloading https://files.pythonhosted.org/packages/26/66/613b34aa7246e1be223e7f539212d8972e41046ec7f2b8bc0ba3e2cfcf22/django_extensions-2.1.6-py2.py3-none-any.whl (218kB)
    100% |████████████████████████████████| 225kB 7.0MB/s 
Requirement already satisfied: six>=1.2 in /home/ubuntu/.pyenv/versions/3.6.7/envs/orm-venv/lib/python3.6/site-packages (from django_extensions) (1.12.0)
Installing collected packages: django-extensions
Successfully installed django-extensions-2.1.6
You are using pip version 19.0, however version 19.0.3 is available.
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
    'django_extensions',
    'crud',
]
```



```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py shell_plus
```

```shell
# Shell Plus Model Imports
from crud.models import Post
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
# Shell Plus Django Imports
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, Exists, OuterRef, Subquery
from django.utils import timezone
from django.urls import reverse
Python 3.6.7 (default, Jan 21 2019, 06:56:12) 
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

>>> post = Post(title='hello-1')
>>> post
<Post: Post object (None)>

>>> post.title
'hello-1'

>>> post.save()
>>> post
<Post: Post object (1)>

>>> Post.objects
<django.db.models.manager.Manager object at 0x7eff1a8c64a8>

>>> post2 = Post.objects.create(title='hello-2')
>>> post2
<Post: Post object (2)>

>>> post3 = Post()
>>> post3
<Post: Post object (None)>

>>> post3.title
''

>>> post3.title = 'hello-3'
>>> post3.title
'hello-3'

>>> post3
<Post: Post object (None)>

>>> post3.save()
>>> post3
<Post: Post object (3)>

>>> Post.objects.all()
<QuerySet [<Post: Post object (1)>, <Post: Post object (2)>, <Post: Post object (3)>]>

>>> posts = Post.objects.all()
>>> posts
<QuerySet [<Post: Post object (1)>, <Post: Post object (2)>, <Post: Post object (3)>]>

>>> Post.objects.get(id=1)
<Post: Post object (1)>

>>> Post.objects.get(pk=1)
<Post: Post object (1)>

>>> Post.objects.get(title='hello-2')
<Post: Post object (2)>

>>> Post.obejcts.get(title='goodbye')
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: type object 'Post' has no attribute 'obejcts'

>>> Post.objects.filter(pk=1)
<QuerySet [<Post: Post object (1)>]>

>>> Post.objects.filter(pk=1)[0]
<Post: Post object (1)>

>>> Post.objects.filter(pk=1).first()
<Post: Post object (1)>

>>> Post.objects.create(title='hello-1')
<Post: Post object (4)>

>>> Post.objects.filter(title='hello-1')
<QuerySet [<Post: Post object (1)>, <Post: Post object (4)>]>

>>> Post.objects.filter(title='hello')
<QuerySet []>

>>> Post.objects.filter(title='hello').first()
>>> Post.objects.filter(title='hello-1')
<QuerySet [<Post: Post object (1)>, <Post: Post object (4)>]>

>>> Post.objects.filter(title__contains='lo')
<QuerySet [<Post: Post object (1)>, <Post: Post object (2)>, <Post: Post object (3)>, <Post: Post object (4)>]>

>>> Post.objects.all()
<QuerySet [<Post: Post object (1)>, <Post: Post object (2)>, <Post: Post object (3)>, <Post: Post object (4)>]>

>>> Post.objects.order_by('title')
<QuerySet [<Post: Post object (1)>, <Post: Post object (4)>, <Post: Post object (2)>, <Post: Post object (3)>]>

>>> Post.objects.filter(title__contains='hello').order_by('-id')
<QuerySet [<Post: Post object (4)>, <Post: Post object (3)>, <Post: Post object (2)>, <Post: Post object (1)>]>s

>>> Post.objects.all()[0]
<Post: Post object (1)>

>>> Post.objects.all()[1]
<Post: Post object (2)>

>>> post1 = Post.objects.get(pk=1)
>>> post1
<Post: Post object (1)>

>>> post1.title
'hello-1'

>>> post1.title = 'hello-5'
>>> post1.title
'hello-5'

>>> post = Post.objects.get(pk=1)
>>> post
<Post: Post object (1)>

>>> post.title
'hello-1'

>>> post1.save()
>>> post1.title
'hello-5'

>>> post.title
'hello-1'

>>> post = Post.objects.get(pk=1)
>>> post.title
'hello-5'

>>> post
<Post: Post object (1)>

>>> post.delete()
(1, {'crud.Post': 1})

>>> post
<Post: Post object (None)>

>>> post.title
'hello-5'
```



```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py startapp onetomany
```

onetomany 앱 생성



settings.py 수정

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'crud',
    'onetomany',
]
```

onetomany 앱 등록



onetomany / models.py 수정

```python
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.TextField()
    
# User:Post = 1:N
class Post(models.Model):
    title = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

# User:Comment = 1:N
# Post:Comment = 1:N
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
```



```bash
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py makemigrations
Migrations for 'onetomany':
  onetomany/migrations/0001_initial.py
    - Create model Comment
    - Create model Post
    - Create model User
    - Add field user to post
    - Add field post to comment
    - Add field user to comment
    
(orm-venv) minjaejin:~/workspace/django/orm (master) $ \
> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, crud, onetomany, sessions
Running migrations:
  Applying onetomany.0001_initial... OK
```



```shell
>>> user1 = User.objects.create(name='Kim')
>>> user2 = User.objects.create(name='Lee')
>>> post1 = Post.objects.create(title='1글', user=user1)
>>> post2 = Post.objects.create(title='2글', user=user1)
>>> post3 = Post.objects.create(title='3글', user=user2)
>>> c1 = Comment.objects.create(content='1글1댓글', user=user1, post=post1)
>>> c2 = Comment.objects.create(content='1글2댓글', user=user2, post=post1)
>>> c3 = Comment.objects.create(content='1글3댓글', user=user1, post=post1)
>>> c4 = Comment.objects.create(content='1글4댓글', user=user2, post=post1)
>>> c5 = Comment.objects.create(content='2글1댓글', user=user1, post=post2)
>>> c6 = Comment.objects.create(content='!1글5댓글', user=user2, post=post1)
>>> c7 = Comment.objects.create(content='!2글2댓글', user=user2, post=post2)
>>> user1
<User: User object (1)>

>>> user2
<User: User object (2)>

>>> user1.post_set.all()
<QuerySet [<Post: Post object (1)>, <Post: Post object (2)>]>

>>> for post in user1.post_set.all():
...     for comment in post.comment_set.all():
...             print(comment.content)
... 
1글1댓글
1글2댓글
1글3댓글
1글4댓글
!1글5댓글
2글1댓글
!2글2댓글

>>> post1.comment_set.first().user.name
'Kim'

>>> post1.comment_set.all()[0].user.name
'Kim'

>>> Post.objects.filter(title='1글')
<QuerySet [<Post: Post object (1)>]>

>>> Comment.objects.filter(post__title='1글')
<QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>, <Comment: Comment object (3)>, <Comment: Comment object (4)>, <Comment: Comment object (6)>]>

>>> Comment.objects.filter(post__title__contains='1')
<QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>, <Comment: Comment object (3)>, <Comment: Comment object (4)>, <Comment: Comment object (6)>]>
```


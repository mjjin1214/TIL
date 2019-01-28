190128

django

```bash
minjaejin:~/workspace/django/crud (master) $ pyenv virtualenv 3.6.7 curd-venv
Looking in links: /tmp/tmp0i__2bhb
Requirement already satisfied: setuptools in /home/ubuntu/.pyenv/versions/3.6.7/envs/curd-venv/lib/python3.6/site-packages (39.0.1)
Requirement already satisfied: pip in /home/ubuntu/.pyenv/versions/3.6.7/envs/curd-venv/lib/python3.6/site-packages (10.0.1)

minjaejin:~/workspace/django/crud (master) $ pyenv local curd-venv
(curd-venv) minjaejin:~/workspace/django/crud (master) $ pip install django
Collecting django
  Using cached https://files.pythonhosted.org/packages/36/50/078a42b4e9bedb94efd3e0278c0eb71650ed9672cdc91bd5542953bec17f/Django-2.1.5-py3-none-any.whl
Collecting pytz (from django)
  Using cached https://files.pythonhosted.org/packages/61/28/1d3920e4d1d50b19bc5d24398a7cd85cc7b9a75a490570d5a30c57622d34/pytz-2018.9-py2.py3-none-any.whl
Installing collected packages: pytz, django
Successfully installed django-2.1.5 pytz-2018.9
You are using pip version 10.0.1, however version 19.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(curd-venv) minjaejin:~/workspace/django/crud (master) $ django-admin startproject crud .
(curd-venv) minjaejin:~/workspace/django/crud (master) $ python manage.py runserver $IP:$PORT

^C
(curd-venv) minjaejin:~/workspace/django/crud (master) $ python manage.py startapp posts
(curd-venv) minjaejin:~/workspace/django/crud (master) $ \
> python manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0001_initial.py
    - Create model Post
    
(curd-venv) minjaejin:~/workspace/django/crud (master) $ python manage.py migrate
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
  
(curd-venv) minjaejin:~/workspace/django/crud (master) $ python manage.py shell
Python 3.6.7 (default, Jan 21 2019, 06:56:12) 
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
```

```bash
>>> from posts.models import Post
>>> post = Post(title='hello', content='world!')
>>> post
<Post: Post object (None)>

>>> post.title
'hello'

>>> post.save()
>>> Post.objects.all()
<QuerySet [<Post: Post object (1)>]>

>>> post = Post.objects.get(pk=1)
>>> post
<Post: Post object (1)>

>>> post.title
'hello'
>>> posts = Post.objects.filter(title='hello').all()
>>> posts
<QuerySet [<Post: Post object (1)>]>

>>> post = Post.objects.filter(title='hello').first()
>>> post
<Post: Post object (1)>

>>> posts = Post.objects.filter(title__contains='He').all()
>>> posts
<QuerySet [<Post: Post object (1)>]>

>>> posts = Post.objects.order_by('title').all()
>>> posts
<QuerySet [<Post: Post object (2)>, <Post: Post object (1)>, <Post: Post object (3)>]>

>>> posts = Post.objects.order_by('-title').all()
>>> posts
<QuerySet [<Post: Post object (3)>, <Post: Post object (1)>, <Post: Post object (2)>]>

>>> post = Post(title='2번째', content='입니다')
>>> post.save()
>>> post= Post(title='third', content='!!')
>>> post.save()
>>> Post.objects.all()
<QuerySet [<Post: Post object (1)>, <Post: Post object (2)>, <Post: Post object (3)>]>

>>> Post.objects.all()[:1]
<QuerySet [<Post: Post object (1)>]>

>>> post = Post.objects.get(pk=2)
>>> post.title
'2번째'
>>> post.delete()
(1, {'posts.Post': 1})

>>> Post.objects.all()
<QuerySet [<Post: Post object (1)>, <Post: Post object (3)>]>

>>> post = Post.objects.get(pk=1)
>>> post.title
'hello'

>>> post.title = 'hi'
>>> post.title
'hi'

>>> post.save()
>>> post = Post.objects.get(pk=1)
>>> post.title
'hi'
```

```
(curd-venv) minjaejin:~/workspace/django/crud (master) $ \
> python manage.py createsuperuser
사용자 이름 (leave blank to use 'ubuntu'): admin
이메일 주소: admin@admin.com
Password: 
Password (again): 
비밀번호가 이메일 주소와 너무 유사합니다.
비밀번호가 너무 짧습니다. 최소 8 문자를 포함해야 합니다.
비밀번호가 너무 일상적인 단어입니다.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```


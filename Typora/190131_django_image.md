190131

django_image

```bash
(curd-venv) minjaejin:~/workspace/django/crud-files (master) $ python manage.py makemigrations
You are trying to add the field 'created_at' with 'auto_now_add=True' to comment without a default; the database needs something to populate existing rows.

 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py

Select an option: 1
Please enter the default value now, as valid Python
You can accept the default 'timezone.now' by pressing 'Enter' or you can provide another value.
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt

[default: timezone.now] >>> 
Migrations for 'posts':
  posts/migrations/0003_auto_20190131_1024.py
    - Add field created_at to comment
    - Add field updated_at to comment
    
(curd-venv) minjaejin:~/workspace/django/crud-files (master) $ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0003_auto_20190131_1024... OK
  
(curd-venv) minjaejin:~/workspace/django/crud-files (master) $ pip install Pillow
Collecting Pillow
  Downloading https://files.pythonhosted.org/packages/85/5e/e91792f198bbc5a0d7d3055ad552bc4062942d27eaf75c3e2783cf64eae5/Pillow-5.4.1-cp36-cp36m-manylinux1_x86_64.whl (2.0MB)
    100% |████████████████████████████████| 2.0MB 11.0MB/s 
Installing collected packages: Pillow
Successfully installed Pillow-5.4.1
You are using pip version 10.0.1, however version 19.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(curd-venv) minjaejin:~/workspace/django/crud-files (master) $ pip install pilkit
Collecting pilkit
  Downloading https://files.pythonhosted.org/packages/c4/5c/318d9c20f309e6a79ea4d4605f86597d05f3e007d3d1925ff02474808659/pilkit-2.0.tar.gz (161kB)
    100% |████████████████████████████████| 163kB 5.9MB/s 
Installing collected packages: pilkit
  Running setup.py install for pilkit ... done
Successfully installed pilkit-2.0
You are using pip version 10.0.1, however version 19.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(curd-venv) minjaejin:~/workspace/django/crud-files (master) $ pip install django-imagekit
Collecting django-imagekit
  Downloading https://files.pythonhosted.org/packages/e5/2a/a5c62376e897c23d1ce21be86c18e68096cb8c83df7d010d24ca81139e9e/django_imagekit-4.0.2-py2.py3-none-any.whl (47kB)
    100% |████████████████████████████████| 51kB 1.8MB/s 
Collecting django-appconf>=0.5 (from django-imagekit)
  Downloading https://files.pythonhosted.org/packages/5b/78/726cdf3e04660560cf25f9def95b8f2736310c581dabed9adfe60154a9f8/django_appconf-1.0.2-py2.py3-none-any.whl
Requirement already satisfied: pilkit>=0.2.0 in /home/ubuntu/.pyenv/versions/3.6.7/envs/curd-venv/lib/python3.6/site-packages (from django-imagekit) (2.0)
Collecting six (from django-imagekit)
  Using cached https://files.pythonhosted.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl
Installing collected packages: django-appconf, six, django-imagekit
Successfully installed django-appconf-1.0.2 django-imagekit-4.0.2 six-1.12.0
You are using pip version 10.0.1, however version 19.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

(curd-venv) minjaejin:~/workspace/django/crud-files (master) $ pip install pilkit
Requirement already satisfied: pilkit in /home/ubuntu/.pyenv/versions/3.6.7/envs/curd-venv/lib/python3.6/site-packages (2.0)
You are using pip version 10.0.1, however version 19.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.


```


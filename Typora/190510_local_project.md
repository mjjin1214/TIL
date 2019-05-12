```bash
student@DESKTOP MINGW64 ~
$ cd minjae/django
bash: cd: minjae/django: No such file or directory

student@DESKTOP MINGW64 ~
$ cd minjae

student@DESKTOP MINGW64 ~/minjae (master)
$ cd django

student@DESKTOP MINGW64 ~/minjae/django (master)
$ python -V
Python 3.5.3

student@DESKTOP MINGW64 ~/minjae/django (master)
$ mkdir api

student@DESKTOP MINGW64 ~/minjae/django (master)
$ cd api

student@DESKTOP MINGW64 ~/minjae/django/api (master)
$ cd ~

student@DESKTOP MINGW64 ~
$ code .bash_profile
```



.bash_profile 수정

```shell 
alias pyton='winpty python'
```



```cmd
C:\Users\student\minjae\django\api>api-venv\Scripts\activate.bat
(api-venv) C:\Users\student\minjae\django\api>pip install django
Collecting django
  Downloading https://files.pythonhosted.org/packages/b1/1d/2476110614367adfb079a9bc718621f9fc8351e9214e1750cae1832d4090/Django-2.2.1-py3-none-any.whl (7.4MB)
    100% |################################| 7.5MB 244kB/s
Collecting sqlparse (from django)
  Downloading https://files.pythonhosted.org/packages/ef/53/900f7d2a54557c6a37886585a91336520e5539e3ae2423ff1102daf4f3a7/sqlparse-0.3.0-py2.py3-none-any.whl
Collecting pytz (from django)
  Cache entry deserialization failed, entry ignored
  Downloading https://files.pythonhosted.org/packages/3d/73/fe30c2daaaa0713420d0382b16fbb761409f532c56bdcc514bf7b6262bb6/pytz-2019.1-py2.py3-none-any.whl (510kB)
    100% |################################| 512kB 3.2MB/s
Installing collected packages: sqlparse, pytz, django
Successfully installed django-2.2.1 pytz-2019.1 sqlparse-0.3.0
You are using pip version 9.0.1, however version 19.1.1 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.

(api-venv) C:\Users\student\minjae\django\api>django-admin startproject api .

(api-venv) C:\Users\student\minjae\django\api>python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
May 10, 2019 - 09:59:17
Django version 2.2.1, using settings 'api.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
[10/May/2019 09:59:24] "GET / HTTP/1.1" 200 16348
Not Found: /robots.txt
[10/May/2019 09:59:24] "GET /robots.txt HTTP/1.1" 404 1966
[10/May/2019 09:59:24] "GET /static/admin/css/fonts.css HTTP/1.1" 200 423
[10/May/2019 09:59:24] "GET /static/admin/fonts/Roboto-Regular-webfont.woff HTTP/1.1" 200 85876
[10/May/2019 09:59:24] "GET /static/admin/fonts/Roboto-Light-webfont.woff HTTP/1.1" 200 85692
[10/May/2019 09:59:24] "GET /static/admin/fonts/Roboto-Bold-webfont.woff HTTP/1.1" 200 86184
Not Found: /favicon.ico
[10/May/2019 09:59:24] "GET /favicon.ico HTTP/1.1" 404 1969
```


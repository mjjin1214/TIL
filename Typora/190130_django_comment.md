190130

django_comment

```bash
(curd-venv) minjaejin:~/workspace/django/crud-plus (master) $ \
python manage.py makemigrations
Migrations for 'posts':
  posts/migrations/0002_comment.py
    - Create model Comment
    
(curd-venv) minjaejin:~/workspace/django/crud-plus (master) $ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0002_comment... OK
  
(curd-venv) minjaejin:~/workspace/django/crud-plus (master) $ python manage.py shell
```

```shell
Python 3.6.7 (default, Jan 21 2019, 06:56:12) 
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

>>> from posts.models import Post, Comment
>>> Post.objects.all()
<QuerySet [<Post: 럭비>, <Post: 볼링>, <Post: 축구>, <Post: 풋살>, <Post: 야구>, <Post: 풋볼>, <Post: 탁구>, <Post: 농구>, <Post: 골프>, <Post: 배>]>

>>> post = Post.objects.last()
>>> post
<Post: 배구>

>>> c = Comment(post=post, content='댓글입니다!')
>>> c.save
<bound method Model.save of <Comment: Comment object (None)>>

>>> c.save()
>>> Comment.objects.all()
<QuerySet [<Comment: Comment object (1)>]>

>>> post.comment_set.all()
<QuerySet [<Comment: Comment object (1)>]>

>>> c = Comment.objects.get(pk=1)
>>> c
<Comment: Comment object (1)>

>>> c.post
<Post: 배구>

>>> post.title
'배구'

>>> c.post.title
'배구'

>>> c.post.content
'공'
>>> post.comment_set.first()
<Comment: Comment object (1)>

>>> post.comment_set.first().content
'댓글입니다!'
```


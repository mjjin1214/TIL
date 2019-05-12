base.html 수정

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous">
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
</head>
```

axios cdn 추가



_post.html 수정

```html
  <div class="card-body">
            <i class="{% if user in post.like_users.all %}fas{% else %}far{% endif %} fa-heart like-button" data-id="{{ post.id }}" style="color:tomato;"></i>
    <p class="card-text">
      {{ post.like_users.count }}명이 좋아합니다.
    </p>
  </div>
```

자바스크립트로 하트 아이콘 제어할 수 있도록 기존 하트 `<a>` 수정



list.html 수정

```html
{% endfor %}

<script>
    const likeButtons = document.querySelectorAll('.like-button')
    likeButtons.forEach(function(button){
        button.addEventListener('click', function(event){
            console.log(event)
            const postId = event.target.dataset.id
            axios.get(`/posts/${postId}/like/`)
            .then(function(response){
                console.log(response)
            })
        })
    })
</script>

{% endblock %}
```

`<script>` 추가



posts / views.py 수정

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import PostForm, CommentForm, ImageFormSet
from .models import Post, Comment
from django.db import transaction
from itertools import chain
from django.http import JsonResponse

@login_required
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.like_users.all():
        # 2. 좋아요 취소
        post.like_users.remove(request.user)
        liked = False
    else:
        # 1. 좋아요!
        post.like_users.add(request.user)
        liked = True
        
    # return redirect('posts:list')
    return JsonResponse({'liked':liked})
```

`JsonResponse` `import` 하고 `like` 함수 수정



list.html 수정

```html
{% endfor %}

<script>
    const likeButtons = document.querySelectorAll('.like-button')
    likeButtons.forEach(function(button){
        button.addEventListener('click', function(event){
            console.log(event)
            const postId = event.target.dataset.id
            axios.get(`/posts/${postId}/like/`)
            .then(function(response){
                // response.data // {liked: true}
                if (response.data.liked){
                    event.target.classList.remove('far')
                    event.target.classList.add('fas')
                } else {
                    event.target.classList.remove('fas')
                    event.target.classList.add('far')
                }
            })
        })
    })
</script>

{% endblock %}
```

좋아요 여부에 따라 하트 클래스를 삭제 추가 하는 코드 작성



posts / views.py 수정

```python
@login_required
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.like_users.all():
        # 2. 좋아요 취소
        post.like_users.remove(request.user)
        liked = False
    else:
        # 1. 좋아요!
        post.like_users.add(request.user)
        liked = True
        
    # return redirect('posts:list')
    return JsonResponse({'liked':liked, 'count': post.like_users.count()})
```

좋아요 사람 수를 `return`


_post.html 수정

```html
  <div class="card-body">
    <i class="{% if user in post.like_users.all %}fas{% else %}far{% endif %} fa-heart like-button" data-id="{{ post.id }}" style="color:tomato;"></i>
    <p class="card-text">
      <span id="like-count-{{ post.id }}">{{ post.like_users.count }}</span>명이 좋아합니다.
    </p>
  </div>
```

JS에서 `<span>`안의 텍스트 값을 변경할 수 있도록  `id` 설정



list.html 수정

```html
<script>
    const likeButtons = document.querySelectorAll('.like-button')
    likeButtons.forEach(function(button){
        button.addEventListener('click', function(event){
            console.log(event)
            const postId = event.target.dataset.id
            axios.get(`/posts/${postId}/like/`)
            .then(function(response){
                // response.data // {liked: true}
                document.querySelector(`#like-count-${postId}`).innerText = response.data.count
                if (response.data.liked){
                    event.target.classList.remove('far')
                    event.target.classList.add('fas')
                } else {
                    event.target.classList.remove('fas')
                    event.target.classList.add('far')
                }
            })
        })
    })
</script>
```

좋아요 숫자 텍스트를 변경하는 코드 작성


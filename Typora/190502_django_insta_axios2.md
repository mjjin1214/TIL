_post.html 수정

```html
  {% if user.is_authenticated %}
  <form action="{% url 'posts:comment_create' post.id %}" method="POST" class="comment-form">
    {% csrf_token %}
    <div class="input-group">
      {{ comment_form }}
      <div class="input-group-append">
        <input type="submit" value="Submit" class="btn btn-primary"/>
      </div>
    </div>
  </form>
  {% endif %}
```

JS에서 사용할 수 있도록 댓글 `form`에 클래스 `comment-form` 추가



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
    
    const commentForms = document.querySelectorAll('.comment-form')
    commentForms.forEach(function(form){
        form.addEventListener('submit', function(event){
            event.preventDefault()
            console.log(event)
            // event.target === form
            const data = new FormData(event.target)
            // Inspect FormData
            for (const item of data.entries()){
                console.log(item)
            }
            axios.post(event.target.action, data)
                .then(function(response){
                    console.log(response)
                })
        })
    })
    
</script>

{% endblock %}
```

댓글을 입력하고 제출버튼을 클릭했을 때, 데이터를 POST 방식으로 요청하는 코드 작성



posts / views.py

```python
@login_required
@require_POST
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
    # return redirect('posts:list')
    return JsonResponse({
        'id' : comment.id,
        'postId' : post_id,
        'username': comment.user.username,
        'content' : comment.content,
    })
```

`comment_create` 함수가 호출됐을 때, `JsonResponse`를 `return`하는 코드 작성



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
    
    const commentForms = document.querySelectorAll('.comment-form')
    commentForms.forEach(function(form){
        form.addEventListener('submit', function(event){
            event.preventDefault()
            console.log(event)
            // event.target === form
            const data = new FormData(event.target)
            // Inspect FormData
            for (const item of data.entries()){
                console.log(item)
            }
            axios.post(event.target.action, data)
                .then(function(response){
                    const comment = response.data
                })
        })
    })
    
</script>
```



_post.html 수정

```html
  <div class="card-body" id="comment-list-{{ post.id }}">
    {% for comment in post.comment_set.all %}
      <div class="card-text">
        <strong>{{ comment.user.username }}</strong> {{ comment.content }}
        {% if comment.user == user %}
        <a href="{% url 'posts:comment_delete' post.id comment.id %}">삭제</a>
        {% endif %}
      </div>
    {% empty %}
      <!--<div class="card-text">댓글이 없습니다.</div>-->
    {% endfor %}
  </div>
```

포스트의 댓글 파트 `<div>`에 `post.id`를 포함하는 `id` 추가



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
    
    const commentForms = document.querySelectorAll('.comment-form')
    commentForms.forEach(function(form){
        form.addEventListener('submit', function(event){
            event.preventDefault()
            console.log(event)
            // event.target === form
            const data = new FormData(event.target)
            // Inspect FormData
            for (const item of data.entries()){
                console.log(item)
            }
            axios.post(event.target.action, data)
                .then(function(response){
                    const comment = response.data
                    const commentList = document.querySelector(`#comment-list-${comment.postId}`)
                    const newComment = `<div class="card-text">
                        <strong>${comment.username}</strong> ${comment.content}
                        <a href="/posts/${comment.postId}/comments/${comment.id}/delete/">삭제</a>
                      </div>`
                     commentList.insertAdjacentHTML('beforeend', newComment)
                	event.target.reset()
                })
        })
    })
    
</script>
```

포스트의 댓글 리스트에 새 댓글을 추가하는 코드 작성
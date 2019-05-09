c9 django/api폴더 복사해 api-vue 생성



vs with-django / index.html 생성

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
</head>
<body>
    <div id="app">

    </div>

    <script>
        const app = new Vue({
            el: '#app',
            data: {

            },
            methods: {
                getMusics: function(){
                    axios.get('http://playground-minjaejin.c9users.io:8080/api/v1/musics/')
                        .then((response)=>{
                            console.log(response.data)
                        })
                },
            },
        })
    </script>
</body>
</html>
```

`<script>` 태그 내에서 이루어진 외부 요청(ex. get)은 장고에서 앱을 만들 때 기본적으로 허용하지 않음

브라우저가 장고 앱에서 보낸 응답에 cors를 허용하는 헤더가 없으면 응답을 차단함



vs index.html 실행

```js
app.getMusics()
undefined
index.html:1 Access to XMLHttpRequest at 'http://playground-minjaejin.c9users.io:8080/api/v1/musics/' from origin 'null' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
spread.js:25 Uncaught (in promise) Error: Network Error
    at e.exports (spread.js:25)
    at XMLHttpRequest.l.onerror (spread.js:25)
```

요청과 응답은 제대로 됐지만 응답에 cors 헤더가 포함돼 있지 않아 에러 발생



c9 terminal

```bash
(api-venv) minjaejin:~/workspace/django/api-vue (master) $ pip install django-cors-headers
Collecting django-cors-headers
  Downloading https://files.pythonhosted.org/packages/83/7f/96fa0dc138d4aab23bcbcb312df31ca63fb34f643805f02dddf9e460c648/django_cors_headers-2.5.3-py2.py3-none-any.whl
Requirement already satisfied: Django>=1.11 in /home/ubuntu/.pyenv/versions/3.6.7/envs/api-venv/lib/python3.6/site-packages (from django-cors-headers) (2.1.8)
Requirement already satisfied: pytz in /home/ubuntu/.pyenv/versions/3.6.7/envs/api-venv/lib/python3.6/site-packages (from Django>=1.11->django-cors-headers) (2019.1)
Installing collected packages: django-cors-headers
Successfully installed django-cors-headers-2.5.3
You are using pip version 10.0.1, however version 19.1.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```

django-cors-header 설치



settings.py 수정

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_swagger',
    'musics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = [
#     'example.com',
# ]
```

외부 요청을 허용하는 헤더 작성을 위해 앱, 미들웨어 추가



vs index.html 실행

```js
app.getMusics()
undefined
index.html:26 (7) [{…}, {…}, {…}, {…}, {…}, {…}, {…}]0: {id: 1, title: "옥탑방", artist: 1}1: {id: 2, title: "그때가 좋았어", artist: 2}2: {id: 3, title: "달라달라", artist: 3}3: {id: 4, title: "작은 것들을 위한 시", artist: 4}4: {id: 5, title: "나만, 봄", artist: 5}5: {id: 6, title: "주저하는 연인들을 위해", artist: 6}6: {id: 7, title: "호랑나비", artist: 6}length: 7__proto__: Array(0)
```

오류 해결



vs index.html 수정

```html
<body>
    <div id="app">
        <ul>
            <li v-for="music in musics">
                {{ music.artist }} - {{ music.title }}
            </li>
        </ul>
    </div>

    <script>
        const app = new Vue({
            el: '#app',
            data: {
                musics: [],
            },
            methods: {
                getMusics: function(){
                    axios.get('http://playground-minjaejin.c9users.io:8080/api/v1/musics/')
                        .then((response)=>{
                            this.musics = response.data
                        })
                        .catch((error)=>{
                            console.log(error)
                        })
                },
            },
            mounted: function(){
                this.getMusics()
            },
        })
    </script>
</body>
```

웹이 mount 될 때 데이터를 요청하고 응답받아 페이지에 출력하는 코드 작성



serializers.py 수정

```python
class MusicSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.name')
    class Meta:
        model = Music
        fields = ['id', 'title', 'artist_name',]
```

`id` 숫자가 아닌 가수 이름을 출력하도록 수정



vs index.html 수정

```html
<body>
    <div id="app">
        <ul>
            <li v-for="music in musics">
                {{ music.artist_name }} - {{ music.title }}
            </li>
        </ul>
    </div>

    <script>
        const app = new Vue({
            el: '#app',
            data: {
                musics: [],
            },
            methods: {
                getMusics: function(){
                    axios.get('http://playground-minjaejin.c9users.io:8080/api/v1/musics/')
                        .then((response)=>{
                            return response.data
                        })
                        .then((music)=>{
                            this.musics = music
                        })
                        .catch((error)=>{
                            console.log(error)
                        })
                },
            },
            mounted: function(){
                this.getMusics()
            },
        })
    </script>
</body>
```

가수 이름이 출력되도록 `<div id='app>` 내용 수정

코드 이해가 쉽도록 `getMusics` 함수 수정



serializers.py 수정

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', ]


class MusicSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.name')
    comment_set = CommentSerializer(many=True)
    class Meta:
        model = Music
        fields = ['id', 'title', 'artist_name', 'comment_set',]
```

`MusicSerializer`가 노래에 대한 댓글 정보를 포함하도록 수정



vs index.html 수정

```html
<body>
    <div id="app">
        <ul>
            <li v-for="music in musics">
                <div>
                    {{ music.artist_name }} - {{ music.title }}
                </div>
                <ul>
                    <li v-for="comment in music.comment_set">
                        {{ comment.content }}
                    </li>
                </ul>
                <div>
                    <input type="text" v-model="music.newComment">
                    <button v-on:click="addComment(music)">+</button>
                </div>
            </li>
        </ul>
    </div>

    <script>
        const app = new Vue({
            el: '#app',
            data: {
                musics: [],
            },
            methods: {
                getMusics: function(){
                    axios.get('http://playground-minjaejin.c9users.io:8080/api/v1/musics/')
                        .then((response)=>{
                            return response.data
                        })
                        .then((musics)=>{
                            this.musics = musics.map((music)=>{
                                return { ...music, newComment:'' }
                            })
                        })
                        .catch((error)=>{
                            console.log(error)
                        })
                },
                addComment: function(music){
                    axios.post(`http://playground-minjaejin.c9users.io:8080/api/v1/musics/${music.id}/comments/`, {content: music.newComment})
                        .then((response)=>{
                            return response.data
                        })
                        .then((comment)=>{
                            music.comment_set.push(comment)
                            music.newComment = ''
                        })
                        .catch((error)=>{
                            console.log(error)
                        })
                },
            },
            mounted: function(){
                this.getMusics()
            },
        })
    </script>
</body>
```

`<div id='app'>` : 노래에 달린 댓글을 출력되게하고, 댓글 입력란과 버튼 생성

`getMusics` : 노래 데이터를 응답 받고, 오브젝트에 `newComment` 키 추가하는 코드 작성

`addComment` : 댓글을 생성하는 요청을 보내고, 그 내용을 웹에 바로 출력하는 코드 작성



vs index.html 수정

```html
<body>
    <div id="app">
        <ul>
            <li v-for="music in musics">
                <div>
                    {{ music.artist_name }} - {{ music.title }}
                </div>
                <ul>
                    <li v-for="comment in music.comment_set">
                        {{ comment.content }} <button v-on:click="deleteComment(music, comment)">X</button>
                    </li>
                </ul>
                <div>
                    <input type="text" v-model="music.newComment">
                    <button v-on:click="addComment(music)">+</button>
                </div>
            </li>
        </ul>
    </div>

    <script>
        const app = new Vue({
            el: '#app',
            data: {
                musics: [],
            },
            methods: {
                getMusics: function(){
                    axios.get('http://playground-minjaejin.c9users.io:8080/api/v1/musics/')
                        .then((response)=>{
                            return response.data
                        })
                        .then((musics)=>{
                            this.musics = musics.map((music)=>{
                                return { ...music, newComment:'' }
                            })
                        })
                        .catch((error)=>{
                            console.log(error)
                        })
                },
                addComment: function(music){
                    axios.post(`http://playground-minjaejin.c9users.io:8080/api/v1/musics/${music.id}/comments/`, {content: music.newComment})
                        .then((response)=>{
                            return response.data
                        })
                        .then((comment)=>{
                            music.comment_set.push(comment)
                            music.newComment = ''
                        })
                        .catch((error)=>{
                            console.log(error)
                        })
                },
                deleteComment: function(music, comment){
                    axios.delete(`http://playground-minjaejin.c9users.io:8080/api/v1/musics/${music.id}/comments/${comment.id}/`)
                        .then((response)=>{
                            music.comment_set = music.comment_set.filter((c)=>{
                                return c.id !== comment.id
                            })
                        })
                        .catch((error)=>{
                            console.log(error)
                        })
                },
            },
            mounted: function(){
                this.getMusics()
            },
        })
    </script>
</body>
```

댓글 삭제 버튼 생성, 

댓글 삭제 요청을 보내고, 페이지에서 해당 댓글을 지우는 함수 `deleteComment` 생성
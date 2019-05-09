웹 앱 서버에 올리기

```cmd
C:\Users\student\minjae\vue\chat>npm install -g firebase-tools
C:\Users\student\AppData\Roaming\npm\firebase -> C:\Users\student\AppData\Roaming\npm\node_modules\firebase-tools\lib\bin\firebase.js
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.9 (node_modules\firebase-tools\node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.9: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

+ firebase-tools@6.9.0
added 508 packages from 280 contributors in 16.389s

C:\Users\student\minjae\vue\chat>firebase login
? Allow Firebase to collect anonymous CLI usage and error reporting information? Yes

Visit this URL on any device to log in:
https://accounts.google.com/o/oauth2/auth?client_id=563584335869-fgrhgmd47bqnekij5i8b5pr03ho849e6.apps.googleusercontent.com&scope=email%20openid%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloudplatformprojects.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffirebase%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform&response_type=code&state=63195420&redirect_uri=http%3A%2F%2Flocalhost%3A9005

Waiting for authentication...

+  Success! Logged in as moc0etan@gmail.com

C:\Users\student\minjae\vue\chat>firebase init

     ######## #### ########  ######## ########     ###     ######  ########
     ##        ##  ##     ## ##       ##     ##  ##   ##  ##       ##
     ######    ##  ########  ######   ########  #########  ######  ######
     ##        ##  ##    ##  ##       ##     ## ##     ##       ## ##
     ##       #### ##     ## ######## ########  ##     ##  ######  ########

You're about to initialize a Firebase project in this directory:

  C:\Users\student\minjae\vue\chat

? Are you ready to proceed? Yes
? Which Firebase CLI features do you want to set up for this folder? Press Space to select features, the
n Enter to confirm your choices. Database: Deploy Firebase Realtime Database Rules, Hosting: Configure a
nd deploy Firebase Hosting sites

=== Project Setup

First, let's associate this project directory with a Firebase project.
You can create multiple project aliases by running firebase use --add,
but for now we'll just set up a default project.

? Select a default Firebase project for this directory: vue-chat-minjae (vue-chat)
i  Using project vue-chat-minjae (vue-chat)

=== Database Setup

Firebase Realtime Database Rules allow you to define how your data should be
structured and when your data can be read from and written to.

? What file should be used for Database Rules? database.rules.json
+  Database Rules for vue-chat-minjae have been downloaded to database.rules.json.
Future modifications to database.rules.json will update Database Rules when you run
firebase deploy.

=== Hosting Setup

Your public directory is the folder (relative to your project directory) that
will contain Hosting assets to be uploaded with firebase deploy. If you
have a build process for your assets, use your build's output directory.

? What do you want to use as your public directory? public
? Configure as a single-page app (rewrite all urls to /index.html)? Yes
? File public/index.html already exists. Overwrite? No
i  Skipping write of public/index.html

i  Writing configuration info to firebase.json...
i  Writing project information to .firebaserc...
i  Writing gitignore file to .gitignore...

+  Firebase initialization complete!
```



database.rules.json 수정

```json
{
  "rules": {
    "messages": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```



```cmd
C:\Users\student\minjae\vue\chat>firebase deploy

=== Deploying to 'vue-chat-minjae'...

i  deploying database, hosting
i  database: checking rules syntax...
+  database: rules syntax for database vue-chat-minjae is valid
i  hosting[vue-chat-minjae]: beginning deploy...
i  hosting[vue-chat-minjae]: found 1 files in public
+  hosting[vue-chat-minjae]: file upload complete
i  database: releasing rules...
+  database: rules for database vue-chat-minjae released successfully
i  hosting[vue-chat-minjae]: finalizing version...
+  hosting[vue-chat-minjae]: version finalized
i  hosting[vue-chat-minjae]: releasing new version...
+  hosting[vue-chat-minjae]: release complete

+  Deploy complete!

Project Console: https://console.firebase.google.com/project/vue-chat-minjae/overview
Hosting URL: https://vue-chat-minjae.firebaseapp.com
```


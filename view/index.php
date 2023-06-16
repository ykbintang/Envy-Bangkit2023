<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <!--=============== CSS ===============-->
   <style>

/* =============== GOOGLE FONTS =============== */
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap");

/* =============== VARIABLES CSS =============== */
:root {
  /* =========== Colors =========== */
  /* Color mode HSL(hue, saturation, lightness) */
  --white-color: hsl(0, 0%, 100%);
  --black-color: hsl(0, 0%, 0%);
  
  /* =========== Font and typography =========== */
  /* .5rem = 8px | 1rem = 16px ... */
  --body-font: "Poppins", sans-serif;
  --h1-font-size: 1.75rem;
  --normal-font-size: 1rem;
  --small-font-size: .813rem;
  
  /* =========== Font weight =========== */
  --font-medium: 500;
}

/* =============== BASE =============== */
* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

body, input, button {
  font-size: var(--normal-font-size);
  font-family: var(--body-font);
}

body {
  color: var(--white-color);
}

input, button {
  border: none;
  outline: none;
}

a {
  text-decoration: none;
}

img {
  max-width: 100%;
  height: auto;
}

/* =============== LOGIN =============== */
.login {
  position: relative;
  height: 100vh;
  display: grid;
  align-items: center;
}

.login_img {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.login_form {
  position: relative;
  background-color: hsla(0, 0%, 10%, 0.1);
  border: 2px solid var(--white-color);
  margin-inline: 1.5rem;
  padding: 2.5rem 1.5rem;
  border-radius: 1rem;
  backdrop-filter: blur(8px);
}

.login_title {
  text-align: center;
  font-size: var(--h1-font-size);
  font-weight: var(--font-medium);
  margin-bottom: 2rem;
}

.login_register {
  font-size: var(--small-font-size);
}

.login_button {
  width: 100%;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: var(--white-color);
  font-weight: var(--font-medium);
  cursor: pointer;
  margin-bottom: 2rem;
}

.login_register {
  text-align: center;
}

.login_register a {
  color: var(--white-color);
  font-weight: var(--font-medium);
}

.login_register a:hover {
  text-decoration: underline;
}

/* =============== BREAKPOINTS =============== */
/* For medium devices */
@media screen and (min-width: 576px) {
  .login {
    justify-content: center;
  }
  
  .login_form {
    width: 432px;
    padding: 4rem 3rem 3.5rem;
    border-radius: 1.5rem;
  }
  
  .login_title {
    font-size: 2rem;
  }
}

      .login_button {
         display: inline-block;
         padding: 0.75rem 1.5rem;
         background-color: #e9e9e9;
         color: #333;
         border: none;
         border-radius: 0.5rem;
         text-decoration: none;
         font-weight: bold;
         text-align: center;
         transition: background-color 0.3s ease;
      }

      .login_button:hover {
         background-color: #ccc;
      }
   </style>

   <title>Welcome to ENVy Endpoint</title>
</head>
<body>
   <div class="login">
      <img src="assets/img/login-bg.png" alt="login image" class="login_img" id="loginImage">

      <form action="" class="login_form">
         <h1 class="login_title">Welcome to ENVy Endpoint</h1>
         <p class="login_register" style="margin-bottom: 50px;">For get ApiKey, you must register</p>
         <a href="docs" class="login_button" style="margin-bottom: 5px;">Docs</a>
      </form>
   </div>

   <!--=============== MAIN JS ===============-->
<script>
   var images = [
    "assets/img/login-bg.png",
    "assets/img/login-bg2.png",
    "assets/img/login-bg3.png"
];

var index = 0;
var loginImage = document.getElementById("loginImage");

function changeBackgroundImage() {
    index = (index + 1) % images.length;
    loginImage.src = images[index];
}

// Mengubah gambar latar belakang setiap 5 detik
setInterval(changeBackgroundImage, 5000);

function validateForm() {
    // ...
}
</script>
</body>
</html>
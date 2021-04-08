// Get text inputs from the form
let username = document.forms['login_form']['username'];
let password = document.forms['login_form']['password'];

// Get the hidden error div that will show when submission error
let usernameError = document.getElementById("username_error");
let passwordError = document.getElementById("password_error");

// Event listeners for when the error raised after submission is fixed
username.addEventListener('blur', usernameCheck);
password.addEventListener('blur', passwordCheck);

function Validate(){
    // Check if username is empty
    if (username.value === ""){
        username.style.border = "1px solid red";
        document.getElementById('username').style.color = "red";
        usernameError.textContent = "Username is required";
        username.focus();
        return false;
    }

    // Check if the password is empty
    if (password.value === ""){
        password.style.border = "1px solid red";
        document.getElementById('password').style.color = "red";
        passwordError.textContent = "Password is required";
        password.focus();
        return false;
    }
};

function usernameCheck(){
    // If not empty, then the field will go back to normal
    if (username.value !== ""){
        username.style.border = "1px solid blue";
        document.getElementById('username').style.color = "black";
        usernameError.innerHTML = "";
        return true;
    }
};

function passwordCheck(){
    // If not empty, then the field will go back to normal
    if (password.value !== ""){
        password.style.border = "1px solid blue";
        document.getElementById('password').style.color = "black";
        passwordError.innerHTML = "";
        return true;
    }
};

// If they have an account, then redirect to login page
document.getElementById("signup").onclick = function(){
    location.href = 'signup';
};

// On submission, check if the form the valid
document.getElementById("login_form").onsubmit = function(){
    return Validate()
};

window.onload = function(){
    incorrectPassword();
};

// For incorrect logins
function incorrectPassword(){
    if (document.getElementById("password_error").innerHTML.trim() === "Incorrect Username or Password") {
        password.style.border = "1px solid red";
        document.getElementById('password').style.color = "red";
        username.style.border = "1px solid red";
        document.getElementById('username').style.color="red";
        password.focus();
    }
};
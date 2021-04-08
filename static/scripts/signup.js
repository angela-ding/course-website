let firstName = document.forms['sign_up_form']['firstName'];
let lastName = document.forms['sign_up_form']['lastName'];
let username = document.forms['sign_up_form']['username'];
let password = document.forms['sign_up_form']['password'];
let email = document.forms['sign_up_form']['email'];
let sori = document.forms['sign_up_form']['sori'];

let firstError = document.getElementById("first_name_error");
let lastError = document.getElementById("last_name_error");
let usernameError = document.getElementById("username_error");
let passwordError = document.getElementById("password_error");
let emailError = document.getElementById("email_error");
let soriError = document.getElementById("user_type_error");

// Event listeners for when the error raised after submission is fixed
username.addEventListener('blur', usernameCheck);
password.addEventListener('blur', passwordCheck);
firstName.addEventListener('blur', firstCheck);
lastName.addEventListener('blur', lastCheck);
email.addEventListener('blur', emailCheck);
sori.addEventListener('blur', soriCheck);

function Validate(){
    // Check if username is empty
    if (firstName.value === ""){
        firstName.style.border = "1px solid red";
        document.getElementById('firstname').style.color = "red";
        firstError.textContent = "First name is required";
        firstName.focus();
        return false;
    }

    // Check if the password is empty
    if (lastName.value === ""){
        lastName.style.border = "1px solid red";
        document.getElementById('lastname').style.color = "red";
        lastError.textContent = "Last name is required";
        lastName.focus();
        return false;
    }

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

    // Check if username is empty
    if (email.value === ""){
        email.style.border = "1px solid red";
        document.getElementById('email').style.color = "red";
        emailError.textContent = "Email is required";
        email.focus();
        return false;
    }

    // Check if the password is empty
    if (sori.value === ""){
        sori.style.border = "1px solid red";
        document.getElementById('user_type').style.color = "red";
        soriError.textContent = "User type is required";
        sori.focus();
        return false;
    }
};

function firstCheck(){
    // If not empty, then the field will go back to normal
    if (firstName.value !== ""){
        firstName.style.border = "1px solid blue";
        document.getElementById('firstname').style.color = "black";
        firstError.innerHTML = "";
        return true;
    }
};

function lastCheck(){
    // If not empty, then the field will go back to normal
    if (lastName.value !== ""){
        lastName.style.border = "1px solid blue";
        document.getElementById('lastname').style.color = "black";
        lastError.innerHTML = "";
        return true;
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

function emailCheck(){
    // If not empty, then the field will go back to normal
    if (email.value !== ""){
        email.style.border = "1px solid blue";
        document.getElementById('email').style.color = "black";
        emailError.innerHTML = "";
        return true;
    }
};

function soriCheck(){
    // If not empty, then the field will go back to normal
    if (sori.value !== ""){
        sori.style.border = "1px solid blue";
        document.getElementById('user_type').style.color = "black";
        soriError.innerHTML = "";
        return true;
    }
};

// If they have an account, then redirect to login page
document.getElementById("login").onclick = function(){
    location.href = 'login';
};

// On submission, check if the form the valid
document.getElementById("sign_up_form").onsubmit = function(){
    return Validate()
};

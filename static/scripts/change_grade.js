let changeMark = document.forms[0]['changed_mark'];
let mark_msg = document.getElementById("mark_msg");
let form = document.forms[0];

// If a grade was changed successfully submitted, send an alert
window.onload = function(){
    if (document.getElementById("hidden").innerHTML.trim() == "success"){
        setTimeout(function(){alert("Mark has been updated");}, 100);
    }
}

// Validate to check if the form is empty
form.onsubmit = function(){
    return validate();
}

function validate(){
    // Check if the user ot the mark change fields are empty
    if (changeMark.value == ""){
        // Provide error message if empty
        mark_msg.innerHTML = "Please enter a new mark";
        mark_msg.style.color = "red";
        changeMark.style.border = "1px solid red";
        return false;
    }
    // If both fields are not empty then it is ok to submit
    return true;
}
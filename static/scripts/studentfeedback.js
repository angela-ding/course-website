function makeStrPlusInt(str1, int1){
	result = str1;
	return result;
}

// If a grade was changed successfully submitted, send an alert
window.onload = function(){
    if (document.getElementById("hidden").innerHTML.trim() == "success"){
        setTimeout(function(){alert("Feedback has been submitted");}, 100);
    }
}

// Validate to check if the form is empty
form.onsubmit = function(){
    return true();
}
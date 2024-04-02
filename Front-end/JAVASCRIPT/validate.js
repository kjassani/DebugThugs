function isBlank(inputField)
{
    if (inputField.value=="")
    {
	     return true;
    }
    return false;
}

function makeRed(inputDiv){
	inputDiv.style.borderColor="#AA0000";
}

function makeClean(inputDiv){
	inputDiv.style.borderColor="#FFFFFF";
}

window.onload = function()
{   

    var mainForm = document.getElementById("mainForm");
    var requiredInputs = document.querySelectorAll(".required");

    mainForm.onsubmit = function(e)
    {
	    var requiredInputs = document.querySelectorAll(".required");
        var err = false;

	     for (var i=0; i < requiredInputs.length; i++)
       {
	        if( isBlank(requiredInputs[i]))
          {
		          err |= true;
		          makeRed(requiredInputs[i]);
	        }
	        else
          {
		          makeClean(requiredInputs[i]);
	        }
	    }
      if (err == true)
      {
        e.preventDefault();
      }
      else
      {
        console.log('checking match');
        checkPasswordMatch(e);
      }
    }
}

function checkPasswordMatch(e){
    var p = document.getElementById("newPassword");
    var pass2 = document.getElementById("confirmNewPassword");
    

    var password = p.value;
    var passCheck = pass2.value;
 
    if(password !== passCheck){ 
      makeRed(p);
      makeRed(pass2);
      if(!document.getElementById("errorMsg")){
        var p = document.createElement("p");
        p.innerHTML = '<p id = "errorMsg"></p>';
        p.style.color = "red";


        var error = document.createTextNode("Passwords do not match");
        p.appendChild(error);

        var parent = document.getElementById("mainForm");
        parent.appendChild(p);
      }
      return e.preventDefault();
    }
    oldPassCheck(e);
  }
function oldPassCheck(e){
    var oldP = document.getElementById("oldPassword");
    var oldPass = oldP.value;
    
    var password = "password";

    if(oldPass != password){
        makeRed(oldP);
        if(!document.getElementById("errorMsg")){
            var p = document.createElement("p");
            p.innerHTML = '<p id = "errorMsg"></p>';
            p.style.color = "red";
    
            var error = document.createTextNode("Old password is incorrect!");
            p.appendChild(error);
    
            var parent = document.getElementById("mainForm");
            parent.appendChild(p);
        }
        return e.preventDefault();
    }
    else if(oldPass == password){
        var parent = document.getElementById("mainForm");
        parent.appendChild(p);
        window.alert("Successfully changed password");
    }
}

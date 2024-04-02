

function checkPasswordMatch(e){
    
    var password = e;
    var passCheck = "password";
 
    if(password != passCheck){ 
      // makeRed(password);
      // makeRed(passCheck);
      // if(!document.getElementById("errorMsg")){
      //   var p = document.createElement("p");
      //   p.innerHTML = '<p id = "errorMsg"></p>';
      //   p.style.color = "red";


      //   var error = document.createTextNode("Passwords do not match");
      //   p.appendChild(error);

      //   var parent = document.getElementById("mainForm");
      //   parent.appendChild(p);
      // }
      return false;
    }
    return true;
  }

  module.exports = checkPasswordMatch
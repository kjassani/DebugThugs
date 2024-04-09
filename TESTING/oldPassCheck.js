function oldPassCheck(e){
    var oldPass = e;

    var password = "password";

    if(oldPass != password){
      //  makeRed(oldP);
        // if(!document.getElementById("errorMsg")){
        //     var p = document.createElement("p");
        //     p.innerHTML = '<p id = "errorMsg"></p>';
        //     p.style.color = "red";
    
        //     var error = document.createTextNode("Old password is incorrect!");
        //     p.appendChild(error);
    
        //     var parent = document.getElementById("mainForm");
        //     parent.appendChild(p);
        // }
        return false;
    }
    return true;
}

module.exports = oldPassCheck
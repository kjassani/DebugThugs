
window.onload = function()
{   
    document.getElementById("button_form_submit").addEventListener("click", function(event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // Get the value entered in the input field
        var username = document.getElementById("fusername").value;
        
        //Check if the username value is valid and act appropriatly
        if(username == "")
        {
            document.getElementById("display_username").textContent = "Invalid Entry!";
        }
        else
        {
        // Display the entered username below the form
        document.getElementById("display_username").textContent = "Entered username: " + username;
        
        // Clear the input field
        document.getElementById("fusername").value = "";
        }
      });
}

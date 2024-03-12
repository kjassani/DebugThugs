<!DOCTYPE html>
<html>
<head>
<title>Customer Page</title>
</head>
<body>

<%
if (session.getAttribute("creationStatus") != null)
	out.println("<p style=\"color:red\">"+session.getAttribute("creationStatus").toString()+"</p>");
%>

<form name="acccreate" method="post" action="validatenewaccount.jsp">

    <h4>First Name</h4>
    <input type="text" name="firstName" value="">

    <h4>Last Name</h4>
    <input type="text" name="lastName" value="">

    <h4>E-mail</h4>
    <input type="text" name="email" value="">
 
    <h4>Username</h4>
    <input type="text" name="newuserid" value="">

    <h4>Password</h4>
    <input id="pw" type="password" name="password" value="">
    <input type="checkbox" onclick="togglePassword()"> Show Password

    <!-- Submit button -->
    <h4></h4>
    <input type="submit" name="Submit" value="Create Account">
</form>


<script>
function togglePassword() {
  var x = document.getElementById("pw");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}
</script>
</body>
</html>
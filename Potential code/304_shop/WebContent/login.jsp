<!DOCTYPE html>
<html>
<head>
<title>Login Screen</title>
</head>
<body>

<div style="margin: 0 auto; text-align: center;">

    <h3>Please Login to System</h3>

    <%
    // Print prior error login message if present
    if (session.getAttribute("loginMessage") != null)
        out.println("<p>" + session.getAttribute("loginMessage").toString() + "</p>");
    %>

    <br>

    <div style="display: inline-block; background: lightgray; padding: 10px;">

        <form name="MyForm" method="post" action="validateLogin.jsp">
            <table>
                <tr>
                    <td><div align="right"><font face="Arial, Helvetica, sans-serif" size="2">Username:</font></div></td>
                    <td><input type="text" name="username" size="10" maxlength="10"></td>
                </tr>
                <tr>
                    <td><div align="right"><font face="Arial, Helvetica, sans-serif" size="2">Password:</font></div></td>
                    <td><input type="password" name="password" size="10" maxlength="10"></td>
                </tr>
            </table>
            <br/>
            <input class="submit" type="submit" name="Submit2" value="Log In">
        </form>

        <a href="accountcreation.jsp" style="background: lightgray; display: block; margin-top: 10px; padding: 5px;">Create Account</a>

    </div>

</div>



</body>
</html>


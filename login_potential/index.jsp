<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Pinyon+Script&display=swap" rel="stylesheet">
        <title>Discord_login</title>
		<style>
        .search-form {
            position: absolute;
            top: 0;
            right: 0;
        }
		h1 { color: green; }
		.search-form input[type="text"] {
			background: #f1f1f1;
			border: 0 none;
			font-size: 16px;
			height: 30px;
			padding-left: 10px;
			width: 200px;
			font-style: italic;
			color: blue;
		}
		.logout-link{
			position: absolute;
			top: 0;
			left: 0;
			font-size: 13px;
			color: red;
		}
		.menu-bar {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #333;
        }

        .menu-bar li {
            float: left;
        }

        .menu-bar li a {
            display: block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
			font-family: 'Times New Roman', Times, serif;
        }
		.welcome-message {
    		font-size: 22px; 
			color: white;
    		text-align: right;
		}

        .menu-bar li a:hover {
            background-color: #111;
			font-family: Airal;
			font-weight: bold;
        }
		body {
            background-image: url('img/dis.jpg');
            background-repeat: no-repeat;
            background-size: cover;
			background-attachment: fixed;
        }
		</style>
</head>
<body>
<h1 align = "center">Discord</h1>

<ul class = "menu-bar">
	<li><a href="login.jsp">Login</a></li>
	<li><a href="logout.jsp">Log out</a></li>
	<li class="welcome-message">Welcome, ${empty sessionScope.authenticatedUser ? 'Guest' : sessionScope.authenticatedUser}</li>
</ul>




<%
	String userName = (String) session.getAttribute("authenticatedUser");
	if (userName != null)
		out.println("<h3 align=\"center\">Signed in as: "+userName+"</h3>");
%>

<%-- <h4 align="center"><a href="ship.jsp?orderId=1">Test Ship orderId=1</a></h4> 

<h4 align="center"><a href="ship.jsp?orderId=3">Test Ship orderId=3</a></h4> --%>

</body>
</head>



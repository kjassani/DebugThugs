<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Pinyon+Script&display=swap" rel="stylesheet">
        <title>Darkest Souls Main Page</title>
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

        .menu-bar li a:hover {
            background-color: #111;
			font-family: 'Pinyon Script', cursive;
        }
		body {
            background-image: url('img/imggg.jpg');
            background-repeat: no-repeat;
            background-size: cover;
			background-attachment: fixed;
        }
		</style>
</head>
<body>
<h1 align = "center">Welcome to Darkest Souls</h1>

<ul class = "menu-bar">
	<li><a href="login.jsp">Login</a></li>
	<li><a href="listprod.jsp">Begin Shopping</a></li>
	<li><a href="listorder.jsp">List All Orders</a></li>
	<li><a href="customer.jsp">Customer Info</a></li>
	<li><a href="admin.jsp">Administrators</a></li>
	<li><a href="logout.jsp">Log out</a></li>
	<li><a href="listCategory.jsp">Search Categories</a></li>
	<li><a>Welcome, ${empty sessionScope.authenticatedUser ? 'Guest' : sessionScope.authenticatedUser}<a></li>
</ul>
<form method="get" action="listprod.jsp" class="search-form">
<input type="text" name="productName" size="25" placeholder="search for the mysterious">
<input type="submit" value="Submit"><input type="reset" value="Reset"> 
</form>



<%
	String userName = (String) session.getAttribute("authenticatedUser");
	if (userName != null)
		out.println("<h3 align=\"center\">Signed in as: "+userName+"</h3>");
%>

<%-- <h4 align="center"><a href="ship.jsp?orderId=1">Test Ship orderId=1</a></h4> 

<h4 align="center"><a href="ship.jsp?orderId=3">Test Ship orderId=3</a></h4> --%>

</body>
</head>



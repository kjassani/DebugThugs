<!DOCTYPE html>
<html>
<head>
<title>Customer Page</title>
</head>
<body>

<%@ include file="auth.jsp"%>
<%@ page import="java.text.NumberFormat" %>
<%@ include file="jdbc.jsp" %>

<%
	String userName = (String) session.getAttribute("authenticatedUser");
%>

<%

// TODO: Print Customer information
String sql = "SELECT * FROM customer WHERE userId = ?";
// Make the connection
		String url = "jdbc:sqlserver://cosc304_sqlserver:1433;DatabaseName=orders;TrustServerCertificate=True";
        String uid = "sa";
        String pw = "304#sa#pw";              
        
        try ( Connection con = DriverManager.getConnection(url, uid, pw);) 
        {
			PreparedStatement ps = con.prepareStatement(sql);
			ps.setString(1,userName);
			ResultSet result = ps.executeQuery();
			result.next();

			//Display customer info
			out.println("<h1 align=center>Customer Profile</h1><table align=center border=1><tbody>");
			out.println("<tr><td>Id</td><td>" + result.getString("customerId") + "</td></tr>");
			out.println("<tr><td>First Name</td><td>" + result.getString("firstName") + "</td></tr>");
			out.println("<tr><td>Last Name</td><td>" + result.getString("lastName") + "</td></tr>");
			out.println("<tr><td>E-mail</td><td>" + result.getString("email") + "</td></tr>");
			out.println("<tr><td>Phone Number</td><td>" + result.getString("phonenum") + "</td></tr>");
			out.println("<tr><td>Address</td><td>" + result.getString("address") + "</td></tr>");
			out.println("<tr><td>City</td><td>" + result.getString("city") + "</td></tr>");
			out.println("<tr><td>State</td><td>" + result.getString("state") + "</td></tr>");
			out.println("<tr><td>Postal Code</td><td>" + result.getString("postalCode") + "</td></tr>");
			out.println("<tr><td>Country</td><td>" + result.getString("country") + "</td></tr>");
			out.println("<tr><td>User Id</td><td>" + userName + "</td></tr>");
			out.println("</tbody></table>");
// Make sure to close connection
			con.close();
		} catch(SQLException ex){
			out.println(ex);
		}


%>

<div align=center><a href="editaccount.jsp"style="background: lightgray">Edit Account</a</div>
<div align=center><a href="logout.jsp" style="background: lightgray">Log Out</a</div>


</body>
</html>


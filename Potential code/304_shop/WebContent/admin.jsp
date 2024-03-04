<!DOCTYPE html>
<html>
<head>
<title>Administrator Page</title>
</head>
<body>

<%
// TODO: Include files auth.jsp and jdbc.jsp
%>

<%@ include file="auth.jsp" %>
<%@ include file="jdbc.jsp" %>
<%@ page import="java.text.NumberFormat" %>

<%

// TODO: Write SQL query that prints out total order amount by day
String sql = "SELECT SUM(price * quantity),CONVERT(DATE,orderDate) FROM ordersummary JOIN orderproduct ON ordersummary.orderId = orderproduct.orderId GROUP BY CONVERT(DATE,orderDate)";
// Make the connection
		String url = "jdbc:sqlserver://cosc304_sqlserver:1433;DatabaseName=orders;TrustServerCertificate=True";
        String uid = "sa";
        String pw = "304#sa#pw";              
              
        try ( Connection con = DriverManager.getConnection(url, uid, pw);) 
        {
            PreparedStatement ps = con.prepareStatement(sql);
            ResultSet result = ps.executeQuery();
            out.println("<table align=center border=1><tbody><tr><td>Date</td><td>Total Order Amount</td>");
            while(result.next()){
                out.println("<tr>");
                out.println("<td>" + result.getString(2) + "</td>");
                out.println("<td>" + NumberFormat.getCurrencyInstance().format(result.getDouble(1)) + "</td>");
                out.println("</tr>");
            }
            out.println("</tbody></table>");

            con.close();
        } catch(SQLException ex){
            out.println(ex);
        }

%>

</body>
</html>


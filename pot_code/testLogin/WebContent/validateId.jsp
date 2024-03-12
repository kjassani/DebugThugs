<%@ page import="java.sql.*" %>
<%@ page import="java.text.NumberFormat" %>
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.Iterator" %>
<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Map" %>
<%@ page import="java.io.*" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF8"%>
<!DOCTYPE html>
<html>
<head>
<title>Darkest Souls</title>
</head>
<body>

<% 
// Get customer id
String custId = request.getParameter("customerId");
session.setAttribute("customerId", custId);
@SuppressWarnings({"unchecked"})
HashMap<String, ArrayList<Object>> productList = (HashMap<String, ArrayList<Object>>) session.getAttribute("productList");

// Make connection
		String url = "jdbc:sqlserver://cosc304_sqlserver:1433;DatabaseName=orders;TrustServerCertificate=True";
        String uid = "sa";
        String pw = "304#sa#pw";              
              
        try ( Connection con = DriverManager.getConnection(url, uid, pw);) 
        {

			ResultSet res;
			PreparedStatement ps;

// Determine if valid customer id was entered
			try{
				ps = con.prepareStatement("SELECT * FROM customer WHERE customerId = ?");
				ps.setString(1,custId);
				res = ps.executeQuery();
				if(res.next() == false){
					out.println("<h1>INVALID CUSTOMER ID.</h1><h2>Please go back and try again.</h2>");
					return;
				}
			   } catch(SQLException e){
				   out.println("<h1>INVALID CUSTOMER ID.</h1><h2>Please go back and try again.</h2>");
				   return;
			   }

// Determine if there are products in the shopping cart
			if(productList==null||productList.isEmpty()){
				out.println("<h1>CART IS EMPTY.</h1><h2>Please go back and add an item to the cart.</h2>");
				return;
			}
            
	con.close();
	}
	catch (SQLException ex)
	{
		StringWriter sw = new StringWriter();
    PrintWriter printers = new PrintWriter(sw);
    ex.printStackTrace(printers);
    String stackTrace = sw.toString();

    out.println("SQLException: " + ex.getMessage());
    out.println("<pre>" + stackTrace + "</pre>");
	}
    

    /*
    // Use retrieval of auto-generated keys.
    PreparedStatement pstmt = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);			
            ResultSet keys = pstmt.getGeneratedKeys();
            keys.next();
            int orderId = keys.getInt(1);
            
    */




// Here is the code to traverse through a HashMap
// Each entry in the HashMap is an ArrayList with item 0-id, 1-name, 2-quantity, 3-price

/*
    Iterator<Map.Entry<String, ArrayList<Object>>> iterator = productList.entrySet().iterator();
    while (iterator.hasNext())
    { 
        Map.Entry<String, ArrayList<Object>> entry = iterator.next();
        ArrayList<Object> product = (ArrayList<Object>) entry.getValue();
        String productId = (String) product.get(0);
        String price = (String) product.get(2);
        double pr = Double.parseDouble(price);
        int qty = ( (Integer)product.get(3)).intValue();
            ...
    }
*/



// Clear cart if order placed successfully
%>
<%
// Add a line to go to address.jsp
response.sendRedirect("address.jsp");
%>
</BODY>
</HTML>

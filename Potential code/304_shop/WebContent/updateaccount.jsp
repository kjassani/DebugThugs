<%@ page language="java" import="java.io.*,java.sql.*"%>
<%@ include file="jdbc.jsp" %>
<%
	String updateStatus = null;
    session.setAttribute("updateStatus",null);

    String olduserid = (String) session.getAttribute("authenticatedUser");
        String newuserid = request.getParameter("newuserid");
        String firstName = request.getParameter("firstName");
        String lastName = request.getParameter("lastName");
        String email = request.getParameter("email");
        String phonenum = request.getParameter("phonenum");
        String address = request.getParameter("address");
        String city = request.getParameter("city");
        String state = request.getParameter("state");
        String postalCode = request.getParameter("postalCode");
        String country = request.getParameter("country");
        String password = request.getParameter("password");

	try
	{
        String url = "jdbc:sqlserver://cosc304_sqlserver:1433;DatabaseName=orders;TrustServerCertificate=True";
        String uid = "sa";
        String pw = "304#sa#pw";  
        Connection con = DriverManager.getConnection(url, uid, pw);

//begin transaction
        con.setAutoCommit(false);

        String sql = "SELECT userid FROM customer WHERE userid = ?";
        PreparedStatement ps = con.prepareStatement(sql);
        ps.setString(1,newuserid);
        ResultSet result = ps.executeQuery();
    
        //check if username is already taken
        if(!result.next() || newuserid.equals(olduserid)){
           
            sql = "UPDATE customer SET firstName = ?, lastName = ?, email = ?, phonenum = ?, address = ?, city = ?, state = ?, postalCode = ?, country = ?, password = ?, userid = ? WHERE userid = ?";
            ps = con.prepareStatement(sql);
            ps.setString(1,firstName);
            ps.setString(2,lastName);
            ps.setString(3,email);
            ps.setString(4,phonenum);
            ps.setString(5,address);
            ps.setString(6,city);
            ps.setString(7,state);
            ps.setString(8,postalCode);
            ps.setString(9,country);
            ps.setString(10,password);
            ps.setString(11,newuserid);
            ps.setString(12,olduserid);

            ps.executeUpdate();

            //check if change was succesful
            ps = con.prepareStatement("SELECT * FROM customer WHERE userid = ?");
            ps.setString(1,newuserid);
            result = ps.executeQuery();
            if (result.next() &&
                result.getString("firstName").equals(firstName) &&
                result.getString("lastName").equals(lastName) &&
                result.getString("email").equals(email) &&
                result.getString("phonenum").equals(phonenum) &&
                result.getString("address").equals(address) &&
                result.getString("city").equals(city) &&
                result.getString("state").equals(state) &&
                result.getString("postalCode").equals(postalCode) &&
                result.getString("country").equals(country) &&
                result.getString("password").equals(password)) 
                {
            // The values in the database match the variables
            //update userid
            session.setAttribute("authenticatedUser", newuserid);
            con.commit();
            } else {
                // The values in the database do not match the variables
                con.rollback();
                updateStatus = "Account could not be updated.";
            }

            //end transaction
            con.setAutoCommit(true);

            

        } else{
            updateStatus = "Invalid Username. Username may already be taken.";
        }

    con.close();
	}
    catch(SQLException ex){
        out.println(ex);
    }

	if(updateStatus == null)
		response.sendRedirect("customer.jsp");		// Successful update
	else{
        session.setAttribute("updateStatus",updateStatus);
        response.sendRedirect("editaccount.jsp");		// Failed update - redirect back to page with a message 
    }
		
%>
<%@ page language="java" import="java.io.*"%>
<%@ page import="java.sql.*" %>
<%@ include file="jdbc.jsp" %>

<%
	String creationStatus = null;
    session.setAttribute("creationStatus",null);

        //Get parameters from form submission
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


        // Check for empty fields
        if (newuserid == null || newuserid.isEmpty()) {
            creationStatus = "Please enter a Username.";
        } else if (firstName == null || firstName.isEmpty()) {
            creationStatus = "Please enter a first name.";
        } else if (lastName == null || lastName.isEmpty()) {
            creationStatus = "Please enter a last name.";
        } else if (email == null || email.isEmpty()) {
            creationStatus = "Please enter an email address.";
        } else if (phonenum == null || phonenum.isEmpty()) {
            creationStatus = "Please enter a phone number.";
        } else if (address == null || address.isEmpty()) {
            creationStatus = "Please enter an address.";
        } else if (city == null || city.isEmpty()) {
            creationStatus = "Please enter a city.";
        } else if (state == null || state.isEmpty()) {
            creationStatus = "Please enter a state.";
        } else if (postalCode == null || postalCode.isEmpty()) {
            creationStatus = "Please enter a postal code.";
        } else if (country == null || country.isEmpty()) {
            creationStatus = "Please enter a country.";
        } else if (password == null || password.isEmpty()) {
            creationStatus = "Please enter a password.";
        }

        //if any fields are invalid, redirect back to account creation with error message
        if(creationStatus != null){
            session.setAttribute("creationStatus",creationStatus);
            response.sendRedirect("accountcreation.jsp");		// Failed update - redirect back to page with a message 
        }

try
	{
        String url = "jdbc:sqlserver://cosc304_sqlserver:1433;DatabaseName=orders;TrustServerCertificate=True";
        String uid = "sa";
        String pw = "304#sa#pw";  
        Connection con = DriverManager.getConnection(url, uid, pw);



        String sql = "SELECT * FROM customer WHERE userid = ?";
        PreparedStatement ps = con.prepareStatement(sql);
        ps.setString(1,newuserid);
        ResultSet result = ps.executeQuery();
        //check if username is taken


        if(!result.next()){

            //Begin transaction
            con.setAutoCommit(false);
            //attempts to add new account into the database
            sql = "INSERT INTO customer (firstName, lastName, email, phonenum, address, city, state, postalCode, country, userid, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            ps = con.prepareStatement(sql);
            ps.setString(1, firstName);
            ps.setString(2, lastName);
            ps.setString(3, email);
            ps.setString(4, phonenum);
            ps.setString(5, address);
            ps.setString(6, city);
            ps.setString(7, state);
            ps.setString(8, postalCode);
            ps.setString(9, country);
            ps.setString(10, newuserid);
            ps.setString(11, password);

            ps.executeUpdate();

            //check if account was created
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
                //account was inserted approprately. Commit insert
                con.commit();
            }
            else{
                //failure. rollack insert and give an error message
                con.rollback();
                creationStatus = "Account could not be created.";
            }
           

        } else{
            creationStatus = "Username Already Taken";
        }

    //end transaction
    con.setAutoCommit(true);
    con.close();
	}
    catch(SQLException ex){
        out.println(ex);
    }

	if(creationStatus == null)
		response.sendRedirect("login.jsp");		// Successful update
	else{
        session.setAttribute("creationStatus",creationStatus);
       		// Failed update - redirect back to page with a message 
        response.sendRedirect("accountcreation.jsp");	
    }
		
%>
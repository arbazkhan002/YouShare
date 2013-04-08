<?php
session_start();
if (isset($_SESSION['username'])) {
	header('Location: securedpage.php');
}
require_once('func.php');
//unlink('del_folder');
//rrmdir('users/aman');
//rrmdir('users/pavan.rock');
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" >

<head>

<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<title>CS425-ShareU</title>

<link rel="stylesheet" href="css/style.css" type="text/css" />

<link rel="stylesheet" href="css/screen.css" />


</head>
<body>
<h1 id="banner"><a href="http://web.cse.iitk.ac.in/users/cs425/">CS425-Computer Networks</a> Dropbox Prototype</h1>
<div class="header content clearfix">
<span class="signup-button"><d4>New to ShareU? <a  id="link-signup" class="g-button g-button-red" href="signup.php"><b>CREATE AN ACCOUNT</d4></a></b></span>
</div>
</div>
<br>
<br>
<br>
<br>
<div class ="left ">
	<d7>Aman Kumar Singh</d7><br>
	<d8>Junior Undergraduate Student
	<br>Department of Computer Science &amp; Engineering
	<br>IIT Kanpur
	<br>Kanpur 208016 , INDIA
	<br><a href="http://home.iitk.ac.in/~akrsingh/">Homepage</a></d8>

	
	
</div>
<div class ="right ">
	<d7>Pavan Sharma</d7><br>
	<d8>Junior Undergraduate Student
	<br>Department of Computer Science &amp; Engineering
	<br>IIT Kanpur
	<br>Kanpur 208016 , INDIA
	<br><a href="http://home.iitk.ac.in/~pavans/">Homepage</a></d8>
	
	
</div>
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>


<div class ="left ">
	<d7>Arbaz Khan</d7><br>
	<d8>Junior Undergraduate Student
	<br>Department of Computer Science &amp; Engineering
	<br>IIT Kanpur
	<br>Kanpur 208016 , INDIA
	<br><a href="http://home.iitk.ac.in/~arbazk/">Homepage</a></d8>

	
	
</div>

<div class ="right ">
	<d7>Mayank Dang</d7><br>
	<d8>Junior Undergraduate Student
	<br>Department of Computer Science &amp; Engineering
	<br>IIT Kanpur
	<br>Kanpur 208016 , INDIA
	<br><a href="http://home.iitk.ac.in/~mayankd/">Homepage</a></d8>

	
</div><br><br><br><br>



	<div class="shareU-footer-bar"> 
  <div class="footer content clearfix"> 
  <ul> 
  <li><a href="index.php" ><d9>Home</d9></a></li>
	<li><a href="aboutus.php" target="_blank"><d9>About Us</d9></a></li>
	<li><a href="terms.php" target="_blank"><d9>Terms &amp; Privacy</d9></a></li>
	<li><d9>&copy; 2011 ShareU</d9></li> 
  </ul> 
  </div> 
</div> 
</body>
</html>

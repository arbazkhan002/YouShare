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
<br>
<br>
<br>
<br>
<br>
<br>
<br>






<?php
require_once('func.php');
$name=$_POST['reg_name'];
$user=$_POST['reg_username'];
$email=$_POST['reg_email'];
$password=$_POST['reg_pass'];
if(strlen($user)<4){
	echo '<div class= "errorbox"><d1>Too short username. </d1><a href="signup.php"><d2> Return</d2></a></div>';
}
else if(strlen($user)>20){
	echo '<div class= "errorbox"><d1>Too long username. </d1><a href="signup.php"><d2> Return</d2></a></div>';
}
else if(!validEmail($email)){
	echo '<div class= "errorbox"><d1>Invalid email. </d1><a href="signup.php"><d2> Return</d2></a></div>';
}
else if(user_exists($user)){
	echo '<div class= "errorbox"><d1>Username already in use. </d1><a href="signup.php"><d2> Return</d2></a></div>';
}
else if(email_exists($email)){
	echo '<div class= "errorbox"><d1>Email address already registered. <a href="signup.php"><d2> Return</d2></a></d1></div>';
}
else{
	$code = substr(md5($email),8,5);
	Email($email,"registration confirmation",$code);
	echo '<div class= "errorbox"><d2>Everything is ok!</br>We have sent you a mail with confirmation code.</d1></br>';
	echo '<form method="POST" action="confirm.php">';
	echo '<input type="hidden" name="reg_name" value = '.$name.' size="50">';
	echo '<input type="hidden" name="reg_user" value = '.$user.' size="20">';
	echo '<input type="hidden" name="reg_email" value = '.$email.' size="50">';
	echo '<input type="hidden" name="reg_pass" value = '.$password.' size="20">';
	echo '<input type="hidden" name="code" value = '.$code.' size="5">';
	echo '<d2>Enter the code received in your mail: </d2><input type="text" name="code_entered" size="5">';
	echo '<input type="submit" name="submit" value="Submit">';
	echo '</form></div>';
}
?>
</body>
</html>

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
<div class= "errorbox">




<?php
require_once('func.php');
echo '<html>';
if($_POST['code']==trim($_POST['code_entered'])){
	echo 'Email address confirmed. </br>';
	$con_name=$_POST['reg_name'];
	$con_user=$_POST['reg_user'];
	$con_pass=$_POST['reg_pass'];
	$con_email=$_POST['reg_email'];
	if(reg_user($con_name,$con_user,$con_pass,$con_email)){
		echo '<d2>Registration complete.Continue to </d2><a href="index.php"><d2>Signin</d2></a>.';
		echo '<form method="POST" action="download.php">';
		echo '<input type="hidden" name="file_path" size="50" value="">';
		echo '<input type="hidden" name="pre_path" value = "users/install_files.tar.gz" size="50">';
		echo '<input type="submit" name="download" value="Download">';
		echo '</form>';
	}
	else echo '<d2>Registration failed.</d2><a href="signup.php"><d2>Signup</d2></a>.';
}
else{
	echo '<d2>Wrong code</d2>';
}
echo '</div></html>';
?>

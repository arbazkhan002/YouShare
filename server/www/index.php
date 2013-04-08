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

<div class="form">


<div class ="right">
<h2>User Login</h2>
<table border="0">
<?php
if(isset($_SERVER['HTTP_USER_AGENT'])){
	echo '<form method="POST" action="loginproc.php">';
}
?>
<tr><td><d5><b>Username</d5></b></td><td>:</td><td><input type="text" name="username" size="20"></td></tr>
<tr><td><d5><b> Password </d5></b></td><td>:</td><td><input type="password" name="password" size="20"></td></tr>
<tr><td>&nbsp;</td><td>&nbsp;</td><td><input type="submit" name="login" value="Login"></td></tr>
</form>
</table>

</div>

<div class=loginleft>
<d6>ShareU</d6><br>
<d7>Web-based file hosting and syncing service</d7>
<br><br>
<d8>A web-based file hosting software (like Dropbox) that enable users
to store and share files and folders with others across the Internet using file
synchronization. Also, if a user has uploaded a file to your web server, then any
changes he makes to his file locally should automatically be synced with the file on
the server whenever there is internet connectivity.<br>Share-U has:</d8>
<br>
<br>
<ul class="features">
	<li>
	<img src="images/tick_logoBLUE.png" width="40" height="38" alt="">
	<p><d7>Online Storage.</d7></p>
	<p><d8> Access important files from any online computer.</d8></p>
	</li>
	<li>
	<img src="images/tick_logoBLUE.png" width="40" height="38" alt="">
	<p><d7>Starting Space</d7></p>
	<p><d8>Over 20 Megabytes of free storage.</d8></p>
	</li>
	<li>
	<img src="images/tick_logoBLUE.png" width="40" height="38" alt="">
	<p><d7>Secure Backup.</d7></p>
	<p><d8> Enjoy the piece of mind knowing your files are safe.</d8></p>
	</li>
	
</ul>
</div>
	</div>
	</div>
	</div>
	
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
</div>
</body>
</html>

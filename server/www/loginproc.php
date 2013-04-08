<?php
session_start();
require_once('connect.php');
require_once('func.php');
$query='select * from users where username="'.$_POST['username'].'"';
$result=mysql_query($query);
$row=mysql_fetch_assoc($result);
if(user_exists($_POST['username'])){
	if($row['password']==trim($_POST['password'])){
		$_SESSION['username'] = $_POST['username'];
		if($_SERVER['HTTP_USER_AGENT']=='MyApplication'){
			header('Location: loginpy.php');
		}
		else{
			header('Location: securedpage.php');
		}
	}
	else{
		echo 'Wrong password.Would you like to <a href = "index.php">try again</a>?';
	}
}
else{
	echo '<p>Username not registered.Would you like to <a href = "index.php">try again</a>?</p>';
}
?>

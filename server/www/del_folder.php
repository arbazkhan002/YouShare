<?php
session_start();
require_once('func.php');
if($_POST['path']!='' && substr($_POST['path'],-1)!='/'){
	$folder='users/'.$_SESSION['username'].'/'.trim($_POST['path']);
	if(is_dir($folder)){
		rrmdir($folder);
		header('Location:securedpage.php');
	}
	else{
		echo $folder.':No such directory';
	}
}
else header('Location:securedpage.php');
?>

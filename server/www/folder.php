<?php
session_start();
if($_POST['path']!='' && substr($_POST['path'],-1)!='/'){
	$folder='users/'.$_SESSION['username'].'/'.$_POST['path'];
	if(!is_dir($folder)){
		mkdir($folder);
		$fh=fopen('logs/'.$_SESSION['username'].'.txt','a');
		fwrite($fh,$folder.'/');
		header('Location:securedpage.php');
	}
	else{
		echo $folder.' already exists';
	}
}
else header('Location:securedpage.php');
?>

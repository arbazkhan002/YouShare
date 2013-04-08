<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" >

<head>

<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<title>CS425-ShareU</title>
<script type="text/javascript" >

</script>


<link rel="stylesheet" href="css/style.css" type="text/css" />
<link rel="stylesheet" href="css/screen.css" />


</head>
<body>
<h1 id="banner"><a href="http://web.cse.iitk.ac.in/users/cs425/">CS425-Computer Networks</a> Dropbox Prototype</h1>
<br>
<br>
<br>
<br>


<div class= "errorbox">

<?php
$target = $_POST['pre_path'].$_POST['dir_path'];
$user = $_POST['username'];
$full_target = '/var/www/'.$target;
$link_name = $_POST['link_name'];
$full_path = 'users/'.$user.'/'.$link_name;
if(is_dir('users/'.$user)){
	if(is_dir($target)){
		if(is_file($full_path) || is_dir($full_path) || is_link($full_path)){
			echo '<br><d1>Destination already exists.Choose a different name for your link. </d1><br><br><a href="securedpage.php"><d2> Home</d2></a>';
		}
		else if($_POST['dir_path']!='' && substr($_POST['dir_path'],-1)!='/'){
			symlink($full_target,$full_path);
			$fh=fopen('logs/'.$user.'.txt','a');
			fwrite($fh,$full_path."/\r\n");
			echo 'Your folder is shared with '.$user.' now.<a href="securedpage.php"><d2> Home</d2></a>';
		}
		else{
			 echo '<br><d1>Dude! If you dont want your privacy. Hey! who am I to stop you! </d1><br><br><a href="securedpage.php"><d2> Home</d2></a>';
		}
	}
	else if(is_file($target)){
		if(is_file($full_path) || is_dir($full_path) || is_link($full_path)){
			echo 'Destination already exists.Choose a different name for your link.';
		}
		else{
			symlink($full_target,$full_path);
			$fh=fopen('logs/'.$user.'.txt','a');
			fwrite($fh,$full_path."\r\n");
			echo 'Your folder is shared with '.$user.' now.<a href="securedpage.php"><d2> Home</d2></a>';
		}
	}
	else{
		echo 'Target is not valid <a href="securedpage.php"><d2> Home</d2></a>';
	}
}
else{
	echo 'No such user name is here.<a href="securedpage.php"><d2> Home</d2></a>';
}
?>
</div>
</body>
</html>

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
if(!is_link($_POST['pre_link_path'].$_POST['link_path'])){
	echo '<d1>Not a valid link. </d1><a href="securedpage.php"><d2> Return</d2></a>.';
}
else{
	$path=readlink($_POST['pre_link_path'].$_POST['link_path']);
	$array = explode('/',$path);
	array_shift($array);array_shift($array);array_shift($array);
	$path = implode('/',$array);
	if(is_dir($path)){
		list_dir($path);
		echo '<form method="POST" action="download.php">';
		echo '<d1>Download: </d1><input type="text" name="file_path" size="50">';
		echo '<input type="hidden" name="pre_path" value = '.$path.' size="50">';
		echo '<input type="submit" name="download" value="Download">';
		echo '</form>';
		if(round(f_size($path)/(1024*1024))<=21){
		echo '<form action="upload.php" method="POST" enctype="multipart/form-data">';
		echo '<label for="file"><d1>Upload: </d1></label>';
		echo '<input type="file" name="file" id="file" />';
		echo '<d1>To: </d1><input type="text" name="destination" size="50"/>';
		echo '<input type="hidden" name="pre_path" value = '.$path.' size="50">';
		echo '<input type="hidden" name="link_stat" value = "yes" size="5">';
		echo '<input type="submit" name="submit" value="Upload" />';
		echo '</form>';
		}
		else echo 'the owner of the link has run out of space.';
	}
	else if(is_file($path)){
		echo 'The link is to a file.</br>'.$path;
		echo '<form method="POST" action="download.php">';
		echo '<input type="hidden" name="file_path" size="50" value="">';
		echo '<input type="hidden" name="pre_path" value = '.$path.' size="50">';
		echo '<input type="submit" name="download" value="Download">';
		echo '</form>';
	}
	else if(is_link($path)){
		echo '<d1>The link is to a link. <a href="securedpage.php"><d2> Return</d2></a></d1>';
	}
}
?>
</div>
</body>
</html>

<?php
session_start();
$full_dest = $_POST['pre_path'].$_POST['destination'];
echo $full_dest;
if(trim($_POST['link_stat'])=='no'){
	$fh=fopen('logs/'.$_SESSION['username'].'.txt','a');
}
else{
	$arr=explode('/',$full_dest);
	echo '----'.$arr[1].'----';
	$fh=fopen('logs/'.$arr[1].'.txt','a');

}

if(is_dir($full_dest)){
  if ($_FILES["file"]["error"] > 0){
    echo '<html><head><meta http-equiv="content-type" content="text/html; charset=iso-8859-1" /><title>CS425-ShareU</title><link rel="stylesheet" href="css/style.css" type="text/css" /><link rel="stylesheet" href="css/screen.css" /></head><body><h1 id="banner"><a href="http://web.cse.iitk.ac.in/users/cs425/">CS425-Computer Networks</a> Dropbox Prototype</h1><br><br><br><br><br><br><br><div class= "errorbox">Return Code: ' . $_FILES["file"]["error"] . '<br />';
    echo 'The file you were trying to upload was too big. <a href="securedpage.php"><d2> Return</d2></a></div></body></html>';
  }
  else{
    if (is_file($full_dest .'/'. $_FILES["file"]["name"]) || is_link($full_dest .'/'. $_FILES["file"]["name"])){
		echo $_FILES["file"]["name"] . " already exists. ";
    }
    else{
		move_uploaded_file($_FILES["file"]["tmp_name"],$full_dest .'/'. $_FILES["file"]["name"]);
		echo "Upload: " . $_FILES["file"]["name"] . "<br />";
		echo "Type: " . $_FILES["file"]["type"] . "<br />";
		echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
		fwrite($fh,$full_dest .'/'. $_FILES["file"]["name"]."\r\n");
    }
  }
  //echo 'logs/'.$_SESSION['username'].'.txt';
}
else{
	echo '<html><head><meta http-equiv="content-type" content="text/html; charset=iso-8859-1" /><title>CS425-ShareU</title><link rel="stylesheet" href="css/style.css" type="text/css" /><link rel="stylesheet" href="css/screen.css" /></head><body><h1 id="banner"><a href="http://web.cse.iitk.ac.in/users/cs425/">CS425-Computer Networks</a> Dropbox Prototype</h1><br><br><br><br><br><br><br><div class= "errorbox"><d1>Invalid destination </d1><a href="securedpage.php"><d2>Home</d2></a></div></body</html>';
	//echo $full_dest;
}
?> 
</div>
	</div>
	</div>
	</div>
</body>
</html>

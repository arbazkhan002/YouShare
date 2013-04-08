<?php
$full_path=$_POST['pre_path'].$_POST['file_path'];
if(is_file($full_path)){
	$mtype=mime_content_type($full_path);
	if(trim($_POST['file_path'])!=''){
		$arr = explode('/',$_POST['file_path']);
		$asfname=array_pop($arr);
	}
	else{
		$arr = explode('/',$full_path);
		$asfname=array_pop($arr);
	}
	$fsize=filesize($full_path);
	header("Pragma: public");
	header("Expires: 0");
	header("Cache-Control: must-revalidate, post-check=0, pre-check=0");
	header("Cache-Control: public");
	header("Content-Description: File Transfer");
	header("Content-Type: $mtype");
	header("Content-Disposition: attachment; filename=\"$asfname\"");
	header("Content-Transfer-Encoding: binary");
	header("Content-Length: " . $fsize);
	$file = @fopen($full_path,"rb");
	if ($file) {
		while(!feof($file)){
			print(fread($file, 1024*8));
			flush();
			if (connection_status()!=0) {
				@fclose($file);
				die();
			}
		}
		@fclose($file);
	}
}
else
	echo '<html><head><meta http-equiv="content-type" content="text/html; charset=iso-8859-1" /><title>CS425-ShareU</title><link rel="stylesheet" href="css/style.css" type="text/css" /><link rel="stylesheet" href="css/screen.css" /></head><body><h1 id="banner"><a href="http://web.cse.iitk.ac.in/users/cs425/">CS425-Computer Networks</a> Dropbox Prototype</h1><br><br><br><br><br><br><br><div class= "errorbox"><d1><br>This is not a valid file. </d1><a href="securedpage.php"><d2> Home</d2></a>.</div></body></html>';
	//echo $full_path;
?>

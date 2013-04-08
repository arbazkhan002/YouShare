<?php
require_once('connect.php');
function f_size($path){
	$ret=0;
    $dir_handle = opendir($path);
    while (false !== ($file = readdir($dir_handle))) {
        $dir =$path.'/'.$file;
        if(is_dir($dir) && $file != '.' && $file !='..' )
        {  
			$ret += f_size($dir);
        }
        elseif($file != '.' && $file !='..')
        {
			if(!is_link($dir)){
				$ret+=filesize($dir);
			}
        }
    }
    closedir($dir_handle);
    return $ret;
}
function list_dir($path)
{	
    echo "<ol>";
    $dir_handle = opendir($path);
    while (false !== ($file = readdir($dir_handle))) {
        $dir =$path.'/'.$file;
        if(is_dir($dir) && $file != '.' && $file !='..' )
        {
            if(is_link($dir)) 
				echo "<li><b><i><u>$file</u></i></b></li>";
            else{
				echo "<li><b>$file</b></li>";
				list_dir($dir);
			}
        }
        elseif($file != '.' && $file !='..')
        {
			if(is_link($dir)){
				echo "<li><u><i>$file</i></u></li>";
			}
			else{
				echo "<li>$file</li>";
			}
        }
    }
   
    echo "</ol>";
    closedir($dir_handle);
}
function str_file($path,$str,$offset)
{
	$dir_handle = opendir($path);
    while (false !== ($file = readdir($dir_handle))) {
        $dir =$path.'/'.$file;
        if(is_dir($dir) && $file != '.' && $file !='..' )
        {  
			$str = str_file($dir,$str,$offset);
        }
        elseif($file != '.' && $file !='..')
        {
			if(!is_link($dir)){
				$str=$str.'"'.substr($dir,$offset).'",';
			}
        }
    }
    closedir($dir_handle);
    return $str;
}
function str_dir($path,$str,$offset)
{
    $dir_handle = opendir($path);
    while (false !== ($file = readdir($dir_handle))) {
        $dir =$path.'/'.$file;
        if(is_dir($dir) && $file != '.' && $file !='..' )
        {  
			$str=$str.'"'.substr($dir,$offset).'",';
			$str = str_dir($dir,$str,$offset);
        }
    }
    closedir($dir_handle);
    return $str;
}
function str_link($path,$str,$offset)
{
	$dir_handle = opendir($path);
    while (false !== ($file = readdir($dir_handle))) {
        $dir =$path.'/'.$file;
        if(is_dir($dir) && $file != '.' && $file !='..' )
        {
			$str = str_link($dir,$str,$offset);
        }
        elseif($file != '.' && $file !='..')
        {
			if(is_link($dir)){
				$str=$str.'"'.substr($dir,$offset).'",';
			}
        }
    }
    closedir($dir_handle);
    return $str;
}
function RecursiveCopy($source, $dest, $diffDir = ''){
    $sourceHandle = opendir($source);
    if(!$diffDir)
            $diffDir = $source;
   
    mkdir($dest . '/' . $diffDir,0777);
    
   
    while($res = readdir($sourceHandle)){
        if($res == '.' || $res == '..')
            continue;
       
        if(is_dir($source . '/' . $res)){
            RecursiveCopy($source . '/' . $res, $dest, $diffDir . '/' . $res);
        } else {
            copy($source . '/' . $res, $dest . '/' . $diffDir . '/' . $res);
			chmod($dest . '/' . $diffDir . '/' . $res,0777);
        }
    }
} 
function rrmdir($dir) {
  if (is_dir($dir)) {
    $files = scandir($dir);
    foreach ($files as $file)
    if ($file != "." && $file != "..") rrmdir("$dir/$file");
    rmdir($dir);
  }
  else if (file_exists($dir)) unlink($dir);
  else if(is_link($dir)) unlink($dir);
} 
function Email($to,$subject,$body){
	$ccid="pavans";
	$pass="98268708";
	$smtp_server = fsockopen("smtp.cc.iitk.ac.in", 25);
	fwrite($smtp_server, "HELO me\r\n");
	fwrite($smtp_server, "auth login\r\n");
	fwrite($smtp_server, base64_encode($ccid)."\r\n");
	fwrite($smtp_server, base64_encode($pass)."\r\n");
	fwrite($smtp_server, "MAIL FROM:".$ccid."\r\n");
	fwrite($smtp_server, "RCPT TO:".$to."\r\n");
	fwrite($smtp_server, "DATA\r\n");
	fwrite($smtp_server, "subject:".$subject."\r\n");
	fwrite($smtp_server, $body."\r\n");
	fwrite($smtp_server, ".\r\nQUIT\r\n");	
}
function allow_reg(){
	$query='select * from users';
	if(!$result=mysql_query($query)){
		echo mysql_error();
		return false;
	}
	if(mysql_num_rows($result)<=10)	return true;		//checks how many users are already registered
	else return false;
}
function user_exists($username){
	$query='select * from users where username="'.$username.'"';
	if(!$result=mysql_query($query)){
		echo mysql_error();
	}
	return mysql_num_rows($result);
}
function email_exists($email){
	$query='select * from users where email="'.$email.'"';
	if(!$result=mysql_query($query)){
		echo mysql_error();
	}
	return mysql_num_rows($result);
}
function reg_user($name,$username,$password,$email){
	if(allow_reg()){
		$query='insert into users values("'.$name.'","'.$username.'","'.$password.'","'.$email.'")';
		if(!$result=mysql_query($query)){
			echo mysql_error();
			return false;
		}
		mkdir('users/'.$username);
		copy('users/log.txt','logs/'.$username.'.txt');
		chmod('logs/'.$username.'.txt',0777);
		return true;
	}
	else return false;
}
function validEmail($email)
{
	return eregi("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$", $email);
}
?>

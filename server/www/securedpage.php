<?php
// Inialize session
session_start();
// Check, if username session is NOT set then this page will jump to login page
if (!isset($_SESSION['username'])) {
header('Location: index.php');
}
$user = $_SESSION['username'];
$path='users/'.$user;
require_once('func.php');
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" >

<head>

<!meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<title>CS425-ShareU</title>

<link rel="stylesheet" href="css/style.css" type="text/css" />
<link rel="stylesheet" href="css/screen.css" />

<link href="css/jquery-ui.css" rel="stylesheet" type="text/css"/>
  <script src="scripts/jquery.min.js"></script>
  <script src="scripts/jquery-ui.min.js"></script>
  
  <script>
  $(document).ready(function() {
    $("input#autocompletefile").autocomplete({
    source: [<?php echo substr(str_file($path,'',strlen($path)),0,-1); ?>]
    
});
  });
  </script>
  <script>
  $(document).ready(function() {
    $("input#autocompletedir").autocomplete({
    source: [<?php echo substr(str_dir($path,'',strlen($path)),0,-1); ?>]
});
  });
  </script>
  
  <script>
  $(document).ready(function() {
    $("input#autocomplete").autocomplete({
    source: [<?php echo str_dir($path,'',strlen($path)).substr(str_file($path,'',strlen($path)),0,-1); ?>]
});
  });
  </script>
  
  <script>
  $(document).ready(function() {
    $("input#autocompletelink").autocomplete({
    source: [<?php echo substr(str_link($path,'',strlen($path)),0,-1); ?>]
});
  });
  </script>

</head>
<body>
<h1 id="banner"><a href="http://web.cse.iitk.ac.in/users/cs425/">CS425-Computer Networks</a> Dropbox Prototype</h1>
<div class="header content clearfix">
<span class="signup-button"> <d4><a  id="link-signup" class="g-button g-button-red" href="logout.php">Logout</a></d4></span>
</div>
<?php
//echo 'Your Files Preview<br>';
list_dir($path);
echo '<br><br>';
//******************************************************************************************
echo '<div class ="leftt">';
echo '<form method="POST" action="download.php">';
echo '<d1>Download: </d1><input id="autocompletefile" type="text" name="file_path" size="50">';
echo '<input type="hidden" name="pre_path" value = '.$path.' size="50">';
echo '<input type="submit" name="download" value="Download">';
echo '</form><br>';
echo '</div>';
//******************************************************************************************
echo '<div class ="rightt">';
echo '<form method="POST" action="link.php">';
echo '<d1>View Link: </d1><input id= "autocompletelink" type="text" name="link_path" size="50">';
echo '<input type="hidden" name="pre_link_path" value = '.$path.' size="50">';
echo '<input type="submit" name="view_link" value="View Link">';
echo '</form><br>';
echo '</div><br><br><br><br>';
//******************************************************************************************
echo '<br><br><br><br><div class ="leftt">';
echo '<form method="POST" action="folder.php">';
echo '<d1>Create folder: </d1><input type="text" name="path" size="50">';
echo '<input type="submit" name="folder" value="Create folder">';
echo '</form><br>';
echo '</div>';

//******************************************************************************************

echo '<div class ="rightt">';
echo '<form method="POST" action="share.php">';
echo '<d1>Share: </d1><input id= "autocomplete" type="text" name="dir_path" size="50">';
echo '<br><d1>With: </d1><input type="text" name="username" size="20">';
echo '<br><d1>By name: </d1><input type="text" name="link_name" size="50">';
echo '<input type="hidden" name="pre_path" value = '.$path.' size="50">';
echo '<input type="submit" name="share" value="Share">';
echo '</form>';
echo '</div><br><br><br><br>';

//******************************************************************************************


/*
echo '<div class ="rightt">';
echo '<form method="POST" action="del_folder.php">';
echo '<d1>Delete folder: </d1><input type="text" name="path" size="50">';
echo '<input type="submit" name="folder" value="delete folder">';
echo '</form><br>';
echo '</div><br><br><br><br>';
*/

//******************************************************************************************
if(round(f_size($path)/(1024*1024))<=21){
echo '<br><br><br><br><div class ="leftt">';
echo '<form action="upload.php" method="POST" enctype="multipart/form-data">';
echo '<label for="file"><d1>Upload: </d1></label>';
echo '<input type="file" name="file" id="file" />';
echo '<br><d1>To: </d1><input id = "autocompletedir"  type="text" name="destination" size="50"/>';
echo '<input type="hidden" name="pre_path" value = '.$path.' size="50">';
echo '<input type="hidden" name="link_stat" value = "no" size="5">';
echo '<input type="submit" name="submit" value="Upload" />';
echo '</form><br>';
echo '</div>';
}
else
 echo 'you have exceeded the size limit';
//******************************************************************************************


?>

</body>
</html>

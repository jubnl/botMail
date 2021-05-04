<?
$email = $_GET['email'];
header("Location: mailto:".$email);
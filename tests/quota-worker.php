<?php
require '/var/www/html/wp-load.php';
$_SERVER['REMOTE_ADDR']='192.0.2.1'; // Reserved documentation/test address.
echo (getenv('GNF_WORKER_KIND')==='rate' ? \GymNotFound\Providers::rate() : \GymNotFound\Providers::reserve('geoapify')) ? '1' : '0';

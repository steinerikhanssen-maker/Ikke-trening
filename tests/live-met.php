<?php
use GymNotFound\Providers;
// A public central-Oslo area; never a test visitor's GPS. No HTTP mock.
$result=Providers::weather(59.91,10.71);
echo wp_json_encode(['provider'=>'MET Norway','status'=>$result['status'],'forecast_at'=>$result['forecast_at'] ?? null,'fetched_at'=>$result['fetched_at'] ?? null,'current'=>isset($result['forecast_at']) && abs(time()-strtotime($result['forecast_at']))<=5400,'key_required'=>false],JSON_PRETTY_PRINT)."\n";
if ($result['status']!=='ok') throw new RuntimeException('MET live test did not return a current forecast');

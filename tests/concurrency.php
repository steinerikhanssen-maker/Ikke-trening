<?php
use GymNotFound\Providers as P;
$saved=get_option('gnf_settings',[]);
function gnf_workers(string $kind): int {
    putenv('GNF_WORKER_KIND='.$kind);$workers=[];
    for ($i=0;$i<8;$i++) {
        $pipes=[];$process=proc_open([PHP_BINARY,'/var/www/html/gnf-tests/quota-worker.php'],[0=>['pipe','r'],1=>['pipe','w'],2=>['pipe','w']],$pipes);
        if (!is_resource($process)) throw new RuntimeException('Could not start PHP worker');
        fclose($pipes[0]);$workers[]=[$process,$pipes];
    }
    $allowed=0;
    foreach($workers as [$process,$pipes]) {
        $output=stream_get_contents($pipes[1]);$errors=stream_get_contents($pipes[2]);fclose($pipes[1]);fclose($pipes[2]);$code=proc_close($process);
        if($code || $errors || !in_array($output,['0','1'],true))throw new RuntimeException('Unexpected worker result');
        $allowed+=(int)$output;
    }
    return $allowed;
}
try {
    update_option('gnf_settings',['hour_cap'=>1,'day_cap'=>1,'weather'=>true,'places'=>false],false);delete_option('gnf_usage_geoapify');
    if(gnf_workers('quota')!==1)throw new RuntimeException('FAIL concurrent quota');
    echo "PASS D7 one of eight concurrent PHP workers reserves the last quota slot\n";
    $_SERVER['REMOTE_ADDR']='192.0.2.1';
    $key='gnf_rate_'.substr(hash_hmac('sha256',$_SERVER['REMOTE_ADDR'],wp_salt('nonce')),0,32);delete_transient($key);delete_transient('gnf_global_rate');
    for($i=0;$i<26;$i++)if(!P::rate())throw new RuntimeException('Rate prime failed');
    if(gnf_workers('rate')!==4)throw new RuntimeException('FAIL concurrent rate limit');
    echo "PASS D12 only four of eight concurrent workers consume the remaining public rate slots\n";
} finally {update_option('gnf_settings',$saved,false);delete_option('gnf_usage_geoapify');delete_transient($key ?? 'gnf_noop');delete_transient('gnf_global_rate');}

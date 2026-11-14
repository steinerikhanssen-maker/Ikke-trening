<?php
/** Runs in a real local WordPress/MariaDB, intercepting outbound HTTP only. */
use GymNotFound\Providers as P;
use GymNotFound\Content as C;
global $gnf_assertions,$gnf_calls,$gnf_mock,$gnf_clock;
$gnf_assertions=0;$gnf_calls=[];$gnf_clock=strtotime('2026-10-14T12:00:00Z');
$gnf_mock=new WP_Error('http_request_failed','Fixture: unconfigured source');
function gnf_assert($condition,string $name): void { global $gnf_assertions;if (!$condition) throw new RuntimeException('FAIL '.$name);$gnf_assertions++;echo 'PASS '.$name."\n"; }
function gnf_reset(): void {global $wpdb,$gnf_calls;$gnf_calls=[];$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_gnf_%' OR option_name LIKE '_transient_timeout_gnf_%'");wp_cache_flush();delete_option('gnf_usage_met');delete_option('gnf_usage_geoapify');}
function gnf_http(array $body,int $code=200,array $headers=[]): array {return ['headers'=>$headers,'body'=>wp_json_encode($body),'response'=>['code'=>$code,'message'=>'fixture'],'cookies'=>[]];}
function gnf_met(float $temperature=14,float $wind=2,float $rain=0): array {global $gnf_clock;return ['properties'=>['timeseries'=>[['time'=>gmdate('c',$gnf_clock),'data'=>['instant'=>['details'=>['air_temperature'=>$temperature,'wind_speed'=>$wind]],'next_1_hours'=>['details'=>['precipitation_amount'=>$rain]]]]]]];}
function gnf_place(string $id,string $category='leisure.park',array $extra=[]): array {return ['type'=>'Feature','properties'=>array_merge(['place_id'=>$id,'name'=>'TEST FIXTURE '.$id,'lat'=>59.91,'lon'=>10.71,'categories'=>[$category]],$extra),'geometry'=>['type'=>'Point','coordinates'=>[10.71,59.91]]];}
$saved=['settings'=>get_option('gnf_settings',[]),'key'=>get_option('gnf_geoapify_key','')];
add_filter('gymnotfound_now',function() {global $gnf_clock;return $gnf_clock;});
add_filter('pre_http_request',function($pre,$args,$url){global $gnf_calls,$gnf_mock;$gnf_calls[]=['url'=>$url,'args'=>$args];return $gnf_mock;},10,3);
try {
  gnf_reset();update_option('gnf_settings',['weather'=>true,'places'=>false,'hour_cap'=>12,'day_cap'=>75],false);P::set_key('');
  gnf_assert(count(C::all())===36,'A4 36 editable published bilingual templates');
  C::seed();gnf_assert(count(C::all())===36,'A2 reactivation seed is idempotent');
  $api=rest_get_server();
  $call=function(string $route,array $payload) { $r=new WP_REST_Request('POST','/gymnotfound/v1/'.$route);$r->set_header('Content-Type','application/json');$r->set_body(wp_json_encode($payload));return rest_do_request($r); };
  $r=$call('context',[]);gnf_assert($r->get_status()===200 && !$gnf_calls,'D3 no position means zero external requests');
  $r=$call('context',['lat'=>59.912345,'lon'=>10.712345,'time'=>15,'environment'=>'auto']);
  gnf_assert(!$gnf_calls || count($gnf_calls)===1,'D5 unconfigured Geoapify never calls places');
  gnf_reset();$gnf_mock=gnf_http(gnf_met(),200,['expires'=>gmdate('D, d M Y H:i:s',$gnf_clock+1800).' GMT','last-modified'=>gmdate('D, d M Y H:i:s',$gnf_clock-60).' GMT']);
  for($i=0;$i<5;$i++) $weather=P::weather(59.91234,10.71345);
  gnf_assert($weather['status']==='ok' && count($gnf_calls)===1,'D8 five area requests make one MET call');
  parse_str(wp_parse_url($gnf_calls[0]['url'],PHP_URL_QUERY),$query);
  gnf_assert($query['lat']==='59.91' && $query['lon']==='10.71','D2 only rounded coordinates sent');
  $args=$gnf_calls[0]['args'];gnf_assert(str_contains($args['headers']['User-Agent'],'GymNotFound/') && str_contains($args['headers']['User-Agent'],'https://github.com/'),'D2 identifying User-Agent');
  gnf_assert($args['sslverify'] && $args['timeout']===5 && $args['redirection']===0 && $args['limit_response_size']===196608 && str_starts_with($gnf_calls[0]['url'],P::MET.'?'),'E5 fixed TLS endpoint allowlist, timeout, size and no redirects');
  $key='gnf_met_'.md5('59.91:10.71');$cache=get_transient($key);$cache['expires']=$gnf_clock-1;set_transient($key,$cache,DAY_IN_SECONDS);
  $gnf_mock=gnf_http([],304,['expires'=>gmdate('D, d M Y H:i:s',$gnf_clock+1200).' GMT']);$weather=P::weather(59.91,10.71);
  gnf_assert($weather['status']==='ok' && isset($gnf_calls[1]['args']['headers']['If-Modified-Since']),'D2 Last-Modified conditional revalidation / 304');
  foreach([[14,2,0],[14,2,3],[14,15,0],[-4,2,0]] as $numbers){gnf_reset();$gnf_mock=gnf_http(gnf_met(...$numbers));$w=P::weather(59.91,10.71);gnf_assert($w['status']==='ok' && $w['temperature']===$numbers[0]+0.0,'D1 real adapter parses forecast '.implode('/',$numbers));}
  gnf_reset();$old=gnf_met();$old['properties']['timeseries'][0]['time']='2025-01-01T12:00:00Z';$gnf_mock=gnf_http($old);gnf_assert(P::weather(59.91,10.71)['status']==='stale','D1 stale data never shown as current');
  foreach([403,429,500,'timeout','invalid','oversized'] as $failure){
    gnf_reset();$gnf_mock=$failure==='timeout' ? new WP_Error('http_request_failed','fixture timeout') : gnf_http([],is_int($failure)?$failure:200);
    if($failure==='oversized')$gnf_mock['body']=str_repeat('x',196609);
    $w=P::weather(59.91,10.71);P::weather(59.91,10.71);
    gnf_assert(in_array($w['status'],['unavailable','rate_limited'],true)&&count($gnf_calls)===1,'D4 MET fallback / backoff '.$failure);
  }
  gnf_reset();$token=wp_generate_password(32,false,false);gnf_assert(P::set_key($token) && P::key()===$token && !str_contains(get_option('gnf_geoapify_key'),$token),'A5 key is encrypted server-side');
  update_option('gnf_settings',['weather'=>true,'places'=>true,'hour_cap'=>12,'day_cap'=>75],false);
  $features=[gnf_place('A'),gnf_place('A'),gnf_place('B','leisure.park',['name'=>'TEST FIXTURE A']),gnf_place('PRIVATE','leisure.park',['access'=>'private']),gnf_place('UNSAFE','leisure.park',['unsafe'=>true]),gnf_place('CLOSED','leisure.park',['closed'=>true]),gnf_place('COST','entertainment.museum'),gnf_place('XSS','education.library',['name'=>'<img src=x onerror=alert(1)>Fixture Library']),gnf_place('MALFORMED','leisure.park',['name'=>['array']]),'invalid'];
  $gnf_mock=gnf_http(['features'=>$features]);for($i=0;$i<5;$i++)$p=P::places(59.91234,10.71345,15,'auto');
  gnf_assert(count($gnf_calls)===1 && count($p['items'])===3,'D6/D8 normalized, deduped, filtered and cached POIs');
  gnf_assert($p['items'][1]['possible_cost'] && !str_contains($p['items'][2]['name'],'<'),'C5/D12 costs cautious; injected markup removed');
  $encoded=wp_json_encode($p);gnf_assert(!str_contains($encoded,$token) && !str_contains(wp_json_encode(P::diagnostics()),$token),'A5 no key in responses or diagnostics');
  parse_str(wp_parse_url($gnf_calls[0]['url'],PHP_URL_QUERY),$query);gnf_assert($query['limit']==='20' && str_contains($query['filter'],'circle:10.71,59.91,1500'),'D6 bounded Geoapify request');
  foreach([401,403,429,500,'timeout','invalid','oversized'] as $failure){gnf_reset();$gnf_mock=$failure==='timeout'?new WP_Error('http_request_failed','fixture'):gnf_http([],is_int($failure)?$failure:200);if($failure==='oversized')$gnf_mock['body']=str_repeat('x',196609);$p=P::places(59.91,10.71,15,'auto');P::places(59.91,10.71,15,'auto');gnf_assert(!$p['items'] && count($gnf_calls)===1,'D7 Geoapify bounded fallback '.$failure);}
  gnf_reset();$gnf_mock=gnf_http(['features'=>[]]);gnf_assert(P::places(59.91,10.71,30,'rural')['items']===[],'C3 empty rural result remains empty');parse_str(wp_parse_url($gnf_calls[0]['url'],PHP_URL_QUERY),$query);gnf_assert(str_ends_with($query['filter'],',10000'),'C3 capped 10 km search, no invented time');
  gnf_reset();update_option('gnf_settings',['weather'=>true,'places'=>true,'hour_cap'=>1,'day_cap'=>2],false);P::places(59.9,10.7,2,'auto');$p=P::places(59.8,10.6,2,'auto');gnf_assert($p['status']==='quota'&&count($gnf_calls)===1,'D7 hard hourly quota');
  $usage=get_option('gnf_usage_geoapify');$usage['hour']='old';$usage['daily']=2;update_option('gnf_usage_geoapify',$usage,false);gnf_assert(P::places(59.7,10.5,2,'auto')['status']==='quota' && count($gnf_calls)===1,'D7 hard daily quota');
  gnf_reset();update_option('gnf_settings',['weather'=>true,'places'=>true,'hour_cap'=>12,'day_cap'=>75],false);$gnf_mock=gnf_http(['features'=>[['properties'=>['city'=>'Fixture Town','country'=>'Fixture Country','lat'=>59.91234,'lon'=>10.71345,'housenumber'=>'9','street'=>'Not retained']]]]);$search=P::search('Fixture Town');P::search('Fixture Town');gnf_assert($search['items'][0]['lat']===59.91 && !str_contains(wp_json_encode($search),'Not retained') && count($gnf_calls)===1,'D9 explicit manual town search is coarse and cached');
  gnf_reset();foreach([['lat'=>'https://evil.invalid','lon'=>1],['lat'=>91,'lon'=>1],['lat'=>1,'lon'=>1,'url'=>'https://evil.invalid'],['lat'=>1,'lon'=>1,'time'=>99],['lat'=>[1],'lon'=>1]] as $bad){$r=$call('context',$bad);gnf_assert($r->get_status()===400 && !$gnf_calls,'E5 reject malformed or SSRF parameters');}
  $r=$call('search',['query'=>'<script>alert(1)</script>']);gnf_assert($r->get_status()===400&&!$gnf_calls,'E5 reject town input injection');
  $r=new WP_REST_Request('POST','/gymnotfound/v1/context');$r->set_body(str_repeat('x',2049));gnf_assert(rest_do_request($r)->get_status()===413,'D12 reject oversized public request');
  gnf_reset();$success=0;for($i=0;$i<31;$i++){$r=$call('context',[]);if($r->get_status()===200)$success++;}gnf_assert($success===30 && $r->get_status()===429 && !$gnf_calls,'D12 public rate limit: 30/min, no provider calls');
  wp_set_current_user(0);$r=new WP_REST_Request('GET','/gymnotfound/v1/diagnostics');gnf_assert(rest_do_request($r)->get_status()===403,'E4 anonymous diagnostics denied');
  $admin=get_user_by('login','gnf_test_admin');wp_set_current_user($admin->ID);gnf_assert(rest_do_request($r)->get_status()===403,'E4 admin without nonce denied');$r->set_header('X-WP-Nonce',wp_create_nonce('wp_rest'));gnf_assert(rest_do_request($r)->get_status()===200,'E4 admin with capability and nonce allowed');
  $exercise=wp_insert_post(['post_type'=>'gnf_activity','post_status'=>'publish','post_title'=>'TEST REVIEW CARD','post_content'=>'Fixture instruction']);$c=json_decode(file_get_contents(dirname(GNF_FILE).'/content/activities.json'),true)[0];$c['instructions']=true;update_post_meta($exercise,'_gnf_card',$c);
  gnf_assert(!in_array('custom-'.$exercise,array_column(C::all(),'id'),true),'E3 unreviewed exercise hidden');
  $c['instructions']=false;update_post_meta($exercise,'_gnf_card',$c);wp_update_post(['ID'=>$exercise,'post_content'=>'Do ten squats and repeat the repetitions.']);
  gnf_assert(!in_array('custom-'.$exercise,array_column(C::all(),'id'),true),'E3 recognised exercise instructions cannot bypass the gate with an unchecked flag');
  $c['instructions']=true;update_post_meta($exercise,'_gnf_card',$c);
  $review=['approved'=>true,'by'=>$admin->ID,'reviewer'=>'Fixture qualified reviewer','date'=>gmdate('Y-m-d'),'sources'=>'https://example.invalid/test-review','safety'=>'Fixture safety','alternative'=>'Fixture alternative','hash'=>C::hash($exercise)];update_post_meta($exercise,'_gnf_review',$review);gnf_assert(C::reviewed($exercise),'E3 exact reviewed version accepted');
  foreach(['date'=>'2099-01-01','sources'=>'http://example.invalid','safety'=>'','hash'=>'wrong'] as $field=>$value){update_post_meta($exercise,'_gnf_review',array_merge($review,[$field=>$value]));gnf_assert(!C::reviewed($exercise),'E3 reject invalid approval '.$field);}
  update_post_meta($exercise,'_gnf_review',$review);
  wp_update_post(['ID'=>$exercise,'post_content'=>'Edited version']);gnf_assert(!C::reviewed($exercise) && !in_array('custom-'.$exercise,array_column(C::all(),'id'),true),'E3 any content change invalidates approval');wp_delete_post($exercise,true);
  gnf_assert($gnf_assertions>=50,'Test counter verifies execution');echo 'TOTAL '.$gnf_assertions." assertions\n";
} finally {
  gnf_reset();update_option('gnf_settings',$saved['settings'],false);if($saved['key'])update_option('gnf_geoapify_key',$saved['key'],false);else delete_option('gnf_geoapify_key');delete_option('gnf_status_met');delete_option('gnf_status_geoapify');
}

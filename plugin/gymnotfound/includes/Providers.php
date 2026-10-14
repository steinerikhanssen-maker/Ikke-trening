<?php
namespace GymNotFound;
if (!defined('ABSPATH')) exit;
/** Fixed external endpoints. No client URLs, redirects, raw error bodies or personal logs. */
final class Providers {
    const MET = 'https://api.met.no/weatherapi/locationforecast/2.0/compact';
    const PLACES = 'https://api.geoapify.com/v2/places';
    const SEARCH = 'https://api.geoapify.com/v1/geocode/search';
    const CATEGORIES = 'leisure.park,tourism.attraction.viewpoint,entertainment.museum,education.library,catering.cafe';
    public static function now(): int { return (int)apply_filters('gymnotfound_now',time()); }
    public static function settings(): array {
        $saved=get_option('gnf_settings',[]);
        return array_merge(['weather'=>true,'places'=>false,'hour_cap'=>12,'day_cap'=>75],is_array($saved)?$saved:[]);
    }
    public static function key(): string {
        $record=get_option('gnf_geoapify_key','');
        if (!$record) return '';
        if (!function_exists('openssl_decrypt') || !is_string($record)) return '';
        $blob=base64_decode($record,true);
        if ($blob===false || strlen($blob)<29) return '';
        $plain=openssl_decrypt(substr($blob,28),'aes-256-gcm',hash('sha256',wp_salt('auth'),true),OPENSSL_RAW_DATA,substr($blob,0,12),substr($blob,12,16));
        return is_string($plain) ? $plain : '';
    }
    public static function set_key(string $key): bool {
        if (!$key) { delete_option('gnf_geoapify_key'); return true; }
        if (!function_exists('openssl_encrypt')) return false;
        if (!preg_match('/^[A-Za-z0-9_-]{8,128}$/',$key)) return false;
        $iv=random_bytes(12);$tag='';
        $cipher=openssl_encrypt($key,'aes-256-gcm',hash('sha256',wp_salt('auth'),true),OPENSSL_RAW_DATA,$iv,$tag);
        if ($cipher===false) return false;
        update_option('gnf_geoapify_key',base64_encode($iv.$tag.$cipher),false);
        return true;
    }
    /** Serialise quota checks across web workers without retaining IPs or locations. */
    public static function lock(string $name, callable $work, int $wait=2) {
        global $wpdb;
        $name='gnf_'.substr(hash('sha256',DB_NAME.$wpdb->prefix.$name),0,48);
        // phpcs:ignore WordPress.DB.DirectDatabaseQuery.DirectQuery, WordPress.DB.DirectDatabaseQuery.NoCaching -- Database advisory mutex must execute on each acquisition across PHP workers.
        if ((int)$wpdb->get_var($wpdb->prepare('SELECT GET_LOCK(%s,%d)',$name,$wait))!==1) return null;
        try { return $work(); }
        finally {
            // phpcs:ignore WordPress.DB.DirectDatabaseQuery.DirectQuery, WordPress.DB.DirectDatabaseQuery.NoCaching -- Release the acquired database mutex even on failure; never cache a lock operation.
            $wpdb->get_var($wpdb->prepare('SELECT RELEASE_LOCK(%s)',$name));
        }
    }
    public static function rate(): bool {
        $ip=filter_var(sanitize_text_field(wp_unslash($_SERVER['REMOTE_ADDR'] ?? '')),FILTER_VALIDATE_IP) ?: 'unknown'; // Never logged or persisted verbatim.
        $id=hash_hmac('sha256',$ip,wp_salt('nonce'));
        return self::lock('rate',function()use($id){
            $now=self::now();$key='gnf_rate_'.substr($id,0,32);$entry=get_transient($key);
            if (!is_array($entry) || $entry['until']<=$now) $entry=['until'=>$now+60,'count'=>0];
            if ($entry['count']>=30) return false;
            $entry['count']++;set_transient($key,$entry,90);
            $global=get_transient('gnf_global_rate');
            if (!is_array($global) || $global['until']<=$now) $global=['until'=>$now+60,'count'=>0];
            if ($global['count']>=120) return false;
            $global['count']++;set_transient('gnf_global_rate',$global,90);
            return true;
        }) === true;
    }
    public static function reserve(string $provider): bool {
        return self::lock('quota',function()use($provider){
            $now=self::now();$day=gmdate('Y-m-d',$now);$hour=gmdate('Y-m-d H',$now);
            $key='gnf_usage_'.$provider;$usage=get_option($key,[]);
            if (!is_array($usage) || ($usage['day'] ?? '')!==$day) $usage=['day'=>$day,'hour'=>$hour,'daily'=>0,'hourly'=>0];
            if ($usage['hour']!==$hour) { $usage['hour']=$hour;$usage['hourly']=0; }
            $s=self::settings();$maxDay=$provider==='geoapify' ? max(0,min(100,(int)$s['day_cap'])) : 300;
            $maxHour=$provider==='geoapify' ? max(0,min(30,(int)$s['hour_cap'])) : 60;
            if ($usage['daily']>=$maxDay || $usage['hourly']>=$maxHour) return false;
            $usage['daily']++;$usage['hourly']++;
            update_option($key,$usage,false);
            return true;
        }) === true;
    }
    private static function request(string $base, array $query, array $headers=[]): array|\WP_Error {
        if (!in_array($base,[self::MET,self::PLACES,self::SEARCH],true)) return new \WP_Error('gnf_host','Unsupported host');
        // Strict fixed HTTPS endpoint allowlist above + no redirects prevent SSRF.
        // wp_remote_get also works through a forward proxy without local origin DNS.
        $args=['timeout'=>5,'redirection'=>0,'limit_response_size'=>196608,'sslverify'=>true,'headers'=>array_merge(['Accept'=>'application/json','User-Agent'=>'GymNotFound/'.GNF_VERSION.' (+https://github.com/steinerikhanssen-maker/Ikke-trening)'],$headers)];
        if (defined('GNF_CA_BUNDLE') && is_readable(GNF_CA_BUNDLE)) $args['sslcertificates']=GNF_CA_BUNDLE;
        $result=wp_remote_get(add_query_arg($query,$base),$args);
        return is_array($result) || is_wp_error($result) ? $result : new \WP_Error('gnf_response','Invalid source response');
    }
    private static function failure(string $provider, string $key, int $code=0): array {
        $delay=$code===429 ? 900 : ($code===401 || $code===403 ? 3600 : 120);
        set_transient($key.'_backoff',true,$delay);
        update_option('gnf_status_'.$provider,['state'=>$code===429?'rate_limited':'unavailable','checked_at'=>gmdate('c',self::now()),'http_status'=>$code],false);
        return ['status'=>$code===429?'rate_limited':'unavailable'];
    }
    private static function ttl($header, int $fallback): int {
        $time=is_string($header) ? strtotime($header) : false;
        return $time ? max(0,min(86400,$time-self::now())) : $fallback;
    }
    public static function weather(float $lat, float $lon): array {
        if (!self::settings()['weather']) return ['status'=>'disabled'];
        $lat=round($lat,2);$lon=round($lon,2);$key='gnf_met_'.md5($lat.':'.$lon);
        $cached=get_transient($key);
        if (is_array($cached) && $cached['expires']>self::now()) return self::forecast($cached['rows'],$cached['fetched_at']);
        if (get_transient($key.'_backoff')) return ['status'=>'unavailable'];
        return self::lock($key,function()use($lat,$lon,$key){
            $cached=get_transient($key);$now=self::now();
            if (is_array($cached) && $cached['expires']>$now) return self::forecast($cached['rows'],$cached['fetched_at']);
            if (!self::reserve('met')) return ['status'=>'quota'];
            $headers=[];
            if (!empty($cached['last_modified'])) $headers['If-Modified-Since']=$cached['last_modified'];
            $response=self::request(self::MET,['lat'=>$lat,'lon'=>$lon],$headers);
            if (is_wp_error($response)) return self::failure('met',$key);
            $status=wp_remote_retrieve_response_code($response);
            if ($status===304 && is_array($cached)) {
                $cached['expires']=$now+self::ttl(wp_remote_retrieve_header($response,'expires'),1800);
                set_transient($key,$cached,2*DAY_IN_SECONDS);
                update_option('gnf_status_met',['state'=>'ok','checked_at'=>gmdate('c',$now),'http_status'=>304,'cache_expires_at'=>gmdate('c',$cached['expires'])],false);
                return self::forecast($cached['rows'],$cached['fetched_at']);
            }
            if ($status!==200) return self::failure('met',$key,$status);
            $body=wp_remote_retrieve_body($response);
            if (strlen($body)>=196608) return self::failure('met',$key);
            $json=json_decode($body,true);$rows=$json['properties']['timeseries'] ?? null;
            if (!is_array($rows) || !$rows) return self::failure('met',$key);
            $safe=[];
            foreach (array_slice($rows,0,96) as $row) {
                if (!is_array($row) || !is_array($row['data'] ?? null)) continue;
                $details=$row['data']['instant']['details'] ?? []; $next=$row['data']['next_1_hours']['details'] ?? $row['data']['next_6_hours']['details'] ?? [];
                $temperature=$details['air_temperature'] ?? null;$wind=$details['wind_speed'] ?? null;$rain=$next['precipitation_amount'] ?? null;
                if (!isset($row['time']) || !is_string($row['time']) || !strtotime($row['time']) || !is_numeric($temperature) || !is_numeric($wind) || !is_numeric($rain)) continue;
                if ($temperature < -100 || $temperature > 65 || $wind < 0 || $wind > 150 || $rain < 0 || $rain > 1000) continue;
                $safe[]=['forecast_at'=>$row['time'],'temperature'=>(float)$temperature,'wind'=>(float)$wind,'precipitation'=>(float)$rain];
            }
            if (!$safe) return self::failure('met',$key);
            $cache=['rows'=>$safe,'expires'=>$now+self::ttl(wp_remote_retrieve_header($response,'expires'),1800),'last_modified'=>sanitize_text_field(wp_remote_retrieve_header($response,'last-modified')),'fetched_at'=>gmdate('c',$now)];
            set_transient($key,$cache,2*DAY_IN_SECONDS);
            update_option('gnf_status_met',['state'=>'ok','checked_at'=>gmdate('c',$now),'http_status'=>200,'cache_expires_at'=>gmdate('c',$cache['expires'])],false);
            return self::forecast($safe,$cache['fetched_at']);
        },0) ?? ['status'=>'busy'];
    }
    public static function forecast(array $rows, string $fetched): array {
        $now=self::now();$nearest=null;$distance=PHP_INT_MAX;
        foreach ($rows as $row) {
            $delta=abs(strtotime($row['forecast_at'])-$now);
            if ($delta<$distance) { $nearest=$row;$distance=$delta; }
        }
        if (!$nearest || $distance>90*MINUTE_IN_SECONDS) return ['status'=>'stale'];
        return array_merge($nearest,['status'=>'ok','fetched_at'=>$fetched,'provider'=>'met','source_url'=>'https://api.met.no/doc/locationforecast/HowTO']);
    }
    public static function places(float $lat, float $lon, int $time, string $environment): array {
        $s=self::settings();$token=self::key();
        if (!$s['places'] || !$token) return ['status'=>'not_configured','items'=>[]];
        $lat=round($lat,2);$lon=round($lon,2);
        $radius=$time===30 ? ($environment==='rural' ? 10000 : 5000) : ($environment==='rural' ? 3000 : 1500);
        $key='gnf_poi_'.md5($lat.':'.$lon.':'.$radius);
        $cached=get_transient($key);
        if (is_array($cached)) return $cached;
        if (get_transient($key.'_backoff')) return ['status'=>'unavailable','items'=>[]];
        return self::lock($key,function()use($lat,$lon,$radius,$key,$token){
            $cached=get_transient($key);if (is_array($cached)) return $cached;
            if (!self::reserve('geoapify')) return ['status'=>'quota','items'=>[]];
            $response=self::request(self::PLACES,['categories'=>self::CATEGORIES,'filter'=>'circle:'.$lon.','.$lat.','.$radius,'limit'=>20,'apiKey'=>$token]);
            if (is_wp_error($response)) return array_merge(self::failure('geoapify',$key),['items'=>[]]);
            $status=wp_remote_retrieve_response_code($response);
            if ($status!==200) return array_merge(self::failure('geoapify',$key,$status),['items'=>[]]);
            $body=wp_remote_retrieve_body($response);$json=json_decode($body,true);
            if (strlen($body)>=196608 || !is_array($json['features'] ?? null)) return array_merge(self::failure('geoapify',$key),['items'=>[]]);
            $result=['status'=>'ok','items'=>self::normalize_places(array_slice($json['features'],0,20)),'retrieved_at'=>gmdate('c',self::now())];
            set_transient($key,$result,DAY_IN_SECONDS);
            update_option('gnf_status_geoapify',['state'=>'ok','checked_at'=>gmdate('c',self::now()),'http_status'=>200,'cache_expires_at'=>gmdate('c',self::now()+DAY_IN_SECONDS)],false);
            return $result;
        },0) ?? ['status'=>'busy','items'=>[]];
    }
    public static function normalize_places(array $features): array {
        $out=[];$seen=[];
        $categories=['leisure.park'=>'park','education.library'=>'library','service.library'=>'library','entertainment.museum'=>'museum','catering.cafe'=>'cafe','tourism.attraction.viewpoint'=>'viewpoint'];
        foreach ($features as $feature) {
            if (!is_array($feature) || !is_array($feature['properties'] ?? null)) continue;
            $p=$feature['properties'] ?? [];$coords=$feature['geometry']['coordinates'] ?? [];
            $lat=$p['lat'] ?? ($coords[1] ?? null);$lon=$p['lon'] ?? ($coords[0] ?? null);
            if (!is_numeric($lat) || !is_numeric($lon) || abs((float)$lat)>90 || abs((float)$lon)>180) continue;
            $cats=$p['categories'] ?? [];if (!is_array($cats)) continue;$kind=null;
            foreach ($categories as $category=>$name) if (in_array($category,$cats,true)) { $kind=$name;break; }
            if (!$kind || array_intersect($cats,['building.private','natural.cliff','access.private','dangerous','restricted'])) continue;
            $raw=$p['datasource']['raw'] ?? [];if (!is_array($raw)) $raw=[];
            $access=$p['access'] ?? ($raw['access'] ?? 'unknown');
            if (!is_string($access) || in_array($access,['private','no','restricted','customers'],true) || !empty($p['private']) || !empty($p['unsafe']) || !empty($p['closed'])) continue;
            if (!is_string($p['place_id'] ?? null) || !is_string($p['name'] ?? null)) continue;
            $id=sanitize_text_field((string)($p['place_id'] ?? ''));$name=mb_substr(sanitize_text_field((string)($p['name'] ?? '')),0,120);
            if (!$id || !$name) continue;
            $signature=mb_strtolower($name).':'.round((float)$lat,5).':'.round((float)$lon,5);
            if (isset($seen[$id]) || isset($seen[$signature])) continue;$seen[$id]=true;$seen[$signature]=true;
            $fee=$p['fee'] ?? ($raw['fee'] ?? 'unknown');
            $possible=in_array($kind,['museum','cafe'],true) || ($fee!==false && !in_array($fee,['no','0',0,'unknown'],true));
            $out[]=['id'=>mb_substr($id,0,160),'name'=>$name,'category'=>$kind,'lat'=>(float)$lat,'lon'=>(float)$lon,'provider'=>'geoapify','possible_cost'=>$possible,'retrieved_at'=>gmdate('c',self::now()),'access'=>'unverified'];
        }
        return $out;
    }
    public static function search(string $query): array {
        if (!self::settings()['places'] || !self::key()) return ['status'=>'not_configured','items'=>[]];
        $key='gnf_search_'.hash_hmac('sha256',mb_strtolower($query),wp_salt('auth'));
        $cached=get_transient($key);if (is_array($cached)) return $cached;
        if (get_transient($key.'_backoff')) return ['status'=>'unavailable','items'=>[]];
        return self::lock($key,function()use($query,$key){
            $cached=get_transient($key);if (is_array($cached)) return $cached;
            if (!self::reserve('geoapify')) return ['status'=>'quota','items'=>[]];
            $response=self::request(self::SEARCH,['text'=>$query,'type'=>'city','limit'=>5,'apiKey'=>self::key()]);
            if (is_wp_error($response)) return array_merge(self::failure('geoapify',$key),['items'=>[]]);
            $status=wp_remote_retrieve_response_code($response);
            if ($status!==200) return array_merge(self::failure('geoapify',$key,$status),['items'=>[]]);
            $body=wp_remote_retrieve_body($response);$json=json_decode($body,true);$out=[];
            if (strlen($body)>=196608 || !is_array($json['features'] ?? null)) return array_merge(self::failure('geoapify',$key),['items'=>[]]);
            foreach (array_slice($json['features'],0,5) as $feature) {
                if (!is_array($feature) || !is_array($feature['properties'] ?? null)) continue;
                $p=$feature['properties'] ?? [];$coords=$feature['geometry']['coordinates'] ?? [];
                $lat=$p['lat'] ?? ($coords[1] ?? null);$lon=$p['lon'] ?? ($coords[0] ?? null);
                if (!is_numeric($lat) || !is_numeric($lon) || abs((float)$lat)>90 || abs((float)$lon)>180) continue;
                $name=$p['city'] ?? $p['county'] ?? $p['state'] ?? $p['country'] ?? '';
                if (!is_string($name) || !is_string($p['country'] ?? '')) continue;
                $name=sanitize_text_field($name);
                if (!$name) continue;
                $country=sanitize_text_field((string)($p['country'] ?? ''));
                $out[]=['label'=>mb_substr($name.($country && $country!==$name ? ', '.$country : ''),0,100),'lat'=>round((float)$lat,2),'lon'=>round((float)$lon,2)];
            }
            $result=['status'=>'ok','items'=>$out];set_transient($key,$result,DAY_IN_SECONDS);return $result;
        },0) ?? ['status'=>'busy','items'=>[]];
    }
    public static function diagnostics(): array {
        $usage=['met'=>get_option('gnf_usage_met',[]),'geoapify'=>get_option('gnf_usage_geoapify',[])];
        $met=get_option('gnf_status_met',['state'=>'not_tested']);$geo=get_option('gnf_status_geoapify',['state'=>'not_tested']);
        foreach (['met'=>&$met,'geoapify'=>&$geo] as &$status) $status['last_cache_unexpired']=isset($status['cache_expires_at']) && strtotime($status['cache_expires_at'])>self::now();
        unset($status);
        return ['key_configured'=>(bool)self::key(),'met'=>$met,'geoapify'=>$geo,'usage'=>$usage,'geoapify_credit_upper_estimate'=>20*(int)($usage['geoapify']['daily'] ?? 0),'credit_estimate_note'=>'Conservative upper estimate for the displayed day: 20 credits per Geoapify request. No billing integration.'];
    }
}

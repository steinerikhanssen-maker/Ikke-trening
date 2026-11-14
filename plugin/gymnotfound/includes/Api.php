<?php
namespace GymNotFound;
if (!defined('ABSPATH')) exit;
/** Only coarse, explicitly chosen locations enter the public API. No history endpoint. */
final class Api {
    public static function register(): void {
        register_rest_route('gymnotfound/v1','/context',['methods'=>'POST','callback'=>[self::class,'context'],'permission_callback'=>[self::class,'public_permission']]);
        register_rest_route('gymnotfound/v1','/search',['methods'=>'POST','callback'=>[self::class,'search'],'permission_callback'=>[self::class,'public_permission']]);
        register_rest_route('gymnotfound/v1','/diagnostics',['methods'=>'GET','callback'=>fn()=>rest_ensure_response(Providers::diagnostics()),'permission_callback'=>[self::class,'admin_permission']]);
    }
    public static function public_permission(\WP_REST_Request $request): bool|\WP_Error {
        if (strlen($request->get_body())>2048) return new \WP_Error('gnf_size','Request too large',['status'=>413]);
        return Providers::rate() ? true : new \WP_Error('gnf_rate','Please try again later',['status'=>429]);
    }
    public static function admin_permission(\WP_REST_Request $request): bool|\WP_Error {
        if (!current_user_can('manage_options') || !wp_verify_nonce($request->get_header('X-WP-Nonce'),'wp_rest')) return new \WP_Error('gnf_forbidden','Administrator permission and nonce required',['status'=>403]);
        return true;
    }
    private static function payload(\WP_REST_Request $request, array $allowed): array|\WP_Error {
        $data=$request->get_json_params();
        if (!is_array($data) || array_diff(array_keys($data),$allowed)) return new \WP_Error('gnf_input','Invalid parameters',['status'=>400]);
        return $data;
    }
    public static function context(\WP_REST_Request $request): array|\WP_Error {
        $data=self::payload($request,['lat','lon','time','environment']);
        if (is_wp_error($data)) return $data;
        if (!isset($data['lat'],$data['lon'])) return ['weather'=>['status'=>'no_location'],'places'=>['status'=>'no_location','items'=>[]]];
        foreach (['lat'=>90,'lon'=>180] as $key=>$limit) {
            if ((!is_int($data[$key]) && !is_float($data[$key])) || !is_finite((float)$data[$key]) || abs($data[$key])>$limit) return new \WP_Error('gnf_coordinates','Invalid coordinates',['status'=>400]);
        }
        $time=$data['time'] ?? 2;$environment=$data['environment'] ?? 'auto';
        if (!in_array($time,[2,15,30],true) || !in_array($environment,['auto','urban','suburban','rural','home','anywhere'],true)) return new \WP_Error('gnf_choices','Invalid preferences',['status'=>400]);
        $lat=round($data['lat'],2);$lon=round($data['lon'],2);
        return ['weather'=>Providers::weather($lat,$lon),'places'=>$environment==='home' ? ['status'=>'not_needed','items'=>[]] : Providers::places($lat,$lon,$time,$environment)];
    }
    public static function search(\WP_REST_Request $request): array|\WP_Error {
        $data=self::payload($request,['query']);
        if (is_wp_error($data)) return $data;
        $query=$data['query'] ?? null;
        if (!is_string($query) || mb_strlen($query)<2 || mb_strlen($query)>80 || !preg_match('/^[\p{L}\p{M}\p{N} .,\x{0027}’\-]+$/u',$query)) return new \WP_Error('gnf_query','Enter a town or area name',['status'=>400]);
        return Providers::search(trim($query));
    }
}

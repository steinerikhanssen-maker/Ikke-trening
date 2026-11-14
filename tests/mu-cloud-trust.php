<?php
/** Local cloud test infrastructure only. Never shipped in the plugin ZIP. */
if (!defined('ABSPATH')) exit;
add_filter('http_request_args',function($args,$url){
    $host=wp_parse_url($url,PHP_URL_HOST);
    if (defined('GNF_CA_BUNDLE') && is_readable(GNF_CA_BUNDLE) && wp_parse_url($url,PHP_URL_SCHEME)==='https' && in_array($host,['api.wordpress.org','downloads.wordpress.org','wordpress.org','api.met.no','api.geoapify.com'],true)) $args['sslcertificates']=GNF_CA_BUNDLE;
    return $args; // TLS verification and the managed forward proxy remain enabled.
},10,2);

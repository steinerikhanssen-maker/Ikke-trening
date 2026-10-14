<?php
namespace GymNotFound;
if (!defined('ABSPATH')) exit;
final class Plugin {
    public static function activate(): void {
        if (version_compare(PHP_VERSION,'8.2','<') || version_compare(get_bloginfo('version'),'6.7','<')) wp_die(esc_html__('GymNotFound requires WordPress 6.7 and PHP 8.2 or newer.','gymnotfound'));
        Content::register();Content::seed();
        // Deliberately no page creation, account, cron job or external request.
    }
    public static function boot(): void {
        add_action('init',[Content::class,'register']);
        add_action('rest_api_init',[Api::class,'register']);
        add_action('admin_menu',[self::class,'menu']);
        add_action('admin_post_gnf_settings',[self::class,'save']);
        add_shortcode('gymnotfound_app',[self::class,'shortcode']);
        add_filter('template_include',[self::class,'template'],99);
        add_action('wp_enqueue_scripts',[self::class,'page_assets']);
    }
    public static function chosen(): bool {
        $id=(int)get_option('gnf_page_id',0);
        return $id>0 && is_page($id);
    }
    public static function template(string $path): string {
        return self::chosen() ? dirname(GNF_FILE).'/templates/app.php' : $path;
    }
    public static function page_assets(): void {
        if (self::chosen() || (is_singular() && has_shortcode((string)get_post_field('post_content',get_queried_object_id()),'gymnotfound_app'))) self::assets();
        if (self::chosen()) {
            remove_action('wp_head','print_emoji_detection_script',7);
            remove_action('wp_enqueue_scripts','wp_enqueue_emoji_styles');
            remove_action('wp_print_styles','print_emoji_styles');
        }
    }
    private static function assets(): void {
        $url=plugin_dir_url(GNF_FILE).'assets/';
        wp_enqueue_style('gymnotfound',$url.'app.css',[],GNF_VERSION);
        foreach (['catalog','locales','engine','storage'] as $name) wp_enqueue_script('gnf-'.$name,$url.$name.'.js',[],GNF_VERSION,true);
        wp_enqueue_script('gymnotfound',$url.'app.js',['gnf-catalog','gnf-locales','gnf-engine','gnf-storage'],GNF_VERSION,true);
        $s=Providers::settings();
        $config=['endpoint'=>rest_url('gymnotfound/v1/'),'version'=>GNF_VERSION,'language'=>str_starts_with(get_locale(),'nb') || str_starts_with(get_locale(),'nn') ? 'nb' : 'en','weatherEnabled'=>(bool)$s['weather'],'placesEnabled'=>(bool)($s['places'] && Providers::key()),'nim'=>$url.'nim.svg','mark'=>$url.'mark.svg','catalog'=>Content::all()];
        wp_add_inline_script('gymnotfound','window.GNF_CONFIG='.wp_json_encode($config,JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT).';','before');
    }
    public static function shortcode(): string {
        self::assets();
        return '<div id="gymnotfound" class="gnf"><noscript>'.esc_html__('Enable JavaScript to choose an activity. No account or location required.','gymnotfound').'</noscript></div>';
    }
    public static function menu(): void {
        add_menu_page('GymNotFound','GymNotFound','manage_options','gymnotfound',[self::class,'admin'],'dashicons-palmtree',57);
        add_submenu_page('gymnotfound','Activities','Activities','manage_options','edit.php?post_type=gnf_activity');
    }
    public static function save(): void {
        if (!current_user_can('manage_options')) wp_die(esc_html__('Administrator permission required.','gymnotfound'),'',403);
        check_admin_referer('gnf_settings');
        $action=sanitize_key(wp_unslash($_POST['gnf_action'] ?? 'save'));
        $status='saved';
        if ($action==='create') {
            $existing=(int)get_option('gnf_page_id',0);
            if (!$existing || !get_post($existing) || get_post_status($existing)==='trash') {
                $id=wp_insert_post(['post_type'=>'page','post_status'=>'draft','post_title'=>'GymNotFound','post_content'=>'[gymnotfound_app]'],true);
                if (is_wp_error($id)) $status='failed'; else update_option('gnf_page_id',$id,false);
            }
            $status=$status==='failed' ? $status : 'created';
        } elseif ($action==='test') {
            $lat=filter_var(wp_unslash($_POST['gnf_test_lat'] ?? ''),FILTER_VALIDATE_FLOAT);
            $lon=filter_var(wp_unslash($_POST['gnf_test_lon'] ?? ''),FILTER_VALIDATE_FLOAT);
            if ($lat===false || $lon===false || abs($lat)>90 || abs($lon)>180) $status='invalid';
            else {
                $result=['weather'=>Providers::weather(round($lat,2),round($lon,2))['status'],'places'=>Providers::places(round($lat,2),round($lon,2),2,'auto')['status']];
                update_option('gnf_test_result',$result,false);$status='tested';
            }
        } else {
            $s=['weather'=>!empty($_POST['gnf_weather']),'places'=>!empty($_POST['gnf_places']),'hour_cap'=>min(30,absint(wp_unslash($_POST['gnf_hour_cap'] ?? 12))),'day_cap'=>min(100,absint(wp_unslash($_POST['gnf_day_cap'] ?? 75)))];
            update_option('gnf_settings',$s,false);
            $id=absint($_POST['gnf_page_id'] ?? 0);
            if (!$id || (get_post_type($id)==='page' && get_post_status($id)!=='trash')) update_option('gnf_page_id',$id,false);
            $key=sanitize_text_field(wp_unslash($_POST['gnf_key'] ?? ''));
            if (!empty($_POST['gnf_remove_key'])) Providers::set_key('');
            elseif ($key && !Providers::set_key($key)) $status='invalid';
        }
        wp_safe_redirect(add_query_arg(['page'=>'gymnotfound','gnf_status'=>$status,'gnf_notice_nonce'=>wp_create_nonce('gnf_notice')],admin_url('admin.php')));exit;
    }
    public static function admin(): void {
        if (!current_user_can('manage_options')) return;
        $s=Providers::settings();$id=(int)get_option('gnf_page_id',0);$diagnostics=Providers::diagnostics();
        echo '<div class="wrap"><h1>GymNotFound '.esc_html(GNF_VERSION).'</h1>';
        $status=!empty($_GET['gnf_notice_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_GET['gnf_notice_nonce'])),'gnf_notice') ? sanitize_key(wp_unslash($_GET['gnf_status'] ?? '')) : '';
        $messages=['saved'=>'Settings saved.','created'=>'Draft app page ready. Preview it, then publish it when you choose.','tested'=>'Source check complete. Results below; unavailable sources keep generic activities working.','invalid'=>'Invalid key or coordinates. Check your entry.','failed'=>'Could not create the page.'];
        if (isset($messages[$status])) echo '<div class="notice notice-info"><p>'.esc_html($messages[$status]).'</p></div>';
        echo '<p>'.esc_html__('One recommendation flow, local guest history, English and Norwegian. No visitor accounts.','gymnotfound').'</p>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'"><input type="hidden" name="action" value="gnf_settings">';wp_nonce_field('gnf_settings');
        echo '<h2>'.esc_html__('App page','gymnotfound').'</h2><p><label>'.esc_html__('Use the independent app shell on this page:','gymnotfound').' ';
        echo '<select name="gnf_page_id"><option value="0">— No selected page —</option>';
        foreach (get_posts(['post_type'=>'page','post_status'=>['publish','draft','private'],'numberposts'=>-1]) as $page) echo '<option value="'.esc_attr($page->ID).'" '.selected($id,$page->ID,false).'>'.esc_html($page->post_title).'</option>';
        echo '</select></label></p>';
        if ($id && get_post($id)) echo '<p><a class="button" href="'.esc_url(get_preview_post_link($id)).'">'.esc_html__('Preview app','gymnotfound').'</a> <a href="'.esc_url(get_edit_post_link($id)).'">'.esc_html__('Edit / publish page','gymnotfound').'</a></p>';
        echo '<p><button class="button" name="gnf_action" value="create">'.esc_html__('Create draft app page','gymnotfound').'</button></p><p>'.esc_html__('For theme integration, add [gymnotfound_app] to another page. Activation never creates a page.','gymnotfound').'</p>';
        echo '<h2>'.esc_html__('Optional sources','gymnotfound').'</h2>';
        foreach (['weather'=>'Enable MET Norway weather (only for a chosen location)','places'=>'Enable Geoapify places (optional free-plan key required)'] as $key=>$label) echo '<p><label><input type="checkbox" name="'.esc_attr('gnf_'.$key).'" value="1" '.checked($s[$key],true,false).'> '.esc_html($label).'</label></p>';
        echo '<p>'.esc_html($diagnostics['key_configured'] ? 'Geoapify key configured. Its value is never displayed.' : 'No Geoapify key. Generic activities work without it.').'</p><p><label>'.esc_html__('Replace Geoapify key','gymnotfound').' <input type="password" name="gnf_key" autocomplete="new-password" value="" maxlength="128"></label></p><p><label><input type="checkbox" name="gnf_remove_key" value="1"> '.esc_html__('Remove stored key','gymnotfound').'</label></p>';
        foreach (['hour_cap'=>['hour',30],'day_cap'=>['day',100]] as $key=>$spec) echo '<p><label>'.esc_html('Maximum Geoapify requests per '.$spec[0]).' <input type="number" name="'.esc_attr('gnf_'.$key).'" min="0" max="'.esc_attr($spec[1]).'" value="'.esc_attr($s[$key]).'"></label></p>';
        echo '<p>'.esc_html__('Defaults: 12/hour, 75/day. Zero stops new requests. Each request is conservatively budgeted as up to 20 credits; check your free-plan allowance. No automatic billing or upgrade. Caches are shared by coarse area for 24 hours.','gymnotfound').'</p>';
        echo '<button class="button button-primary" name="gnf_action" value="save">'.esc_html__('Save settings','gymnotfound').'</button></form>';
        echo '<h2>'.esc_html__('Activity templates','gymnotfound').'</h2><p><a class="button" href="'.esc_url(admin_url('edit.php?post_type=gnf_activity')).'">'.esc_html__('Edit bilingual activities','gymnotfound').'</a></p><p>'.esc_html__('Specific exercise instructions are hidden until a qualified reviewer approves the exact content version with sources, date, safety and an alternative. Any edit invalidates that approval.','gymnotfound').'</p>';
        echo '<h2>'.esc_html__('Diagnostics (no visitor history or coordinates)','gymnotfound').'</h2><pre>'.esc_html(wp_json_encode($diagnostics,JSON_PRETTY_PRINT)).'</pre>';
        $result=get_option('gnf_test_result',[]);if ($result) echo '<p>'.esc_html('Last explicit source check: '.wp_json_encode($result)).'</p>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'"><input type="hidden" name="action" value="gnf_settings">';wp_nonce_field('gnf_settings');
        echo '<p>'.esc_html__('Test a public area of your choice. This makes quota-limited source calls, not visitor tracking. Leave places disabled to test MET only.','gymnotfound').'</p><p><label>Latitude <input name="gnf_test_lat" type="number" step="0.01" min="-90" max="90" required></label> <label>Longitude <input name="gnf_test_lon" type="number" step="0.01" min="-180" max="180" required></label></p><button class="button" name="gnf_action" value="test">'.esc_html__('Test sources','gymnotfound').'</button></form>';
        echo '<h2>'.esc_html__('Credits & privacy','gymnotfound').'</h2><p>MET Norway: <a href="https://api.met.no/doc/locationforecast/HowTO">Locationforecast</a> · <a href="https://www.geoapify.com/">Powered by Geoapify</a> · <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>.</p><p>'.esc_html__('History and feedback stay in the visitor’s browser. Chosen locations are rounded to two decimal places. Maps opens externally; no map SDK or analytics. Deactivation preserves settings and templates. Uninstall also preserves them; delete templates/settings explicitly if retiring the app.','gymnotfound').'</p></div>';
    }
}

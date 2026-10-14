<?php
namespace GymNotFound;
if (!defined('ABSPATH')) exit;
final class Content {
    const FAMILIES = ['fresh_air','discovery','practical','home','routine','nature','connection','playful','place'];
    const ENVIRONMENTS = ['anywhere','urban','suburban','rural','home'];
    public static function register(): void {
        register_post_type('gnf_activity', [
            'labels'=>['name'=>__('Activity ideas','gymnotfound'),'singular_name'=>__('Activity idea','gymnotfound')],
            'public'=>false, 'show_ui'=>true, 'show_in_menu'=>'gymnotfound', 'supports'=>['title','editor'],
            'capabilities'=>['edit_posts'=>'manage_options','edit_others_posts'=>'manage_options','publish_posts'=>'manage_options','read_private_posts'=>'manage_options','delete_posts'=>'manage_options','create_posts'=>'manage_options'],
            'map_meta_cap'=>true,
        ]);
        add_action('add_meta_boxes', fn()=>add_meta_box('gnf_content', __('Bilingual activity and safety','gymnotfound'), [self::class,'fields'], 'gnf_activity'));
        add_action('save_post_gnf_activity', [self::class,'save'], 10, 2);
    }
    public static function seed(): void {
        if (get_option('gnf_seed_version') === '1') return;
        $seed = json_decode(file_get_contents(dirname(GNF_FILE).'/content/activities.json'), true);
        $seen=[];
        foreach (get_posts(['post_type'=>'gnf_activity','post_status'=>['publish','draft','private','trash'],'numberposts'=>-1]) as $post) $seen[] = get_post_meta($post->ID,'_gnf_seed_id',true);
        foreach ($seed as $card) {
            if (in_array($card['id'],$seen,true)) continue;
            $id = wp_insert_post(['post_type'=>'gnf_activity','post_status'=>'publish','post_title'=>$card['en']['title'],'post_content'=>$card['en']['description']], true);
            if (is_wp_error($id)) wp_die(esc_html__('Activity import failed. Please retry activation.','gymnotfound'));
            update_post_meta($id, '_gnf_seed_id', $card['id']);
            update_post_meta($id, '_gnf_card', $card);
        }
        update_option('gnf_seed_version','1',false);
    }
    public static function hash(int $id): string {
        $post = get_post($id);
        return hash('sha256', wp_json_encode([$post->post_title,$post->post_content,get_post_meta($id,'_gnf_card',true)]));
    }
    public static function requires_review(array $card): bool {
        if (!empty($card['instructions'])) return true;
        $parts=[];
        foreach (['en','nb'] as $language) foreach (['title','description','step','nim'] as $field) if (is_string($card[$language][$field] ?? null)) $parts[]=$card[$language][$field];
        // Conservative publication guard, not medical advice or an exercise generator.
        return (bool)preg_match('/\b(squats?|push[ -]?ups?|sit[ -]?ups?|planks?|lunges?|repetitions?|reps|heel raises?|single[ -]leg|one[ -]leg stance|balance exercises?|knebøy|armheving(?:er)?|balanseøvelse(?:r)?|tåhev|repetisjoner|stå på ett (?:ben|bein))\b/iu',implode(' ',$parts));
    }
    public static function reviewed(int $id): bool {
        $review = get_post_meta($id,'_gnf_review',true);
        if (!is_array($review) || empty($review['approved']) || empty($review['by'])) return false;
        foreach (['reviewer','date','sources','safety','alternative'] as $key) if (empty($review[$key])) return false;
        $date = $review['date'];
        if (!preg_match('/^\d{4}-\d{2}-\d{2}$/',$date) || !strtotime($date) || gmdate('Y-m-d',strtotime($date)) !== $date || $date > gmdate('Y-m-d')) return false;
        if (!preg_match('~https://\S+~',$review['sources'])) return false;
        return hash_equals(self::hash($id),(string)($review['hash'] ?? ''));
    }
    public static function all(): array {
        $out=[];
        foreach (get_posts(['post_type'=>'gnf_activity','post_status'=>'publish','numberposts'=>-1,'orderby'=>'ID','order'=>'ASC']) as $post) {
            $card=get_post_meta($post->ID,'_gnf_card',true);
            if (!is_array($card)) continue;
            $card['id'] = get_post_meta($post->ID,'_gnf_seed_id',true) ?: 'custom-'.$post->ID;
            $card['en']['title']=wp_strip_all_tags($post->post_title);
            $card['en']['description']=wp_strip_all_tags($post->post_content);
            $card['instructions']=self::requires_review($card);
            $card['reviewed']=self::reviewed($post->ID);
            if (!empty($card['instructions']) && !$card['reviewed']) continue;
            if (!empty($card['instructions'])) {
                $review=get_post_meta($post->ID,'_gnf_review',true);
                $card['safety']=$review['safety']; $card['alternative']=$review['alternative'];
            }
            $out[]=$card;
        }
        return $out;
    }
    public static function fields(\WP_Post $post): void {
        wp_nonce_field('gnf_content','gnf_content_nonce');
        $card=get_post_meta($post->ID,'_gnf_card',true) ?: [];
        echo '<p>'.esc_html__('WordPress title and editor above contain the English title and description. All fields below are plain text.','gymnotfound').'</p>';
        foreach (['en'=>__('English','gymnotfound'),'nb'=>__('Norwegian','gymnotfound')] as $lang=>$label) {
            echo '<h3>'.esc_html($label).'</h3>';
            foreach (['title','description','step','nim'] as $key) {
                if ($lang==='en' && in_array($key,['title','description'],true)) continue;
                echo '<p><label>'.esc_html($key).'<br><textarea style="width:100%" name="'.esc_attr('gnf_'.$lang.'_'.$key).'" rows="2" maxlength="1000">'.esc_textarea($card[$lang][$key] ?? '').'</textarea></label></p>';
            }
        }
        $maps=['time'=>[2=>'2',15=>'10–15',30=>'30+'],'energy'=>['low'=>'Low / Lavt','some'=>'Some / Litt','high'=>'High / Bra'],'family'=>array_combine(self::FAMILIES,self::FAMILIES),'cost'=>['free'=>'No purchase required','maybe'=>'Possible costs'],'place_category'=>[''=>'No specific place','park'=>'Park','library'=>'Library','museum'=>'Museum','cafe'=>'Café','viewpoint'=>'Viewpoint']];
        foreach ($maps as $key=>$values) {
            echo '<p><label>'.esc_html($key).' <select name="'.esc_attr('gnf_'.$key).'">';
            foreach ($values as $value=>$label) echo '<option value="'.esc_attr($value).'" '.selected($card[$key] ?? '',$value,false).'>'.esc_html($label).'</option>';
            echo '</select></label></p>';
        }
        foreach (self::ENVIRONMENTS as $value) echo '<label style="margin-right:15px"><input type="checkbox" name="gnf_contexts[]" value="'.esc_attr($value).'" '.checked(in_array($value,$card['contexts'] ?? ['anywhere'],true),true,false).'> '.esc_html($value).'</label>';
        foreach (['outdoors'=>'Requires going outdoors','instructions'=>'Contains specific movement/exercise instructions'] as $key=>$label) echo '<p><label><input type="checkbox" name="'.esc_attr('gnf_'.$key).'" value="1" '.checked(!empty($card[$key]),true,false).'> '.esc_html($label).'</label></p>';
        $review=get_post_meta($post->ID,'_gnf_review',true) ?: [];
        echo '<h3>'.esc_html__('Professional review (required for specific exercise instructions)','gymnotfound').'</h3>';
        foreach (['reviewer','date','sources','safety','alternative'] as $key) echo '<p><label>'.esc_html($key).'<br><input style="width:100%" name="'.esc_attr('gnf_review_'.$key).'" value="'.esc_attr($review[$key] ?? '').'" maxlength="1000"></label></p>';
        echo '<label><input type="checkbox" name="gnf_review_approved" value="1"> '.esc_html__('Approve this exact version after professional review. Check again only after reviewing any change.','gymnotfound').'</label>';
    }
    public static function save(int $id, \WP_Post $post): void {
        if (wp_is_post_revision($id) || !current_user_can('manage_options') || empty($_POST['gnf_content_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['gnf_content_nonce'])),'gnf_content')) return;
        $card=[];
        foreach (['en','nb'] as $lang) foreach (['title','description','step','nim'] as $key) {
            $value=$lang==='en' && $key==='title' ? $post->post_title : ($lang==='en' && $key==='description' ? $post->post_content : sanitize_textarea_field(wp_unslash($_POST['gnf_'.$lang.'_'.$key] ?? '')));
            $card[$lang][$key]=mb_substr(sanitize_textarea_field($value),0,1000);
        }
        $time=absint(wp_unslash($_POST['gnf_time'] ?? 2));
        $card['time']=in_array($time,[2,15,30],true) ? $time : 2;
        foreach (['energy'=>['low','some','high'],'family'=>self::FAMILIES,'cost'=>['free','maybe'],'place_category'=>['','park','library','museum','cafe','viewpoint']] as $key=>$allowed) {
            $value=sanitize_text_field(wp_unslash($_POST['gnf_'.$key] ?? ''));
            $card[$key]=in_array($value,$allowed,true) ? $value : $allowed[0];
        }
        $contexts=is_array($_POST['gnf_contexts'] ?? null) ? array_map('sanitize_key',wp_unslash($_POST['gnf_contexts'])) : [];
        $card['contexts']=array_values(array_intersect($contexts,self::ENVIRONMENTS)) ?: ['anywhere'];
        foreach (['instructions','outdoors'] as $key) $card[$key]=!empty($_POST['gnf_'.$key]);
        $card['instructions']=self::requires_review($card);
        $card['place_category']=$card['place_category'] ?: null;
        update_post_meta($id,'_gnf_card',$card);
        $review=[];
        foreach (['reviewer','date','sources','safety','alternative'] as $key) $review[$key]=mb_substr(sanitize_textarea_field(wp_unslash($_POST['gnf_review_'.$key] ?? '')),0,1000);
        $review['approved']=!empty($_POST['gnf_review_approved']);
        $review['by']=get_current_user_id();
        $review['hash']=$review['approved'] ? self::hash($id) : '';
        update_post_meta($id,'_gnf_review',$review);
    }
}

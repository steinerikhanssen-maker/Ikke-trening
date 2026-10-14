<?php
if (!defined('ABSPATH')) exit;
?><!doctype html>
<html <?php language_attributes(); ?>>
<head><meta charset="<?php bloginfo('charset'); ?>"><meta name="viewport" content="width=device-width, initial-scale=1">
<?php if (!current_theme_supports('title-tag')) echo '<title>'.esc_html(get_the_title()).'</title>'; wp_head(); ?></head>
<body class="gnf-shell"><?php
wp_body_open();
// phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- Shortcode returns only static markup and escaped noscript text.
echo \GymNotFound\Plugin::shortcode();
wp_footer(); ?></body>
</html>

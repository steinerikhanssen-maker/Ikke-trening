<?php
/**
 * Plugin Name: GymNotFound
 * Description: One useful activity idea. Optional weather and places. No account required.
 * Version: 0.1.0-beta.1
 * Requires at least: 6.7
 * Requires PHP: 8.2
 * Text Domain: gymnotfound
 * License: GPL-2.0-or-later
 */
namespace GymNotFound;
if (!defined('ABSPATH')) { exit; }
define('GNF_VERSION', '0.1.0-beta.1');
define('GNF_FILE', __FILE__);
foreach (['Content','Providers','Api','Plugin'] as $gymnotfound_class) {
    require_once __DIR__ . '/includes/' . $gymnotfound_class . '.php';
}
unset($gymnotfound_class);
register_activation_hook(__FILE__, [Plugin::class,'activate']);
add_action('plugins_loaded', [Plugin::class,'boot']);

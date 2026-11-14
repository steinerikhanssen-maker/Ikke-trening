=== GymNotFound ===
Contributors: steinerikhanssen-maker
Tags: activities, wellbeing, local, weather
Requires at least: 6.7
Tested up to: 7.1
Requires PHP: 8.2
Stable tag: 0.1.0-beta.1
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

One small activity idea, without an account. English and Norwegian, optional weather and real places, local guest history.

== Description ==
GymNotFound is an activity companion, with 36 editable bilingual ideas. One rule engine uses time, energy, environment and your recent answers. NIM is optional.

No account, analytics, background tracking or measured exercise. Trying does not count as completing. Only an explicit Done stores a self-reported activity in this browser. Preferences, feedback and history can be exported or deleted.

The owner explicitly creates or selects an app page. Activation creates activity templates, never a page. Use [gymnotfound_app] on another page for theme integration.

Specific exercise instructions are excluded until an administrator records a qualified professional review of the exact content version. The included activities are general everyday choices, not an exercise programme or medical advice.

== External services ==
Optional MET Norway Locationforecast provides weather only after a visitor chooses an approximate area. Coordinates are rounded to two decimals. Requests are server-side, cached and limited. Terms: https://api.met.no/doc/TermsOfService ; credits: https://www.met.no/frie-meteorologiske-data/lisensiering-og-kreditering . No key required.

Optional Geoapify Places and Geocoding receive approximate coordinates or an explicitly submitted town search only if the owner enables them with a free-plan key. The key is encrypted on the server. No history is sent. Maximum 20 results, shared 24-hour cache and hard hourly/daily request caps. Terms: https://www.geoapify.com/terms-and-conditions/ ; privacy: https://www.geoapify.com/privacy-policy/ . Places credit Geoapify and https://www.openstreetmap.org/copyright . Check your account allowance; the app never enables billing.

Google Maps URLs open externally only on a link click. Links contain a public destination, not the visitor's origin or history. No Maps API/SDK. Terms/privacy: https://policies.google.com/ .

Ideas work without any external service. Hosting may maintain ordinary access logs. The app uses short-lived salted IP hashes for anonymous rate limits, with no IP/location log. Read the repository's docs/PERSONVERN.md before installing on a test site.

== Installation ==
1. In WordPress 6.7+ with PHP 8.2+, open Plugins > Add New > Upload Plugin.
2. Upload gymnotfound-0.1.0-beta.1.zip and activate GymNotFound.
3. Open GymNotFound > Create draft app page, preview, then publish when authorised.
4. Optional: enable Geoapify and enter your free-plan key. Generic use needs no key.

No Node, Composer or terminal is required on hosting. HTTPS is needed for browser geolocation. Deactivation and uninstall preserve settings/templates; delete them explicitly when retiring the app. Browser data is removed through My choices.

== Frequently Asked Questions ==
= Does Try count as completed? =
No. Only Done creates completed_self_report. No steps, timers or streaks.

= Does offline work? =
An already opened app continues with generic ideas offline. A first-ever visit or reload offline needs the site connection; no service worker is installed.

== Changelog ==
= 0.1.0-beta.1 =
First activity-companion beta: 36 bilingual ideas, one engine, local guest data, optional MET and Geoapify, Google Maps URLs and editable reviewed content.

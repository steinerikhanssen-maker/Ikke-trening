# IKKE TRENING 5.0 – teknisk WordPress-arkitektur

## A. Leveransemodell: én ZIP, ett plugin, to visningsmoduser

- Plugin-slug: `ikke-trening`; tekst-domene: `ikke-trening`; appversjon i WordPress plugin-header: `0.1.0-beta.1`. Ingen avhengighet til Viamo, Husvarme, HighBias eller andre personlige plugins.
- **Fullskjerm appmodus:** valgfri WordPress-side knyttes til pluginens appmal med `template_include`, kun for valgt side-ID (aldri alle sider). Skallet inkluderer nødvendige WordPress hooks, SEO/noindex-kontroll for lukket test, dokumenttittel, sikkerhetsheaders der mulig, skjermlesertilgang og tydelig innloggings-/utloggingsnavigasjon.
- **Innebygd modus:** Gutenberg-blokk `ikke-trening/app` med server-side `render_callback`, samt fallback-kortkode `[ikke_trening_app]` for eksisterende temaer. JS/CSS styres lokalt i komponentens root og isoleres fra globalt tema-CSS. Shortcode skal ikke kjøre på tilfeldige sider.
- **UI-tema:** pluginskinn med egne tokens, CSS-moduler / scoped styles; ikke en separat WordPress-theme. WP admins eksisterende tema skal fungere. Et eget fullsite-markedsføringstema kan eventuelt bestilles senere.
- Installerbar WordPress-plugin-ZIP må inneholde ferdig bygde webassets. Ingen npm, node_modules, composer-installasjon eller SSH på webhotellet kreves etter opplasting i wp-admin. React/Vite eller tilsvarende kan brukes under utvikling, men distribuert ZIP må være selvforsynt. Ikke bruke CDN eller eksterne fonter/biblioteker i vanlig drift.
- Minimumsmiljø: WordPress 6.7+; PHP 8.2+, test særlig PHP 8.3/8.4 og moderne MySQL/MariaDB; HTTPS på nettstedet. WordPress anbefaler i 2026 PHP 8.3+, MariaDB 10.11+ eller MySQL 8.0+. Ikke anta tilgang til shell på webhotellet.
- Aktivering: sjekk kompatibilitet, opprett/oppgrader datatabeller idempotent, registrer innholdstyper, opprett **ingen** offentlig side og aktiver ikke registrering på hele nettstedet automatisk.

## B. Backend og datamodell

Bruk WordPress' brukeradministrasjon og cookie-basert autentisering for førstegangsutgaven. Ingen separat passorddatabase, ingen egengenererte JWT-er i localStorage. Kontoer opprettes via WordPress sine dokumenterte flyter; admin styrer om eksterne testere får registrere seg. `Subscriber` er tilstrekkelig for vanlige brukere. Lag custom capability for app-administrasjon hvis nødvendig, men gi den ikke til abonnenter.

**Forslag til skjema (nøyaktig valg kan optimaliseres av Codex, men datastrømmene/tilgangskravene er normative):**

1. `wp_ikt_events`: `id`, `user_id`, `client_uuid` (unik idempotency key), `event_type` (suggested/planned/attempted/completed/skipped/rested/declined), `kind`, **nullable `anchor_id`/`movement_id`** (bare med eierskapssjekk), `reported_minutes` (nullable, vanlig aktivitet), **`reported_reps` og `reported_seconds` nullable** (mikrohandlinger; minst ett positivt for `completed` mikro), `reported_exertion` nullable, `feel` nullable, `barrier` nullable, `source` enum (`self_report`/`admin_test`), `created_at_utc`, `local_date`. Ingen personlig fritekst i tekniske loggfelter uten bevisst behov.
2. `wp_ikt_plans`: `id`, `user_id`, `cue`, `scheduled_at_utc` nullable, `timezone`, `backup`, `state`, `created_at_utc`, `updated_at_utc`.
3. `wp_ikt_unlocks`: `user_id`, `world_id`, `chapter_id`, `local_day`, `activity_event_id`, `created_at_utc`; unik for user + chapter; håndhev maks én belønnet gjennomføring per bruker og lokal dag på server.
4. `wp_ikt_groups`: id, oppretter, valgfritt navn, opprettet, lukket; `wp_ikt_group_members`: `group_id`, `user_id`, `display_label`, `opt_in_share`, `role`, `joined_at`, `left_at`; `wp_ikt_group_contributions`: `id`, `group_id`, `user_id`, `event_id`, `period_id`, `created_at_utc`. Gruppeinnlegg uten rå minutter, puls, diagnose eller lokasjon.
5. `wp_ikt_invites`: `id`, `group_id`, `token_hash`, `created_by`, `expires_at_utc`, `accepted_by` nullable, `revoked_at_utc`. Token håndteres som hemmelighet, hash ved lagring, tidsbegrenset og engangsbruk; ingen e-postliste over invitasjonsmål uten behov.
6. `wp_usermeta`: kort versjonert profil/innstillinger, valgt verden, NIM-valg, frivillig deling, varslingsvalg, siste valgte hinder. Ikke lag omfattende tidsserie eller store eventhistorikker i `usermeta`.
7. **Integrerte hverdagsankre (P0):** `wp_ikt_anchors`: `id`, `user_id`, `cue_type`, `custom_label`, `movement_id`, `enabled`, `created_at_utc`, `updated_at_utc`. Tidsankre er valgte rutiner, ikke detekterte sensorhendelser. Øvelseskort som **`ikt_movement` CPT**, publiseres bare etter eksplisitt kontroll av fagrevisor, kilder og sikkerhetsbeskrivelse. Eget admin-lukket testmodus når gjennomgang mangler. `kind=micro_movement` er kun en **hendelsestype i den felles aktivitetsloggen**, ikke separat brukerhistorikk. Samme anbefalingstjeneste velger hverdagsmikrobevegelser, turer eller annen handling. Se `07_HVERDAGSANKRE_OG_MIKROBEVEGELSE.md` og `08_PRESISERING_INTEGRERT_AKTIVITET.md`.
8. Historieinnhold som `ikt_world` / `ikt_chapter` CPT med WP-editor, sorteringsrekkefølge, publish/draft, felt for originalt innhold, og tilgang kun for admin/redaktør med riktig capability. Lag versjonert seed-import av minst 24 ekte kapitler i to verdener, uten å overskrive redaksjonelle endringer ved oppgraderinger.

Bruk `$wpdb->prefix`, `dbDelta()` der tabeller trengs, versjonert migreringsfunksjon, ryddige indekser på `user_id`, `group_id` og tid. Ikke bruke direkte SQL uten `wpdb->prepare()` for alle data fra bruker. Reflektér over begrensninger ved `dbDelta()` for migreringer med sletting/endring.

## C. REST API-kontrakt

Namespace `ikke-trening/v1`. Eksempelendepunkter som Codex kan tilpasse, men kontrakt og testbarhet er påkrevd:

- `GET /bootstrap` – returner innlogget/guest-status, adminopsjoner for feature flags, publikumsverdener, ikke sensitive brukerdetaljer.
- `GET/PATCH /me/profile` – kun innlogget eier; avgrenset input og eksplisitte samtykker.
- `GET /me/suggestion?barrier=...` – forklarbar hjelp; ingen personlige data fra andre.
- `POST /me/events` – servervalidert aktivitet, plan, avslag, hvile, idempotent `client_uuid` og tiltatt rate limiting.
- `GET /me/events`, `GET/POST/PATCH/DELETE /me/plans` – private for riktig eier.
- `GET /movements`, `GET/POST /me/anchors`, `PATCH/DELETE /me/anchors/{id}` – kvalitetssikret innhold, privat eierstyrt ankerhåndtering og strengt skille mellom plan og faktisk aktivitet.
- `GET /worlds`, `GET /worlds/{id}/chapters` – publisert innhold, status for opplåsing kun når innlogget; ikke tilgang til andre brukeres progresjon.
- `GET /me/unlocks`, `POST /me/export`, `DELETE /me/data` – eierstyrt eksport/sletting, re-autentisering/bekreftelse for destruktive operasjoner.
- `POST /groups`, `GET /groups/{id}`, `POST /groups/{id}/invites`, `POST /invites/accept`, `PATCH /groups/{id}/member`, `POST /groups/{id}/leave` – autorisasjon og medlemskap på hver handling, ikke bare «logged in».
- Admin-only `/admin/health`, `/admin/config` og innholdsforvaltning via WP-admin; ingen personlige rapporter i offentlig API.

Registrer ruter på `rest_api_init` med eksplisitt `permission_callback` hver gang. Cookie-autentisering med `X-WP-Nonce` for innloggede frontendkall; **nonce er CSRF-beskyttelse, ikke tilgangsstyring**, så kontroller eier/medlemskap på serveren for hvert ID. Ikke stol på user_id, group_id eller aktivitetstall fra klienten for eierskap/reward. Schema-validering og escaping overalt. Separat tilgangssikret token-flyt for aksept av invitasjon.

## D. Frontend og separasjon av logikk

- `routine anchor engine`: `proposeAnchor(cue, context, preferences)`, `selectSafeMovement(...)`, `recordAnchorFeedback(...)`; ankerutløsing er **brukerstyrt**, ingen påstått deteksjon av tannpuss/kaffe/dusj. Filtrer eksplisitt ut øvelser på vått gulv, med opptatte hender eller usikre støttepunkter.
- `behaviour engine`: `assessBarrier(user_input, history) -> proposedSupportType`, `selectAction(...)`, `explainReason(...)`, `recordFeedback(...)`. Ren domenelogikk, testbar med fixture-data, uten browser- eller WordPress-avhengighet.
- `reward/story engine`: `eligibleUnlock(user, completedEvent, localDay)`, `nextChapter(world, unlocks)`. Kun backend avgjør unlock; frontend renderer tilstand. Pause straffer ikke, og et rapportert minutt er ikke automatisk «treningseffekt».
- `social engine`: legitime gruppebidrag fra serverhendelser, frivillig samtykke, ingen offentlig aktivitet.
- Presenter alltid faktisk status. Ikke bruk mock-data i innlogget brukerflate. Demo-data i eksplisitt admin/demo environment med tydelig merking og nullstillingsmulighet.
- i18n fra start, norske strenger. CSS isoleres for ikke å overstyre globale WordPress-sider. Responsive SVG for NIM. Lag ingen skjult tredjepartsoppkobling.
- En sjenerøs guest view kan lese offentlige historier eller prøve onboarding, men **ingen** gjeste-REST-rute må kunne skrive en annen persons data.

## E. Sikkerhet, personvern og lovmessig avgrensning

- HTTPS, WordPress-auth, tilgangsregler for hver ressurs, CSRF-nonce, input-validering, output-escaping, preparerte DB-spørringer, rate limiting for invitasjoner og skriveruter. Test IDOR mellom kontoer og tilgang uten autentisering.
- Social by default OFF. Alle individuelle aktivitetsdetaljer private by default. Brukerkontroll for gruppevisning, gruppeekstensjoner, utmelding og blokkering/rapportering dersom det senere bygges chat. Ikke lag chat i beta.
- GDPR: dataminimering (ingen diagnose, puls, posisjon, vekt eller medisinske risikoscorer); personverntekst; WordPress privacy exporter/eraser; brukerbasert eksport/sletting og tydelige spor etter sletting. Nettstedsoperatøren må vurdere behandlingsgrunnlag og eventuelt DPIA før ekstern bruk.
- Unngå ukontrollerte logger av URLer med invitasjonstoken, eksponering i referrer eller analytics. `Referrer-Policy`/redirect etter tokenaksept; hash-token; kort levetid.
- Ikke eksponer komplett fysisk aktivitetslogg i administratorens generelle analytics. Innsyn må være eksplisitt begrunnet.
- Innhold som gir konkrete bevegelsesinstrukser må ha faglig publiseringsstatus i metadata. Uten dokumentert gjennomgang skal kun administrativ testvisning vise disse kortene, ikke ordinære brukere. Ikke lagre diagnoser eller automatiske medisinske vurderinger; nødvendige funksjonsvalg behandles som potensielt sensitive.
- Data slettes **ikke** ved plugin-deaktivering. Avinstallasjon med mulig sletting skal være uttrykkelig valgt av administrator; dokumenter konsekvensene.

## F. UI-leveransekrav

- Mobil innlogget: tittellinje, hindringsvalg (kompakt), **ett aktuelt forslag fra samme motor** og hovedknapp innen 390×844 uten lang scrolling. Forslaget kan være en hverdagsforankret mikrobevegelse; brukeren skal ikke måtte velge en egen «Hverdagsankre»-fane eller forlate «I dag». Valg/justering av «Når jeg ...»-rutine vises i den samme anbefalings-/planflyten når relevant, eller i ordinære innstillinger. NIM vises kompakt på innlogget start; stor hero kun på informativ landing.
- Sans-serif systemfont lokalt, ingen ekstern Google Fonts. Tema tokens for lys/mørk (mørk frivillig), høy kontrast og reduksjon av animasjon.
- Førsteside og alle brukerreiser norsk. Klare tomtilstander for ingen aktivitet, ingen venner, ferdig historie, og etter pause.
- WCAG 2.2 AA som mål; konkret testing må dokumenteres (inkl. automatisk axe-undersøkelse + manuell tab/fokus/kontrast/skjermleser-røyk-test).

## G. Ingen tvungne løpende kostnader

Bruk WordPress eksisterende PHP/DB, lokale CSS/JS/SVG, WordPress-e-post hvis frivillig og testet. Ingen Stripe, ingen LLM API, ingen betalt kart, ingen Push-leverandør, ingen lisenspliktig ikonpakke eller bakgrunnstjeneste i første beta. En ordentlig WordPress-installasjon har naturligvis eksisterende hostingkostnad, men selve pluginen introduserer ingen fast ekstern tjenesteavgift.

## H. Installerings- og oppgraderingsprosedyre

I wp-admin: Utvidelser → Legg til ny → Last opp ZIP → Installer → Aktiver → «IKKE TRENING» i admin → oppsettveiviser → opprett/velg testside → forhåndsvis app → tillat evt. innlogging/brukere → test med to egne WP-testkontoer. Ved ny versjon må pluginen oppdatere skjema og assets uten tap av data. WP-admin, publiserte sider og andre plugins skal fortsatt fungere.

**Produksjonsport:** Codex skal levere ZIP + README + rapport om tester/avvik, men ikke selv installere på et produksjonsdomene, endre DNS eller slå på offentlig registrering. Testen først på isolert WordPress-domene; produksjon krever separat godkjenning.

## Primære tekniske kilder

- https://developer.wordpress.org/themes/getting-started/what-is-a-theme/
- https://developer.wordpress.org/reference/hooks/template_include/
- https://developer.wordpress.org/reference/functions/register_block_type/
- https://developer.wordpress.org/apis/shortcode/
- https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/
- https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/
- https://developer.wordpress.org/apis/security/nonces/
- https://developer.wordpress.org/plugins/creating-tables-with-plugins/
- https://developer.wordpress.org/plugins/privacy/privacy-related-options-hooks-and-capabilities/
- https://wordpress.org/about/requirements/
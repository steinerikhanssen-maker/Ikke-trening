# Testrapport — GymNotFound 0.1.0-beta.1

Kjørt 14.10.2026 for issue #1, med kravene i docs/10 og docs/11. Pluginen er testet lokalt, uten produksjonsinstallasjon eller merge. Alle kjerne- og feilscenarier nedenfor består. Eksterne/andre miljøer som ikke er verifisert står som **NOT RUN**, og omfattes ikke av PASS.

**Miljø:** isolerte Docker-stakker på loopback, MariaDB 11.4, WordPress 6.8.3 for ren WP-admin ZIP-installasjon og WordPress 7.1.3 for den siste backend-/nettlesersuiten. PHP 8.3.28 i Apache, PHP 8.3.35 i WP-CLI. Node 24.19.0, Playwright 1.56.1, system-Chromium 154, axe via @axe-core/playwright 4.10.2, WordPress Plugin Check 2.1.0. ZIP-stakken har egne volum og **ingen montert plugin-kildekode**. Lokal CA/proxy-teststøtte er utenfor ZIP-en. Ingen tunge GitHub Actions-jobber er opprettet.

**Utført:** 16 Node-tester, 57 WordPress-assertions, to tester med åtte samtidige PHP-prosesser, 17 Chromium-tester på både 7.1.3 og den opplastede ZIP-en på 6.8.3 (34 beståtte browserkjøringer), faktisk ZIP-opplasting/aktivering/adminredigering og en ekte MET-forespørsel. Plugin Check og PHP lint er kjørt. Detaljert nettleserresultat ligger i [kilde-instansens JSON](../evidence/browser-results.json) og [ZIP-instansens JSON](../evidence/zip-browser-results.json). Fixtures finnes bare under tests/ og blir ikke levert i pluginen.

## A — WordPress, ZIP og admin

| ID | Testcase | PASS-FAIL-NOT RUN | Testmetode | Miljø | Bevislenke | Bemerkning |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Ren ZIP-installasjon uten build på hosting | PASS | Faktisk filopplasting og aktivering i WP-admin; ZIP-CRC/innhold og SHA256 | Ren WP 6.8.3/Apache PHP 8.3.28 | [ZIP-test](../evidence/zip-install.txt), [pakke](../dist/gymnotfound-0.1.0-beta.1.zip), [checksum](../dist/gymnotfound-0.1.0-beta.1.zip.sha256) | Ingen source mount, npm eller Composer i pluginen. |
| A2 | Aktivering, deaktivering, reaktivering og side-idempotens | PASS | Admin-E2E; seed-idempotens i faktisk database | ZIP-stakk + WP 7.1.3 | [ZIP-test](../evidence/zip-install.txt), [backend](../evidence/integration.txt) | Aktivering lager ingen side; uttrykkelig oppretting lager ett utkast. |
| A3 | GymNotFound-header, selvstendig appskall og shortcode | PASS | Installert ZIP-forhåndsvisning, anonym app og ordinær tema-side | WP 6.8.3/7.1.3, Chromium | [ZIP-test](../evidence/zip-install.txt), [sideintegrasjon](../evidence/page-integration.txt) | Slug/text domain gymnotfound, versjon 0.1.0-beta.1. |
| A4 | Innstillinger, status, 36 maler, begge språk og forhåndsvisning | PASS | Klikket opprett/preview/malredigering/lagre; CPT og cache-/kvotestatus | ZIP-stakk + backend | [adminbevis](../evidence/zip-install.txt), [adminbilde](../screenshots/wordpress-admin.png), [backend](../evidence/integration.txt) | Valgfri nøkkel har tomt erstatningsfelt; kildetest er uttrykkelig. |
| A5 | Ingen nøkkel eller private GPS-/historikkdata i offentlig output | PASS | Kryptering/dekryptering; public/diagnostics-svar; normalisert lokal eksport; arkivinspeksjon | Backend, Node, Chromium | [backend](../evidence/integration.txt), [storage](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Testnøkkel genereres i minnet og ryddes. Kun fiktiv lokal WP-testkonto brukes. |

## B — Første skjerm og gjesteflyt

| ID | Testcase | PASS-FAIL-NOT RUN | Testmetode | Miljø | Bevislenke | Bemerkning |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | Hele kortet, hovedhandling og Ny idé over fold på 390×844 | PASS | Bounding-box-assertions og visuell inspeksjon | Chromium/WP | [nettleser](../evidence/browser.txt), [første skjerm](../screenshots/mobile-first-screen.png) | Ingen stor hero. |
| B2 | Uten konto og posisjon, norsk/engelsk | PASS | Anonym nettleser; GPS-kall teller 0; begge komplette språkflyter | Chromium/WP | [nettleser](../evidence/browser.txt) | Ingen ekstern klientressurs eller GPS-prompt ved første åpning. |
| B3 | Tid/energi påvirker forslag med korte valg | PASS | Alle ni tids-/energikombinasjoner; native to-trinns velgere | Node + Chromium | [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Avsatt tid; ingen beregnet gangtid. |
| B4 | Åtte påfølgende ulike, gyldige ideer | PASS | Testet åtte valg i begge språk, sparse område, dårlig vær og offline | Node + Chromium | [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Variasjon overstyrer aldri harde sikkerhetsfiltre. |
| B5 | Prøv ≠ fullført; Gjort/avslag/Ikke nå virker | PASS | Les lagret state før/etter eksplisitt handling og reload | Node + Chromium | [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Kun completed_self_report i historikken; avslag lagres. |
| B6 | Gjenåpning bevarer egne gamle handlinger uten skyld | PASS | Reload og migrering; historikkdato uavhengig av besøksdato; gjennomgang av NIM-tekster | Node + Chromium/innhold | [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Ingen streak, energi-tap, påminnelsesjobb eller negativ pause-status. |
| B7 | Min vei, JSON-eksport og bekreftet sletting | PASS | Faktisk filnedlasting, JSON-inspeksjon, avbryt/slett og behold annet nettsteddata | Chromium + Node | [nettleser](../evidence/browser.txt), [unit](../evidence/unit.txt) | Ingen oppdiktede minutter/skritt/helseeffekt. |
| B8 | Legg bort mobilen uten timer eller krav | PASS | Try-tilstand og reload; eksplisitte tilbake/senere/ikke nå | Chromium | [nettleser](../evidence/browser.txt) | Opphold er ikke completion; appen kan lukkes. |
| B9 | NIM av/på og full funksjon uten maskot | PASS | Preferanse av, navigasjon, samme aktivitetshandlinger | Chromium | [nettleser](../evidence/browser.txt) | Ingen tom plass eller funksjon bundet til NIM. |

## C — Sted, land/by og samme motor

| ID | Testcase | PASS-FAIL-NOT RUN | Testmetode | Miljø | Bevislenke | Bemerkning |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | By: 12 navngitte POI-er i flere kategorier | PASS | Fixture på den eksakte produksjonsmotoren; rendret sted/kilde/Maps | Node + Chromium | [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Navnet kommer fra fixture-kilden, ikke generering. Fixtures leveres ikke. |
| C2 | Landlig: to parker, ingen kafé/museum | PASS | Åtte motorvalg med sparsomt datasett | Node | [unit](../evidence/unit.txt) | Bare faktiske parkstreff eller generiske oppgaver. |
| C3 | Null steder i 10 km, minst tre generiske aktiviteter | PASS | Tomt adapter-svar/radiuskontroll og åtte ulike kildefrie valg | WP + Node | [backend](../evidence/integration.txt), [unit](../evidence/unit.txt) | 30 generiske maler; ingen transport-/kart-/kjøpsplikt. |
| C4 | To avslag for samme familie endrer typen | PASS | Lagret feedback direkte i samme motor; browser-reload | Node + Chromium | [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Familie blir hardt filtrert i nylig feedback. |
| C5 | Kostnad, privat/utrygt/stengt, ukjent åpning | PASS | Filter-fixtures, gratisvalg og synlig forsiktig kildetekst | WP + Node + Chromium | [backend](../evidence/integration.txt), [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Ukjent åpning/adgang er aldri et løfte om åpent/gratis. |
| C6 | Sikre Maps URLs uten falsk routing/avstand | PASS | URL-parser og rendret ekstern lenke | Node + Chromium | [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Ingen avstand vises; destinasjon uten privat origin/API-nøkkel. |
| C7 | Manuelt valgt landlig miljø overstyrer tetthet | PASS | Eksplicit rural med tett og tomt datasett | Node | [unit](../evidence/unit.txt) | Brukervalg får prioritet. |

## D — Integrasjoner og reserveforslag

| ID | Testcase | PASS-FAIL-NOT RUN | Testmetode | Miljø | Bevislenke | Bemerkning |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Opphold, regn, vind, kulde, ukjent og gammelt vær | PASS | MET-parser + motor-fixtures; datert prognose og synlig igjen etter seks timer | WP + Node + Chromium | [backend](../evidence/integration.txt), [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Dårlig vær gir innevalg; stale vær fjernes. |
| D2 | MET server-side, UA, avrunding, Expires/Last-Modified/304 | PASS | Intercept kun HTTP, kjør ekte adapter/cacher og valider request-argumenter | WP/MariaDB | [backend](../evidence/integration.txt) | Faste TLS-endepunkter, timeout 5s, ingen redirects, responsgrense. |
| D3 | Ingen posisjon gir null MET/Geoapify-kall | PASS | REST uten område, GPS-/nettverksteller ved første skjerm | WP + Chromium | [backend](../evidence/integration.txt), [nettleser](../evidence/browser.txt) | Gjelder appens kilder; vanlig WordPress kan ha egne oppdateringskall. |
| D4 | MET 403/429/500/timeout/ugyldig/stor respons | PASS | Faktisk feilgren/backoff og åpen offline-app | WP + Chromium | [backend](../evidence/integration.txt), [nettleser](../evidence/browser.txt) | Ingen endeløs spinner, falskt vær eller blank app. |
| D5 | Geoapify uten nøkkel/av | PASS | Eksplisitt null nøkkel og disabled provider; fullt gjesteforløp | WP + Chromium | [backend](../evidence/integration.txt), [nettleser](../evidence/browser.txt) | Ingen stedskall eller fantasitreff. |
| D6 | Geoapify 200 treff/tomt, normalisering og attributter | PASS | Fixtures med id, kategorier, koordinater, duplikater, private og injeksjon | WP + Node + Chromium | [backend](../evidence/integration.txt), [nettleser](../evidence/browser.txt) | Maksimum 20 svar, kategorier kontrollert i leverandørens dokumentasjon. |
| D7 | Geoapify feil og harde time-/døgnkvoter | PASS | 401/403/429/500/timeout, kvoter og åtte samtidige PHP-prosesser | WP/MariaDB | [backend](../evidence/integration.txt), [samtidighet](../evidence/concurrency.txt) | Nøyaktig én prosess får siste kvoteplass; ingen automatisk retry/betaling. |
| D8 | Fem oppslag i samme grove område bruker ett kildekall | PASS | Faktiske transients og adapter med request-teller | WP/MariaDB | [backend](../evidence/integration.txt) | Testet separat for MET og Geoapify. |
| D9 | Posisjon, avslag, grovt manuelt søk og fjern/slett | PASS | API-searchfixture; eksplisitt browser-GPS; reset og forsinket callback etter sletting | WP + Chromium | [backend](../evidence/integration.txt), [nettleser](../evidence/browser.txt) | Rå GPS lagres ikke; sen callback gjenoppretter ikke slettet område. |
| D10 | MET/Geoapify/OSM-kreditering bare ved faktisk bruk | PASS | Rendret aktuelle kildefixtures og stale/offline | Chromium | [nettleser](../evidence/browser.txt) | Admin har separat kildeliste. |
| D11a | Direkte MET-livetest, korrekt UA | PASS | Ingen mock, produksjonsadapter mot offentlig sentralt Oslo-område | WP 7.1.3/server | [livebevis](../evidence/met-live.json) | Aktuell forecast med kilde-/hentetid; ingen nøkkel. |
| D11b | Direkte Geoapify-livetest | NOT RUN | Ikke utført uten legitim nøkkel | Ingen key konfigurert | [begrunnelse](../evidence/external-not-run.txt) | Fixtures og kvote-/feilgrener består; reell konto-/provider-test gjenstår. |
| D12 | Responsgrenser, anonyme rate limits, XSS og gjentatt bruk | PASS | 196608-byte grense, 2048-byte request, 30/min og åtte samtidige workers; injisert HTML | WP + Chromium | [backend](../evidence/integration.txt), [samtidighet](../evidence/concurrency.txt), [nettleser](../evidence/browser.txt) | Direkte URL/arrays/out-of-range avvises; HTML blir tekst. |

## E/F — Innhold, sikkerhet og kvalitet

| ID | Testcase | PASS-FAIL-NOT RUN | Testmetode | Miljø | Bevislenke | Bemerkning |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | Ingen sosial-/demobrukere eller helsegevinstpåstand | PASS | Kode-/innholdsgjennomgang av levering og tre appfaner | Runtime-kode og Chromium | [plugin](../plugin/gymnotfound/gymnotfound.php), [maler](../plugin/gymnotfound/content/activities.json), [nettleser](../evidence/browser.txt) | Vanlig frivillig selskap er en aktivitet, ikke appens venneinfrastruktur. |
| E2 | Generelle valg, ingen skjult klinisk profil | PASS | Motortest alle preferanser, lagrings-whitelist og gjennomgang | Node/PHP | [unit](../evidence/unit.txt), [backend](../evidence/integration.txt) | Tid/energi/miljø/feedback, ikke diagnose/alder/kjønn. |
| E3 | Faglig port og samme flyt for rutineanker | PASS | Ureviewet/gjenkjent skjult; gyldig revisjon; ugyldig dato/kilde/sikkerhet/hash; endring; offline og gammel pending-tittel | WP + Node + Chromium | [backend](../evidence/integration.txt), [unit](../evidence/unit.txt), [nettleser](../evidence/browser.txt) | Ingen instruerende kort i seed. Ordguard erstatter ikke faglig gjennomgang. |
| E4 | Admin capability + nonce; private options skjult | PASS | REST og faktiske admin-post-feil uten nonce/innlogging | WP + installert ZIP | [backend](../evidence/integration.txt), [ZIP-test](../evidence/zip-install.txt) | Uautorisert route/data avvises før endring. |
| E5 | Faste eksterne adresser, SSRF og XSS | PASS | Malformed URL/koordinater/search/HTML; TLS/redirect-args; rendret tekst | WP + Chromium | [backend](../evidence/integration.txt), [nettleser](../evidence/browser.txt) | wp_remote_get med eksakt intern HTTPS-allowlist og null redirects; ingen klient-URL. |
| E6 | Lokal eksport/sletting og forståelig personvern | PASS | Faktisk JSON og dialog + dokumentgjennomgang | Chromium | [nettleser](../evidence/browser.txt), [personvern](PERSONVERN.md) | Hostinglogger og korte saltede rate-limit-hasher er beskrevet. |
| E7 | Komplett norsk/engelsk, også feil/tom/slett | PASS | Begge komplette flyter og axe på alle tre sider; ordliste | Chromium/Node | [nettleser](../evidence/browser.txt), [ordliste](../plugin/gymnotfound/assets/locales.js) | Stedsnavn forblir kilde-/egennavn. |
| F1 | 320/360/390/768/1024/1440, tastatur og kontrast | PASS | Ingen overflow; synlig fokus; axe WCAG 2/2.1/2.2 AA-tags og visuell inspeksjon | Chromium | [nettleser](../evidence/browser.txt), [mobil](../screenshots/chromium-390-nb.png), [desktop](../screenshots/chromium-1440-nb.png) | WCAG 2.2 AA er testmål, ikke en sertifisering eller full skjermleserrevisjon. |
| F2 | Reduced motion og NIM av | PASS | emulateMedia reduced-motion, DOM/layout og preferanse | Chromium | [nettleser](../evidence/browser.txt) | Ingen obligatorisk animasjon. |
| F3a | Moderne Chromium | PASS | 17 E2E-/layout-/tilgjengelighetstester | Chromium 154 | [nettleser](../evidence/browser.txt), [JSON](../evidence/browser-results.json) | Begge språk, åpen-app offline og nektet lagring. |
| F3b | Andre browser: Firefox | NOT RUN | Offisiell nedlasting; faktiske oppstartsprober feilet før page-tilkobling | Firefox 142.0.1/Playwright 1495 | [oppstartsbevis](../evidence/firefox-not-run.txt) | Skrivebeskyttet /proc, fontcache/grafikk/sandbox; ingen påstått app-kompatibilitet. |
| F4 | PHP lint og WordPress Plugin Check | PASS | Faktisk container-PHP og Plugin Check 2.1.0 | WP 7.1.3/PHP 8.3 | [lint](../evidence/php-lint.txt), [Plugin Check](../evidence/plugin-check.json) | Reviewed inline-ignore bare for nødvendige DB-mutexer og allerede escapet statisk shell-markup. |
| F5 | Full mobil-E2E og installasjonsguide uten terminal | PASS | Anonym → valg → prøv → gjort → feedback → eksport → slett; faktisk WP-upload | Chromium/ZIP-stakk | [nettleser](../evidence/browser.txt), [ZIP-test](../evidence/zip-install.txt), [guide](INSTALLASJON.md) | Hostingdelen trenger ingen utviklingsverktøy. |
| F6 | Ingen produksjonsinstallasjon eller merge | PASS | Isolerte loopback-stakker og åpen PR til separat eiergjennomgang | Lokal test/GitHub | [Compose](../compose.yaml), [ZIP-Compose](../compose.zip.yaml) | Produksjon, offentlig pilot og merge er ikke autorisert eller utført. |
| COMPAT-1 | Separat WP 6.7/PHP 8.2-minimum | NOT RUN | Ekstra image-pull stoppet av midlertidig plassmangel; eksisterende teststack brukt | Minstekombinasjon | [begrunnelse](../evidence/external-not-run.txt) | Faktisk testet 6.8.3/7.1.3 med PHP 8.3, ikke minstekombinasjonen. |

## Praktiske grenser

En allerede åpnet app fortsetter med generiske ideer uten nett. Førstegangsbesøk/reload offline trenger WordPress-forbindelse; ingen service worker er lovet eller installert. Delte Geoapify-cacher kan brukes til utløp også når nye kall stanses med kvote null. Kildetest på et annet webhotell, reell Geoapify-nøkkel, Firefox/andre nettlesere og en faktisk skjermleser bør verifiseres i en separat godkjent pilot.

Betaversjonen er en implementert og lokalt verifisert ZIP/PR-leveranse. Rapporten gir ingen produksjonsklarhets- eller publiseringstillatelse.

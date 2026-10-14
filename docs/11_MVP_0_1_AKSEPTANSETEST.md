# GymNotFound 0.1.0-beta.1 – bindende akseptanse- og testplan

**Dato 14.10.2026.** Dette dokumentet er release-gate for **første** installérbare plugin. Går foran den eldre 5.0-testplanen når kravene gjelder utsatte funksjoner. Produktomfang er dokument 10_MVP_0_1_AKTIVITETSKAMERAT.md.

## Leveranse-gate: alt P0 må bestå i reelt miljø

### A. Installasjon / WordPress / admin
- [ ] ZIP dist/gymnotfound-0.1.0-beta.1.zip eksisterer, kan pakkes ut og installeres via WP-admin på ren WP 6.7+ / PHP 8.2+ uten shell/npm/composer på webhotellet.
- [ ] Aktivering og deaktivering gir ingen PHP-fatal, duplikate sider eller feil i eksisterende temaer. Pluginen oppretter appside KUN når admin ønsker det.
- [ ] Plugin-header, navn og slug er GymNotFound/gymnotfound; frontend virker i selvstendig mobilapp-skall og minst én enkel WP page-integration.
- [ ] WP-admin finnes med: settings, integrasjonsstatus, sikker nøkkellagring, 36 redigerbare maler (norsk + engelsk), fallback/test og tydelig «forhåndsvis».
- [ ] Ingen secrets, API-nøkler, e-post, persondata eller privat GPS i JS-bundle, REST-responser, PHP-logger eller testfixtures. Ingen API-nøkkel kreves for generisk bruk.

### B. Første opplevelse / kort mobilflyt
- [ ] På 390x844 vises ett komplett aktivitetskort, én hovedhandling og «Ny idé» på første skjerm. Ikke stor illustrasjon som skyver kortet nedenfor skjermen.
- [ ] Gjest kan åpne direkte uten registrering og UTEN å gi posisjon. Får fungerende anbefaling på engelsk eller norsk.
- [ ] Tid 2 / 10-15 / 30+ og energi lav / litt / høy påvirker hvilken aktivitet som vises. Endringer krever maks to enkle trykk, ingen lange skjemaer.
- [ ] «Ny idé» gir forskjellig, gyldig aktivitet i rimelig antall forsøk (test minst 8 påfølgende valg) uten identiske overskrifter hele tiden; konteksten må fortsatt passe.
- [ ] «Jeg gjør det» registrerer IKKE completed. «Gjort» registrerer eksplisitt completed_self_report. «Passet ikke» endrer neste forslag og huskes lokalt. «Ikke nå» utløser ingen skyld, straff eller påminnelse.
- [ ] Gjenåpning etter lang pause: ingen mistet streak/negativ maskot, egne gamle fullførte handlinger ligger lagret i samme nettleser.
- [ ] «Min vei» viser kun egenrapportering, ingen oppdiktede timer/skritt/medisinsk gevinst. Eksport JSON og slett med bekreftelse fungerer.
- [ ] «Legg bort mobilen»-tilstanden kan avsluttes uten timer eller påtvunget ny appinteraksjon.
- [ ] NIM av/på virker, ingen manipulerende replikker; appen fungerer fullt uten maskot.

### C. By / på landet / ingen stedsdata: automatiserte scenarier
Scenario C1 – «by»: fixture med 12 navngitte POI-er (kafé, park, bibliotek, museum, kultursted) innen gitt radius; 15 minutter, litt overskudd, oppholdsvær. Appen kan foreslå ett RETT sted fra datakilden, kilde og Maps-lenke. Ingen fantasisteder.
Scenario C2 – «landlig»: fixture 0 kafeer og 0 museer; 2 parker / kjent offentlig besøkssted og ellers naturpunkter. Appen MÅ IKKE foreslå kafé eller museum. Den kan foreslå faktiske tilgjengelige stedstreff eller generisk selvstendig uteaktivitet.
Scenario C3 – «svært spredt»: null POI-er i 10 km radius. Må få minst tre forskjellige generiske aktiviteter som ikke krever sted, transport, kjøp eller kart.
Scenario C4 – «stadig avslag»: bruker velger «Passer ikke» to ganger for samme familie. Neste forslag bytter aktivitetstype eller sted, aldri samme tekst om igjen uten forklaring.
Scenario C5 – «dyrt / privat / stengt ukjent»: tilbyderdata har kostnad, adgang eller åpningstid ukjent; appen lover ikke at stedet er åpent eller gratis; den filtrerer privat/utrygt og følger gratispreferanse.
Scenario C6 – «avstand»: hvis koordinatavstand angis, står «luftlinje»; ingen oppdiktet gangtid eller gå-/kjørerute. Ekstern Google Maps URL dannes gyldig og trygt.
Scenario C7 – «brukerstyrt miljø»: manuell innstilling «på landet» gir egnet stil også når POI ikke er tilgjengelig. Automatisk kategorisering må aldri trumfe et uttrykkelig brukerønske.

### D. Vær og integrasjons-fallback
- [ ] Med MET-fixture for sol/opphold, regn, sterk vind, kulde og ukjent vær velger motoren relevante ute-/innealternativer. Ved dårlig vær skal det fortsatt være et ekte alternativ.
- [ ] MET forespørsel er server-side med identifiserende User-Agent, maks 4 desimaler, følger Expires/Last-Modified, har timeout/backoff og viser lisenskreditering.
- [ ] Ingen posisjon: INGEN skjulte MET/Geoapify-kall; første skjerm virker.
- [ ] MET 403 / 429 / 500 / timeout: appen gir fortsatt et relevant forslag, ingen tom side, spinn som aldri stopper, eller oppdiktet vær.
- [ ] Geoapify IKKE konfigurert: ingen POI-forespørsler, ingen oppdiktede stedstreff, full appfunksjon med generiske aktiviteter.
- [ ] Geoapify 200 med treff: normaliser id/kategori/posisjon/attribusjon og vis relevant ekte sted. 200 tomt: fall tilbake.
- [ ] Geoapify 401/403/429/500 og administrativ kredittgrense: ingen ukontrollert retry, ingen betalingskrav, fall tilbake. Ikke lekk API-nøkkel i svar/logg.
- [ ] Første forespørsel / samme avrundede område fem ganger: tilsiktet cache hit, ikke fem kostbare provider-kall.
- [ ] Posisjon gitt og fjernet: slett brukerens posisjonshistorikk/lokale preferanse når vedkommende ber om det; ingen bakgrunnsinnsamling.
- [ ] Eksterne krediteringer vises: MET Norway, Geoapify og OpenStreetMap for relevant output. Uten databruk vises ikke misvisende kreditering.
- [ ] Direkte livetest mot MET med gyldig User-Agent hvis testmiljø har internett. Direkte Geoapify-test bare hvis legitim API-nøkkel er satt; ellers oppgi NOT RUN, IKKE PASS.
- [ ] Test både stadig repeterte eksterne forespørsler, respons-grenser, rate limit for offentlige REST-ruter og HTML-/input-injeksjon via POI-navn.

### E. Sikkerhet, personvern og innhold
- [ ] Ikke implementert sosial-/demo-venner. Ingen påstand om velferd/helseeffekt.
- [ ] Anbefaling av aktivitet baseres på generelle preferanser, ikke diagnose, alder eller skjulte profiler.
- [ ] Konkrete styrke-/balanseøvelser som krever faglig sjekk skal IKKE være synlig offentlig uten godkjent revisjon; tester verifiserer publiseringsport. Integrerte «rutineankre» er ikke egen hovedfane.
- [ ] Admin-endepunkter krever capability og nonce, og private options vises ikke til anonyme brukere.
- [ ] Alle eksterne serveradresser er fast konfigurert, ikke klientstyrte URL-er; SSRF-håndtering og XSS sanitisering/escaping er testet.
- [ ] Gjestens egne lokale data kan eksporteres/slettes; personverntekst forklarer datakilder, formål og at historikk er per nettleser.
- [ ] Norsk og engelsk er komplett nok til å gjennomføre hele flyten. Feilmeldinger, tomtilstand og slettedialog er oversatt.

### F. Tilgjengelighet / layout / installasjonsklar ZIP
- [ ] Ingen horisontal scrolling / skjulte knapper på 320, 360, 390, 768, 1024, 1440 px. Bruk skjermleserlabels, riktig tastaturfokus, synlig fokusmarkering og trygge kontraster.
- [ ] prefers-reduced-motion respekteres. NIM av gir ikke tomlayout.
- [ ] Testet i minst moderne Chromium og én annen browser dersom testmiljø tillater det; oppgi faktisk matrise.
- [ ] PHP lint og WordPress Plugin Check kjørt i virkelig miljø dersom mulig; hvis ikke, markér eksplisitt NOT RUN og hvorfor.
- [ ] Mobil E2E minst: anonym => velg tid/energi => forslag => plan => lagre fullført => feedback => nytt relevant forslag => eksport => slett.
- [ ] Dokumentert manuell installasjonsguide som ikke forutsetter terminal på One.com / WordPress webhotell.
- [ ] Ingen produksjonsdeploy eller merge uten uttrykkelig eiergodkjenning.

## Gjennomføring og statusformat

Codex skal levere en testmatrise med kolonnene: ID / testcase / PASS-FAIL-NOT RUN / testmetode / miljø / bevislenke / bemerkning.
Gjenbruk fake/provider-fixtures KUN i automatiserte tester, og hold tydelig produksjonsmodus uten fiktive personer/steder. Fravær av reell leverandørtest MÅ fremgå.

Før «klar til installasjon på lukket testdomene» er tillatt:
1. En ekte installérbar ZIP (ikke bare dokumentasjon eller HTML) er generert og kontrollert.
2. Alle P0-kjerne- og feilscenarier består med reelt kodeeksekveringsbevis, og kjente ikke-beståtte feil er utbedret.
3. Systemet virker helt uten Geoapify-nøkkel og selv uten MET-respons.
4. Eieren har godkjent installasjon separat. Ingen automatisk publisering.

Milepæler for intern utvikling, uten splitting av produktet:
- M1: Plugin-skjelett, admin, første kort, norske/engelske generiske maler; ZIP installerer.
- M2: Regelmotor, lokal historikk, feedback, NIM.
- M3: MET-væradapter, Geoapify-adapter med fallback, stedskategorisering og Google Maps URL-lenker.
- M4: hardening, tests, docs, ZIP, PR.
Det er én sammenhengende app med én anbefalingsmotor fra første milepæl.

**CI-kostnadsregel:** Ikke opprett tunge Actions-jobber som kjøres ved hvert push. Lokale tester først; en lett jobb på PR og eventuelt manuell full suite. Oppgi eksakt hva som er kjørt.

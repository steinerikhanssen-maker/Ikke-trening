# OPPDRAG TIL CODEX – IKKE TRENING 5.0 (installerbar WordPress-beta)

## Rolle og hovedordre

Du er ansvarlig utvikler/arkitekt for et nytt, **selvstendig** WordPress-produkt med arbeidsnavn **IKKE TRENING**. Lever en faktisk fungerende, installerbar WordPress-plugin som gir en mobiltilpasset webapp med atferdshjelp, maskoten NIM, fortellingsspill og ekte frivillig vennefunksjonalitet. Dette skal installeres av en ikke-teknisk eier via WP-admin på et isolert testdomene. Det skal ikke være en statisk HTML-prototype pakket inn i en plugin.

Bruk de medfølgende dokumentene som normative kilder i denne rekkefølgen:
1. `01_KRITISK_EVALUERING.md` – hva som er galt med 4.1 og hvilke beslutninger som er tatt.
2. `02_PRODUKTKRAV_5_0.md` – fullstendig funksjonell leveranse.
3. `03_TEKNISK_ARKITEKTUR_WORDPRESS.md` – teknisk arkitektur, sikkerhet, lagring, WordPress-integrasjon.
4. `04_AKSEPTANSEKRAV_OG_TESTPLAN.md` – P0-gates, konkrete testscenarier.
5. `07_HVERDAGSANKRE_OG_MIKROBEVEGELSE.md` – **normative P0-krav for integrerte aktiviteter**: vanekobling, sikker mikroaktivitet og faglig publiseringsport.
6. `08_PRESISERING_INTEGRERT_AKTIVITET.md` – **obligatorisk brukeravklaring**: ikke bygg en separat synlig modul, fane eller sideflyt for «exercise snacks».
7. `kilder_prototype_4_1/` + `dokumentasjon/` – referansekode/eksisterende design og tidligere faglig grunnlag.

Ved konflikt: sikkerhet/personvern og 04 > 07 (øvelsessikkerhet) > 08 (produktintegrasjon) > 03 > 02 > 01 > kildeprototypen. Den gamle prototypen skal inspirere, **ikke** kopieres ureflektert. Ikke bland prosjektet med Viamo, Husvarme eller HighBias.

## Beslutninger som ikke skal diskuteres på nytt uten et konkret blockerfunn

- Lag **én WordPress-plugin-ZIP** `ikke-trening-0.1.0-beta.1.zip` med ferdigbygde CSS/JS/illustrasjoner og innebygget visuelt appskall. **Ikke krev et eget WordPress-tema.** Støtt både en egen fullskjerms appside og et shortcode-/Gutenberg-alternativ.
- Frittstående WordPress-DB og WP-kontoer. **Ingen betalte API-er, AI-tokens, abonnementer, tredjepartsfont/CDN eller andre nye faste utgifter.** Ikke krev build-verktøy på webhotellet.
- Lag ekte backendløsninger for egen historikk, handlingstyper, fortellingsprogresjon, private vennegrupper og konto. Ingen falsk serverpersistens eller simulerte venner i ekte kontoer.
- **Integrert kjerneprinsipp (presisering fra bestiller):** «Exercise snacks»/aktivitetsdrypp og frivillige hverdagsankre er **førsteklasses aktivitetsalternativer i den SAMME handlings- og motivasjonsmotoren** som turer, ærend, opplevelser, sosial aktivitet, planlegging og gjenstart. For eksempel kan «etter tannpuss» eller «etter kaffe» være dagens **primære forslag**. IKKE lag et eget synlig trenings-/mikrobevegelsesområde på siden, ekstra obligatorisk meny, egen onboarding eller konkurrerende gamification/logg. Brukervalg kan knytte aktiviteter til rutiner uten at appen må åpnes ved hver gjennomføring. Ingen trening i våt dusj, ingen medisinsk personalisering ut fra bare kjønn/alder og ingen automatisk tolkning av rutiner. Kun faglig reviderte bevegelseskort får publiseres; se 07 og 08.
- Behold fagmodellen fra 4.0: identifiser type hindring og velg passende type støtte **før** fysisk aktivitet foreslås. Maskot, historier og gruppe er **valgfrie lag**.
- Ingen tapsrekker, dårlig samvittighet, barnslek eller medisinske påstander. App skal fungere med maskoten helt avskrudd.
- Skriv naturlig norsk, redaksjonelt faktisk innhold; minst **24 kapitler fordelt på to verdener** i betaen, redigerbare i WP-admin. Gjenbruk original NIM-design som start, men øk profesjonaliteten.
- Hovedoppdrag synlig uten lang scrolling i innlogget mobilvisning. God webapp-utseende for voksne.
- Ikke sett i produksjon, installer på annet nettsted, opprett offentlig WP-side, aktiver offentlig registrering eller endre DNS uten brukerens uttrykkelige godkjenning.

## Gjennomføringsrekkefølge i samme nye repository

**M1 – WP-fundament**
- Opprett pluginfiler, namespacede PHP-klasser, aktiveringslogikk, tabellmigrering, minst én WP-adminside, appside i fullskjerm, Gutenberg-blokk og shortcode, samlet build pipeline med bundlet JS/CSS. Vis demo-/guest-landing og innloggingsskall. Oppdater README.

**M2 – ekte kjernefunksjonalitet**
- Brukerprofil, type hindring, forklarbar rekommanderingslogikk som **kan velge mikrobevegelse ved eksisterende rutine som første forslag på nøyaktig samme «I dag»-skjerm som annen aktivitet**, registrering av forsøkt/planlagt/gjennomført/hvilt/avvist, privat persistens, gjenstart, ingen falsk aktivitetsregistrering. Lag REST-ruter med ekte eierkontroll. Skriv domeneenhetstester.

**M2B – ferdigstill det integrerte hverdagsankerdomenet (P0, internt arbeidssteg før spillbelønning)**
- Bygg `EverydayAnchors` som **intern kode-/datakomponent i den allerede felles M2-motoren**, IKKE separat synlig funksjonsmodul. Legg til anker-CRUD, publiseringsstyrt `ikt_movement`-bank, trygg «Når jeg …»-flyt i ordinære forslag/planer, egne typer egenrapporterte hendelser i **samme** aktivitetslogg, sensorbegrensningsforklaring og eier-/idempotens-tester. Bruk samme tilbakemelding, gjenstart og rapport-/belønningsmotor, med én dagsbonus på tvers av aktivitetstyper. Følg `07_HVERDAGSANKRE_OG_MIKROBEVEGELSE.md` og `08_PRESISERING_INTEGRERT_AKTIVITET.md`.
- **Faglig innholdsport:** Codex skal ikke hevde å være fysioterapeut eller godkjenne øvelser på egen hånd. Før redaksjonell kvalitetssikring foreligger kan administrator teste kortene i tydelig merket sandkasse; vanlige brukere skal ikke få ferdige bevegelsesinstrukser fra en upublisert bank. Gi eier eksakt liste over kort som må faglig kontrolleres.

**M3 – spill / maskot / innhold**
- NIM som original responsiv SVG, 3 visuelle varianter, av/på, prefers-reduced-motion. 2 verdener / 12 kapitler hver, WP-redigering, personlig kart, opplåsing kun av servergodkjent selvrapportert gjennomføring, maks 1/dag; ingen tap ved pause. Løs tomme slutt-/låsestatus.

**M4 – ekte vennedel**
- Gruppe 2–4, engangsinvitasjon med utløp, aksept, opt-in bidragsdeling, asynkrone gruppebidrag og utmelding. Ingen personlige aktivitetsminutter, lokasjonsdata eller negative sammenligninger. Sikkerhetstester med to kontoer.

**M5 – personvern, tilgjengelighet, polering**
- GDPR-funksjoner, eksport/sletting, WP privacy hooks, administrasjonsinnstillinger og personverntekst. Full mobil-UX, tilgjengelighetstester, rollesikring, feil-/tomtilstander. Ingen eksterne tracking scripts.

**M6 – release/gate**
- Ferdig installérbar ZIP, release notes, screenshot, testlogg, manuell installinstruks. Dokumentér testet WordPress/PHP-konfigurasjon. Kjør alle P0-tester fra 04. Hvis testen krever WordPress du ikke kan starte, rapportér `NOT RUN` og lever en eksakt lokal prosedyre i stedet for å late som den er kjørt.

Milepæler kan være egne små PR-er dersom arbeidsmiljøet tilsier det, men sluttmålet er **en samlet testbar beta**, ikke kun de første sidene. Ikke stopp etter designskisser eller bare en aktivitetskatalog. Bruk PR-er/review fremfor å merge på `main` automatisk. Bruk skånsomt GitHub Actions-oppsett med lokalt kjørte tester og ingen kostbar matrix på hvert push.

## Teknisk implementasjonsfrihet – innenfor klare rammer

Du kan velge en liten reaktiv frontend eller moderne React/Vite hvis resultatet blir robust. ZIP skal likevel ha ferdigbygde assets og ikke kreve Node på serveren. Bruk WordPress' standardbrukere, REST API, capabilities, cookie auth, WP nonce, usermeta for begrensede innstillinger, custom tables for voksende historikk og CPT for redaksjonelle kapitler. Oppsettveiviser i wp-admin skal gjøre installasjon mulig for en ikke-teknisk eier. CSS må være isolert fra WordPress-temaet og fra andre plugins.

Sosiale invitasjoner og datalesing må ha eier-/medlemskapskontroll på hver private REST-rute. Test IDOR/CSRF/XSS og sletting. Ikke bare skjul knapper i frontend. WordPress' personverneksportør og -sletter skal støtte dataene.

## Førstegangsskjermen

Prioriter den umiddelbare nytten: en kort velkomst, et tydelig hindringsvalg og ett relevant forslag – **som ut fra konteksten like gjerne kan være hverdagsforankret mikrobevegelse som gåtur eller praktisk oppgave**. Den store eksisterende hero-maskoten og markedsføringsteksten fra 4.1 skal **ikke** stjele første skjermhøyde for innloggede brukere. La maskoten være kompakt og sympatisk. Verdenskart, venner og historikk ligger sekundært.

## Definition of Done

1. Installérbar ZIP uten server-build.
2. Et oppsett i wp-admin som lar eier lage en valgfri testside, redigere hverdagsankre/bevegelseskort og styre faglig publiseringsstatus.
3. Ekte to-kontotest: hver konto ser bare egne data; opprett invitasjon, akseptér, del ett bidrag, meld deg ut.
4. **Én fungerende integrert anbefalings-/plan-/rapporterings-/gjenstartflyt**, der **hverdagsankre med trygg mikroaktivitet er likestilt med andre aktiviteter**. Ikke belønn plan eller start. Ingen separat mikrobevegelsesfane.
5. NIM av/på, to komplette verdener, historiefremgang riktig etter dagbegrensning.
6. Gyldig norsk UI og responsiv mobil. Ingen JS/PHP-fatal.
7. Privat eksport og slett appdata; security checklist bestått.
8. Testrapport med PASS/FAIL/NOT RUN og ingen overdrivelser.
9. Bare isolert testdomene ved eventuell senere installasjon; ingen produksjonsendring på eget initiativ.

## Når du er ferdig, lever nøyaktig dette

- `dist/ikke-trening-0.1.0-beta.1.zip` – WordPress-plugin klar for WP-admin-opplasting.
- Git-repository med redigerbare kildefiler, låste avhengigheter, byggeinstruksjon, migreringer, server- og frontendtester.
- `docs/INSTALLASJON.md`, `docs/ARKITEKTUR.md`, `docs/TESTRAPPORT.md`, `docs/PERSONVERN.md`, `CHANGELOG.md`.
- Skjermbilder av innlogget mobil, desktop, oppdrag, **hverdagsanker og mikrohandling**, historie, virkelig vennestatus, WP-admin og guest landing.
- Kort oppsummering av nøyaktig hva som er implementert, hva som mangler og hvilke tester som ble kjørt.

**Start nå med M1. Ikke be om mer spesifikasjon med mindre en faktisk blocker oppstår.** Hold målbildet M1–M6 samlet, slik at enkeltmoduler ikke motarbeider hverandre. Ingen fiktiv «ferdig»-rapport. Bruk norsk i sluttstatus.
# IKKE TRENING 5.0 – Hverdagsankre og mikroaktivitet (normative produktkrav)

**Oppdatert:** 13.10.2026. **Status:** Beslutning og Codex-spesifikasjon – ikke en påstand om klinisk validering. Les dette som del av `02_PRODUKTKRAV_5_0.md`, `03_TEKNISK_ARKITEKTUR_WORDPRESS.md` og `04_AKSEPTANSEKRAV_OG_TESTPLAN.md`. Ved konflikt gjelder sikkerhet, personvern og 04 før dette dokumentet.

## 1. Hvorfor dette er en integrert del av produktkjernen

**Bestillers presisering:** Dette dokumentet er en egen **teknisk og faglig kravbeskrivelse**, men «exercise snacks»/aktivitetsdrypp skal **IKKE** oppleves som en modul ved siden av hovedappen. Hverdagsankre og mikrobevegelser er en likestilt aktivitetstype i **den samme** atferds-, anbefalings-, plan-, rapporterings- og gjenstartmotoren som turer, ærend, historier og sosial aktivitet. Ved relevant hindring (som startfriksjon eller tidsklemme), valgte rutiner og trygg tilgjengelig aktivitet kan dagens **primære** forslag være en mikrobevegelse. Ingen separat hovedfane, egen parallell onboarding, særskilt gamification-valuta eller påtvunget «mikroprogram». Internt kan koden deles i komponenter for sikkerhet og vedlikehold. Se `08_PRESISERING_INTEGRERT_AKTIVITET.md`.

En bruker kan ha sterke interesser og likevel mangle anledning eller lyst til å «trene». Vedkommende har derimot allerede hverdagsrutiner: sette på kaffe, avslutte tannpussen, reise seg fra sofaen, gå mellom rom eller avslutte et måltid. Korte bevegelser koblet til selvvalgte, eksisterende hendelser senker oppstartskostnaden og kan bidra til regelmessighet. De brukes når de faktisk passer personens mål og hverdag – ikke som en generell erstatning for tur, styrke eller annen aktivitet.

Faglig skille:

- *Exercise snacks* er korte, ofte strukturerte aktivitetsøkter. En BJSM-gjennomgang (11 RCT-er, 414 personer) fant lovende forbedringer i kondisjon for voksne og muskulær utholdenhet for eldre; evidenssikkerhet lav/svært lav på flere utfall. Meta-analyse 2026 (11 RCT-er/472 deltakere) fant bl.a. forbedring i 60-sekunders stol-til-stå-resultat, men begrenset studiegrunnlag. Dette er **ikke** direkte evidens for våre eksakte øvelser eller dose.
- En RCT med 90 eldre med redusert styrke/balanse rapporterte forbedring etter 12 uker progressiv styrke-/tai chi-snacking; funnene kan ikke ukritisk overføres til alle.
- En metaanalyse fra 2026 om faste kontekster (14 studier, 6 069 personer) fant små korrelasjoner med fysisk aktivitet og vanestyrke. Rutineanker er plausibelt, ikke bevist som akkurat vår løsning.
- En 2026-metaanalyse av *exercise snacks* fant **ikke sikker forbedring av VO₂maks i undergruppen over 50 år**, og resultater på styrke/metabolske mål varierte. Ikke lov spesifikk helsegevinst fra denne aktivitetstypen.
- Helsedirektoratet: all aktivitet teller; få minutter kan være en god start. Men styrke for store muskelgrupper minst 2 dager/uke og samlet 150–300 minutter moderat aktivitet/uke er fortsatt overordnede anbefalinger for voksne, tilpasset den enkeltes kapasitet. Mikrohandlinger teller ikke automatisk som fullverdig styrketrening.

## 2. Brukeropplevelsen (P0)

### 2.1 Finn en allerede eksisterende rutine

**Samme «I dag»-flyt:** Anbefalingsmotoren kan foreslå en hverdagsforankret bevegelse direkte som dagens handling. Brukeren kan også bytte forslag og velge «knytt til noe jeg allerede gjør» i ordinær plan-/tilpassflyt. Ikke opprett en separat hverdagsaktivitet-fane eller forlang at brukeren går til en annen modul. Brukeren kan om ønskelig velge ett eller to ankre som passer, eksempelvis:

- **Etter at kaffen er satt på** – bare dersom man kan stå trygt bort fra varme apparater.
- **Etter tannpussen** – etter at tannbørsten er lagt fra seg, ikke balansetrening med munnen full eller hendene opptatt.
- **Når jeg reiser meg fra sofaen** – en ekstra kontrollert oppreisning / kort ekstra runde.
- **Når jeg går gjennom stua** – ta en liten ekstra runde på fri og trygg gulvflate.
- **Etter at jeg har dusjet, og gulvet er tørt** – et signal for aktivitet *utenfor* dusjen.
- **Etter lunsj / før jeg setter meg ved PC-en** – et selvvalgt rutinepunkt.
- **Eget anker** – kort egen tekst, uten fritekst om sykdom og uten at appen tolker hvilken hendelse som faktisk har skjedd.

Brukeren skal kunne avstå fra ankre, endre ankre, sette dem på pause eller slette dem. Ingen daglig kravliste. Ingen "kaffen må starte kl. 08:00" – det er et situasjonssignal, ikke automatisk sensordeteksjon. I denne WordPress-betaen oppdager ikke appen faktisk tannpuss, dusj eller kaffe; det må forklares tydelig.

### 2.2 Velg en passende mikrohandling

Appen foreslår én kvalitetssikret mikrohandling for ankeret (tilpassbar varighet, svært lav terskel) og kan tilby «et enklere alternativ», «annet forslag», «ikke nå» og «dette passer ikke kroppen min». Ikke mer enn én anbefaling om gangen. Før registrering velges om man faktisk gjennomførte. **Å opprette anker, se instruks, velge start eller lagre avtale teller ikke som aktivitet.**

Foreslåtte **startmaler** for intern demonstrasjon, ikke medisinske forskrivninger:

| Bevegelsesfamilie | Forslag til mikrohandling | Kontekst og beskyttelse |
|---|---|---|
| Underkropp / funksjon | Reis deg rolig fra en stødig stol og sett deg kontrollert | Stabil, sklisikker stol uten hjul; bruker velger egen komfortabel dose; stopp ved ubehag |
| Press / overkropp | Rolige armhevinger mot en solid vegg | Stabil vegg, godt fotfeste; unngå ved smerter som provoseres |
| Legger | Rolige tåhev med begge føtter og fast støtte | Tørt gulv, to hender fri ved behov; **ikke** på vått baderomsgulv |
| Lett hverdagsaktivitet | Gå en ekstra liten runde på ryddet gulv | Ingen snublefare, personlig tempo |
| Trekk / øvre rygg (frivillig) | Enkel roøvelse med elastisk treningsstrikk | Krever egen strikk, riktig feste og faglig godkjent instruks; **ikke seed som standard uten kontroll** |

Disse dekker **ikke automatisk alle store muskelgrupper**. Appen skal vise et enkelt aktivitetsmønster som forskjell mellom «du har fått inn noen små bevegelser» og «du har et tilstrekkelig styrke-/utholdenhetsopplegg». Frivillig progresjon mot mer helhetlig aktivitet kommer i eget spor og må kvalitetssikres faglig.

Ingen faste kjønnsspesifikke øvelser. Alder alene er ikke grunnlag for intensitetsvalg. Bruk i stedet selvvalgt trygghetsnivå, funksjonsevne og gjennomføringsrespons. Ikke spør etter diagnose eller medisinsk historie for å drive anbefalingsmotoren. Hvis brukeren oppgir skjevstilling/ryggproblem, leddplager, balanseproblem eller andre funksjonelle begrensninger, tilbys kun trygg, generell informasjon eller råd om vurdering hos kvalifisert helsepersonell – **ikke automatisk spesialprogram**.

### 2.3 Beslutningsflyten i appen

1. Samme anbefalingsmotor som ellers velger type støtte/aktivitet; når rutinebevegelse passer, foreslås anker og en bevegelse fra den kvalitetssikrede katalogen direkte på «I dag». Brukeren kan også selv velge «knytt til rutine». Ingen påtvunget påminnelse.
2. Systemet foreslår en betinget formulering: **«Når jeg har satt fra meg tannbørsten, gjør jeg noen rolige tåhev ved en fast benk – hvis det kjennes greit.»**
3. Bruker kan velge «passet», «vil prøve senere», «for tungt», «ubehag», «nei takk», eller «gjennomført».
4. Ved gjennomført: ett eget `completed`-event knyttet til anker + bevegelse, med antall repetisjoner **eller** varighet i sekunder som **egenrapport** (ikke verifiserte repetisjoner eller styrkeeffekt). Beholder `reported_minutes = NULL` dersom kun repetisjoner er rapportert.
5. Ved negativ tilbakemelding foreslås lettere variant, annen bevegelsesfamilie, endret sted eller pause. Aldri automatisk høyere belastning.
6. «Min vei» viser ankerutførelse/frekvens adskilt fra aerobic-minutter, styrkedager og spill. Ikke summer rå repetisjoner som aktivitetsminutter eller hev at 3 tåhev er dokumentert helseeffekt.
7. Oppdagelsesreise/NIM får *høyst ett dagsbidrag* fra samlet registrert aktivitet etter serverreglene, enten det er hverdagsanker, gåtur eller annen aktivitet. Ingen dobbeltelling og ingen premiumpoeng for å dele en rutine i mange små innrapporteringer.
8. Brukeren kan gjenoppta et tidligere anker etter uker uten logg uten tap av kapittel eller dårlig samvittighet. Fravær fra app betyr ikke nødvendigvis inaktivitet.

## 3. Sikkerhet og innholdsforvaltning (P0)

- **Ikke gi instrukser om øvelser inne i en våt dusj.** «Dusj» kan brukes som tidsanker først *etter* at personen står på tørt, trygt underlag og er ferdig med hygiene. Ingen ettbeinsøvelser eller balanseutfordringer når en hånd er opptatt under tannpuss eller man håndterer kokende vann.
- Ingen øvelser som krever utrygge møbler, glatte fliser, ustabile benker, skjulte vekter, hodestående eller automatisk høy intensitet. Filtrer risikofulle handlinger etter kontekst, ikke vis belønning for å ignorere kroppslige faresignaler.
- Stopp aktiviteten ved smerter, svimmelhet, uvanlig tung pust eller ubehag; ved alvorlige symptomer må brukeren søke medisinsk hjelp. Ingen diagnostisk beslutningsstøtte i appen.
- Tilleggskort som spesifikt foreskriver styrke, balanse eller belastning for skader/helsetilstander skal **ikke publiseres før faglig gjennomgang**. Redaksjonelt skjema i WP-admin skal ha navn på ansvarlig fagrevisor, revisjonsdato, kildelenker, versjon, tekst om forutsetninger, skriftlige instruksjoner, tryggere alternativ og når man skal avstå/søke råd. Øvelsesbank skal kun bruke redaksjonelt gjennomgått, publisert innhold; uferdige kort i `draft` er ikke tilgjengelige for vanlige brukere.
- Dersom kvalifisert øvelsesgjennomgang **ikke** er dokumentert, må funksjonen for bevegelsesinstruksjoner være **avskrudd for offentlig pilot**. Codex skal likevel implementere hele modulens administrasjon og flyt i testmodus med tydelig varsel. Det er **ikke** lov å utstede egen faglig godkjenning fra Codex.
- Ingen bilder eller animasjoner som kan forveksles med korrekt faglig teknikk før de er kontrollert. Unngå copyright-gjenbruk av NHS-tegninger; skriv original tekst og kildehenvisning.

## 4. Teknisk kontrakt for WordPress (P0)

**Rolle:** interne PHP-/datakomponenter `EverydayAnchors` / `MicroMovementCatalog` for vedlikehold, faglig publiseringskontroll og eierskap. De **skal brukes av én felles anbefalings-/planleggings-/aktivitetstjeneste og ett brukergrensesnitt**, ikke en separat produktside. Egne REST-ruter for CRUD er tillatt, men klientens ordinære handlingsflyt skal være sammenhengende. Spillmotorens belønninger holdes teknisk adskilt fra faktiske aktivitetsdata.

- DB-tabell `{$wpdb->prefix}ikt_anchors`: `id` (PK), `user_id` (FK/eier), `cue_type` (whitelist enum), `custom_label` (kort, valgfri, sanitert), `movement_id` (WP-post-ID til kvalitetssikret kort), `enabled`, `times_suggested`, `created_at_utc`, `updated_at_utc`. Maks et rimelig antall aktive ankre (eksempelvis 4), men ingen daglig tvangsgrense. Ingen automatiske klokkeslett for hendelsesbaserte ankre.
- `wp_ikt_events` utvides med nullable `anchor_id` og `movement_id` samt `reported_reps` og `reported_seconds` (nullable, minst ett positivt ved mikro-`completed`); `reported_minutes` skal være `NULL` når kun repetisjoner oppgis. Ingen omregning til minutes eller styrkegevinst. Dette gjelder `completed` eller `attempted`, med eierkontroll også på referanser. Separate `kind`-verdier for `micro_movement` og `walk`/`daily_task`. Tellelogikk validerer at `completed` faktisk er selvrapportert og aldri oppstår ved opprettelse av anker.
- CPT `ikt_movement`: kun publiserte, redaksjonelt vurderte kort eksponeres. Metadata: `movement_family`, `duration_hint`, `safety_context` (dry_floor, stable_support osv.), `equipment`, `low_load_variant`, `avoid_when`, `source`, `reviewer`, `reviewed_at`, `review_status` og `version`. Validering ved publisering; bare autorisert rolle kan godkjenne. Bruk WordPress' eksisterende editor/role permissions og revisjoner.
- REST: `GET /movements` (kun publiserte kort/ offentlig minimum), `GET /me/anchors`, `POST /me/anchors`, `PATCH /me/anchors/{id}`, `DELETE /me/anchors/{id}`. Alle private endepunkter med serverens eierkontroll, nonce og inputvalidering; ikke les / endre en annen brukers anker-ID.
- **Den felles** anbefalingsmotoren bruker `cue_type`, brukers valgte aktivitetspreferanse og tidligere erfaring; den kan på tvers av aktiviteter velge et anker, en tur, noe praktisk eller en pause, og foreslå annet anker, enklere kort eller annen handling ved avslag. Ikke krev bakgrunnssensor, push, e-post eller smartklokke for å virke.
- All historikk (inkludert ankeretiketter) inngår i brukerens eksport/sletting og WordPress Privacy API; slette anker fjerner kobling/snapshot på en forutsigbar måte, men bevarer kun selvvalgt historikk i henhold til offentlig dokumentert regel.
- Intet brukergrensesnitt skal vise at appen *vet* at en rutine har funnet sted; det gjør den ikke. Ordlyd: «Når du er ferdig med ...» eller «Vil du prøve ...?» – aldri «Vi så at du pusset tennene».

## 5. Testscenarier – inngår i leveransegaten

1. Bruker A lager `etter_tannpuss`→tåhev og `etter_kaffe`→stol-til-stå; B kan ikke se, oppdatere eller slette noen av ankrene til A.
2. Opprettelse, endring, pausing, sletting og gjenopptakelse av anker **gir ingen aktivitets- eller spilletelling**.
3. Appen lager riktig når–så-tekst, ingen oppdiktet sensorhendelse eller automatisk påminnelse.
4. `dusj` gir bare **etter dusj + tørt underlag** og kortene for `wet_floor`/`one_hand_busy` kan ikke velges.
5. Ved «ubehag» eller «for tungt» økes ingen belastning; appen tilbyr tryggere alternativ/pausestopp og kan vise behov for faglig hjelp.
6. En egenrapportert kort gjennomføring ligger i aktivitetsloggen med tydelig type og kilde; fem tåhev blir **fem repetisjoner, ikke fem minutter**, kan eksporteres og slettes, og gir maksimalt ett serverstyrt dagsbidrag til NIM/historien.
7. Tre separate rapporter samme dag gir ikke tre kapitler; heller ikke gjentatt samme POST med samme `client_uuid`.
8. Bank inneholder beskrivelser av minst tre godkjente bevegelser før de vises i ikke-admin visning; uten faglig revisjon er bevegelsesbanken avskrudd/kun i eksplisitt admin-sandbox.
9. Valgfri og fravalgbar aktivitetstype fungerer også uten NIM, sosial del eller eksterne API-er. Fra samme «I dag» kan man bytte mellom relevant mikrohandling og annen aktivitet, uten eget «mikro»-navigasjonsnivå.
10. Bevegelseskort med instruksjon og varianter er leselige på 320 px mobil, tastaturnavigerbare og forståelige uten lyd eller video.

## 6. Kildespor til produktbeslutningene

- Helsedirektoratet, voksne/eldre, litt aktivitet bedre enn ingen, styrke større muskelgrupper minst to dager: https://www.helsedirektoratet.no/faglige-rad/fysisk-aktivitet-i-forebygging-og-behandling/voksne-og-eldre
- WHO 2020, fysisk aktivitet av enhver varighet teller: https://pmc.ncbi.nlm.nih.gov/articles/PMC7719906/
- BJSM / PubMed, *Effect of exercise snacks on fitness and cardiometabolic health in physically inactive individuals* (11 RCT-er, 414 deltakere, lav/svært lav sikkerhet): https://pubmed.ncbi.nlm.nih.gov/41057224/
- Journal of Nutrition, Health and Aging 2026, metaanalyse fysisk funksjon (11 RCT-er, 472 deltakere): https://www.sciencedirect.com/science/article/pii/S1279770726000680
- Journal of Nutrition, Health and Aging 2026, subgruppe >50 år uten sikker VO₂maks-forbedring (21 RCT-er, 921 deltakere): https://pubmed.ncbi.nlm.nih.gov/42571752/
- Journal of Frailty & Aging (2024), hjemmebasert styrke- og tai chi-snacking 90 eldre: https://link.springer.com/article/10.14283/jfa.2024.32
- Metaanalyse 2026 om faste kontekstsignaler (14 studier / 6 069 deltakere): https://pmc.ncbi.nlm.nih.gov/articles/PMC13467471/
- NHS, generelle hjemmeøvelser og trygg stabil stol: https://www.nhs.uk/live-well/exercise/strength-exercises/
- NHS, forebygging av fall, vått bad: https://www.nhs.uk/conditions/falls/
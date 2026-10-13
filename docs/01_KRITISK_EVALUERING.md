# IKKE TRENING 4.1 – kritisk evaluering før WordPress-utvikling

Dato: 13.10.2026. Grunnlag: eksisterende `app.js`, `styles.css`, `index.html`, konsept 4.0 og 4.1, skjermbilder, originale Playwright-tester; testene ble kjørt på nytt med vellykket resultat. Dette er en kildekode-/konseptevaluering, ikke en ekstern brukertest, sikkerhetspenetrasjonstest eller medisinsk evaluering.

## Kort beslutning

**GO for å utvikle en installerbar WordPress-beta. NO-GO for å legge 4.1-HTML rett i en plugin og omtale den som ferdig.** Bygg en ny applikasjon med 4.0 som atferdsfaglig kjerne og 4.1 som valgfritt, konkret spillag. Gjør den testbar på eget WordPress-domene uten eksterne abonnementer eller API-kostnader. Ikke publiser mot ekte brukere før adgangskontroll, privatliv og ende-til-ende-tester er bestått.

## Hva som er godt i 4.1

- Klart produktproblem: ikke mer treningsteori, men praktisk støtte til folk som utsetter, unngår eller slutter.
- 4.0 skiller mellom manglende evne/kapasitet, mulighet og motivasjon. Mange tiltak skal ikke ende i «gå fem minutter».
- Tre alternative interaksjonsstiler: nysgjerrighet/oppdagelse, «bare få det gjort», sosial støtte.
- Maskoten NIM er original og valgfri. Ikke skuffet ved fravær, ingen tapsrekker. Maskoten er implementert som SVG, altså ikke avhengig av lisenser eller ekstern bildegenerering.
- Avtaler telles ikke som utført aktivitet. Selvrapportert gjennomføring merkes ærlig.
- Pause straffes ikke. En negativ erfaring kan føre til forslag av annen type.
- Foreløpige responsive visninger finnes for både smal mobil og desktop.
- Ingen betalte AI-API-er, bildelisenser eller treningsdata-API-er kreves for konseptet.

## Dokumenterte svakheter i konkret 4.1-kode

1. **Alt er lokal nettleserlagring.** `load()` og `save()` benytter én `localStorage`-nøkkel. Det finnes ingen WordPress-konto, databasesynkronisering, tilgangsstyring, versjonert migrering mellom enheter eller serverbasert personvernflyt. Eksport og sletting er bare lokal JSON.
2. **Mangler reell sosial funksjonalitet.** `together()` bygger gruppens aktivitet av egne rapporter og en bryter `simulated` som legger til to oppdiktede venner. Ingen inviterte kontoer, aksept, per-person-samtykke eller privat deling finnes.
3. **Progresjon er demonstrasjonslogikk.** `progressCount()` er `Math.min(s.session.length, 6)`. Hver enkelt selvrapport gir ett nytt kapittel, uavhengig av tidligere handlinger, varighet, tid eller relevans. Seks rapporter åpner alt. Ingen fortellingsøkonomi eller langsiktig innholdsforvaltning finnes.
4. **Lite innhold.** To temaer (steder og natur) med seks korttekster hver. Bra for skjermdemo, ikke for gjentatt bruk i uker eller måneder.
5. **Regelmotoren er for flat.** `offer()` består av et lite antall `if`-grener. Bare den aller siste negative opplevelsen av et «experience»-forslag påvirker eksplisitt en bestemt anbefaling. Ingen generell modell for gjennomføring, avslag, situasjon eller brukerens egne valg over tid.
6. **Veldig mange avslag gir ikke nødvendigvis nye tiltak.** Flere grener er i praksis låst til en årsak. Manglende tid = generisk plan; ubehag = generisk forsiktighet; sosialt = invitasjon. Det mangler ett relevant oppfølgingsspørsmål og en meningsfull reservehandling.
7. **Belønningen står ikke i forhold til objektivt målt aktivitet.** Applikasjonen kan bare vite hva brukeren selv registrerer. Det er greit som bevisst design i test-beta, men spillets fremdrift må ikke presenteres som dokumentert helsefremgang.
8. **Ingen fungerende oppfølging utenfor appen.** Lagrede avtaler er passive. Ingen varsler, kalenderhandlinger eller ekte menneskekontakt. Dette er et av de viktigste problemene konseptet forsøker å løse.
9. **Mobil før handling:** Skjermbildet på 390 px viser stor produktoverskrift, forklaring, tre chips og en stor NIM-hero før hele hindringslisten. Hovedhandlingen kommer lavt; dette må snus i innlogget app. Landingssiden kan beholde mer fortelling.
10. **Ingen publiserbar WordPress-leveranse.** Ingen plugin-header, install/upgrade/uninstall, WP-admin, blokker/shortcode, PHP-REST API, database, rettigheter eller eksport-/slettingsintegrasjon.
11. **Ikke tilstrekkelig tilgjengelighetstest.** Det finnes støtte for `prefers-reduced-motion` og flere labels. Det mangler dokumentert reell skjermlesertest, gjennomført tastaturnavigasjon, fokus-/modaltester og kontrastkontroll.
12. **Ingen sikkerhetstest i flerbrukermiljø.** Dette er en statisk demo. Vi kan ikke konkludere med at en flerbruker-WordPress-versjon er trygg uten omfattende tester for CSRF, XSS, IDOR og gruppedeling.

## Viktig psykologisk kvalitetskontroll

- En maskot har *ikke* dokumentert selvstendig effekt i vår målgruppe. Gamification er kun et virkemiddel. Metaanalysen 2024 (ofte omtalt i 2025) med 36 RCT-er viser i gjennomsnitt rundt **489 ekstra skritt/dag**, en liten tilleggseffekt i sammensatte tiltak; dette kan ikke overføres direkte til NIM.
- Utforskning og korte fortellinger kan oppleves kunstige. Det må finnes en «ingen spill»-modus med full funksjonalitet.
- Daglige aktivitetsrekker som går tapt og skam-/skyldesignaler forbys i standardproduktet.
- Sosiale oppdrag må være frivillige og asynkrone; deltakere skal ikke sammenlignes på rå skritt eller straffes for at andre tar pause.
- Å være borte fra appen er ikke bevis på fysisk inaktivitet. Kommunikasjon og «gjenstart» må aldri bygges på den antakelsen.
- Enkeltstående to-minutters aktiviteter kan redusere startmotstand, men må ikke presenteres som tilstrekkelig kondisjons-/styrketrening.
- Appen er verken klinisk behandling eller en helserisikoscore. Ingen diagnoser, løfter om forebygging av hjerteinfarkt eller automatisk økning i intensitet ved smerte/uvanlige symptomer.

## Nytt funn: Hverdagsankre og mikrobevegelser

Brukerinnspillet om å bevege seg etter tannpuss, mens kaffen brygger og når man reiser seg fra sofaen treffer en reell svakhet: 4.1 forutsetter vanligvis et eget "oppdrag". Mange vil heller gjøre noen enkle bevegelser på toppen av noe de allerede gjør. Forskning på *exercise snacks* og faste vanesignaler støtter dette som en lovende **integrert aktivitetstype i samme handlings- og vanemodell**, men studiene varierer i intensitet, alder og resultat. Enkle tåhev eller stol-til-stå er ikke alene et komplett styrkeprogram, og effekten hos personer over 50 er ikke entydig.

**Produktbeslutning (presisert av bestiller):** Gjør et lite utvalg av valgbare, hverdagsforankrede aktiviteter til en **integrert P0-del av kjernemotoren** i WordPress-betaen – IKKE en egen meny/fane/sekundær app ved siden av planlegging, gjenstart og spill. Aktiviteter knyttet til eksisterende rutiner skal kunne være appens **primære anbefaling**, der hindring, kontekst og tidligere erfaring tilsier det. Personalisér først og fremst etter trygghet, funksjon og preferanse – ikke stereotype kjønns- eller aldersregler. Dusj er aldri øvingssted. Klinisk innhold krever dokumentert faglig gjennomgang før offentlig test. Se `07_HVERDAGSANKRE_OG_MIKROBEVEGELSE.md`.

## Marked og nyhetsverdi

Gamification, dyr/venner, kart, fortellinger og treningsfrie aktivitetsforslag finnes allerede, bl.a. hos Duolingo, Finch, Pikmin Bloom og flere aktivitetsapper. Konkurransefordelen kan ikke være «vi har en maskot». Den må være et kvalitetsløp for å identifisere *riktig type støtte* før aktiviteten, kombinere den med frivillige spillmekanismer og bevare autonomi og støtte for tilbakekomst.

## Avgjørelse om tema og teknisk løsning

WordPress skiller tematisk mellom tema (presentasjon) og plugin (funksjonalitet). En plugin kan levere en dedikert fullskjerms appside via WordPress' malfilter og korte koder/blokker uten at brukeren må installere et ekstra tema. **Lever én ZIP-plugin med innebygget designsystem**. Utvikle ikke eget fullsite-tema nå. Pluginen skal valgfritt kunne rendres både i isolert appskall og i en vanlig WP-side med innkapslet layout.

## Avgjørelse om første fullverdige testversjon

Første WordPress-utgave: `IKKE TRENING 5.0 – WordPress beta`, teknisk semver `0.1.0-beta.1`. Den skal være komplett for testformålet, ikke et statisk design. **Må ha:** WordPress-brukerkonto; database; ekte forslag/plangjennomføring/tilbakemelding; valgbare hverdagsankre med gjennomgåtte mikrohandlinger; NIM; redaksjonelt historiekart; ekte frivillige venneinvitasjoner og private fellesbidrag; enkel WP-admin; eksport/sletting; norsk frontend; trygg mobilvisning; brukbar dokumentasjon og tester. **Ikke bygg i denne leveransen:** betalt AI-coach, betaling, geolokasjon, Health Connect, Apple Health, offentlige ledertabeller, push/SMS-leverandører eller klinisk funksjonalitet.

## Test- og lanseringsport

Resultatet er klart for lukket test på testdomene når Codex har generert en installerbar ZIP, Plugin Check / PHP-sjekk og kritiske backend- og E2E-tester passerer, en testbruker faktisk kan legge inn en aktivitet, gjenåpne kontoen på annen enhet, dele via invitasjon og slette sine data, uten rolleforveksling, offentlige aktivitetslogger eller demo-venner. Fremtidig helseeffekt skal aldri erklæres validert på dette grunnlaget.
# IKKE TRENING 5.0 – akseptansekrav, sikkerhet og kvalitet

Codex skal rapportere hver sjekk som `PASS`, `FAIL` eller `NOT RUN`, med kommando, resultat og eventuelle feilmeldinger. Ingen kosmetisk «alle tester grønne»-rapport hvis noe ikke faktisk ble kjørt. Alle P0 må være PASS før en ZIP anbefales for lukket test.

## P0 – installasjon og grunnplattform

- [ ] En eneste ZIP lar seg laste opp og aktivere på en **ren WordPress-installasjon** med oppgitte minimumsversjoner, uten SSH, npm, composer på verten eller eksternt API.
- [ ] Appens plugin-administrasjon vises. Ingen offentlig appside opprettes før administrator velger det.
- [ ] Innlogget bruker kan gå til app på valgt URL, og blokk/kortkode viser appen også på vanlig WP-side.
- [ ] Bytte av WordPress-tema endrer ikke lagrede appdata og knekker ikke appens visning.
- [ ] Deaktivering/reaktivering mister ikke brukerdata; versjonsoppgradering utfører migrering idempotent.
- [ ] Ingen varsel-feil i `WP_DEBUG` ved normal bruk; ingen PHP-fatal eller alvorlige JS-feil.

## P0 – ekte atferd og profil

- [ ] En bruker kan velge samme eller ny hindring på to ulike dager, få meningsfull ulik type hjelp og overstyre forslaget.
- [ ] «Har ikke tid» leder til en konkret anledning + reserveplan og **ikke** automatisk aktivitetsregistrering.
- [ ] «Ubehag/smerter» leder til skånsom tilpasning/hvile og evt. råd om profesjonell vurdering, ikke belønning for høy intensitet.
- [ ] «Bare få det gjort» fungerer uten lyd, fortelling og NIM.
- [ ] Positiv eller negativ opplevelse endrer valget av støtte/aktivitet på forståelig vis; minst énhetstest for hver hindringskategori.
- [ ] Start/plan/forsøk/pause/avslag teller **aldri** som gjennomført aktivitet; kun eksplisitt selvrapportert `completed` med gyldig varighet **eller** antall repetisjoner/sekunder for mikroaktivitet gjør det.
- [ ] Egenrapportering lagres hos riktig WP-bruker og kommer frem ved ny innlogging i en annen nettleser. Data vises alltid som *selvrapportert*.
- [ ] Gjentatt sending av samme `client_uuid` lager ikke doble rapporter eller dobbelt opplåst kapittel.

## P0 – hverdagsankre og sikker mikroaktivitet (integrert i kjernen)

- [ ] En bruker med «lite tid», «kommer ikke i gang» og valgt rutine «etter kaffe» får relevant mikrobevegelse som **hovedforslag på «I dag»**, uten å navigere til en egen ankermodul. En annen bruker kan få gåtur eller annen aktivitet fra **samme anbefalingsmotor**.
- [ ] Opprett ett eller to ankre, eksempelvis «etter tannpuss» og «etter kaffe», og endre, pause, gjenoppta og slette dem uten at noen gjennomføring logges.
- [ ] Person A kan ikke lese eller endre Person Bs ankre via ID i REST API, selv om A kjenner ID. Eksport/sletting inkluderer ankerdata.
- [ ] Ikke foreslå øvelser **i dusjen eller på vått gulv**; «etter dusj» betyr bare etter at brukeren er tørr og på sikkert underlag. Ingen utrygge ettbeinsøvelser mens hendene er opptatt.
- [ ] Samme aktivitet anbefales med tydelig tilpasning av trygghet og tidligere respons, ikke automatisk styrkeprogresjon basert på kjønn/alder.
- [ ] Publiser bare bevegelseskort med eksplisitt fagrevisor, revisjonsdato, kilder og sikkerhets-/alternativtekst. Uten fagrevisjon er instruerende øvelsesbank **utilgjengelig for ordinære brukere**, men admin kan teste funksjonsflyten isolert.
- [ ] Kun eksplisitt `completed` fra riktig eier med positivt antall repetisjoner eller sekunder gir egenrapportert mikroaktivitet; anker/plan/start/skippet/hvilt teller ikke. Repetisjoner blir **ikke automatisk aktivitetsminutter**. Mikroaktivitet vises separat fra moderat aktivitet og fullverdig styrke i «Min vei».
- [ ] Ingen dobbelt belønning: mikroaktivitet, gåtur og annen aktivitet på samme lokale dag gir maksimalt ett kapittelopplåsingsbidrag sammenlagt, ved servervalidert/idempotent behandling.
- [ ] Hverdagsankre fungerer uten NIM, venner, push/SMS, kontoekstern sensor eller betaling. Tydelig tekst om at appen ikke kan oppdage tannpuss/kaffe automatisk.
- [ ] Mikrobevegelse, gåtur og sosial/praktisk aktivitet følger **én sammenhengende brukerreise** for forslag → plan/start → tilbakemelding → logg → gjenstart; ingen separat hovedmeny, aktivitetsfeed eller konkurrerende belønningssystem for mikrobevegelser.
- [ ] Når brukeren avviser en rutinemikrobevegelse, kan samme motor tilby en annen type aktivitet; når en tur avvises som for tidkrevende, kan samme motor foreslå en trygg, godkjent rutinemikrobevegelse. Dersom godkjente kort ikke finnes, gis ikke ureviewede øvelsesinstruksjoner.

## P0 – NIM, fortelling, progresjon

- [ ] NIM vises både i mobil og desktop, har tre paletter og kan slås av uten å miste tilgang til hele appen.
- [ ] Ingen tapt fremgang ved fravær, sykdom eller manuelt valgt pause; NIM viser ikke skuffelse.
- [ ] Minst 2 verdener x 12 lesbare, redigerbare kapitler. Riktig innhold vises for riktig verden og for innlogget brukers opplåste nivå.
- [ ] Oppdagelseskapittel låses opp kun etter servergodkjent egenrapportert gjennomføring, **maks ett per lokal kalenderdag**. Flere rapporter samme dag kan lagres, men åpner ikke ekstra kapitler.
- [ ] Ingen rapport gir mer enn ett nytt kapittel; 6, 12 og 24 rapporter håndteres uten å gå utenfor innholdslisten.
- [ ] Når alle kapitler er åpnet, vises meningsfull avslutning og forslag om en annen verden; ikke generer evige tomme belønninger.
- [ ] Blandet tilstand (spillet skrudd av, aktivitet på) påvirker aldri rå aktivitetslogg.

## P0 – ekte, privat vennedeling

- [ ] A inviterer B med gyldig tidsbegrenset lenke. B ser invitasjonen, aksepterer, og vises først da som medlem. Uautorisert C kan ikke se gruppen.
- [ ] Medlemsskap/tilgang kontrolleres på server for alle gruppeendepunkter. Et angitt `user_id` i request gir aldri tilgang til en annens data.
- [ ] Gruppens felles bidrag vises bare etter uttrykkelig delingsvalg. Ingen rå minutter, lokasjon eller private hinderdata deles.
- [ ] B kan trekke tilbake deling eller forlate gruppen. Gruppen fungerer videre uten straff eller falsk «skyld».
- [ ] Token kan ikke brukes etter utløp, tilbakekalling eller første aksept. Ingen offentlig side viser ekte aktivitetsdata.
- [ ] Ingen oppdiktede «Venn A/B» vises for ekte brukere. Demofigurer kan kun vises via en tydelig merket admin-demo.

## P0 – personvern og sikkerhet

- [ ] En vanlig `Subscriber` kan ikke se eller endre en annens planer, rapporter, profil, invitasjoner, fremgang eller dataeksport.
- [ ] Anonyme REST-kall mot private skriveruter får korrekt avvisning. Manglende/ugyldig CSRF-nonce avvises for WP-cookie-auth.
- [ ] Alle relevante REST-ruter har eksplisitte `permission_callback` og validerte schemas.
- [ ] XSS-tekst innsendt som navn, plan, mål, invitasjon, kategori eller historieinnhold blir ikke kjørt i app eller WP-admin.
- [ ] SQL-parametre bindes; ingen klientstyrt database-tabell, spørring eller bruker-ID med direkte tilgang.
- [ ] Bruker kan eksportere egne data og slette egne appdata, og eksport/eraser er integrert med WP Privacy-verktøy.
- [ ] Data fra en slettet bruker er ikke synlige i eksisterende gruppevisning etter slett/anonymisering.
- [ ] Ukjent gjest kan bruke forhåndsvisning uten serverlagret aktivitetsprofil eller ekte deling.

## P0 – faktisk mobilbruk

- [ ] På 390×844: innlogget hovedskjerm viser ett relevant forslag og primærknapp uten omfattende skrolling forbi produktreklame.
- [ ] 320, 360, 390, 768, 1024 og 1440 px uten vannrett scrolling eller knapper bak navigasjon.
- [ ] Fokusring tydelig; skjemaer har labels; faner kan navigeres med tastatur; tilbake-knapp og feiltilstander fungerer.
- [ ] Respekt for redusert bevegelse; NIM-animasjon deaktiveres ved brukerinnstilling/OS-preferanse. Ingen autoplay-lyd.
- [ ] Kontrast/tekststørrelse og viktigste skjermleserflyt kontrollert og dokumentert med funn.

## P1 – kvalitet ved installasjon

- [ ] Oppsettveiviser forklarer hva pluginen gjør, hva den lagrer, hva den ikke gjør, og registrerings-/delingstilstand.
- [ ] Admin kan redigere verdener/kapitler og forhåndsvise uten at en uferdig historie blir offentlig.
- [ ] PHP lint, JS lint, PHP-enhetstester, domenelogikktester og Playwright E2E for to kontoer følger med.
- [ ] `readme.txt`, norsk `README.md`, changelog, installasjonsinstruks, driftsnotat og liste over kjente begrensninger følger ZIP/Repo.
- [ ] Bruk WP-CLI for local testing hvis tilgjengelig; ellers Docker Compose / `wp-env`. Ved krav på webhotellet skal Node/Composer ikke være nødvendig.

## Tester Codex konkret skal utføre

1. **Ren install:** WordPress + plugin, admin åpner oppsettveiviser og lager testside.
2. **Isolasjon:** A og B oppretter logger, prøver feil `user_id`, manipulert `group_id` og direkte REST-kall.
3. **Belønning:** A rapporterer én aktivitet, får ett kapittel; rapporterer igjen samme dag, får ingen ekstra; neste lokale dag får ett; gjentatt HTTP-request gir ingen ekstra.
4. **Flere enheter:** A logger inn i to ulike nettleserkontekster og ser samme aktiviteter/fremgang.
5. **Plan uten aktivitet:** Lag plan, forsøk, avbryt og hvil; sjekk at kun completed telles.
6. **Venner:** A inviterer B, B aksepterer, B velger privat/offentlig bidrag innen gruppe, A kan ikke se detaljer som B ikke har samtykket til.
7. **Avvisning:** Negativ respons endrer meningsfullt neste forslag uten å presse gjennom høyere belastning.
8. **Gjenstart:** Manipulert testtid 15 dager senere gir valgfri velkomst og fortsatt opplåst innhold.
9. **Datalivssyklus:** Eksport, WP privacy export, slette appdata, deaktiver/reaktiver og oppgrader fra et eldre skjemanummer.
10. **Integrerte hverdagsankre:** A får mikrobevegelse som primær anbefaling på «I dag» for relevant hindring og kan bytte sømløst til gåtur; A velger etter-tannpuss→tåhev og etter-kaffe→stol-til-stå; B prøver uberettiget tilgang; anker-plan/avslag gir ingen aktivitet; completed gir ett markert egenrapportert bidrag; dobbel POST gir ikke dobbel bonus. Test «etter dusj» ikke øvelser på vått gulv; test faglig publiseringslås.
11. **Kompatibilitet:** Test WP-standardskjerm, et annet tema, liten mobil og desktop.

## Leveranse-GATE

**Ikke erklær «klar til å installere» hvis:** plugin-ZIP ikke er bygget; WP ikke er kjørt; sosiale delinger er falske; tilgangskontroll ikke er testet; rapporter bare finnes lokalt; innholdet er 6 demokapitler; øvelseskort vises offentlig uten dokumentert faglig vurdering; PHP-feil finnes; app ikke fungerer på mobil; gratis-/kostnadsforutsetning er brutt. Oppgi i så fall presist blokkering, kode og neste steg.

## GitHub Actions – hold kostnaden nede

Arbeidet bør teste lokalt før push. Én begrenset CI-jobb på manuell `workflow_dispatch` og/eller PR med relevante endringer, `concurrency` med cancel-in-progress og kort timeout; ikke bygg stor PHP×WP×Node-matrise på hvert commit. Samtidig må viktige tester ikke droppes for å spare minutter. Dersom GitHub Actions er begrenset, inkluder kommandoer og logger for lokal kjøring og rapporter CI-status ærlig.
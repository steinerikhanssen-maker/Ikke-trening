# GymNotFound 0.1.0-beta.1 – bindende produktbestilling til Codex

**Besluttet 14.10.2026.** Dette dokumentet DEFINERER FØRSTE FUNGERENDE VERSJON av GymNotFound. Det erstatter eldre 5.0-omfang der disse krever fortellingsverdener, full venneinfrastruktur, kontoer, AI, aktivitetsmålere eller omfattende sosiale funksjoner før beta. Eldre dokumenter er konseptreferanse og senere backlog. Se ny prioritetsregel i rotfilen AGENTS.md og testene i 11_MVP_0_1_AKSEPTANSETEST.md.

## A. Én produktidé

GymNotFound er en litt ironisk og overraskende intelligent aktivitetskamerat som hjelper folk bort fra skjermen og ut i livet. Brukerne kan mislike trening eller ha lavt overskudd. Hovedmålet er at appen gjør det enklere å FINNE PÅ og GJENNOMFØRE små, relevante aktiviteter uten treningspress, poengjag eller stadige varsler.

**Kjerneløfte:** «Bruk appen i 30 sekunder. Gjør noe i virkeligheten.» Dette er et designmål, ikke en garantert tidsgrense. Humoren er tørr, vennlig og aldri på brukerens bekostning. NIM er en liten karakter/personlighet, IKKE et følelsesmessig avhengighetsspill.

En konsis daglig brukerreise:
1. Åpne appen uten registreringsplikt eller posisjonstillatelse.
2. Se dagens ENE forslag umiddelbart. Juster enkelt «Overskudd: lavt / litt / bra» og «Tid: 2 / 10–15 / 30+ min». Knapp for annet forslag. For førstegangsbruker: kom i gang uten langt skjema.
3. Forslaget kan være et rutineanker, en lavterskelaktivitet hjemme, en trygg kort uteaktivitet eller et faktisk sted å besøke. Vis kort hvorfor det passer, og hvor opplysningene kommer fra.
4. «Jeg gjør det» viser enkel, positiv ut-av-skjerm-oppsummering. IKKE start klokkestyring, tvangsløp eller registrer aktivitet som fullført.
5. Etterpå eller ved neste åpning: «Gjort», «Passet ikke», «Senere» eller «Ikke nå». Bare eksplisitt «Gjort» oppretter completed-event. Lagret respons endrer forslag. Ingen skyld, tapte rekker eller påstått målt trening.

## B. Scope / ikke scope

### Obligatorisk i MVP (P0)
- Én selvstendig, installerbar WordPress-plugin ZIP med innebygd mobilapp, ikke krav til eget WP-tema, Node eller Composer på server.
- Gjestemodus fra første skjerm, enkel lokal lagring av preferanser, aktiviteter og feedback. Eksport og sletting av lagrede appdata. Ikke samle e-post eller opprette WP-kontoer for vanlige besøkende i MVP.
- Regelbasert, lokal/serverbasert anbefalingsmotor som tar hensyn til tid, overskudd, brukervalg, svarhistorikk, vær når tilgjengelig og tilgjengelige faktiske steder når leverandør er konfigurert.
- MINST 36 reelt skrevne aktivitetsmaler (norsk + engelsk), fordelt på by, mindre steder/land, hjem, nærområde, rutineankre, oppdagelse og lett sosialt samvær. Minst 12 må fungere uten posisjonsdata, uten vær og uten POI-data. Variasjon i lav/høy terskel, 2, 10–15, 30+ minutter; unngå generiske kopier av samme tekst. Oppgaver skal være lovlige, trygge og gratis som standard, ikke kreve kjøp eller inngangsbillett.
- NIM SVG fra tidligere 4.1 som inspirasjon, kompakt og valgfri. Håndskrevet variasjon av norske og engelske korte replikker. Funksjonalitet skal være like god med NIM deaktivert.
- Frivillig nettleserposisjon ved eksplisitt handling. Førstegangsbesøk og avslag på posisjon gir fullverdig generisk anbefaling. Frivillig manuell stedssøk hvis stedstilbyder er konfigurert; uten den tilbys «uten posisjon».
- MET Norway Locationforecast (gratis, verdensdekkende) via server som værkilde når stedet er kjent. Varsom, enkel værtilpassing uten medisinske konklusjoner.
- Geoapify Places som valgbar, GRATIS plan-basert POI-leverandør. API-nøkkel er frivillig og angis av nettstedets eier i WP admin. Uten API-nøkkel eller ved feil skal appen fortsatt fungere uten oppdiktede steder; stedbaserte funksjoner vises som utilgjengelige. Ingen automatisk overgang til betalte abonnementer.
- Google Maps URLs som ekstern «Vis sted / veibeskrivelse»-lenke; INGEN Google Places API, ingen innbygd betalingsstyrt Google Maps SDK. Riktig URL-encoding og koordinater; åpner ny fane.
- WP-admin: appside/oppsett, aktiver/deaktiver vær/sted, Geoapify-nøkkel og kvotegrep, administrering av aktivitetsmaler og språk, feilsøking med ikke-personlige statusdata, tydelig kreditering.
- Privatliv, sikkerhet, språkvalg (engelsk + norsk), tilgang/kontrast/tastatur/mobil og fallbacks som lar produktet fungere uten eksterne tjenester.

### IKKE implementer i MVP (utsett uten å slette idéene)
AI/ChatGPT API; Ticketmaster; arrangementskatalog og live arrangementer; konkurranser, globale feed, push, reklame, betaling; rute-/turforskrifter og lovnader om gåtid; påtvunget brukerregistrering, WP-kontosynk, venneinvitasjoner og delt historikk; 24 fortellingskapitler/tunge verdenskart; kartfliser/mapkit; skritt/puls/medisinske sensorer; health-profilering, diagnoser eller øvelsesprogram uten faglig godkjenning. Ikke bygg avansert sosialt system eller chat. Hold gammelt omfang som «senere».

## C. Hovedskjerm og språk

Første synlige mobilskjerm ved ca. 390 x 844 skal vise ett faktisk oppdrag og primærhandling uten å rulle. Ikke stor hero/markedsføring, ikke skjema, ikke feed. NIM liten. Komponenter:
- Kort og tydelig navn: GymNotFound. En liten valgfri, tørr kommentar fra NIM.
- Kompakt værstatus KUN når prognosen er aktuell og sted er valgt. Datakilde/kreditering tilgjengelig.
- Ett kort: handling, frivillig kategori, cirka tidsramme som AVSAT tid (ikke oppdiktet gangtid), hvorfor det passer, eventuell navngitt sted med kilde.
- Handlingene: «Prøv denne», «Ny idé», «Ikke nå». Etter «Prøv denne», la bruker legge bort telefonen; senere mulighet for «Gjort / Passet ikke».
- Diskré tilgang til «Min vei» (egne egenrapporterte handlinger, ikke skritt), «Mine valg» (tid, overskudd, lokasjon, ingen penger, språk, NIM av/på, slett og eksporter).
- Ingen tvungen profilregistrering eller GPS-dialog ved sideinnlasting. Null auto-play lyd, ingen evig skrolling eller distraksjonsmekanismer.

Default English/Norwegian UI med separat lokaliserbar ordliste, ingen hardkodet tekst som hindrer utvidelse. Bruk moderne, voksent, lekent designspråk fra 4.1; ikke kopier gamle problematiske demonstrasjonsdata. Brand/slug gymnotfound. Teknisk pluginversjon 0.1.0-beta.1.

## D. Aktivitetsdatamodell (redigerbar og reell)

Hvert kort har ID, språkstrenger, aktivitetstype, konteksttagger (urban / suburban / rural / home / anywhere), tidsbånd, innsats/overskudd, utendørs/innendørs, vær-egnethet, gratis/valgfri kostnad, stedskategori eller null, sikkerhetskrav, faglig godkjenningsstatus ved konkret bevegelsesinstruks, og kort NIM-replikk.

Dynamiske aktivitetsmaler må ha tydelig skille mellom:
- Et faktisk verifisert sted fra leverandør, med provider-ID, navn, type, koordinat, dato for oppslag og lenke.
- En GENERELL oppgave uten spesifikt sted, som «Ta en rolig liten runde på et kjent og trygt sted», «Se etter tre ulike farger på veien», «Gjør en liten oppgave mens kaffen blir klar». Skriv aldri oppdiktet kafé, bibliotek, attraksjon, arrangement, åpningstid, pris eller tilgjengelighet.
- Rutineankre (etter kaffe, etter tannpuss, når du reiser deg fra sofaen) er kandidater i SAMME forslagmotor, ikke egen app, menu eller valuta. Konkret øvelsesinstruksjoner SKAL IKKE publiseres uten registrert faglig gjennomgang. I MVP kan ufarlige, generelle valg brukes uten å foreskrive eksakte repetisjoner/belastning.

Foreslåtte malfamilier:
1. 2-minutters ting: gå ut og få luft, se utover, ta en trygg ekstrarunde i huset, oppdag tre lyder.
2. 10–15 minutter: se en annen gate, utforsk en trygg sti du kjenner, gå til en faktisk nærliggende park/bibliotek når den finnes, kort hjemmeprosjekt.
3. 30+ minutter: besøk et faktisk nærliggende utsiktspunkt, bibliotek eller museum dersom relevant, en oppdagelsesrunde uten kjøpsplikt, et frivillig sosialt ærend.
4. Ved lite overskudd eller dårlig vær: små innendørs aktiviteter, pause/hvile som legitimt utfall, eller svært lavterskel oppgaver. Ikke behandle «ikke nå» som feil.

## E. By versus land – intelligent uten AI

IKKE bestem aktivitet ut fra bare alder, kjønn eller kommune/navnet på stedet. Bruk innholdet i faktiske stedsdata. De to viktige forholdene er hva som FINNES og hvor mye innsats brukeren ønsker.

Algoritme:
1. Sett kontekst fra brukerens frivillige posisjon/manuelle søk. Lokalt kan brukeren velge «Jeg er i byen / mindre sted / på landet / ingen steder» som overstyrer generiske maler; ikke påstå at dette er maskinverifisert.
2. Hvis Geoapify er konfigurert, hent et lite, relevant utvalg POI-er innenfor avgrenset radius (eksempel: nær 1,5–3 km først; utvid eventuelt til 5–10 km når valgt tidsramme/kontekst tilsier det). DeDUPliser på id/koordinat/navn, filtrer irrelevante, private, farlige eller utilgjengelige kandidater. Maks noen få POI-oppslag per område og server-cache.
3. Beregn en enkel kategoriscore/densitet for handlingsrelevante POI-er, ikke grov befolkningstetthet. Urban: mange relevante steder, flere byvandring-/kulturforslag. Landlig: få tilbud, mer natur/egen nabolagsutforskning/kjente runder. Ikke foreslå kafé uten faktisk kafétreff; ikke foreslå skogssti/utsiktspunkt uten kilde som bekrefter et aktuelt besøkssted.
4. Når POI-resultatene er tomme eller leverandøren nede, tilby med vilje generiske aktiviteter som virker OGSÅ på landet. Det er bedre enn å foreslå en falsk destinasjon.
5. Ikke konverter rettlinjet avstand til gange-/kjøretid uten routing. Hvis avstand vises, kall det «omtrent X km i luftlinje». Krev ikke at 30-minutters forslag er mulig innenfor 30 minutters faktisk gåtid. Brukeren kan åpne Google Maps for rute.
6. Prioriter gratis aktiviteter; kafé er kun valgfritt dersom bruker har tillatt potensielle kostnader. Ikke anta åpningstid, tilgjengelighet, billett eller privatadgang.

En regelmotor kan velge med score: sikkerhet/harde filtre først, deretter tid/overskudd, relevant sted, vær, historikk/preferanser og variasjon. «Ny idé» må gi et faktisk alternativ og ikke samme kort om igjen. Begrens repetering av samme type i nærliggende økter, men aldri vis farlige/ikke-godkjente kort bare for variasjon. Ingen AI eller fri generering nødvendig.

## F. Vær, sted og data – konkrete integrasjonsregler

### MET Norway Locationforecast
- Endpoint: https://api.met.no/weatherapi/locationforecast/2.0/compact
- HTTP forespørsel SERVER-SIDE i WP, aldri klienten. Sett identifiserende User-Agent med prosjekt-URL/kontakt; følger Cache Expires / Last-Modified / If-Modified-Since. Avrund koordinater til maks 4 desimaler for deres cache; lavere presisjon er anbefalt for cache/personvern der det er praktisk.
- Tolking av nærmeste forecast til nå, nedbør og vind, temperatur. Unngå falske eksakte værmeldinger, for mange kall og kliniske råd. Værtilpassing styrer bare valg av innendørs/utendørs og tidspunkt/komfort, ikke absolutte sikkerhetsgarantier.
- Vis «Basert på data fra MET Norway» og kildelenke. Feil, forsinket, manglende sted eller timeout: motoren fungerer UTEN vær og appen oppgir ikke stale data som nåværende.

### Geoapify Places (optional)
- Docs: https://apidocs.geoapify.com/docs/places/
- Kun admin setter inn gratis API-nøkkel i WP innstillinger, lagret trygt server-side. Ikke hardkod nøkler, aldri lek dem til REST payload, HTML eller kildekode.
- Bruk egnede kategorier som leisure.park, tourism.attraction.viewpoint, tourism.sights, entertainment.museum, natural, catering.cafe, utvalgte community facilities. Ikke bulk-spørr eller bygg egen allomfattende katalog i v1. Max 20 svar per API-kall for kredittkontroll; bare relevante kategorier.
- Avgrens oppslag geografisk, server-cache per område og kategori, minimum 12-24 timer så lenge provider-vilkår tillater det. Rate limiting / per-hour og per-day hard internal cap, kontrollert fra admin med trygg lav default. Ingen automatisk oppgradering eller fakturering. Hvis tomt, over kvote eller 429: fall tilbake til stedsløse forslag.
- Kildevisning: «© OpenStreetMap contributors» lenket til https://www.openstreetmap.org/copyright og «Powered by Geoapify» lenket til https://www.geoapify.com/ ved stedstreff. Påkrevd kreditering må være korrekt i både kort og krediteringsvisning.
- Hvis bruker velger manuell stedsøking, kan Geoapify Geocoding brukes med samme nøkkel etter eksplisitt handling. Ikke bruk offentlig Nominatim som automatisk autocomplete eller POI-backend.
- I admin vis om nøkkel finnes, antall egne API-kall/kredittestimater, utløpt cache og test-knapp. Ikke tilby skru på betalt abonnement.
- Ingen påstand om at et sted er åpent NÅ med mindre kilde og oppdatering faktisk kan dokumentere det. Koble «Vis i Google Maps» til offisielle, nøkkelfrie Maps URLs.
- Ikke bruk offentlige Overpass-endepunkter som produksjonsbackend for høy trafikk; lisens og kapasitetsforbehold.

### Personvern og feilmodi
- Ingen automatisk GPS-permission prompt. Browser geolocation kun ved trykk og tydelig formål, ingen bakgrunnssporing. Bruk geokoordinat til det konkrete oppslaget, ikke lagre rå GPS i aktivitetsloggen. Ikke logg IP+GPS, ikke samle personhelseinfo.
- Tillat manuell reset av lagret grovt område/sted og sletting av all historikk. Del aldri brukerens historikk med en steds-/værleverandør. En ekstern leverandør får bare det som er nødvendig for stedssøk/vær.
- Ingen tredjepartssporing eller ekstern analytics, CDN, bilder eller fonter påkrevd.
- Server-kall med allowlist for vertsnavn, faste endepunkter, streng parameter-validering, tidsavbrudd, buffergrenser og SSRF-beskyttelse. Offentlige anonyme REST-kall rate-limiteres og server-cache deles på avrundet geografisk celle, ikke privat brukeridentitet.
- Tekst som legges inn i WP admin eller fra API må escapes/sanitiseres for XSS; capabilities/nonce på admin. Bruk WP transients/object cache der mulig. Alle eksterne feil må degraderes til relevant generisk forslag.

## G. Lokal lagring – ærlig MVP

- Første beta trenger IKKE pålogging eller serverprofiler: lagre kun lokale preferanser, sist brukte forslag, eksplisitt egenrapportert «gjort» og feedback i nettleseren, med versjonert schema/migrering. Lagringen gjelder per nettleser/enhet – kommuniser dette nøkternt.
- «Prøv» = accepted/planned, «Gjort» = completed_self_report, «Ikke nå» = declined, «Passet ikke» = feedback. Starttrykk teller IKKE som gjennomført aktivitet. Eksport til JSON og «slett mine data»-knapp med bekreftelse.
- Ingen tvungen tidslogg, skritt, GPS-spor, aktivitetsscore eller streaks. Om etterregistrering brukes, skil ordinære aktiviteter og eventuelle godkjente mikroøvelser; ikke finn på minutter fra repetisjoner.
- Ingen sosial-/vennesimulering. Gamle demofigurer må aldri fremstå som ekte brukere i MVP.

## H. WordPress-arkitektur og leveranse

- Én plugin, teknisk slug/text domain gymnotfound, versjon 0.1.0-beta.1. WordPress 6.7+, PHP 8.2+, MySQL/MariaDB som vanlig. App-side opprettes ved eksplisitt adminhandling, ikke ved plugin-aktivering. Appskall via dedikert side/template uten krav om eget WP-tema. Admin kan også bruke shortcode eller server-rendered blokk som fallback dersom enkelt å vedlikeholde.
- Pluginens PHP/JS/CSS/assets leveres BYGGET i ZIP. Ingen byggekrav på kundens hosting, ingen eksterne lisensierte pakker for vanlig funksjon.
- Bruk samme modulære motor for rutineanker og sted/uteaktivitet. Intern komponentstruktur kan være moduler, men bare EN sømløs brukerflyt.
- Lag WordPress admin for malredigering; kort med øvelsesinstruks er upublisert til registrert fagrevisor, dato og sikkerhetsbeskrivelse er godkjent. Generelle tur-/opplevelseskort trenger ikke medisinsk fagrevisor.
- Oppgi kvalitetskrav WCAG 2.2 AA som testmål, ikke som udokumentert erklæring. Respekter reduced-motion, ESC/fokus, skjermleser-labels, trygge fargekontraster, responsive 320/360/390/768/1024/1440.
- Installérbar ZIP: dist/gymnotfound-0.1.0-beta.1.zip. Dokumentasjon: README installasjon, docs/INSTALLASJON.md, docs/TESTRAPPORT.md, docs/PERSONVERN.md, CHANGELOG.md, skjermbilder 390px + desktop, server/testmiljø og sjekkliste for evt. mangler.
- Lokal test/CI kostnadskontroll: ingen mange push-matriser, ingen GitHub Actions-spam; kjør PHP lint, Plugin Check, unit-/integrasjonstest og reelle e2e-steg der mulig. Eksakte PASS / FAIL / NOT RUN og testmiljø.
- Opprett egen implementasjonsgren og PR. IKKE merge PR, IKKE installer hos eieren, IKKE offentlig lansering uten separat eiergodkjenning. Ikke endre andre repos, domener, DNS eller betalingsløsninger.
- Bygg komplett, sammenhengende MVP før nye ekstra features; Codex tar rutinevalg selv. Ved blokkering: dokumenter ærlig, lever fungerende avgrenset løsning, ikke falske demo-data.

## I. Kilder / kontrollerte eksterne påstander (pr. 14.10.2026)

- MET API: https://api.met.no/doc/locationforecast/HowTO og https://api.met.no/doc/TermsOfService – verdensdekkende vær, identifisering, cache og attribusjon.
- MET lisens/kreditering: https://www.met.no/frie-meteorologiske-data/lisensiering-og-kreditering
- Geoapify Places / kategorier / kreditter: https://apidocs.geoapify.com/docs/places/ og https://www.geoapify.com/pricing/ – gratisnivå 3 000 kreditter/dag (vilkår kan endres), kreditering og kvoter.
- Geoapify attribusjon: https://www.geoapify.com/terms-and-conditions/ – OSM + Geoapify på gratisplanen.
- Google Maps URL uten API-nøkkel: https://developers.google.com/maps/documentation/urls/get-started
- Google Places krever fakturering/API-nøkkel og inngår IKKE: https://developers.google.com/maps/documentation/places/web-service/get-api-key
- Nominatim begrensninger/forbud mot autocomplete på public API: https://operations.osmfoundation.org/policies/nominatim/
- Overpass public instance fairness: https://dev.overpass-api.de/overpass-doc/en/preface/commons.html

## J. Produktfilosofi / suksesskriterier

De to viktigste tingene er: (1) brukeren ser et nyttig forslag straks; (2) forslaget kan gjennomføres uten at appen må være åpen. Det er IKKE et mål å maksimere tid i app. Målingen i første pilot skjer frivillig, fra selvrapportert «gjort» og tilbakemelding, uten tracking. Dette er en aktivitetskamerat – ikke en treningsplan, turistportal, chatbot eller sosial plattform.

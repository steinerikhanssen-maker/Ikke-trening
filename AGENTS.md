# AGENTS.md – GymNotFound

Dette er hovedinstruksen til Codex og kodeagenter. **Gjeldende første leveranse er GymNotFound 0.1.0-beta.1**, en enkel, overraskende intelligent aktivitetskamerat som får folk bort fra skjermen og ut i livet. Besluttet av eier 14.10.2026.

## Lesefølge og gjeldende prioritet

1. **docs/10_MVP_0_1_AKTIVITETSKAMERAT.md** – bindende produkt, omfang og arkitektur for FØRSTE installérbare beta.
2. **docs/11_MVP_0_1_AKSEPTANSETEST.md** – bindende MVP release-gate.
3. **docs/09_MERKEVARE_GYMNOTFOUND.md** – offentlig navn GymNotFound, slug/text-domain gymnotfound, NIM.
4. **docs/08_PRESISERING_INTEGRERT_AKTIVITET.md** og **docs/07_HVERDAGSANKRE_OG_MIKROBEVEGELSE.md** – én anbefalingsmotor; ingen medisinske/konkrete øvelser uten godkjenning.
5. **docs/03_TEKNISK_ARKITEKTUR_WORDPRESS.md** – gjenbruk tekniske WP-/sikkerhetsprinsipper der de passer med MVP.
6. **docs/02_PRODUKTKRAV_5_0.md**, **docs/04_AKSEPTANSEKRAV_OG_TESTPLAN.md**, **docs/05_CODEX_OPPDRAG_KOPIER_TIL_CODEX.md** og 4.1-referansen – TIDLIGERE større målbilde, ikke release-gate for første MVP.

**Ved motstrid:** (i) personvern, sikkerhet, lovkrav og publiseringsport for faglige øvelser, deretter (ii) MVP akseptansekrav i dokument 11, (iii) MVP produktbestilling i dokument 10, (iv) merkevarevalg og samme-motor-prinsippet, (v) eldre fremtidsdokumenter. Gamle krav om to fortellingsverdener, full vennedeling og påloggingssynk er UTSATT, ikke P0.

## Ufravikelige produktregler

- Ett lett tilgjengelig forslag av gangen; uten registreringsplikt, uten skam/tapte streaks og uten å holde brukeren inne i appen. «Gjør noe ute i livet», ikke «få flere skjermminutter».
- Ett regelbasert forslagssystem for hjemme, hverdagsanker, by, landlige områder og ekte POI-er. Aldri fantasisteder, fantasivær, oppdiktede åpningstider eller falske tidsberegninger.
- Integrasjoner: MET Norway via server med korrekt cache/attribution; Geoapify Places kun med frivillig gratis API-nøkkel og eget kvotetak; Google Maps URLs kun som ekstern lenke uten API-nøkkel. IKKE Google Places, Ticketmaster, betalt AI eller kostnadsplikt.
- Offline/ingen posisjon/feil hos kilder: appen fungerer med minst 12 generiske, relevante, redigerte aktiviteter.
- NIM valgfri og voksen/vennlig humor. Engelsk og norsk i første versjon.
- Ikke vis instruerende øvelseskort før dokumentert faglig godkjenning. Legg rutineankre i SAMME anbefalingsflyt, ikke egen modul i grensesnittet.
- Skill «prøver»/«planlagt» og «gjennomført»; kun selvrapportert utført aktivitet i historikk. Ingen oppdiktede minutter/skritt, ingen tracking eller helsediagnoser.
- Data lokalt i gjestemodus. Ingen falske vennekontoer og ingen automatisk konto-/sosialfunksjon i MVP.
- Secure WP PHP: capabilities og nonce for admin, sanitizing/escaping, begrensede eksterne serverkall, rate-limit, aldri nøkkel i klienten eller logger, håndter feil og kvoter.
- Installerbar én-ZIP-plugin, eget appskall uten nødvendig WP-tema. Ikke Node/Composer i produksjonsinstallasjonen.

## Arbeidsmetode og begrensninger

- Opprett egen implementasjonsgren og PR. Codex skal bygge kode, teste og levere ZIP dist/gymnotfound-0.1.0-beta.1.zip, installasjonsveiledning, testbevis, skjermbilder og personverndokumentasjon.
- Gjør rutinemessige utviklingsvalg autonomt innen spesifikasjonen. Bruk ekte tester og oppgi PASS/FAIL/NOT RUN – ikke hev produksjonsklarhet uten verifikasjon.
- Kjør lokale tester først og minimer GitHub Actions-minutter; unngå CI-jobber på hvert push.
- Ikke merge PR, ikke installer på noe live nettsted, ikke endre andre prosjekter, domene, DNS, betaling eller åpne offentlig pilot uten uttrykkelig eiergodkjenning.
- Reference/ med 4.1-prototypen er kun DESIGN-/idé-/kodehistorikk. Den er ikke en installérbar WordPress-plugin.

# AGENTS.md – IKKE TRENING

Dette dokumentet er bindende for Codex og andre kodeagenter i dette repositoriet.

## Arbeidsoppdrag og rekkefølge

Bygg **IKKE TRENING 5.0** som én installérbar WordPress-plugin med mobiltilpasset webapp. Følg `docs/05_CODEX_OPPDRAG_KOPIER_TIL_CODEX.md` og de øvrige dokumentene i `docs/`.

**Prioritet ved motstrid:** sikkerhet/personvern og `docs/04_AKSEPTANSEKRAV_OG_TESTPLAN.md` > `docs/07_HVERDAGSANKRE_OG_MIKROBEVEGELSE.md` > `docs/08_PRESISERING_INTEGRERT_AKTIVITET.md` > `docs/03_TEKNISK_ARKITEKTUR_WORDPRESS.md` > `docs/02_PRODUKTKRAV_5_0.md` > `docs/01_KRITISK_EVALUERING.md` > tidligere demo.

Tidligere grunnmodell og demo finnes under `reference/`. Disse brukes **kun som referanser**, ikke som installérbar produksjonskode. Eldre dokumenter som viser til `kilder_prototype_4_1/` og `dokumentasjon/`, mener materialet under `reference/` i dette repositoriet.

## Ufravikelige produktregler

- **Én integrert hovedflyt.** *Exercise snacks*, mikrobevegelser og rutineankre (kaffe, tannpuss, sofa osv.) er ordinære kandidater i den SAMME anbefalings-/motivasjonsmotoren som turer, ærend, opplevelser og sosial støtte. Ikke lag egen synlig mikrobevegelsesfane, egen poengvaluta eller separat onboarding.
- Atferdsmotoren velger riktig **type hjelp** ut fra hindring (evne/mulighet/motivasjon), deretter relevant handling. Den skal tåle «ikke nå», hvile og avslag.
- Gamification med NIM, kapitler og venner er valgfri; ingen tapte rekker, skyldsignaler eller obligatorisk konkurranse.
- Skille logisk og i databasen mellom planlagt, startet og **egenrapportert gjennomført** aktivitet; repetisjoner/sekunder må ikke oppfinnes som aktivitetsminutter.
- Ikke publiser konkrete bevegelsesinstruksjoner før det finnes registrert faglig godkjenning for kortet. Ved ubehag, smerter eller usikkerhet: sikre alternativer og relevante advarsler, ingen automatisk medisinsk personalisering.
- Ingen eksterne betalte API-er, tracking, CDN, lisenskrav eller nye faste utgifter; ingen hemmeligheter i repo eller logger.
- Bygg en WordPress-plugin med eget responsivt appskall. **Eget WordPress-tema er ikke påkrevd.** Ingen produksjonsinstallasjon fra Codex uten særskilt godkjenning.

## Gjennomføring og kontroll

- Implementer i avgrensede, testbare steg med egne fornuftige commits/PR-er. Ikke be om nye avgjørelser for rutinemessige utviklingsvalg som allerede er avklart.
- Kjør lokale tester først. Hold GitHub Actions-kjøringer på et minimum; ikke legg til ressurskrevende matriser eller automatiske jobber ved hvert push.
- Kontroller WordPress-autorisasjon, nonces, validering, utgående tekst, brukerisolasjon og vennedeling.
- Lever en ZIP som kan installeres via **WordPress → Utvidelser → Legg til ny → Last opp utvidelse** uten Node/npm/Composer på webhotellet.
- Oppgi faktisk testet WordPress/PHP-miljø og eventuelle blockerfunn. Ikke skriv «produksjonsklar» bare fordi ZIP bygges.

# START HER – GymNotFound 0.1.0-beta.1

**Ny eierbeslutning 14.10.2026.** Det gamle «IKKE TRENING 5.0»-oppdraget var for omfattende som første lansering. Vi bygger først en liten, fullt fungerende og installerbar WordPress-app: **en humoristisk aktivitetskamerat som får brukeren bort fra skjermen og inn i livet.**

## Gjeldende dokumenter til Codex

1. [AGENTS.md](../AGENTS.md) – dokumentprioritet, krav og begrensninger.
2. [10_MVP_0_1_AKTIVITETSKAMERAT.md](10_MVP_0_1_AKTIVITETSKAMERAT.md) – én hovedflyt, anbefaling, by/land, vær, reelle steder, fallback og teknisk arkitektur.
3. [11_MVP_0_1_AKSEPTANSETEST.md](11_MVP_0_1_AKSEPTANSETEST.md) – testbar release-gate med mange konkrete scenarier.
4. [09_MERKEVARE_GYMNOTFOUND.md](09_MERKEVARE_GYMNOTFOUND.md) – brand, språk og maskot.
5. Eldre 5.0-krav og 4.1-prototypen – **referanser og senere utvikling**, ikke krav om funksjoner som er uttrykkelig utsatt i 10/11.

## Første WordPress-versjon

Kjerne: én relevant anbefaling på første mobilskjerm, enkel valg av tid og overskudd, én regelmotor, frivillig vær (MET), valgfrie faktiske steder (Geoapify), lokal historikk og tydelig «Legg bort telefonen»-flyt. Uten posisjon, uten POI-nøkkel og ved API-feil må den fremdeles være nyttig. Norsk/engelsk og valgfri NIM.

Utsatt: AI, Ticketmaster, arrangementer, Google Places, store historiekart, sosial plattform, tvungne kontoer og betalte tjenester.

## Utviklingsinstruks

Codex skal lage en NY implementasjonsgren og PR i dette eksisterende repositoriet, levere kildekode, faktiske tester og **dist/gymnotfound-0.1.0-beta.1.zip**, samt installasjonsguide og PASS/FAIL/NOT RUN matrise. Ikke lag en statisk HTML-demo og kall den plugin. Ikke merge eller installer på produksjon uten særskilt eiergodkjenning.

Dette repositoriet eksisterer og er allerede koblet til GitHub. Eldre instruks om å opprette nytt repo er utdatert.

**Status nå:** Spesifikasjon er lagt inn. Installerbar WP-plugin er foreløpig ikke bygget. Tidligere 4.1 er et referanseutkast i reference/, ikke en installasjonsklar WP-plugin.

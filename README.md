# GymNotFound

**En morsom, overraskende intelligent aktivitetskamerat som får folk bort fra skjermen og ut i livet.** Ikke en vanlig treningsapp; ikke et sosialt nettverk.

Offentlig navn: **GymNotFound**. Teknisk slug: **gymnotfound**. NIM er en valgfri maskot. Engelsk og norsk fra første versjon.

## Gjeldende byggemål fra 14.10.2026

**GymNotFound 0.1.0-beta.1 – første installérbare WordPress-beta.**

Den eldre «IKKE TRENING 5.0»-spesifikasjonen var for omfattende som første leveranse. Eier har nå besluttet en smalere MVP med én hovedskjerm, relevant aktivitetsforslag, ekte vær- og stedsintegrasjoner der datakilder er tilgjengelige, by/land-tilpasning og enkel privat historikk. AI, Ticketmaster, større fortellinger og venne-/kontosystem er utsatt.

**Start hos [MVP produktkrav og datakilder](docs/10_MVP_0_1_AKTIVITETSKAMERAT.md) og [MVP akseptanse- og testkrav](docs/11_MVP_0_1_AKSEPTANSETEST.md).**

[AGENTS.md](AGENTS.md) bestemmer dokumentenes prioritet. Eldre dokumenter i docs/00–09 er beholdt som konseptgrunnlag, senere backlog og bindende sikkerhetsprinsipper der de ikke står i konflikt med MVP-scope.

## Hva første versjon gjør

- Gjest åpner appen uten konto og får straks ett relevant og lavterskel aktivitetsforslag.
- Tid, overskudd, svarhistorikk og valgfri urban/landlig kontekst påvirker en **regelbasert** motor. NIM tilfører tørr humor uten å skape press.
- Minimum 36 redigerte aktivitetsmaler på engelsk og norsk. Fungerer uten GPS, API-nøkler eller nettbaserte stedstreff.
- **MET Norway** leverer gratis værdata når lokasjon er kjent (server-side og cached).
- Valgfri gratis **Geoapify Places**-nøkkel gir faktiske steder, kategorier og stedstype; ingen fantasisteder eller krav om Google Places. Google Maps URLs brukes bare til å åpne veibeskrivelser.
- «Gjort» er egenrapportert, «Prøv» er ikke fullført. Lokal historikk, eksport/sletting og enkel administrasjon.
- Én selvstendig WordPress-plugin ZIP med ferdigbygde assets. Ingen obligatorisk WP-theme, AI-API, betalingsabonnement eller eksterne trackingtjenester.

## Status

**Spesifikasjon levert til Codex, pluginen er ikke ferdig utviklet eller installert.** 4.1-prototypen i reference/ er en statisk demo/teknisk referanse, ikke en ferdig WordPress-plugin. Ved ferdig utvikling skal Codex levere dist/gymnotfound-0.1.0-beta.1.zip, PR og dokumentert teststatus.

Ingen merge eller produksjonsinstallasjon uten uttrykkelig eiergodkjenning.

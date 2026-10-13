# IKKE TRENING 5.0 – WordPress/Codex-overlevering

**Status:** Evalueringen og Codex-bestillingen er ferdig. Dette er en **spesifikasjonspakke**, ikke en allerede kodet/installert WordPress-plugin. Den eksisterende 4.1-kilden følger med som referanse. Ingen produksjon eller installasjon er gjort.

## Kort konklusjon

- **GO:** bygg en ordentlig installérbar testversjon på et eget WordPress-domene.
- **NO-GO:** installer 4.1-koden uendret og kall den fullversjon. Mikroøvelser **kan ikke publiseres uten dokumentert faglig gjennomgang av instruksjonene**.
- **Kun én plugin:** eget WordPress-tema er ikke påkrevd; pluginskallet leverer den visuelle appen. Eget tema kan bli aktuelt for en senere selvstendig markedsføringsnettside.
- **Funksjonell test-beta:** WordPress-brukere, datalagring, én samlet atferds- og anbefalingsmotor der **hverdagsankre/mikrobevegelser inngår som ordinære, relevante handlingsvalg**, NIM, to komplette reiser, ekte frivillig vennemodus, privatliv og WP-admin.
- **Ikke bygg enda:** betaling, AI-API, sporing/kart, klinisk helseprofilering eller betalte varslingstjenester.

## Les i denne rekkefølgen

1. `01_KRITISK_EVALUERING.md` – funn i eksisterende konsept og kode.
2. `02_PRODUKTKRAV_5_0.md` – hva appen skal gjøre for brukere og administrator.
3. `03_TEKNISK_ARKITEKTUR_WORDPRESS.md` – plugin, database, API, autorisasjon og design.
4. `04_AKSEPTANSEKRAV_OG_TESTPLAN.md` – objektiv test/leveranse-gate.
5. `05_CODEX_OPPDRAG_KOPIER_TIL_CODEX.md` – ferdig oppdragstekst til Codex.
6. `06_FAKTA_OG_KILDER.md` – utvalgte forsknings- og WordPress-referanser.
7. `07_HVERDAGSANKRE_OG_MIKROBEVEGELSE.md` – **normative, sikkerhetsstyrte krav for en integrert del av samme aktivitetsmotor** (eget dokument er kun for implementasjonsdetaljer, ikke en separat brukerfunksjon).
8. `08_PRESISERING_INTEGRERT_AKTIVITET.md` – **overordnet presisering fra bestiller: ikke separat meny, modul på siden eller konkurrerende flyt.**
9. `kilder_prototype_4_1/` – eksisterende app-filer og skjermbilder som kan brukes som visuell/kodemessig referanse.
10. `dokumentasjon/` – atferdsmodellen fra 4.0 som må bevares.

## Praktisk prosess

1. Opprett et **nytt privat GitHub-repository** med arbeidsnavn `ikke-trening` (ikke bruk repoene for andre prosjekter).
2. Gjør dette dokumentsettet og kildefilene tilgjengelige for Codex i repositoryet, eller last opp ZIP-pakken i arbeidsmiljøet der Codex kjører.
3. Gi Codex innholdet i `05_CODEX_OPPDRAG_KOPIER_TIL_CODEX.md` som hovedoppdrag. Den peker på de øvrige normative kravene.
4. Codex utvikler og tester separat fra annet arbeid, leverer Git-PR-er og **én installerbar ZIP** etter at P0-kravene er oppfylt.
5. Installer bare på ditt **testdomene** etter en egen status-/installasjonskontroll. Ikke sett offentlig pilot i gang før du bestemmer det.

## Merk om GitHub

Ved gjennomgang 13.10.2026 ble bare eksisterende prosjektrepositorier med navnene `Viamo`, `Husvarme` og `HighBias` funnet. Det var ikke et identifisert `ikke-trening`-repo å plassere oppdraget i. Det er grunnen til at denne pakken er produsert som en separat Codex-overlevering, ikke som et opprettet GitHub-issue i et uvedkommende prosjekt.

## Installasjon i fremtiden

WP-admin → Utvidelser → Legg til ny → Last opp ZIP → Installer → Aktiver → IKKE TRENING → Oppsett → Opprett/velg appside → Forhåndsvis. Dette er ønsket sluttresultat; zipen i denne pakken er **IKKE** pluginen, men bestillingen og referansekilden.
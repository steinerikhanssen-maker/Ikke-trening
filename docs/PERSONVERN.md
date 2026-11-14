# Personvern og datakilder — GymNotFound 0.1.0-beta.1

GymNotFound gir generelle aktivitetsideer. Besøkende bruker gjestemodus, uten konto, e-post, annonser, analytics eller tredjepartsfonter. Appen bruker ikke diagnoser, alder, kjønn, skritt, puls eller bakgrunnssporing. Nettstedets eier er ansvarlig for nettstedets samlede personverninformasjon og hostinglogger.

## Data i nettleseren

En versjonert post i lokal lagring (`gymnotfound.v1`, schema 1) inneholder språk, avsatt tid, overskudd, selvvalgt miljø, gratisvalg, NIM-valg, sist viste ideer, feedback, en eventuell idé på lur og egne «Gjort»-rapporter. Opp til 500 fullføringer og 100 svar beholdes; gamle forslag begrenses til 12. Schema 0 migreres til schema 1, ukjent schema eller ødelagt data gir sikre standardvalg.

«Prøv» er `accepted`, og er aldri bevis for fullføring. Bare eksplisitt «Gjort» lager `completed_self_report` med kort-ID, egenrapportert tittel/type og tidspunkt. Ingen målte minutter, trinn, skritt eller posisjon inngår i fullføringer eller feedback. Det finnes ingen serverprofil, gjeste-ID, kontosynk, venner eller delt historikk. Dataene følger denne nettleseren/enheten; privat modus, rydding av nettleserdata eller en annen enhet kan gi tom historikk.

**Mine valg → Eksporter mine data** lager en lokal JSON-fil. Den kan inneholde det grove området du selv har valgt, fordi det er en preferanse. Eksporten sendes ikke til serveren. **Slett mine appdata** krever bekreftelse og nullstiller bare appens egne data. Andre nettsteddata berøres ikke. Dersom nettleseren nekter lagring, fungerer ideene i minnet og appen opplyser at data kan forsvinne.

## Frivillig område

Posisjon hentes én gang, først når besøkende trykker **Bruk min omtrentlige posisjon**. Ingen automatisk tillatelsesdialog, `watchPosition`, GPS-spor eller bakgrunnsinnsamling. Rå browser-koordinater avrundes umiddelbart til to desimaler før de sendes eller lagres. Presisjonen er grovt rundt en kilometer, med variasjon etter breddegrad. Et manuelt valgt område lagres med samme grove presisjon.

Bare dette grove området og de relevante valgene tid/miljø sendes til WordPress for kildeoppslaget. Det lagres ikke en personlig posisjonshistorikk på serveren. Delte provider-cacher er nøkkelsatt med hash av geografisk celle/radius; stedsobjektene er offentlige POI-data fra leverandøren. Et tidligere uttrykkelig valgt område kan brukes ved ny åpning for aktuell prognose/steder. **Glem dette området** fjerner preferansen og bruker stedsløse ideer. Sletting av appdata gjør det samme og ugyldiggjør forsinkede posisjonssvar.

## Eksterne mottakere

| Kilde | Når | Data | Formål og kreditering |
| --- | --- | --- | --- |
| MET Norway Locationforecast | Bare med valgt område og vær aktivert | Avrundet bredde-/lengdegrad, prosjektidentifiserende User-Agent og webhotellets server-IP | Værtilpassing; «Basert på data fra MET Norway» ved aktuell prognose. [Vilkår](https://api.met.no/doc/TermsOfService) og [lisens/kreditering](https://www.met.no/frie-meteorologiske-data/lisensiering-og-kreditering). |
| Geoapify Places | Bare med valgt område, aktivert kilde og adminens valgfrie nøkkel | Grovt område/radius, kategorier, maksimum 20 treff og server-IP | Faktiske stedsforslag med [Geoapify](https://www.geoapify.com/terms-and-conditions/) og [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright). [Personvern](https://www.geoapify.com/privacy-policy/). |
| Geoapify Geocoding | Først ved eksplisitt **Søk** i valgfritt by-/områdesøk | Det innsendte stedsnavnet og server-IP | Velge et grovt område. Ingen autocomplete, gateadressekrav eller automatisk søk mens man skriver. |
| Google Maps | Bare når besøkende klikker lenken | Offentlig destinasjonskoordinat i URL; vanlig nettleser-/IP-informasjon hos Google | Ekstern visning/veibeskrivelse. Brukerens startposisjon og historikk legges ikke i lenken. `noopener noreferrer` brukes. Ingen API-nøkkel eller innebygd Maps SDK. [Googles personvern](https://policies.google.com/privacy). |

Historikk, egenrapporteringer, feedback og andre lokale apppreferanser sendes aldri til MET eller Geoapify. Feil, gammelt vær, tomme stedssvar, fravær av nøkkel og kvotetak gir generiske ideer. Kreditering for vær/steder vises bare når den aktuelle kilden faktisk brukes. Mulige kostnader, adgang og åpningstider er ikke verifisert; appen lover dem ikke. Ingen avstand konverteres til reisetid.

## Server og admin

Adminens Geoapify-nøkkel krypteres med AES-256-GCM og en nøkkel utledet av nettstedets WordPress-salt, i en ikke-autoloadet option. Nøkkelen sendes bare til faste Geoapify HTTPS-endepunkter. Den gjengis ikke i frontend, REST-svar eller appens diagnostikk/logging. En administrator med tilgang til database og WordPress-salts kan naturligvis dekryptere den; kryptering erstatter ikke hostingens tilgangskontroll og sikkerhetskopirutiner. Ingen nøkkel følger med i ZIP eller fixtures.

Anonyme kildeforespørsler begrenses med en saltet HMAC av serverens mottatte IP-adresse, i en kortlivet transient (90 sekunder; 60-sekunders vindu), pluss et globalt tak. Rå IP lagres ikke av appen, og hashene kobles ikke til koordinater eller historikk. Vanlig WordPress/webhotell kan ha egne tilgangslogger med IP, tidspunkt og nettleserinformasjon. Nettstedseieren må kontrollere disse separat, spesielt hvis andre plugins logger HTTP-forespørsler eller POST-innhold.

Admin lagrer redigerte aktivitetsmaler og eventuelle faglige godkjenningsopplysninger i WordPress. Denne innholdsadministrasjonen er ikke en besøksprofil. Kilde-status viser bare tilstand, tidspunkt, cacheutløp og samlede egne kall/kredittestimater. Fast HTTPS-allowlist, null redirects, TLS-verifisering, validerte parametre, tidsavbrudd, responsgrenser, delt cache og atomiske kvoter begrenser kildebruk. Offentlige ruter tar ingen klientstyrt URL og har ingen historikk-/konto-endepunkt.

Deaktivering og avinstallering beholder admininnstillinger og maler for å unngå utilsiktet datatap. Gjesten sletter nettleserdata i appen; eieren fjerner egne serverinnstillinger/maler uttrykkelig dersom nettstedet avvikles. Ingen produksjonsinstallasjon eller offentlig pilot er utført som del av denne leveransen.

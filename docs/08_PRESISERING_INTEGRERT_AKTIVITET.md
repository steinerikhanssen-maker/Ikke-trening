# IKKE TRENING 5.0 – bindende presisering: integrert aktivitet, ikke sidemodul

**Bestilleravklaring 13. oktober 2026.** Denne presiseringen går foran eldre formuleringer som «egen modul» eller «tilleggsmodell» dersom det skulle oppfattes som en separat brukerfunksjon. Den endrer ikke kravene om sikkerhet, personvern eller faglig godkjenning.

## Én produktidé, én brukerreise

IKKE TRENING skal hjelpe brukeren å bevege seg på en måte som passer personens liv. En av måtene er *exercise snacks / aktivitetsdrypp*: noen bevegelser koblet til noe man allerede gjør, for eksempel etter tannpuss, mens kaffen blir klar (på trygg avstand fra varmt utstyr), når man reiser seg fra sofaen eller når man passerer stua. Dette **er en integrert del av produktets hovedkonsept**, på lik linje med turer, praktiske ærend, opplevelser og frivillig sosial aktivitet.

**IKKE bygg:** separat «Mikrobevegelser»-hovedmeny, obligatorisk sidemodul, egen onboarding, separat motiveringsmotor, egne poeng eller et ekstra treningsprogram ved siden av hovedflyten. At WordPress-arkitekturen har interne moduler/tabeller og at kravene er skrevet i et eget dokument, skal ikke føre til en separat brukeropplevelse.

**Bygg i stedet:**

1. Brukeren beskriver hindring, ønsker og hvilken hverdagsrutine som kunne passe. Opplysninger kan velges ved behov; de skal ikke bli en lang obligatorisk kartlegging.
2. **Én felles motor** velger støtte og en handling: ved lite tid kan det være en trygg, kvalitetssikret mikrohandling knyttet til kaffe/tannpuss/sofa; en annen dag en tur, et praktisk gjøremål, et lite fellesskapsoppdrag eller en plan.
3. **Samme «I dag»-kort** viser en relevant handling, med enkel tilgang til «enklere», «annet forslag», «knytt til rutine», «gjør senere», «ikke nå» – uten å navigere til en egen mikro-fane. Rutineankre kan redigeres i samme plan-/innstillingsflyt.
4. Registrering og feedback følger samme hendelses- og læringssløyfe. Loggen kan skille `reported_reps`/`reported_seconds` fra minutter for å være ærlig, men det er fremdeles **én personlig aktivitetslogg**. Hverdagsbevegelser gir ikke automatisk registrering ved planlegging.
5. NIM, kart og frivillig sosial del behandler gjennomført mikroaktivitet som en mulig **daglig** aktivitet på samme vilkår som annen aktivitet, med samme maksimalt én kapittelbonus per dag. Intet separat spill.
6. Ved avslag eller ubehag kan systemet bytte **mellom** mikrobevegelse, tur, praktisk handling, pause eller annen støtte. Ved gjenstart kan det velge tidligere nyttige rutiner.
7. **Ingen obligatorisk appåpning** ved hver rutine: brukeren får et lettfattelig når–så-opplegg som kan følges uten telefon. Eventuell registrering skjer frivillig etterpå; ikke påstå at appen oppdager kaffe eller tannpuss.

## Godkjenningseksempler for Codex

- Profil med hindringen «ingen tid», valgt anker «etter kaffe» og tilgang til faglig gjennomgått kort får et **mikrobevegelsesforslag øverst på den vanlige I dag-skjermen**, ikke en lenke til en egen avdeling.
- Endres hindringen til «vil ha frisk luft», kan den samme motoren anbefale en gåtur. Et avvist turforslag kan lede tilbake til et hverdagsanker.
- En registrert mikrohandling telles som selvrapporterte repetisjoner/sekunder, **ikke oppdiktede minutter eller medisinske effekter**. Dagsbegrensningen for spill er felles.
- NIM av, ingen venner og ingen varsler skal ikke påvirke evnen til å få og gjennomføre et rutinebasert forslag.
- Ingen faglig gjennomgang betyr ingen publisert instruksjonskort til vanlige brukere. Motoren må da tilby en annen trygg, tilgjengelig handling, ikke en uautorisert øvelse.

## Skille mellom produkt og kode

Det er riktig å ha egne PHP-klasser, REST-ruter og lagringsfelter for kvalitet, sikkerhet og datanøyaktighet. **Arkitektonisk modularitet er ikke produktmessig fragmentering.** Codex skal bygge et samlet produkt med et enkelt grensesnitt og én personlig motivasjonsmotor.
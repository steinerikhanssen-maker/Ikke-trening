# IKKE TRENING 4.1 – NIM, oppdagelser og valgfritt fellesskap

**Dato:** 13. oktober 2026  
**Status:** Klikkbar og lokalt testet konseptprototype. Ikke en publisert tjeneste, klinisk validert intervensjon eller automatisk helsemåler.  
**Videreføring av:** IKKE TRENING 4.0, der appen først skal velge riktig type hjelp før den foreslår en aktivitet.

## 1. Beslutning

**Ta inn gamification, men bare når det støtter aktivitet utenfor skjermen.** Ikke gjør hele produktet om til et poengspill. Behold 4.0-prinsippet om at manglende anledning, kapasitet og motivasjon krever forskjellig hjelp.

Vi tester en felles idé: *En aktivitet kan bli mer attraktiv hvis den åpner et lite kapittel i en større fortelling, en original følgesvenn bekrefter fremgangen, og en venn kan delta uten sammenligning av resultater.*

Dette er et **produktdesign vi ønsker å undersøke**, ikke en dokumentert virkningsmekanisme for denne kombinasjonen.

## 2. Hva forskningen sier

- Metaanalysen publisert i 2025 inkluderte 36 randomiserte studier, 10 079 deltakere. Gamification ga i gjennomsnitt rundt 489 skritt ekstra per dag sammenlignet med tilsvarende ikke-spillifiserte apper; effekten var liten. Kilde: https://pubmed.ncbi.nlm.nih.gov/39764571/
- BE ACTIVE (2024), 1 062 deltakere med forhøyet kardiovaskulær risiko: spillmekanismer alene +538 skritt per dag, gamification kombinert med økonomisk incentiv +868 skritt, relativt til kontroll, under ett års intervensjon. Bare kombinasjonen hadde tydelig vedvarende effekt etter korreksjon for flere tester i seks måneders oppfølging. Kilde: https://pubmed.ncbi.nlm.nih.gov/38583084/
- 2026-kartleggingen i JMIR Serious Games omfattet 53 RCT-er/34 unike tiltak, identifiserte 48 spill-elementer. Det er et designkart, **ikke** dokumentasjon for at hver komponent virker. Kilde: https://games.jmir.org/2026/1/e85804/
- STEP UP sammenlignet blant annet støtte, samarbeid og konkurranse. Konkurranse ga størst og mest varig effekt i dette forsøket. Det gir ingen grunn til å påtvinge konkurranse til treningsuvillige. Kilde: https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2749761
- Duolingo hevder at brukere med «Friend Streak» er 22 % mer tilbøyelige til å gjøre daglig leksjon. Dette er selskapets egen produktanalyse, ikke en kontrollert test av vår målgruppe. Kilde: https://blog.duolingo.com/friend-streak/
- Pikmin Bloom lar brukere samarbeide asynkront om gangutfordringer; det gir en relevant modell for vennemodus. Kilde: https://pikminbloom.com/en
- En 2026-diskusjon blant Strava-brukere viser også hvorfor tapsbaserte rekker kan skape dårlig samvittighet, blant annet ved skade. Dette er erfaringer i forum, ikke representativ statistikk. Kilde: https://www.reddit.com/r/Strava/comments/1sljyof/

## 3. Gamification-hypotesene

**H1 – Følgesvenn:** En liten, varm og original maskot kan gjøre det mer lystbetont å åpne appen og gi positiv forsterkning. Figuren har ingen behov som brukeren må oppfylle, og ser aldri skuffet ut ved pause. Maskoten kan slås av.

**H2 – Oppdagelser:** En fiktiv verden med kapitler og små historier gir et nysgjerrighetsmål fremfor et rent treningsmål. Det må finnes ekte innhold – ikke bare merker og XP.

**H3 – Små bidrag sammen:** To eller tre venner kan bidra med handlinger på egne nivåer uten å måtte være fysisk sammen. Ikke vurder hverandre etter rå skritt eller intensitet. Ingen deler aktivitet uten samtykke.

**H4 – Gjenstart uten tap:** Tidligere kapitler, samling og fremgang beholdes etter pause. Aktivitet skal ikke presses frem ved sykdom eller smerte. Dette er i utgangspunktet et etisk designprinsipp og hypotese om tilbakekomst.

**H5 – Riktig hjelp først:** Gamification brukes *etter* grunnleggende forståelse av hindringen. Mangler brukeren tid, må appen hjelpe med planlegging. Ved smerter må den ikke lokke til høyere belastning. Ved manglende mening kan den utforske personlige mål.

## 4. Maskoten NIM

NIM er et foreløpig navn på en original, liten navigasjonsfigur som ligner et lysende, avrundet veimerke, ikke en fugl eller en kopi av Duolingo. Designet balanserer voksen enkelhet og lekenhet:

- Varme naturfarger, avdempet grønn og honninggult, med valgfri mosegrønn, solvarm eller kveldslilla figur.
- Rolig flytende bevegelse; respekterer «redusert bevegelse».
- Korte, situasjonssensitive meldinger, aldri skyldfølelse.
- Ingen «mat», «humør» eller «helse» som taper seg når brukeren hviler.
- Frivillig: en bruker kan slå av figuren og fortsatt bruke hele tjenesten.

**Navn, domene og eventuell varemerkekollisjon er ikke kontrollert.**

## 5. Selve spillet: små ekspedisjoner

1. Brukeren velger hindringen sin, som i 4.0.
2. Brukeren kan velge Nysgjerrig, Bare få det gjort, eller Sammen med noen.
3. Appen gir **én realistisk handling eller hjelpemekanisme**.
4. Å trykke «Start», lage avtale, åpne appen eller simulere venner gir ingen fysiske aktivitetspoeng.
5. Etter faktisk gjennomført aktivitet registrerer brukeren minutter og hvordan det opplevdes. Dette er **egenrapportering**, ikke objektiv måling.
6. En gjennomføring åpner ett av seks korte fortellingskapitler. Teksten kan leses, og en eksperimentell nettleseropplesning er tilgjengelig der den støttes.
7. Har brukeren en negativ opplevelse, forsøker neste forslag å endre typen aktivitet, ikke bare varigheten eller belønningen.
8. Reisen kan fortsette etter uker uten registrering, uten at tidligere kapitler forsvinner.

To små innholdstemaer finnes i demoen: **Byer og steder** og **Skog og landskap**. Seks kapitler er bare nok til å demonstrere mekanikken, ikke til å holde på brukere i måneder.

## 6. Sosial design

**Førstevalg: valgfritt, asynkront samarbeid.** Eksempel: seks bidrag på én uke, der alle kan bidra gjennom gjennomføringer på sitt eget nivå. Ingen vil bli vist som svakeste deltaker, og én som blir syk skal ikke ødelegge for alle.

Det finnes ingen ekte venneløsning i prototypen. Den lar brukeren kopiere en invitasjon og skru på **tydelig merkede, oppdiktede demovenner**. Ingen data sendes til noen.

Konkurranse, rangering og felles aktivitetsdata bør først vurderes etter at vi har testet om brukerne ønsker dette, og etter at samtykke og personvern er på plass. Frivillige, relativt balanserte konkurranser kan være nyttig for noen, men er ikke standard.

## 7. Skjerm- og produktopplevelse

Den første skjermen skal vise: «Hva står i veien i dag?», ett relevant forslag og NIM som en valgfri støtte. Historiekartet er sekundært, men godt synlig. Sosialt samarbeid ligger på egen fane. Brukeren skal kunne registrere aktivitet eller en pause uten å åpne flere menyer.

Vi har ikke implementert en fullverdig aktivitetsmåler, ekte pushvarsler, bakgrunnstjenester, Android Health Connect, Apple Health eller virkelig vennedeling.

## 8. Det som må ikke komme i produksjon ukritisk

- Ingen daglige tapsrekker eller mas om skadde/dårlige dager.
- Ingen skjulte «dopamin»-mekanismer, kjøpepoeng, lokkebokser eller betalte liv/bonuser.
- Ingen rangering av objektivt ulike fysiske forutsetninger som om de var like.
- Ikke mål suksess i appåpninger alene. Mål faktisk aktivitet, varighet, opplevd autonomi, opplevelsen av press og behovet for å komme tilbake.
- Ikke bruk masker med «trist ansikt» for å få mer trening fra syke eller slitne brukere.
- Automatisk registrering krever plattformintegrasjoner; egenrapporterte minutter kan ikke brukes som bevis på reell helseeffekt.
- Spillet kan ikke love å forebygge hjerteinfarkt.

## 9. Nøktern prioritering

**P0 – beholde fra 4.0:** Identifiser riktig type hindring; oppgave gjennomførbar; samtykke til deling; ingen aktivitetspoeng for plan; hvile uten straff.

**P1 – bygge videre på 4.1 hvis brukere vil ha det:** Flere faktiske opplevelser, bedre tilbakemeldinger, flere fortellingsstiler, frivillige venner og enkle støttevalg. En begrenset, manuelt koordinert sosial test før dyr backend.

**P2 – først hvis dokumentert nødvendig:** App-/helseintegrasjoner, profesjonelle historieinnspillinger, stedsbaserte oppdrag, avansert AI-generert fortelling, stor spilløkonomi og reell sosial infrastruktur.

## 10. Det avgjørende forsøket

Sammenlign (A) 4.0 uten spill, (B) 4.1 med følgesvenn og oppdagelser og eventuelt (C) 4.1 med frivillig vennemodus. Det viktigste er gjennomført fysisk aktivitet målt uavhengig av appen, ikke hvor lenge brukeren ser på figuren. Undersøk om maskoten gir økt lyst, irritasjon, prestasjonspress eller ingen forskjell. Et lite eksplorativt forsøk sier ikke noe sikkert om langtidseffekt.

**Konklusjon:** Gamification fortjener en ordentlig produktvariant og brukertest. Maskot + fortelling + frivillig samarbeid er interessant, men må bevises bedre enn en enklere løsning. 4.0 forblir den faglige grunnmuren.
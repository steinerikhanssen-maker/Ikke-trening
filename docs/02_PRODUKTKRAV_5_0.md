# IKKE TRENING 5.0 – fullstendig produktkrav for installerbar WordPress-beta

**Formål:** En reell, privat testversjon på ett WordPress-domene; ikke klinisk helsehjelp og ikke et ferdig kommersielt produkt. Primærspråk norsk bokmål. Brukere kan være kvinner og menn i ulike aldre; motstandstyper er primær segmentering. Første markedsføringsgruppe kan være voksne 40+/50+, men ikke bygg alder/kjønn inn i beslutningsreglene.

## 1. Produktkjernen: rett hjelp, først

Behold 4.0-prinsippet: forstå hva som hindrer handling, og velg *type hjelp* før forslag til aktivitet. Profilen skal aldri tolkes som en diagnose eller låses permanent. Onboarding må kunne gjennomføres på under ett minutt og helt uten konto for en forhåndsvisning. Følg den smale flyten `Jeg vil -> Hva står i veien? -> Slik kan vi hjelpe -> Første konkrete handling -> Hva skjedde? -> Nytt relevant forslag`.

Situasjonskategorier (kan endres fra dag til dag): (a) Kommer ikke i gang, (b) opplever aktivitet som kjedelig, (c) mangler faktisk tid/anledning, (d) lite overskudd, (e) fysisk/sosialt ubehag, (f) ser ikke meningen, (g) ønsker selskap, (h) har falt ut, (i) vil bygge kapasitet. «Smerte/uvanlige symptomer» må trigge nøktern sikkerhetshjelp og tilby hvile/individuell vurdering, ikke automatisk foreslå mer intensitet.

Støttemekanismer velges ut fra kategorien: handlingsstart, hindringsfjerning/kalenderplan + plan B, enklere aktivitet/miljø, verdibasert refleksjon, sosial invitasjon, gjenstart eller trygg frivillig progresjon. Brukeren skal kunne velge annen hjelp. Ta høyde for at noen *ikke* ønsker å like trening, men vil «bare få det gjort».

**Kjerneintegrasjon – obligatorisk:** Handlingsmotoren har én felles beslutningsflyt og **flere likestilte typer fysisk aktivitet**: en liten bevegelse knyttet til tannpuss/kaffe/sofa (*exercise snack*), en gåtur, en praktisk oppgave, en sosial aktivitet eller eventuelt et mer tradisjonelt treningsinnslag. Den velger **riktig handling og riktig anledning ut fra brukerens reelle hindring**. Det finnes IKKE et eget parallelt «exercise snacks»-produkt, separat førstegangsfane eller funksjon som brukeren må navigere til på siden. Brukeren kan selvfølgelig selv velge en mikrobevegelse eller definere et hverdagsanker i den ordinære flyten. Kodens interne ansvarsdeling er ikke det samme som en separat brukeropplevelse.

## 2. Fullverdige brukerreiser – ikke statiske demoer

### 2.1 Første besøk uten konto
- En offentlig, mobiltilpasset produktside viser kort hva tjenesten gjør, en kompakt NIM og én tydelig handling: «Hva står i veien i dag?». Ikke blokkér første opplevelse med registrering.
- Gjør det mulig å prøve en kort interaktiv flyt i **gjestemodus**, uten lagring på server og uten fiktiv eller ekte sosial deling. Gjestemodus skal merkes tydelig og kan bevares lokalt frivillig.
- Ved ønske om å lagre egen historikk/åpne varig reise/ha venner: oppfordre til å opprette eller logge inn med vanlig WordPress-bruker. Ved frivillig overgang skal valg kunne overføres til kontoen etter eksplisitt bekreftelse. Ikke åpne WordPress-registrering automatisk ved plugin-aktivering.

### 2.2 Innlogget «I dag»
- Etter første pålogging vis **én anbefalt handling over folden** på 390 px mobil. Denne kan like gjerne være «når kaffetrakteren er satt på, gjør noen rolige bevegelser» som «ta en kort tur», hvis det passer kontekst og preferanser. Hinder-valg som kompakt endringsknapp, ikke et stort skjema som presser oppdraget langt ned.
- Skille «Foreslått», «Planlagt», «Prøvd», «Gjennomført», «Pauset», «Avvist». Ingen poeng, «skritt», minutter eller historieopplåsing bare fordi en knapp ble trykket.
- Registrering av faktisk aktivitet: vanlige økter oppgir minutter fra 1–120; **mikrobevegelser** kan i stedet oppgi selvrapportert antall repetisjoner eller sekunder (og har da `reported_minutes = NULL`); type (gange / praktisk bevegelse / styrke / mikrobevegelse / annet, valgfri), subjektiv innsats (valgfri), «kunne gjort dette igjen?» og eventuelt «hva hindret neste gang?». Markert **egenrapportert**, ikke målt.
- Negative tilbakemeldinger skal kunne gi relevant endring (sted, støtte, aktivitetstype, varighet eller plan), ikke bare nytt tilfeldig kort. Vis kort «Vi foreslår dette fordi …».
- «Ikke nå» skal være gyldig valg uten negativt signal eller eskalerende påminnelser.

### 2.3 Plan / oppfølging
- En avtale kan ha konkret tidspunkt eller knyttes til en eksisterende hendelse («etter kaffe»), i tillegg til en reserveplan. Avtaler skal kunne redigeres/slettes.
- Kalender: generer gyldig `.ics`-fil for eksplisitt valgte klokkeslett; hvis hendelsen er vag («etter middag»), foreslå en konkret tid før eksport i stedet for å dikte opp klokkeslett.
- I første beta er in-app oversikt og kalender-eksport nok. Ingen lovnad om serverpush eller SMS. Eventuell e-postpåminnelse skal være en **separat** valgfri funksjon som kun aktiveres hvis WP e-post fungerer og bruker uttrykkelig samtykker; aldri nødvendig for at appen skal fungere. Ikke implementer betalte varslingsleverandører.

### 2.4 NIM-maskoten
- Behold grunnformen og originale SVG-utgangspunktet fra 4.1, men videreutvikle den til en tydelig, moderne og veltegnet stil uten tredjepartslisenser. 3 fargevarianter, begrenset antall rolige animasjoner, støtte for `prefers-reduced-motion`.
- Tilstander: nysgjerrig, nøytral, velkomst tilbake, positiv bekreftelse. Ikke trist/syk/hungrig ved pause. Ingen emosjonell utpressing («NIM savnet deg og er skuffet»).
- Maskoten og hele spillaget skal kunne slås av enkelt, og tjenestens handlingsstøtte forbli funksjonell.

### 2.5 Oppdagelsesreise / innhold
- Minst **to redigerbare verdener** (steder/byliv og natur) med minimum **tolv ekte redigerte kapitler per verden** ved beta-levering. Bruk de eksisterende 12 som inspirasjon/utgangspunkt, skriv resten som selvstendige, gjennomarbeidede kapitler. Ingen generiske «gratulerer, du låste opp nivå 4»-tekster som erstatning for faktisk innhold.
- Kartet skal føles som fremdrift gjennom en opplevelse, ikke som en skritteller. Brukeren velger verden; historien kan leses i etterkant. Nettleser-TTS kan tilbys når plattformen støtter det, men kan slås av.
- Opplåsing: et selvrapportert **gjennomført** nytt aktivitetsbidrag kan åpne maksimalt ett kapittel per lokal kalenderdag (server registrerer UTC og brukerens deklarerte tidssone). Flere aktiviteter kan registreres samme dag, men gir ikke uendelig kapittelopplåsing. Ikke lag daglig påbud eller tapsrekke. Ved pause forblir kapitler låst opp. Å registrere varighet skal **ikke** omtales som objektivt verifisert.
- Fortellingen og «spillpoeng» er atskilt fra aktivitetslogg/helseindikatorer. Nullstilling av spill skal være mulig uten å slette helseloggen dersom brukeren ønsker.
- Unngå en skjult uendelig belønningsspiral. Ved ferdig gjennomført tilgjengelig reise: vis «du har fullført denne fortellingen», og gi mulighet til ny verden eller fri aktivitet, ikke gjenta samme premie på hver registrering.

### 2.6 Faktiske venner og frivillig fellesskap
- Gruppen består av 2–4 WordPress-brukere og opprettes frivillig. Invitasjon med tidsbegrenset engangslink eller eksplisitt delingslenke som kun virker etter konto/aksept. Ingen kan melde på andre uten godkjenning.
- En gruppe kan bidra til ett felles oppdagelseskart gjennom **bidrag**, ikke rå minutter eller skritt. Hver gruppevenn må velge om egne bidrag skal deles; i standardvisning vises bare frivillig valgt visningsnavn + «bidro» og eventuelt gruppesum. Ikke vis puls, fysisk kapasitet, ubehag, nøyaktige minutter, geolokasjon eller fravær.
- Ikke vis «siste aktive person», «svakeste deltaker» eller «din venn venter på deg». En syk venn stopper aldri personlig progresjon, og grupper har ikke nedtellingsfrist som straffer andre.
- Bruker kan forlate gruppe når som helst og trekke tilbake deling. Historiske sosiale bidrag må håndteres etter tydelig privatlivsregel (anonymiser bidrag i gruppevisning ved utmelding/sletting).
- **Ingen fiktive deltakere i ekte brukergrensesnitt.** Adminstyrt demosimulering kun i isolert forhåndsvisning og tydelig merket, aldri blandet med reelle aktiviteter.

### 2.7 Gjenstart
- Ved lang pause i appen: vis vennlig «Velkommen tilbake. Hva passer nå?» som et valg, ikke automatisk antakelse om inaktivitet.
- Tilby «Fortsett det jeg likte», «Noe enklere», «Det har endret seg» eller «Pause». Tidligere kapitler og prestasjoner beholdes. Ingen tapte streaks.
- Bevar tidligere erfaringer, men vekten på en enkelt avvisning avtar i regelmotoren, slik at man kan prøve igjen dersom bruker ønsker det.

### 2.8 Min vei / personlig fremgang
- Vis selvrapporterte gjennomføringer og minutter separat fra oppdagelseskapitler, grupper og planer. Ikke konverter «gå en runde i huset» til sannsynlig reduksjon i risiko for hjerteinfarkt.
- Et senere nivå tilbyr tryggere frivillig progresjon mot anbefalt aktivitet, inkludert styrke. **Kun en liten, faglig gjennomgått bank med mikrohandlinger inngår i betaen** (se 2.10); utvidede styrkeprogram eller individuelle belastningsopplegg ved sykdom er ikke en del av denne versjonen.
- Målinger skal ikke forutsette smartklokke. Appen fungerer fullt ut uten Health Connect, Apple Health eller andre eksterne tjenester.

### 2.9 Mine valg / personvern
- Oppdatere mål, oppfølgingsstil, NIM av/på, farger, verden, TTS, tilgjengelighetsvalg, tidssone og frivillig social sharing.
- Eksport av alle egne appdata til maskinlesbart format. Slett alle appdata uten å nødvendigvis slette WordPress-kontoen; bekreft irreversible handlinger tydelig. Gi info om eventuell anonymisering av gruppespor.
- Respekter WordPress' personvernverktøy for eksport, sletting og policytekst.

### 2.10 Hverdagsankre og mikroaktivitet – INTEGRERT P0-DEL AV PRODUKTKJERNEN

**Full normativ spesifikasjon:** `07_HVERDAGSANKRE_OG_MIKROBEVEGELSE.md` og presiseringen i `08_PRESISERING_INTEGRERT_AKTIVITET.md`. Dette er et eget kravavsnitt av tekniske og sikkerhetsmessige grunner, **ikke en egen appmodul i brukeropplevelsen**.

- Hverdagsankre og mikrobevegelser er **en type ordinær anbefaling på «I dag»**, valgt av samme beslutningsmotor som turer, ærend og sosial aktivitet. Når motstanden er tidsmangel/startfriksjon og personen ønsker små bevegelser, kan disse være standardforslaget, ikke en lenke til et separat område. Den som vil, kan velge «Bruk noe du allerede gjør» som valgmulighet i samme flyt – ikke som obligatorisk egen snarveifane.
- La brukeren knytte en slik anbefaling til ett eller to eksisterende signaler: Begynn med ett eller to eksisterende signaler: etter kaffe, etter tannpuss, når man reiser seg fra sofaen, når man passerer stua, etter lunsj, etter dusj **på tørt sted**. Egne ankre kan defineres og endres. Ingen sensorer, ingen påstått automatisk deteksjon.
- Foreslå maksimalt ett relevant og faglig gjennomgått kort per anker, med tydelig instruks, enklere alternativ, stoppsignaler og fri avvisning. Ta hensyn til ønsket trygghet og funksjon, ikke automatisk dose etter alder/kjønn.
- Pilotkatalog med få korte generelle alternativer etter **faglig godkjenning**: stol-til-stå med stabil stol, veggarmheving, tåhev med fast støtte og en liten trygg gå-runde. Ekstra trekk-/ryggøvelse bare med faglig gjennomgang og egnet utstyr. Hvis faglig revisjon ikke er dokumentert: skjul instruerende kort for ordinære brukere, men behold funksjonell admin-/testflyt.
- Ankerstatus og egenrapporterte handlinger er adskilt: å velge/endre/rulle tilbake et anker gir ingen aktivitetsminutter eller kapittelopplåsing. **Repetisjoner omregnes aldri automatisk til minutter, kondisjon eller dokumentert styrkeeffekt.** Ved fullført mikroaktivitet logges kilde og type særskilt. Spillbelønning er dagsbegrenset på tvers av alle aktivitetskategorier.
- «Min vei» skiller korte ankerhendelser fra kondisjons-/styrkeaktivitet. Ikke likestill noen få lette repetisjoner med tilstrekkelig styrke eller hjertehelse. Ingen automatisk belastningsprogresjon ved rygg-/balanse-/smerteproblemer.
- Brukervalg for å pause, slette eller skifte anker og starte igjen uten tapsrekke. Mikrohandlinger virker fullt uten maskot, venner, varsler eller tredjepartsapp.

## 3. Admin-funksjoner
- Eget toppmenypunkt «IKKE TRENING» i wp-admin, med oppsettveiviser, status, prøvevisning, appsidevalg, designinnstillinger, innholdsredigering, funksjonsflagg og kort systemhelse.
- Installerbar plugin oppretter **ikke automatisk en offentlig side**. Ved administratorklikk kan en valgt side opprettes og publiseres/forhåndsvises.
- Opprett og rediger historier/kapitler **og et begrenset utvalg mikroøvelseskort** via egendefinerte innholdstyper, rekkefølge og forhåndsvisning. Øvelseskort krever felter for fagrevisor, dato, sikkerhetsinformasjon og publiseringsstatus. Vis redaksjonelt varselskilt for manglende innhold.
- Styr registrerings- og sosialmodus eksplisitt. Admin kan slå av sosiale funksjoner uten å ødelegge personlige aktiviteter. Demo på eget lukket nettsted kan bruker administratortilgangen, men ekte data skal aldri vises i adminstatistikk uten behov.
- Adminoversikt viser kun aggregert, personverntilpasset teststatistikk som standard; ingen helseprofiler for administrator uten eksplisitt tilleggsbehov.
- Avinstalleringsvalg: data beholdes som standard ved deaktivering; ved reell avinstallering kan administrator uttrykkelig velge full datasletting.

## 4. Designspråk, UI og innhold
- Uttrykk: **moderne, voksent og lekent uten å bli barnslig**. Behold dyp skoggrønn/krem/honning som startpalett, tydelige typografiske nivåer, gode kontraster og konsekvent innkapslede komponenter. Maskot som gjenkjennelig merke, men ikke et helskjerms hinder for hovedhandlingen.
- Landingssiden kan ha visuell hero og fortelling. **Innlogget «I dag» skal vise relevant handling innen første 390×844 px mobilskjerm** uten at brukeren må bla forbi stor reklamehero.
- Nav i app: «I dag», «Min reise», «Sammen», «Min vei», «Mine valg» – juster slik at mobil har maks 4 faste bunnfaner og øvrige sekundærvalg uten horisontal scrolling. Ingen overveldende dashboard.
- Balanser moderne spillstil med seriøsitet. Ikke kopier Duolingo, Finch eller Pokémon GO grafisk.
- Test 320, 360, 390, 768, 1024, 1440 px, tastatur, fokusrekkefølge, høy tekstforstørrelse, kontrast, skjermleser-spotcheck og redusert bevegelse. WCAG 2.2 AA er **akseptansemål**, ikke et resultat som skal påstås uten gjennomgang.
- Alle kritiske tekster på naturlig norsk. Struktur tilrettelegges for oversettelse (`__()`, språkfiler på PHP-siden og lokaliserte JS-tekster).

## 5. Ting som uttrykkelig **ikke** skal bli med i denne betaversjonen

Ingen obligatorisk tema-ZIP, eksternt AI-abonnement, AI-genererte helseråd, helseskår/diagnoser, datadrevet medisinsk råd, betalte belønningsbokser, offentlig leaderboard, lokasjonskart, fri chat mellom fremmede, lydfiler med lisens, ekte SMS/push uten egen avtale, automatisk integrasjon med aktivitetsmåler eller betalingsløsning. Ikke bruk gamification på bekostning av hvile eller selvbestemmelse.
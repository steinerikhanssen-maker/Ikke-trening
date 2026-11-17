# Langtidsdrift og eierskifte

## Hva «driftssikker i mange år» betyr

Systemet skal være autonomt og kunne håndtere vanlige strøm-/nettverksbrudd uten eierens inngripen. Det betyr **ikke** at internett-tilkoblet Home Assistant, Supervisor, Linux, Zigbee og Nabu Casa kan fryses på én versjon i mange år. Sikkerhetsoppdateringer og nye signerte Cube-OS-releaser må inngå i en definert vedlikeholdsplan.

## Vedlikeholdsregime

- **Lokal drift:** lokal temperaturkontroll, Zigbee og Broadlink, ingen avhengighet til eksterne API-er for normal oppvarming.
- **Daglig automatikk:** sjekk at data lagres, at backup fungerer og at det ikke er kritiske disk-, minne-, eMMC-, Zigbee- eller temperaturavvik. Varsler skal være stille når systemet er friskt.
- **Månedlig eller ved kritisk sikkerhetsoppdatering:** kvalifisert administrator gjennomgår Core/app/OS-oppdateringer i testmiljø før produksjon, særlig fordi OS-porten ikke er offisielt støttet.
- **Kvartalsvis:** test restore fra ekstern kryptert backup og dokumenter at private nøkler og tilgang er oppbevart forsvarlig.
- **Årlig:** revider kritiske komponenters kompatibilitet, forsyning, varme og faktisk gjenoppretting. Dersom egen vedlikeholder ikke finnes, bør offisielt støttet hardware vurderes før husets salg.

## Varig minne, historikk og lagring

- Behold kun nødvendige temperatur-/effektmålinger i Recorder. Den nye lette Husvarme-regulatoren skal ikke kopiere dagens utviklings- og læringshistorikk.
- Sett databasens retensjon og ekskludering av støyende sensorer basert på reell 30-dagers vekstmåling, ikke bare et tall fra skrivebordet.
- Bruk eMMC, ikke en USB-minnepinne, til rot- og systempartisjon. Dersom datalagring blir for knapp, planlegg en godkjent SSD med eget fysisk feste, uavhengig strøm og dokumentert backupprosess.
- Ha alltid minst én kryptert sikkerhetskopi på en annen fysisk enhet. Verifiser at nødvendig dekrypteringsnøkkel finnes.

## Elektrisk og termisk drift

- Stabil 5V strømforsyning dimensionert for Cuben (original 5V/2,6A er spesifisert). Kvalitetskabel, ingen usikre grenuttak eller press på USB-kontakt.
- Kjør langtidstest i lukket originalt kabinett. Fjern ikke dekselet permanent uten å vurdere berøringssikkerhet, antenneforhold og støv.
- Bruk den batteristøttede PCF85063-klokken. Ved manglende NTP etter strømbrudd må systemet fortsatt starte, men logger skal merkes med korrekt tid når nettverk er tilbake.

## Gjenoppretting ved strømbrudd

1. Cuben forsøker vanlig oppstart via eMMC.
2. Dersom en ny A/B-slot ikke starter, skal bootloader forsøke den tidligere fungerende sloten; dette skal være fysisk testet.
3. Dersom delt bootpartisjon eller U-Boot skades, brukes ekstern PC med Rockchip Maskrom/UMS og en kjent god image. Prosedyren skal kunne gjennomføres med åpne komponenter og lokal dokumentasjon, uten gamle Futurehome-kontoer.
4. Etter gjenoppretting skal man kontrollere både Home Assistant, MQTT/Zigbee og faktisk lokal oppvarming.

## Eierskifte

- Opprett ny installasjon og ny eierkonto, ikke en kopi av den tidligere eierens tilgang, tokens og historikk.
- Ikke legg private RAUC-signeringsnøkler, personlige Nabu Casa- eller andre kontopassord på boksen.
- Lever QR-kode eller kort instruksjon med lokal URL, plassering av Cube/Broadlink, hva varmeknappene betyr, hvordan man gjenstarter og hvordan man får nytt nettverk.
- Etter innflytting skal gulvtermostater ha fungerende lokal regulering med dokumenterte gulvtemperaturgrenser også om Cube er frakoblet.
- Vedlikeholdsansvar og tilgang til signerte Cube-OS-oppdateringer skal være avklart. Dette er særlig viktig fordi installasjonen er uoffisiell.

## Hva som forblir separate enheter

«Én sentral boks» betyr én styringsdatamaskin, ikke at ekstern Broadlink, Meaco, Toshiba, termostater eller strømforsyninger forsvinner. Nye eiere får full HAOS, med vanlig mobilapp og Nabu Casa *hvis de velger å opprette et eget abonnement*.

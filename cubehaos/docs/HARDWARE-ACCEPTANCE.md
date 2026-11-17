# Maskinvare- og driftsakseptanse – må være bestått før eierskifte

**Testobjekt:** Futurehome CUBE-2V0-EU, en enkelt fysisk enhet. **Sikker oppsett:** alle prøver skjer isolert fra aktiv Zigbee-varmestyring, med USB-strømforsyning som tåler oppgitt 5 V / 2,6 A. Koble ikke prøveinstallasjonen til eksisterende termostater før produksjonssystemet er klarert for migrering.

## Fase A – maskinvare og oppstart

| ID | Test | Bestått når |
|---|---|---|
| A01 | Rockchip identifikasjon over USB-C | Nøyaktig én riktig Loader/Maskrom-enhet på PC, uten tvetydighet |
| A02 | RAM-baserte UMS og eMMC | EMMC gjenkjennes med riktig kapasitet som USB-blokk, uten feil i dmesg |
| A03 | Pinned U-Boot og ARM Trusted Firmware | Kompilerer uten Kconfig-/lenkefeil; konsoll har stabile 1,5 Mbaud |
| A04 | Linux-kjerne / Device Tree | Cube-kompatibel DTS og riktig DTB i image; ingen feilende regulatorreferanser |
| A05 | Første eMMC-oppstart | Kald start til systemd, Docker og Supervisor uten manuelle reparasjoner |
| A06 | Ethernet og DNS | DHCP, stabil lokale adresser, riktige MAC, IPv4/IPv6 etter relevans |
| A07 | USB-A, USB-C, I²C, RTC | Grensesnitt synlig; NXP-PCF85063 RTC holder tiden etter strømbrudd |
| A08 | Temperatur og throttling | Langvarig drift uten temperatur-/strømproblemer i lukket kabinett |
| A09 | Knappe-/LED-funksjon | Ikke introdusere ny reset-logikk før kontrollert og dokumentert |

## Fase B – ekte Home Assistant OS

| ID | Test | Bestått når |
|---|---|---|
| B01 | `ha info`, Supervisor og OS Agent | Tjenestene kjører og rapporterer forventet ARM64 og OS-varianter |
| B02 | Docker og Home Assistant Core | Ny bruker kan opprette eierkonto i UI, nå via LAN |
| B03 | Apps | Mosquitto + Zigbee2MQTT kan installeres, oppdateres og startes |
| B04 | Backup og restore | Lokal full backup kan eksporteres til annen fysisk lagring og gjenopprettes på testinstans |
| B05 | Nabu Casa | Kan frivillig kobles til med ny eiers konto uten å påvirke lokal drift |
| B06 | RAM og swap | Mål normal og toppbelastning; ingen jevn swapping under normal varmestyring |
| B07 | Disk | Ledig plass til to systemversjoner, logging, appoppdateringer og gjenoppretting, med varsel før full disk |
| B08 | Database | Normal temperatur-/effekthistorikk lagres med kontrollert dataretensjon; mål vekst over 30 dager |

## Fase C – oppdatering og gjenoppretting

| ID | Test | Bestått når |
|---|---|---|
| C01 | RAUC-kompatibilitet | Kun verifisert `haos-cube2v0eu` med riktig signatur aksepteres |
| C02 | A → B og B → A | Minst én oppdatering og én tilbaketrekking med korrekt aktiv slot |
| C03 | Ikke flashe SPL ved OS-OTA | Før-/etter-hash på bootloaderområdet er identisk |
| C04 | Mislykket kjerneoppstart | Bootloader går tilbake til fungerende slot etter definerte forsøk |
| C05 | Strømbrudd under oppdatering | Oppstart eller dokumentert Maskrom-recovery uten tap av datapartisjon |
| C06 | Korrupt boot.vfat | Test sikker gjenoppretting via RAM-UMS. Merk at vanlig A/B alene ikke beskytter boot.vfat. |
| C07 | Mislykket nettverksoppdatering | Ingen endringer på fungerende kjørende system før RAUC har verifisert bundle |
| C08 | Tapte SSH-nøkler / endret nett | Lokal fysisk recovery med dokumentert CONFIG-prosedyre |

## Fase D – langtids- og feiltoleransetest

| ID | Test | Bestått når |
|---|---|---|
| D01 | 20 kontrollerte kalde oppstarter | Home Assistant / MQTT / automasjoner kjører hver gang |
| D02 | 20 kontrollerte omstarter | Ingen heng, manglende tjenester eller datatap |
| D03 | 72 timer belastningsprøve | Ingen temperatur-, RAM-, disk-, fildeskriptor- eller I/O-feil |
| D04 | Minst 30 døgn typisk drift | Stabil temperatur, ingen hyppige restart-/Zigbee-repareringsbehov |
| D05 | Tre internettbrudd | Lokal varmeregulering fortsetter uten Nabu Casa eller ekstern tjeneste |
| D06 | Tre LAN-brudd | Klare fallback-tilstander i gulvtermostater; ingen ubekreftede IR-gjentakelser |
| D07 | Sensor `unavailable`/foreldet | Ingen blind oppregulering; tydelig feilsignal og definert lokal grunnregulering |
| D08 | Strømtap til varmepumpe/IR/Shelly | Tidsavgrensede, sikre kommandoer; lokal termostat beholder gulvvern |
| D09 | Raspberry Pi fysisk frakoblet | Hele husets ønskede funksjonsomfang virker fortsatt fra Cube |
| D10 | Ny ruter / nytt nettverk | Ny huseier får tilkobling uten gammel konto, hardkodet IP eller gammel telefon |
| D11 | Uavhengig gjenoppretting | En teknisk kompetent ny administrator kan gjenopprette uten tilgang til utviklerens PC eller private konto |

## Første gyldige release

Ingen `v1.0` eller «klar for ny eier» før A01–D11 er dokumentert bestått (eller eksplisitt nedprioritert med begrunnelse og konsekvens), og maskinvaren har en reproduserbar byggeseddel. Ferdig kompilering ≠ bootbar maskin ≠ vedlikeholdbar varmestyring.

## Serviceavhengigheter

- Zigbee MG12 på CP2102N: krever korrekt strømstyring, firmware og driver. USB/UART-opptak og testnettet skal bekrefte det.
- Zigbee termostater: skal kunne regulere lokalt og beskytte gulvet uten sentralen.
- Broadlink RM4 Pro: er en periferiboks på Wi-Fi som må få strøm og være på nytt nettverk etter eierskifte.
- Meaco: IR-hastighetskommandoer må ha tilstandshåndtering og watt-tilbakemelding.
- Toshiba varmepumpe: unngå kontinuerlige temperaturtrinn; bruk minstetid mellom IR-kommandoer og manuell fallback.

## Ved feilet test

Stopp release. Behold gjeldende fungerende Raspberry Pi-system isolert. Hent UART-logg, dmesg, bootstate, RAUC-status og ressursmåling. Rett kildekode, bygg ny versjon med låste kilder og gjenta testen; ikke send ikke-verifisert image til en ny huseier.

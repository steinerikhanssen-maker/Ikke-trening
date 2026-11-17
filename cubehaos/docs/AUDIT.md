# Teknisk revisjon – CubeHAOS v0.1 → v0.2

Dato: 17. november 2026. Omfang: faktisk kildepakke `CubeHAOS-port-v0.1.zip`, ikke en ferdig firmware. Kildene fra Home Assistant OS og Futurehome Cube board support ble sammenholdt med lokal kode. Risiko betyr mulig konsekvens, ikke at feilen er fysisk påvist.

## Beslutning

**v0.1: ikke installér. v0.2: forbedret kildeprosjekt, fortsatt ikke utgivelsesgodkjent.** Ingen faktisk HAOS-build, firmwarestart eller radiotest er utført i denne gjennomgangen.

## P0 – må rettes/verifiseres før en fysisk flash

| Funn | Underlag | Tiltak v0.2 | Status |
|---|---|---|---|
| Kontroll av bygging feilet åpen | `scripts/build.sh` brukte `inspect_image.py ... || true` | Inspeksjonsfeil stopper bygg; gammel output avvises | **Kodet og testet** |
| Image-inspeksjon verifiserte bare 2048 første bytes | Gammel `inspect_image.py` | Leser hele XZ, validerer GPT-header og CRC for primær/backup-tabeller, A/B og størrelse | **Kodet og testet med syntetiske image** |
| U-Boot/DTB kunne mangle uten at utskiftingsimaget ble stoppet av hook | Gammel `haos-hook.sh` kopierte `*.dtb` ukritisk | Krever nøyaktig Cube-DTB og `boot.scr` | **Kodet og testet statisk** |
| OS-oppdatering kunne skrive SPL/U-Boot direkte på én fysisk lokasjon | HAOS `rauc-hook`, funksjonen `install_spl` | Cube-spesifikk betingelse for å beholde bootloader **og delt FAT-bootpartisjon** under ordinær RAUC | **Kodet; OTA ikke fysisk testet** |
| Mulig overskriving av feil disk ved manuell `flash.sh` | Gammel script sjekket ikke USB-transport eller enhetsstørrelse | Hele disk, USB-transport, 7–9 GB, ingen mounts, fysisk bekreftelse, full read-back | **Kodet; fysisk UMS-identifikasjon ikke testet** |
| Ingen test på konkret RK3328-kort | Original pakken manglet binært image | Fysisk akseptanseplan med tydelige porter | **Åpent: avgjørende** |
| U-Boot-funksjoner og bootflow med denne eksakte kombinasjonen | RK3328 U-Boot 2026.01 og HAOS-baserte oppstartsskript | Beholdt HAOS bootflow, verifisering av kommandoer/partisjon/returflyt spesifisert | **Åpent: build + UART** |
| Full HAOS/Supervisor+Core-installasjon på 2GB og 8GB | Plattformens fysiske ressurser | Resource- og diskbudsjett må måles; ikke lovet ubegrenset datalagring | **Åpent: kapasitetsmåling** |

## P1 – krever løsning før stabil overlevering til nye eiere

| Funn | Tiltak og forventet bevis |
|---|---|
| `qemuarm-64` er kompatibilitetsalias, ikke offentlig Cube-støtte | Verifiser Supervisor og Core-arkitektur, app-oppsett, OS-versjonsstatus og at OTA-bunter fra andre kort avvises. Ingen offisiell OS autooppdatering før egen feed er prøvd. |
| Delt FAT-bootpartisjon uten A/B | **V0.2 fryser FAT-bootdelen under OTA**, mens kernel/rootfs oppdateres A/B. Test at nye kjerner fortsatt fungerer med uendret DTB, og at den frosne bootkjeden kan gjenopprettes fysisk. |
| Driftskritisk kjøling/oppvarming må fortsatt virke ved CPU/restart/nettbrudd | Bygg lokal termostatstyring med gulvvern og normal-settpunkter før full Zigbee-migrering. Test stale sensor, IR-sender og varmebehov. |
| Intern Zigbee-radio er som standard ikke automatisk strøm- og firmwareaktivert | Test GPIO-strøm, CP2102N USB, UART-port og koordinator-firmware på testnett; ikke endre husets Zigbee-nett før bestanden er bekreftet. |
| Broadlink og Meaco er separate nettverks-/IR-periferienheter | Test med kjøpers nettverk, faste enhets-ID-er, IR-intervall og tilbakemelding. Broadlink følger fysisk med huset dersom styringen forutsetter den. |
| eMMC-slitasje over tid og knapp lagringsplass | Behold bare nødvendige Home Assistant-integrasjoner; begrens Recorder-historikk; minimum fri disk må måles. Oppbevar backup på en annen fysisk enhet. |
| Uoffisiell OS-port krever egen vedlikeholder | Dokumenter SHA, signeringsnøkkel, build-oppskrift, kildearkiv og hvem som kan signere ny OTA. Test tilbakeføring fra tidligere versjon. |

## P2 – kvalitetsforbedringer

- Tilpass case-LED og funksjonsknapp til brukerlig status/trygg reset **etter** at normal boot er bevist; board support sin knappesekvens lagres som `bootmode-OPTIONAL-UNTESTED.ush`, men aktiveres ikke automatisk.
- Telemetri: separate grenser for CPU, RAM, swap, eMMC-fri plass, temperatur, Zigbee-drift, oppdateringsstatus og siste vellykkede backup.
- Legg til et enkelt startdashbord, fysisk termostatforrang, Stille/Borte/Normal og tydelig eierreset etter at HAOS er godkjent.

## Bekreftet fra kildekode

- Home Assistant OS bruker Buildroot, Docker, Supervisor og RAUC.
- Cube 2 har Rockchip RK3328, 2GB RAM, 8GB eMMC, intern EFR32MG12 og USB-C Loader/Maskrom.
- Board support leverer Cube-DTS, U-Boot-defconfig og et RAM-basert UMS-bootloader-byggetarget.
- HAOS `green` er en kilde til oppstarts-/partisjonsstruktur, men ikke en kompatibel firmware.
- Eksisterende Cube-DTS har aktiv-lav initsikkerhetslogikk som kan la radioer være avslått til eksplisitt aktivering.

## Det vi ikke kan konkludere med fra kildekoden

- At U-Boot klarer bootflow fra eMMC etter flash.
- At data- og backup-GPT faktisk passer eMMC-modulen uten å kollidere med Rockchip bootstrap.
- At RAUC tilbakefører systemet ved bortfall av nettverk/Supervisor – ikke bare når Linux mangler oppstart.
- At nytt HAOS vil kunne bruke intern Zigbee/Z-Wave-radio uten separat firmwaretilpasning.
- At den fremtidige OS-porten vil motta eller tåle officielle HAOS-oppdateringer automatisk.

## Dokumentasjon

- https://github.com/RockPaperPencil/futurehome-cube2v0eu-boardsupport
- https://github.com/home-assistant/operating-system
- https://contributors.home-assistant.io/os/operating-system/boards/
- https://contributors.home-assistant.io/os/operating-system/update-system/
- https://contributors.home-assistant.io/os/operating-system/configuration/
- https://www.home-assistant.io/more-info/unsupported/os_version/

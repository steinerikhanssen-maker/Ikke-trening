# CubeHAOS: Installasjon og mobil – foreløpig guide

**17. november 2026 – kildekodepakke v0.3. Dette er IKKE et `.img.xz`-image. Ikke flash v0.1/v0.2/v0.3-kildekoden direkte.**

## Hva kan gjøres med mobilen?

- Førstegangsflashing: **Nei, ikke med vanlig Home Assistant-app eller en ordinær Android-mobil.** Stock Cube går i Rockchip Loader/Maskrom, og krever en USB-host med Rockchip-verktøy og kontrollert strømtilførsel.
- Når Cube HAOS er installert og faktisk kjører: Home Assistant Core, apper og Dashboard kan normalt administreres fra Home Assistant-appen på Android/iOS.
- Den uoffisielle Cube-spesifikke HAOS-oppdateringen er **ikke** en offisiell OTA-utgivelse. Mobiloppdatering gjennom HA UI må utvikles og testes særskilt. Midlertidig oppdateringsvei er en **signert RAUC .raucb** på CONFIG-USB etter 5 minutter oppetid; `ha os import` i CLI eller den lokale administrasjonsruten. Ikke lov at nye eiere får automatiske HAOS-oppdateringer før vi har en vedlikeholdt distribusjon.
- Ved feilstart: Linux-PC + USB-C og Maskrom recovery.

## Første fysiske test (uten å slette noe)

1. Cuben frakobles hjemmenettverket. Bruk en **Linux-PC** med korrekt USB-C-datakabel og tilstrekkelig strøm til Cuben. Ikke koble den operative Home Assistant-serveren til dette forsøket.
2. Installer `rkdeveloptool` på PC-en. Bruk **kun** `./scripts/probe_cube.sh` for deteksjon. Følg utviklerens dokumenterte Loader-sekvens med funksjonsknapp.
3. Test en RAM-basert U-Boot loader hvis den er bygget: `./scripts/build_ram_loader.sh` og senere `./scripts/ram_ums.sh`. Dette eksponerer eMMC som en USB-disk. Verifiser nøye enhetsidentiteten.
4. Først når et ekte CubeHAOS-image **er kompilert**, partisjonskontrollert og release-/maskinvaretester er dokumentert, kan installasjon via `flash.sh` vurderes. Det sletter Futurehome-programvaren. **Ingen av de stegene er utført i denne pakken.**

## Bygge et ekte image på Linux-PC (ikke på Raspberry Pi som styrer huset)

Krever Docker, Git, Python 3, stor diskplass og Internett for mange kildepakker. Ingen byggeressurs var tilgjengelig i vår kjøringsøkt. Fra prosjektroten:

```bash
./scripts/verify_source.py
./scripts/verify_build_env.py
./scripts/bootstrap.sh
./scripts/build.sh
```

Byggeskriptet sikter på `haos_cube2v0eu-*.img.xz` og `.raucb`. Et vellykket bygg er **kun en bygge- og strukturell verifikasjon**; oppstart, USB-radio, eMMC, termikk og failover må fortsatt fysisk testes på Cuben før varme styring overtas.

## Etter at systemet starter

- Bruk **Ethernet** til ruteren i huset. Fra mobil på samme lokalnett: åpne `http://homeassistant.local:8123` eller Cube-IP-adressen i Home Assistant-appen.
- Opprett **ny, egen Home Assistant-bruker**. Ikke gjenbruk Futurehome-konto eller personlige brukerdata fra Raspberry Pi.
- Verifiser Supervisor, Core, network, Boot A/B, USB Zigbee-radio og oppdateringssignatur før enheten får ansvar for termostatene.
- Ikke overfør dagens Zigbee-nett før den **innebygde EFR32MG12-radioen** er demonstrert som kompatibel Zigbee-koordinator.

## Kilder

- https://github.com/RockPaperPencil/futurehome-cube2v0eu-boardsupport
- https://contributors.home-assistant.io/os/operating-system/build/
- https://contributors.home-assistant.io/os/operating-system/update-system/
- https://contributors.home-assistant.io/os/operating-system/configuration/
- https://www.zigbee2mqtt.io/guide/adapters/emberznet.html

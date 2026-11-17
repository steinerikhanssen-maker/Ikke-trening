# CubeHAOS v0.4 — Cube 2 board port with hosted build CI

**Never install this source archive as firmware.** This release sets up GitHub Actions
for real Buildroot cross-compilation and artifact validation. Firmware must also be
boot-tested on the physical Cube before it is qualified for installation. See
`docs/BUILD-STATUS.md`, `docs/WINDOWS-INSTALL.md`.

**New in v0.4:** includes the built-in EFR32MG12 Zigbee power-on Device Tree overlay;
adds a dedicated GitHub Actions build workflow and Windows checksum utility.
No Sonoff dongle is part of the target design.

# CubeHAOS v0.4 — kildekodeprosjekt, ennå ikke bootbart image av Home Assistant OS til Futurehome Cube 2

**Mål:** En fremtidig, selvstendig varmestyringssentral som kan overtas av nye huseiere, med full Home Assistant Core/Supervisor/apps og valgfri Nabu Casa, på **Futurehome CUBE-2V0-EU / RK3328 / 2 GB RAM / 8 GB eMMC**. Den opprinnelige Futurehome-programvaren skal erstattes, ikke bevares. Ingen skript kopierer Futurehome-firmware.

**VIKTIG: KILDEKODE, IKKE INSTALLASJONSIMAGE.**

**Viktig status:** Dette er et **utviklingsgrunnlag med forbedrede kontroller**, IKKE et kompilert, bootet eller hardware-testet HAOS-image. `v0.4` er ikke godkjent for drift eller eierskifte. Både maskinvareoppstart og HAOS/Supervisor/nettverk/radio-/recovery-tester må gjennomføres før første produksjonsflash. Det eksisterende Home Assistant-systemet på Raspberry Pi er ikke endret.

## Hva er forbedret etter v0.1?

- Feilsikker bygging: `build.sh` stopper ved manglende/korrupt artefakt (tidligere ble kontrollfeil ignorert med `|| true`).
- Kontroller av hele XZ-strømmen, primær og sekundær GPT med CRC, A/B-systempartisjoner og riktig kortidentitet.
- `haos-hook.sh` stopper bygging hvis Cubens Device Tree eller `boot.scr` mangler.
- Cube-spesifikk RAUC-kontroll bevarer både SPL/U-Boot **og den delte FAT-bootpartisjonen** ved ordinære OS-oppdateringer. En eventuell oppdatering av bootloader gjøres som en separat fysisk prosedyre.
- `flash.sh` godtar kun bekreftet USB-tilkoblet disk i 8-GB-klassen, kontrollerer image og leser tilbake hele det skrevne området for SHA256-sammenligning. Krever eksplisitt bekreftelse.
- `verify_update.sh` krever RAUC-signaturverifisering mot en valgt nøkkelring og eksakt `haos-cube2v0eu`-kompatibilitet.
- CONFIG-USB må være et faktisk montert filsystem med riktig etikett, og kopieringen verifiseres.
- Bootstrapping bruker låste kilde-revisjoner og nekter å tilbakestille en endret sjekk-ut.
- Utvidet testpakke og dokumentasjon for elektrisk, termisk, minne-, lagrings-, nettverks-, oppstarts- og gjenopprettingstest.

## Bygge på en Linux-PC

Krever **Git, Python 3, Docker, internett, ledig diskplass og en ARM64-krysskompilator** for den separate RAM-programmeringslasteren. Bygge-PC-en kjører Home Assistant OS sin Docker-basert byggeprosess. Ikke bygg på Raspberry Pi-en som styrer huset.

```bash
./scripts/bootstrap.sh
./scripts/static_preflight.py work/operating-system
./scripts/build.sh
```

Dette oppretter et låst HAOS-kildeuttrekk i `work/operating-system` og `work/board-support`, og legger inn nytt Buildroot-mål `cube2v0eu`. Siden v0.4 ikke er kompilert på reell Linux-builder, må disse stegene kjøres og eventuelle kompileringsfeil rettes før et `.img.xz` finnes.

### Kontroller kildekoden lokalt

```bash
python3 -m unittest discover -s tests -v
for f in scripts/*.sh; do bash -n "$f"; done
```

Testene verifiserer **kodegenerator og kontroller**, ikke Linux-kompilering. `static_preflight.py` kan kjøres mot et generert kildeuttrekk.

## Grunnleggende implementasjon

- **Boot:** Rockchip ROM → initial SPL/U-Boot fra eMMC → HAOS `boot.scr` → A/B Linux-kjerne → HAOS system.
- **OS:** Buildroot, EROFS, systemd, Docker, Home Assistant Supervisor og Core. **Ikke** en Docker-container på generisk Armbian.
- **Maskinvare:** Cubens board-DTS kopieres fra låst [board-support](https://github.com/RockPaperPencil/futurehome-cube2v0eu-boardsupport) og brukes i Linux og U-Boot; ekstra radio-firmware er en egen leveranse.
- **HA:** Offisielle ARM64-containere via Supervisor med `qemuarm-64` som *midlertidig kompatibilitetsalias*. Dette er ikke et offisielt Cube-maskinnavn og skal testes særskilt.
- **Oppdatering:** Signert RAUC `.raucb` med korrekt `haos-cube2v0eu`, A/B system/rootfs. Oppstartslaster og delt FAT-bootpartisjon bevares ved vanlig OTA. Bare A/B-kjerne og A/B-rootfs oppdateres; dette krever at nye kjerner er kompatible med eksisterende Device Tree. Reell oppdaterings-/strømbruddstest er obligatorisk.
- **Gjenoppretting:** Rockchip Loader/Maskrom og RAM-U-Boot UMS via USB-C. Den opprinnelige Futurehome-programvaren blir ikke sikkerhetskopiert.

## Bygg- og utslippskontroll

Et vellykket bygg skal gi nøyaktig **ett** image `haos_cube2v0eu-*.img.xz` og en tilsvarende `.raucb` i output/images. Verifikasjonen gjennomføres automatisk etter bygging. De neste kravene kommer i tillegg:

1. RAUC-bunten skal kontrolleres med **vår** offentlige nøkkelring (private signeringsnøkler må oppbevares adskilt), f.eks. `scripts/verify_update.sh BUNDLE.raucb TRUSTED-KEYRING.pem`.
2. Image må starte fra eMMC på faktisk Cube, ikke bare bli godkjent av partisjonskontrollen.
3. Normal oppstart, kald oppstart, nettverksbrudd og A/B-oppdatering skal bestå testmatrisen i `docs/HARDWARE-ACCEPTANCE.md`.
4. HA Core, Supervisor, sikkerhetskopiering og maskinvare-ID skal fungere gjennom vanlig lokal UI.
5. Enhver oppdatering må ha en *ekstern*, funksjonell gjenopprettingsmulighet. Test ikke destruktivt på systemet som styrer huset.

## USB-programmering (senere fysisk test)

```bash
./scripts/probe_cube.sh         # bare deteksjon
./scripts/build_ram_loader.sh  # bygger midlertidig RAM U-Boot, ingen skriving
./scripts/ram_ums.sh           # presenterer eMMC som USB-disk på PC
```

Etter første fullstendig vellykkede OS-bygg, release-verifisering og fysisk identifikasjon av Cube-eMMC kan `scripts/flash.sh IMAGE.img.xz /dev/sdX` brukes. Dette **sletter alt** på den valgte blokkenheten, og er derfor ikke en rutine som skal kjøres automatisk eller før identitet er kontrollert. Skriptet tar ingen Futurehome-backup. En feil ved strøm eller eMMC kan gjøre enheten ubrukelig til Maskrom-gjenoppretting er gjennomført.

## Senere RAUC-oppdatering via USB

```bash
./scripts/verify_update.sh haos_cube2v0eu-VERSJON.raucb TRUSTED-KEYRING.pem
sudo ./scripts/make_update_usb.sh haos_cube2v0eu-VERSJON.raucb /media/CONFIG TRUSTED-KEYRING.pem
```

USB-lagringen må ha filsystemetikett **CONFIG**, FAT eller ext4, og må være montert på den oppgitte mappen. Når Cuben har vært oppe i minst fem minutter: `ha os import`. **CONFIG-importen kan erstatte SSH-nøkler og nettverkskonfigurasjon** dersom de ikke finnes på USB-mediet; se [Home Assistant CONFIG-dokumentasjon](https://contributors.home-assistant.io/os/operating-system/configuration/). Brukes først etter signatur- og hardware-test.

## Dokumentasjon

- [AUDIT.md](docs/AUDIT.md) – gjennomgangen av v0.1, alvorlighetsgrader, endringer i v0.2 og åpne tekniske spørsmål.
- [HARDWARE-ACCEPTANCE.md](docs/HARDWARE-ACCEPTANCE.md) – krav og detaljert testløype før flash og overlevering.
- [OPERATIONS.md](docs/OPERATIONS.md) – sikkerhetskopiering, eierskifte, vedlikehold og levetidsstrategi.
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) – systemoppbygning og oppdateringsprinsipp.

**Ingen versjon kan sertifiseres for mange års drift bare gjennom kodeanalyse.** En permanent varmeinstallasjon må bestå fysisk testing og ha en avtalt vedlikeholdsløsning når HAOS, Supervisor eller integrasjoner får sikkerhetsrettelser.

## Revisjonsmerknad v0.4

- Nytt **`INSTALLASJON.md`** med tydelig forskjell mellom USB-initialisering og senere mobiladministrasjon.
- Boot-scriptet nekter å starte kernel med ukjent/minnetilfeldig Device Tree dersom riktig Cube-DTB mangler.
- `release_gate.py` skiller eksplisitt mellom filintegritet og fysisk verifisert oppstart. Ingen test i v0.4 kan alene godkjenne flash.
- `verify_source.py` er kildekode- og shell-syntakstest. `verify_build_env.py` beskriver verktøy som finnes på vertsmaskinen.
- **Ingen ferdig HAOS-image er levert**; kilden må kompileres, maskinvaretestes og signeres før installasjon.

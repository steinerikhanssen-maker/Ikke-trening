# CubeHAOS v0.2 – oppstart, system, oppdatering og enheter

```text
             Futurehome CUBE-2V0-EU (RK3328, 2GB RAM)
                      Rockchip ROM
                           │
             eMMC SPL + pinned U-Boot 2026.01
                           │
                       boot.scr / DTB
                           │
                    A/B bootstate (RAUC)
                     ┌─────┴─────┐
                 Kernel A     Kernel B
                 EROFS A      EROFS B
                     └─────┬─────┘
                           │
                   Home Assistant OS
              systemd · Docker · OS Agent
                           │
                      Supervisor
                     ┌─────┴──────┐
                 HA Core       Apps
                           │
                 House Heat (later phase)
                           │
      ┌────────────────────┼──────────────────┐
      │                    │                  │
  Onboard Zigbee      LAN Broadlink       Other LAN
  EFR32MG12           (Toshiba/Meaco)     devices
```

**Kjerneprinsipp:** Skrivebeskyttet system (EROFS) og separerte A/B-systemplasser, med varige data på egen partisjon. Normal Cube OS-oppdatering skal **ikke** overskrive verken oppstartslaster eller FAT-bootpartisjon; Cube-spesifikke RAUC-hooks avstår fra oppdatering av begge. Nye oppdateringer skriver bare inaktiv A/B-kjerne og A/B-rootfs. Dette krever kompatibilitet med fast Device Tree/bootscript. Bootstate og RAUC-status kan fortsatt endres, og strømbruddtester er derfor obligatoriske.

**Kilder:** Home Assistant OS (Buildroot/RAUC) og RockPaperPencil Cube board support. Alle eksterne kilde-commits er låst i `bootstrap.sh` og `prepare_port.py`, men Docker/byggeavhengigheter må fortsatt verifiseres i faktisk byggemiljø.

**Viktig avgrensning:** `SUPERVISOR_MACHINE=qemuarm-64` er kun foreløpig bruk av tilgjengelig ARM64 image-katalog. Det er ikke bevis for full kompatibilitet eller en godkjent vedlikeholdskanal. Offisiell HAOS autooppdatering på dette maskinaliaset skal ikke brukes før korrekt boardkompatibilitet og maskinidentitet er fysisk kontrollert.

**Åpne portar:** U-Boot bootflow-konfigurasjon, riktig Linux-DTB, intern radio-firmware, OS-Agent-adferd, datadiskstørrelse og automatisk A/B-rollback ved OS-bootfeil eller kontrollert strømbrudd. Hver må dokumenteres med faktisk maskinvare- og oppstartslogg.

# Verifikasjon og release-status for CubeHAOS v0.3

Dato: 17. november 2026.

| Kriterium | Status |
|---|---|
| Riktig modell og kildehenvisninger | Kontrollert fra offentlig board-support-kilde |
| HAOS-byggeoppsett | Generert ved kode-/fixture-test, men ikke kompilert mot reelle kildearkiver |
| 11 automatiserte kildekodetester | BESTÅTT lokalt |
| Bash-syntaks for 8 skript | BESTÅTT lokalt |
| Manglende DTB: boot-stopp | Implementert og kontrollert i generatorens test |
| Fullt HAOS-image `.img.xz` | IKKE BYGGET |
| Signert RAUC-bunt for Cube | IKKE BYGGET |
| Maskinvareoppstart | IKKE TESTET |
| Supervisor, Nabu Casa og Zigbee på Cube | IKKE TESTET |
| Langtidsdrift, termisk test og A/B-failover | IKKE TESTET |
| Godkjent for installasjon i hus som varmes opp | NEI |

**Konklusjon:** V0.3 er verifisert som et statisk kildekodeprosjekt. Det er ikke en verifisert installasjonsfirmware.

Det er ikke mulig å produsere og verifisere ekte `.img.xz` fra det tilgjengelige kjøremiljøet: det mangler Docker og utgående tilgang til GitHub-kilder. En uavhengig byggemaskin må først kompilere hele Buildroot-målet. Deretter kreves fysisk oppstart og test på Cuben.

Ingen Futurehome-originalprogramvare er tatt vare på eller kopiert.

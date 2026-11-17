# CubeHAOS developer image – evidence boundary

v0.4 is a source-to-build project. A GitHub Actions workflow can compile a candidate
`.img.xz` and `.raucb` using a hosted Ubuntu build machine. Local source tests and
synthetic disk-image tests are not evidence that a real Cube boots. The workflow
upload name explicitly says NOT-HARDWARE-TESTED.

For a release to be marked **installation qualified**:

- GitHub build job successful on the exact final commit, with inspect_image.py passing.
- U-Boot/Rockchip ROM boot successfully to kernel on actual CUBE-2V0-EU; identify
  eMMC, USB, Ethernet and power conditions.
- Docker, Supervisor, Core and Apps validated; backup/restore and A/B update tested.
- Built-in EFR32MG12 power-on overlay and adapter serial connection verified.
- Zigbee coordinator firmware, operation with a test device, hard reset and recovery verified.
- Power loss, cold start, high-temperature, full-disk and 14-day soak tests pass.
- Signing key and update process held by owner with safe restoration path.

No GitHub Actions build alone can prove device operation. Do not flash while operating
production heating on any hardware used to host the currently running HA system.

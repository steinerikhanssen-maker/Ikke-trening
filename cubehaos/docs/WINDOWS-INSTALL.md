# Windows-first installation – Futurehome Cube 2v0 EU

The **initial installation cannot presently be done from the Home Assistant mobile app**.
There is not yet a physically boot-tested image; the steps below are reserved for when
one exists and has been validated on a spare, equivalent Cube.

1. A Windows 10/11 PC and a genuine USB-C *data* cable are sufficient as the ordinary user side.
2. A separately tested Rockchip USB/RAM-loader procedure must present the Cube eMMC
   as a USB storage device to Windows. The normal factory USB-C port is not automatically a disk.
3. Confirm physical device identity and size. An eMMC installation will erase the old
   Futurehome system. No Futurehome firmware backup is required by this project.
4. Compare the signed candidate image SHA256 to the published release manifest with
   `windows/VERIFY_IMAGE.ps1`. This does not replace a hardware boot test.
5. Only after a successful hardware qualification, write the `.img.xz` to the positively
   identified Cube USB disk using a trusted Windows disk imaging utility.
6. Remove USB, use the original 5V supply, connect Ethernet and boot normally. Check
   HA Core, Supervisor, the integrated radio and long-term reliability before migration.
7. Later HA Core/app updates can be operated from the Home Assistant UI. Custom Cube
   **OS** updates require separately qualified and signed RAUC bundles; do not install
   official images built for another board.

**No mobile-only first-flash path is validated or promised.** The Cuben does not need a
Linux PC for user operation; Linux build infrastructure is supplied by GitHub Actions.

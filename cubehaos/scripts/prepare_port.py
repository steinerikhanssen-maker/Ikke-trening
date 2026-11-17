#!/usr/bin/env python3
"""Install an experimental HAOS RK3328 board target into a *separate* HAOS checkout.

HARDENING: fail closed when upstream structure changes; disable automatic SPL writes
on Cube firmware upgrades; verify expected boot files before image packaging.

No writes to a physical Cube. Inputs are upstream source trees. For development only.
"""
from __future__ import annotations
import argparse
import difflib
import re
import shutil
from pathlib import Path

BOARD_ID = "cube2v0eu"
TARGET = "cube2v0eu"
DTBASE = "rk3328-futurehome-cube-2v0-eu"
HAOS_BOARD_REL = Path("buildroot-external/board/cube/cube2v0eu")
HAOS_DEF_REL = Path("buildroot-external/configs/cube2v0eu_defconfig")
ARMBIAN_RKBIN_SHA = "98f106532c684c1741c10d027566bfd3662a4698"


def require(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Mangler kildefil: {path}")
    return path


def add_patch(path: str, body: str) -> str:
    """Git-compatible patch adding a source file, applicable with 'patch -p1'."""
    if not body.endswith("\n"):
        body += "\n"
    lines = body.splitlines(keepends=True)
    chunks = list(difflib.unified_diff([], lines, fromfile="/dev/null", tofile=f"b/{path}", n=3))
    return (f"diff --git a/{path} b/{path}\n"
            f"new file mode 100644\n" + "".join(chunks))


def patch_one_line(original: str, updated: str, path: str) -> str:
    parts = list(difflib.unified_diff(original.splitlines(keepends=True),
                                     updated.splitlines(keepends=True),
                                     fromfile=f"a/{path}", tofile=f"b/{path}", n=3))
    if not parts:
        raise RuntimeError(f"Patch without changes: {path}")
    return f"diff --git a/{path} b/{path}\n" + "".join(parts)


def replace_unique(s: str, old: str, new: str) -> str:
    if old not in s:
        raise RuntimeError(f"Upstream format changed; expected fragment: {old!r}")
    return s.replace(old, new)


# HAOS pins a global fileenv command patch written for U-Boot 2026.04.
# Cube intentionally builds 2026.01: that version has no CMD_SM3SUM Makefile line.
# Only the Makefile hunk context changes; the Kconfig and C implementation do not.
HAOS_FILEENV_PATCH = Path("buildroot-external/patches/uboot/0001-CMD-read-string-from-fileinto-env.patch")
FILEENV_2026_04_HUNK = """@@ -176,6 +176,7 @@ obj-$(CONFIG_CMD_SHA1SUM) += sha1sum.o
 obj-$(CONFIG_CMD_SEAMA) += seama.o
 obj-$(CONFIG_CMD_SETEXPR) += setexpr.o
 obj-$(CONFIG_CMD_SETEXPR_FMT) += printf.o
+obj-$(CONFIG_CMD_FILEENV) += fileenv.o
 obj-$(CONFIG_CMD_SPI) += spi.o
 obj-$(CONFIG_CMD_STRINGS) += strings.o
 obj-$(CONFIG_CMD_SM3SUM) += sm3sum.o
"""
FILEENV_2026_01_HUNK = """@@ -175,5 +175,6 @@ obj-$(CONFIG_CMD_SHA1SUM) += sha1sum.o
 obj-$(CONFIG_CMD_SEAMA) += seama.o
 obj-$(CONFIG_CMD_SETEXPR) += setexpr.o
 obj-$(CONFIG_CMD_SETEXPR_FMT) += printf.o
+obj-$(CONFIG_CMD_FILEENV) += fileenv.o
 obj-$(CONFIG_CMD_SPI) += spi.o
 obj-$(CONFIG_CMD_STRINGS) += strings.o
"""


def adapt_fileenv_patch(haos: Path) -> tuple[Path, str]:
    """Return a pinned, minimal patch correction for the Cube's U-Boot 2026.01.

    Never change the upstream repository: bootstrap uses an isolated checkout.
    Reject unrecognized upstream patch content instead of applying a fuzzy fix.
    """
    path = require(haos / HAOS_FILEENV_PATCH)
    content = path.read_text()
    if content.count(FILEENV_2026_04_HUNK) != 1:
        raise RuntimeError("Pinned HAOS fileenv patch changed; refuse U-Boot 2026.01 build")
    return path, content.replace(FILEENV_2026_04_HUNK, FILEENV_2026_01_HUNK, 1)


def build_port(haos: Path, source: Path) -> dict:
    haos, source = haos.resolve(), source.resolve()
    external = require(haos / "buildroot-external")
    green = require(external / "board/nabucasa/green")
    bdir = external / "board/cube/cube2v0eu"
    if bdir.exists() or (haos / HAOS_DEF_REL).exists():
        raise RuntimeError("Mål finnes fra før. Bruk en REN HAOS-sjekk-ut, ikke overskriv eksisterende port.")
    dts = require(source / f"{DTBASE}.dts").read_text()
    dtsi = require(source / f"{DTBASE}-u-boot.dtsi").read_text()
    defconfig = require(source / "futurehome-cube-2v0-eu_defconfig").read_text()
    gr_config = require(external / "configs/green_defconfig").read_text()
    gr_boot = require(green / "uboot-boot.ush").read_text()

    # Validate all known upstream anchors *before* creating/writing anything.
    # This guards the pinned checkout against partial generation when HAOS's
    # internal structure changes.
    required_files = [green / name for name in (
        "boot-env.txt", "cmdline.txt", "haos-hook.sh", "image-spl-spl.cfg",
        "partition-spl-spl.cfg")]
    for file in required_files:
        require(file)
    if 'cp "${BINARIES_DIR}/boot.scr" "${BOOT_DATA}/boot.scr"' not in (green / 'haos-hook.sh').read_text():
        raise RuntimeError('Pinned HAOS hook changed; refusing partial port')
    rauc_pre = require(external / "ota/rauc-hook").read_text()
    if rauc_pre.count('install_spl() {\n') != 1 or rauc_pre.count('install_boot() {\n') != 1:
        raise RuntimeError('Pinned HAOS RAUC hook changed; refusing partial port')
    mk_pre = require(external / 'package/rockchip-blobs/rockchip-blobs.mk').read_text()
    if 'ROCKCHIP_BLOBS_SITE = https://github.com/rockchip-linux/rkbin/archive' not in mk_pre:
        raise RuntimeError('Unexpected Rockchip blob source')
    for expected in ('BR2_LINUX_KERNEL_INTREE_DTS_NAME="rockchip/rk3566-ha-green"',
                     'BR2_TARGET_UBOOT_CUSTOM_VERSION_VALUE="2026.04"',
                     'BR2_PACKAGE_HASSIO_MACHINE="green"'):
        if expected not in gr_config:
            raise RuntimeError(f'Unexpected HAOS Green config: {expected}')
    if "i2c dev 0\nsetenv check_btn_pressed" not in gr_boot or "# HAOS system A/B" not in gr_boot:
        raise RuntimeError('Unexpected HAOS boot script')
    # Validate before generating board files; only write the corrected upstream
    # patch when all Cube port generation has completed successfully.
    fileenv_patch_path, corrected_fileenv_patch = adapt_fileenv_patch(haos)

    bdir.mkdir(parents=True)
    (bdir / "dts/rockchip").mkdir(parents=True)
    (bdir / "dts/rockchip" / f"{DTBASE}.dts").write_text(dts)
    # The radio is intentionally powered off in the base Device Tree.
    # Prepare a separately testable power-on overlay for the built-in EFR32MG12.
    overlay_name = "rockchip-futurehome-cube-2v0-eu-efr32mg12-power-on"
    radio_overlay = source / "device-tree-overlays" / (overlay_name + ".dtso")
    if not radio_overlay.is_file():
        raise FileNotFoundError(f"Required built-in Zigbee overlay missing: {radio_overlay}")
    shutil.copy2(radio_overlay, bdir / "dts/rockchip" / radio_overlay.name)
    for file in ["boot-env.txt", "cmdline.txt", "haos-hook.sh", "image-spl-spl.cfg", "partition-spl-spl.cfg"]:
        shutil.copy2(require(green / file), bdir / file)
    (bdir / "cmdline.txt").write_text("console=ttyS2,1500000n8\n")
    # Enables *hardware power* for the Zigbee chip; it does not join a network,
    # install firmware or alter Home Assistant device pairing.
    (bdir / "boot-env.txt").write_text(f"overlays={overlay_name}\n")
    (bdir / "meta").write_text("""BOARD_ID=cube2v0eu
BOARD_NAME="Cube HAOS – Futurehome CUBE-2V0-EU (experimental)"
CHASSIS=embedded
BOOTLOADER=uboot
KERNEL_FILE=Image
PARTITION_TABLE_TYPE=hybrid
BOOT_SIZE=16M
BOOT_SPL=true
BOOT_SPL_SIZE=16M
BOOT_ENV_SIZE=0x8000
SUPERVISOR_MACHINE=qemuarm-64
SUPERVISOR_ARCH=aarch64
""")
    (bdir / "kernel.config").write_text("""# Cube-2v0-EU specific kernel options. Do not modify generic kernel config.
CONFIG_MMC_DW=y
CONFIG_MMC_DW_ROCKCHIP=y
CONFIG_RTC_DRV_PCF85063=y
CONFIG_USB_SERIAL=y
CONFIG_USB_SERIAL_CP210X=y
CONFIG_USB_SERIAL_CH341=y
CONFIG_USB_SERIAL_FTDI_SIO=y
CONFIG_I2C_CHARDEV=y
CONFIG_GPIO_CDEV=y
CONFIG_ROCKCHIP_THERMAL=y
""")
    (bdir / "uboot.config").write_text("""# Use HAOS common uboot.config: bootflow, FAT, fileenv, A/B.
# These options must be checked against U-Boot 2026.01 and Cube DTS on real hardware.
CONFIG_BOOTDELAY=1
CONFIG_BOOTCOMMAND="bootflow scan -b"
CONFIG_ENV_IS_NOWHERE=y
# CONFIG_ENV_IS_IN_MMC is not set
CONFIG_BOOTSTD=y
CONFIG_BOOTMETH_SCRIPT=y
CONFIG_CMD_BOOTFLOW=y
""")
    # HAOS Green A/B logic is used as tested architectural starting point,
    # but its board-specific reset button code is not relevant to Cube.
    pre = gr_boot.find("i2c dev 0\nsetenv check_btn_pressed")
    end = gr_boot.find("# HAOS system A/B")
    if pre < 0 or end < pre:
        raise RuntimeError("Upstream Green U-Boot script changed; cannot safely remove Green-only I2C button code")
    gr_boot = gr_boot[:pre] + ("# Cube: recovery/button path is handled by Rockchip Loader/Maskrom.\n"
                                  "# Do not run the HA Green I2C power button logic.\n\n") + gr_boot[end:]
    gr_boot = gr_boot.replace("rk3566-ha-green.dtb", f"{DTBASE}.dtb")
    # Never continue with stale memory if the board DTB is not on the boot partition.
    dtb_load = ('echo "Loading standard device tree ${fdtfile}"\n'
                'fatload ${devtype} ${devnum}:${boot_partnum} ${fdt_addr_r} ${fdtfile}\n'
                'fdt addr ${fdt_addr_r}\n')
    guarded = ('echo "Loading standard device tree ${fdtfile}"\n'
               'if fatload ${devtype} ${devnum}:${boot_partnum} ${fdt_addr_r} ${fdtfile}; then\n'
               '    fdt addr ${fdt_addr_r}\n'
               'else\n'
               '    echo "FATAL: Cube DTB missing, refusing kernel boot"\n'
               '    reset\n'
               'fi\n')
    if dtb_load not in gr_boot:
        raise RuntimeError('Upstream HAOS DTB load flow changed; do not generate a bootloader')
    gr_boot = gr_boot.replace(dtb_load, guarded, 1)
    # The Cube recovery button helper from board support is provided for a
    # separate boot-console validation stage. Do not enable an untested GPIO
    # sequence in the default boot path of a heating controller.
    bootmode = source / "futurehome-cube-2v0-eu-bootmode-script.cmd"
    if bootmode.is_file():
        (bdir / "bootmode-OPTIONAL-UNTESTED.ush").write_text(bootmode.read_text())
    (bdir / "uboot-boot.ush").write_text(gr_boot)

    # Fail image assembly if board files are not actually produced. The default
    # upstream HAOS hook blindly copies *.dtb, so a missing Cube DTB could
    # otherwise turn into an apparently valid image.
    hook = (bdir / "haos-hook.sh").read_text()
    hook = hook.replace('    cp "${BINARIES_DIR}/boot.scr" "${BOOT_DATA}/boot.scr"',
        '    test -s "${BINARIES_DIR}/boot.scr" || { echo "MISSING boot.scr" >&2; return 1; }\n'
        '    test -s "${BINARIES_DIR}/' + DTBASE + '.dtb" || { echo "MISSING Cube DTB" >&2; return 1; }\n'
        '    cp "${BINARIES_DIR}/boot.scr" "${BOOT_DATA}/boot.scr"')
    # Bundle the radio overlay so the built-in radio can be activated without a
    # USB dongle. Check exact generated filename before packaging.
    hook = hook.replace(
        '    cp "${BINARIES_DIR}"/*.dtb "${BOOT_DATA}/"',
        '    cp "${BINARIES_DIR}"/*.dtb "${BOOT_DATA}/"\n'
        '    test -s "${BINARIES_DIR}/' + overlay_name + '.dtbo" || { echo "MISSING Cube Zigbee DTBO" >&2; return 1; }\n'
        '    mkdir -p "${BOOT_DATA}/overlays"\n'
        '    cp "${BINARIES_DIR}/' + overlay_name + '.dtbo" "${BOOT_DATA}/overlays/"')
    if "MISSING Cube Zigbee DTBO" not in hook:
        raise RuntimeError("HAOS hook lacked radio overlay insertion")
    if "MISSING Cube DTB" not in hook:
        raise RuntimeError("HAOS hook changed; refusing unverified image assembly")
    (bdir / "haos-hook.sh").write_text(hook)

    # Upstream kernel DTS is supplied with Buildroot CUSTOM_DTS_DIR to copy
    # it into arch/arm64/boot/dts/rockchip, keeping the original source intact.
    # U-Boot needs the Cube defconfig and upstream DT files added as patches.
    patchdir = bdir / "patches/uboot"
    patchdir.mkdir(parents=True)
    items = [
        (f"dts/upstream/src/arm64/rockchip/{DTBASE}.dts", dts),
        (f"arch/arm/dts/{DTBASE}-u-boot.dtsi", dtsi),
        ("configs/futurehome-cube-2v0-eu_defconfig", defconfig),
    ]
    patches = [add_patch(path, body) for path, body in items]
    (patchdir / "0001-add-futurehome-cube-board.patch").write_text("\n".join(patches))

    cfg = gr_config
    cfg = replace_unique(cfg,
        "$(BR2_EXTERNAL_HAOS_PATH)/board/nabucasa/green/patches",
        "$(BR2_EXTERNAL_HAOS_PATH)/board/cube/cube2v0eu/patches")
    cfg = replace_unique(cfg,
        "$(BR2_EXTERNAL_HAOS_PATH)/board/nabucasa/green",
        "$(BR2_EXTERNAL_HAOS_PATH)/board/cube/cube2v0eu")
    cfg = replace_unique(cfg,
        'BR2_LINUX_KERNEL_INTREE_DTS_NAME="rockchip/rk3566-ha-green"',
        'BR2_LINUX_KERNEL_CUSTOM_DTS_DIR="$(BR2_EXTERNAL_HAOS_PATH)/board/cube/cube2v0eu/dts"')
    cfg = replace_unique(cfg,
        'BR2_TARGET_UBOOT_CUSTOM_VERSION_VALUE="2026.04"',
        'BR2_TARGET_UBOOT_CUSTOM_VERSION_VALUE="2026.01"')
    cfg = replace_unique(cfg,
        'BR2_TARGET_UBOOT_BOARD_DEFCONFIG="green"',
        'BR2_TARGET_UBOOT_BOARD_DEFCONFIG="futurehome-cube-2v0-eu"')
    cfg = replace_unique(cfg,
        'BR2_PACKAGE_HASSIO_MACHINE="green"',
        'BR2_PACKAGE_HASSIO_MACHINE="qemuarm-64"')
    cfg = replace_unique(cfg,
        'BR2_PACKAGE_OS_AGENT_BOARD="Green"',
        'BR2_PACKAGE_OS_AGENT_BOARD="Cube2V0EU"')
    cfg = replace_unique(cfg,
        'BR2_PACKAGE_ROCKCHIP_BLOBS_VERSION="b4558da0860ca48bf1a571dd33ccba580b9abe23"',
        f'BR2_PACKAGE_ROCKCHIP_BLOBS_VERSION="{ARMBIAN_RKBIN_SHA}"')
    cfg = replace_unique(cfg,
        'BR2_PACKAGE_ROCKCHIP_BLOBS_ATF="bin/rk35/rk3568_bl31_v1.43.elf"',
        'BR2_PACKAGE_ROCKCHIP_BLOBS_ATF="rk33/rk3328_bl31_v1.42.elf"')
    cfg = replace_unique(cfg,
        'BR2_PACKAGE_ROCKCHIP_BLOBS_TPL="bin/rk35/rk3566_ddr_1056MHz_v1.18.bin"',
        'BR2_PACKAGE_ROCKCHIP_BLOBS_TPL="rk33/rk3328_ddr_933MHz_v1.16.bin"')
    # Strip most wireless firmware from Green, as Cube has wired LAN and EFR32 radios.
    # Retain BlueZ for potential EFR32BG22 host access later.
    cfg = "\n".join(line for line in cfg.splitlines()
                    if not re.match(r"BR2_PACKAGE_LINUX_FIRMWARE_(?!USB_SERIAL).*=y$", line)) + "\n"
    (haos / HAOS_DEF_REL).write_text(cfg)

    # Cube uses files from Armbian/rkbin (Rockchip source tree doesn't ship
    # the rk3328 BL31 ELF in its present structure).
    mk = external / "package/rockchip-blobs/rockchip-blobs.mk"
    old = require(mk).read_text()
    new = replace_unique(old,
                         'ROCKCHIP_BLOBS_SITE = https://github.com/rockchip-linux/rkbin/archive',
                         'ROCKCHIP_BLOBS_SITE = https://github.com/armbian/rkbin/archive')
    mk.write_text(new)

    # HAOS normally updates a single SPL bootloader location in place, even
    # during an A/B OS update. On this unofficial board a failed U-Boot update
    # could make BOTH slots inaccessible. Treat bootloader replacement as a
    # separate USB/Maskrom maintenance operation, not an automatic OS update.
    # The initial disk image STILL contains the pinned U-Boot loader.
    rauc_hook_path = external / "ota/rauc-hook"
    if rauc_hook_path.exists():
        rauc_hook = rauc_hook_path.read_text()
        marker = 'install_spl() {\n'
        if rauc_hook.count(marker) != 1:
            raise RuntimeError("HAOS RAUC hook changed: missing install_spl()")
        rauc_hook = rauc_hook.replace(marker, marker +
            '    if [ "${RAUC_SYSTEM_COMPATIBLE:-}" = "haos-cube2v0eu" ]; then\n'
            '        echo "Cube: installed U-Boot remains pinned; skipping SPL update"\n'
            '        return 0\n'
            '    fi\n')
        # The shared FAT boot partition is another single-point-of-failure:
        # HAOS updates it in place. Freeze Cube boot.scr/DTB/FAT as well during
        # ordinary OS updates; only A/B kernel and rootfs are updated.
        # A future kernel incompatible with pinned DTB MUST fail the release
        # qualification, not silently change boot files in production.
        boot_marker = 'install_boot() {\n'
        if rauc_hook.count(boot_marker) != 1:
            raise RuntimeError("HAOS RAUC hook changed: missing install_boot()")
        rauc_hook = rauc_hook.replace(boot_marker, boot_marker +
            '    if [ "${RAUC_SYSTEM_COMPATIBLE:-}" = "haos-cube2v0eu" ]; then\n'
            '        echo "Cube: shared boot FAT frozen; skipping boot partition rewrite"\n'
            '        return 0\n'
            '    fi\n')
        rauc_hook_path.write_text(rauc_hook)
    else:
        raise FileNotFoundError("HAOS RAUC hook missing; cannot enforce boot partition freeze")

    fileenv_patch_path.write_text(corrected_fileenv_patch)

    (bdir / "UPSTREAM_NOTES.txt").write_text("""Source: RockPaperPencil/futurehome-cube2v0eu-boardsupport, pinned by bootstrap.sh.
Base: home-assistant/operating-system dev, pinned by bootstrap.sh.
Machine alias qemuarm-64 is used to fetch the official aarch64 Core image, NOT for OS OTA updates.
The target BOARD_ID cube2v0eu intentionally has no official HAOS update feed.
RAUC bundles must be built and signed locally from this exact fork.\nRAUC SPL and shared FAT boot writes are disabled for haos-cube2v0eu; U-Boot and DTB upgrades require a separate physically-qualified maintenance procedure.
Rockchip blobs source for this isolated source checkout is armbian/rkbin.
""")
    return {"target": TARGET, "board_dir": str(bdir), "defconfig": str(haos / HAOS_DEF_REL),
            "patch_count": 3, "machine_alias": "qemuarm-64"}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--haos", type=Path, required=True, help="Clean home-assistant/operating-system checkout")
    ap.add_argument("--board-support", type=Path, required=True, help="Pinned Cube board support checkout")
    args = ap.parse_args()
    print(build_port(args.haos, args.board_support))

if __name__ == "__main__":
    main()

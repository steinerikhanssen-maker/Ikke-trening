import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import unittest
SP=importlib.util.spec_from_file_location("static_preflight", Path(__file__).parents[1]/"scripts/static_preflight.py")
static=importlib.util.module_from_spec(SP)
SP.loader.exec_module(static)

SPEC = importlib.util.spec_from_file_location("prepare_port", Path(__file__).parents[1] / "scripts/prepare_port.py")
port = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(port)

class PortTests(unittest.TestCase):
    def fixture(self, d):
        haos = d / "haos"
        green = haos / "buildroot-external/board/nabucasa/green"
        green.mkdir(parents=True)
        for f in ("boot-env.txt", "cmdline.txt", "haos-hook.sh", "image-spl-spl.cfg", "partition-spl-spl.cfg"):
            (green/f).write_text(f"# {f}\n")
        (green/"haos-hook.sh").write_text(
            'function haos_pre_image() {\n    cp "${BINARIES_DIR}/boot.scr" "${BOOT_DATA}/boot.scr"\n    cp "${BINARIES_DIR}"/*.dtb "${BOOT_DATA}/"\n}\n')
        (green/"uboot-boot.ush").write_text(
            'i2c dev 0\nsetenv check_btn_pressed test\nwhile true; do :; done\n'
            '# HAOS system A/B\nha_version="rk3566-ha-green.dtb"\n'
            'echo "Loading standard device tree ${fdtfile}"\n'
            'fatload ${devtype} ${devnum}:${boot_partnum} ${fdt_addr_r} ${fdtfile}\n'
            'fdt addr ${fdt_addr_r}\n'
        )
        cfg = haos / "buildroot-external/configs"
        cfg.mkdir(parents=True)
        (cfg/"green_defconfig").write_text('''BR2_GLOBAL_PATCH_DIR="$(BR2_EXTERNAL_HAOS_PATH)/patches $(BR2_EXTERNAL_HAOS_PATH)/board/nabucasa/green/patches"
BR2_ROOTFS_POST_SCRIPT_ARGS="$(BR2_EXTERNAL_HAOS_PATH)/board/nabucasa/green"
BR2_LINUX_KERNEL_INTREE_DTS_NAME="rockchip/rk3566-ha-green"
BR2_TARGET_UBOOT_CUSTOM_VERSION_VALUE="2026.04"
BR2_TARGET_UBOOT_BOARD_DEFCONFIG="green"
BR2_PACKAGE_HASSIO_MACHINE="green"
BR2_PACKAGE_OS_AGENT_BOARD="Green"
BR2_PACKAGE_ROCKCHIP_BLOBS_VERSION="b4558da0860ca48bf1a571dd33ccba580b9abe23"
BR2_PACKAGE_ROCKCHIP_BLOBS_ATF="bin/rk35/rk3568_bl31_v1.43.elf"
BR2_PACKAGE_ROCKCHIP_BLOBS_TPL="bin/rk35/rk3566_ddr_1056MHz_v1.18.bin"
BR2_PACKAGE_LINUX_FIRMWARE_BRCM_BCM43XX=y
BR2_PACKAGE_LINUX_FIRMWARE_USB_SERIAL_TI=y
''')
        common_patch = haos / "buildroot-external/patches/uboot/0001-CMD-read-string-from-fileinto-env.patch"
        common_patch.parent.mkdir(parents=True)
        common_patch.write_text(
            "diff --git a/cmd/Makefile b/cmd/Makefile\\n"
            "--- a/cmd/Makefile\\n+++ b/cmd/Makefile\\n"
            + port.FILEENV_2026_04_HUNK
        )
        (haos/"buildroot-external/ota").mkdir(parents=True)
        (haos/"buildroot-external/ota/rauc-hook").write_text(
            '#!/bin/sh\ninstall_spl() {\n    echo write-loader\n}\ninstall_boot() {\n    echo write-fat\n}\n')
        pkg = haos / "buildroot-external/package/rockchip-blobs"
        pkg.mkdir(parents=True)
        (pkg/"rockchip-blobs.mk").write_text('ROCKCHIP_BLOBS_SITE = https://github.com/rockchip-linux/rkbin/archive\n')
        b = d / "board"
        b.mkdir()
        (b/"rk3328-futurehome-cube-2v0-eu.dts").write_text('/dts-v1/;\n/ { model = "fixture"; compatible = "rockchip,rk3328"; };\n')
        (b/"rk3328-futurehome-cube-2v0-eu-u-boot.dtsi").write_text('/ { chosen { }; };\n')
        (b/"futurehome-cube-2v0-eu_defconfig").write_text('CONFIG_ARM=y\n')
        overlays = b / "device-tree-overlays"
        overlays.mkdir()
        (overlays / "rockchip-futurehome-cube-2v0-eu-efr32mg12-power-on.dtso").write_text(
            "/dts-v1/; /plugin/; / { compatible = \"rockchip,rk3328\"; };\n")
        return haos, b

    def test_generates_board_files_without_futurehome_backup(self):
        with TemporaryDirectory() as s:
            d=Path(s); haos, board=self.fixture(d)
            result=port.build_port(haos,board)
            self.assertEqual(result['target'],'cube2v0eu')
            audit=static.preflight(haos)
            self.assertTrue(audit['passed'],audit['failures'])
            c=(haos/"buildroot-external/configs/cube2v0eu_defconfig").read_text()
            self.assertIn('BR2_LINUX_KERNEL_CUSTOM_DTS_DIR=',c)
            self.assertIn('BR2_PACKAGE_HASSIO_MACHINE="qemuarm-64"',c)
            self.assertNotIn('board/nabucasa/green',c)
            self.assertNotIn('BR2_PACKAGE_LINUX_FIRMWARE_BRCM_BCM43XX',c)
            self.assertIn('FATAL: Cube DTB missing', (haos/'buildroot-external/board/cube/cube2v0eu/uboot-boot.ush').read_text())
            self.assertIn('rk3328-futurehome-cube-2v0-eu.dtb',
                          (haos/"buildroot-external/board/cube/cube2v0eu/uboot-boot.ush").read_text())
            self.assertNotIn('setenv check_btn_pressed',
                             (haos/"buildroot-external/board/cube/cube2v0eu/uboot-boot.ush").read_text())
            self.assertIn('MISSING Cube Zigbee DTBO',
                (haos/"buildroot-external/board/cube/cube2v0eu/haos-hook.sh").read_text())
            self.assertIn('overlays=rockchip-futurehome-cube-2v0-eu-efr32mg12-power-on',
                (haos/"buildroot-external/board/cube/cube2v0eu/boot-env.txt").read_text())
            self.assertIn('MISSING Cube DTB',
                (haos/"buildroot-external/board/cube/cube2v0eu/haos-hook.sh").read_text())
            self.assertIn('skipping SPL update',
                (haos/"buildroot-external/ota/rauc-hook").read_text())
            self.assertIn('skipping boot partition rewrite',
                (haos/"buildroot-external/ota/rauc-hook").read_text())
            self.assertIn('https://github.com/armbian/rkbin/archive',
                          (haos/"buildroot-external/package/rockchip-blobs/rockchip-blobs.mk").read_text())
            # Verify that all patches can be applied to a dummy U-Boot tree.
            src = d / "uboot";src.mkdir()
            patch = (haos/"buildroot-external/board/cube/cube2v0eu/patches/uboot/0001-add-futurehome-cube-board.patch")
            result=subprocess.run(['patch','-d',str(src),'-p1','--dry-run','-i',str(patch)],
                                  capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            with self.assertRaises(RuntimeError):
                port.build_port(haos,board)


    def test_retargets_global_fileenv_patch_to_exact_2026_01_makefile(self):
        with TemporaryDirectory() as s:
            d=Path(s); haos, board=self.fixture(d)
            port.build_port(haos, board)
            patch = haos / port.HAOS_FILEENV_PATCH
            body = patch.read_text()
            self.assertIn(port.FILEENV_2026_01_HUNK, body)
            self.assertNotIn(port.FILEENV_2026_04_HUNK, body)
            # Reproduce the relevant upstream v2026.01 Makefile context.
            # v2026.01 lacks the CMD_SM3SUM line added in later U-Boot.
            tree = d / "u-boot-2026.01"
            cmd = tree / "cmd"
            cmd.mkdir(parents=True)
            (cmd / "Makefile").write_text(
                "obj-$(CONFIG_CMD_SHA1SUM) += sha1sum.o\\n"
                "obj-$(CONFIG_CMD_SEAMA) += seama.o\\n"
                "obj-$(CONFIG_CMD_SETEXPR) += setexpr.o\\n"
                "obj-$(CONFIG_CMD_SETEXPR_FMT) += printf.o\\n"
                "obj-$(CONFIG_CMD_SPI) += spi.o\\n"
                "obj-$(CONFIG_CMD_STRINGS) += strings.o\\n"
                "obj-$(CONFIG_CMD_SMBIOS) += smbios.o\\n"
            )
            result = subprocess.run(
                ["patch", "-d", str(tree), "-p1", "--batch", "--dry-run", "-i", str(patch)],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unknown_fileenv_patch_does_not_generate_board(self):
        with TemporaryDirectory() as s:
            d=Path(s); haos, board=self.fixture(d)
            target = haos / port.HAOS_FILEENV_PATCH
            target.write_text(target.read_text().replace("CMD_SM3SUM", "CHANGED_UPSTREAM"))
            with self.assertRaisesRegex(RuntimeError, "fileenv patch changed"):
                port.build_port(haos, board)
            self.assertFalse((haos / port.HAOS_BOARD_REL).exists())

    def test_missing_rauc_hook_stops_before_partial_port(self):
        with TemporaryDirectory() as t:
            d=Path(t); haos,board=self.fixture(d)
            (haos/"buildroot-external/ota/rauc-hook").unlink()
            with self.assertRaises(FileNotFoundError):
                port.build_port(haos,board)
            self.assertFalse((haos/"buildroot-external/board/cube/cube2v0eu").exists())

if __name__=='__main__':
    unittest.main()

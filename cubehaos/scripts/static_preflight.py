#!/usr/bin/env python3
"""Review generated port against pinned HAOS source tree, without building."""
import argparse
import json
from pathlib import Path


def preflight(haos: Path) -> dict:
    external=haos/'buildroot-external'
    board=external/'board/cube/cube2v0eu'
    cfg=(external/'configs/cube2v0eu_defconfig').read_text()
    meta=(board/'meta').read_text()
    boot=(board/'uboot-boot.ush').read_text()
    hook=(board/'haos-hook.sh').read_text()
    rauc=(external/'ota/rauc-hook').read_text()
    src=(board/'dts/rockchip/rk3328-futurehome-cube-2v0-eu.dts').read_text()
    patch=(board/'patches/uboot/0001-add-futurehome-cube-board.patch').read_text()
    blobs=(external/'package/rockchip-blobs/rockchip-blobs.mk').read_text()
    fileenv=(external/'patches/uboot/0001-CMD-read-string-from-fileinto-env.patch').read_text()
    required={
       'correct CPU':'"rockchip,rk3328"' in src,
       'correct board id':'BOARD_ID=cube2v0eu' in meta,
       'supervisor machine alias':'BR2_PACKAGE_HASSIO_MACHINE="qemuarm-64"' in cfg,
       'bootloader correct family':'BR2_TARGET_UBOOT_BOARD_DEFCONFIG="futurehome-cube-2v0-eu"' in cfg,
       'custom Linux dts':'BR2_LINUX_KERNEL_CUSTOM_DTS_DIR=' in cfg,
       'expected boot script':'rk3328-futurehome-cube-2v0-eu.dtb' in boot,
       'FDT load refuses missing DTB':'FATAL: Cube DTB missing' in boot,
       'no Green boot button':'check_btn_pressed' not in boot,
       'Cube DTB fail-closed':'MISSING Cube DTB' in hook,
       'Cube boot.scr fail-closed':'MISSING boot.scr' in hook,
       'RAUC compatibility':'haos-cube2v0eu' in rauc,
       'bootloader freeze':'skipping SPL update' in rauc,
       'FAT boot freeze':'skipping boot partition rewrite' in rauc,
       'RK3328 source patches':'rk3328-futurehome-cube-2v0-eu.dts' in patch,
       'blob source pinned fork':'github.com/armbian/rkbin/archive' in blobs,
       'fileenv patch compatible with U-Boot 2026.01':(
           '@@ -175,5 +175,6 @@ obj-$(CONFIG_CMD_SHA1SUM)' in fileenv
           and '+obj-$(CONFIG_CMD_FILEENV) += fileenv.o' in fileenv
           and ' obj-$(CONFIG_CMD_SM3SUM) += sm3sum.o' not in fileenv),
       'no Green board target':'board/nabucasa/green' not in cfg,
    }
    failures=[name for name,passed in required.items() if not passed]
    return {'static_tests':required,'passed':not failures,'failures':failures,
            'note':'Static source checks; NOT evidence of a compiled image or bootable hardware'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('haos',type=Path)
    a=p.parse_args();result=preflight(a.haos)
    print(json.dumps(result,indent=2))
    if not result['passed']:p.exit(1,'Static preflight failed\n')

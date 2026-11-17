#!/usr/bin/env python3
"""Fail-closed HAOS Cube release-artifact verification.

Checks the entire compressed image (not just the first 2 KiB), GPT CRCs,
partition identities and geometry and the presence of an OTA bundle. This is
NOT a boot test, a hardware test or cryptographic validation of a RAUC bundle.
"""
from __future__ import annotations
import argparse
import binascii
import hashlib
import json
import lzma
import re
import struct
from pathlib import Path

BOARD = "cube2v0eu"
# HAOS partitions per current hybrid GPT genimage layout.
PARTS = {"hassos-boot", "hassos-kernel0", "hassos-system0", "hassos-kernel1",
         "hassos-system1", "hassos-bootstate", "hassos-overlay", "hassos-data"}
CHUNK = 4 * 1024 * 1024
MAX_RAW_BYTES = 8_000_000_000  # Nominal 8 GB; actual target capacity is checked at flash.


class ArtifactError(RuntimeError):
    pass


def gpt_partitions(head: bytes, total: int, tail: bytes | None = None) -> list[dict]:
    if len(head) < 65536 or head[510:512] != b"\x55\xaa":
        raise ArtifactError("Disk image lacks a valid MBR/GPT preamble")
    hdr = head[512:1024]
    if hdr[:8] != b"EFI PART":
        raise ArtifactError("GPT primary header missing")
    header_size = struct.unpack_from('<I', hdr, 12)[0]
    if not 92 <= header_size <= 512:
        raise ArtifactError("Invalid GPT header length")
    header_crc = struct.unpack_from('<I', hdr, 16)[0]
    check = bytearray(hdr[:header_size]); check[16:20] = b"\0" * 4
    if binascii.crc32(check) & 0xffffffff != header_crc:
        raise ArtifactError("GPT header checksum mismatch")
    current_lba, backup_lba, first_use, last_use = struct.unpack_from('<QQQQ', hdr, 24)
    if current_lba != 1 or backup_lba * 512 >= total or first_use > last_use:
        raise ArtifactError("GPT primary header geometries invalid")
    entry_lba = struct.unpack_from('<Q', hdr, 72)[0]
    count, entry_size, stored_crc = struct.unpack_from('<III', hdr, 80)
    if not 8 <= count <= 256 or entry_size != 128:
        raise ArtifactError("Unsupported GPT entry layout")
    start, end = entry_lba * 512, entry_lba * 512 + count * entry_size
    if end > len(head):
        raise ArtifactError("Insufficient GPT table data")
    entries = head[start:end]
    if binascii.crc32(entries) & 0xffffffff != stored_crc:
        raise ArtifactError("GPT partition table checksum mismatch")
    if tail is not None:
        if (backup_lba + 1) * 512 != total:
            raise ArtifactError("Backup GPT is not at end of image")
        bh = tail[-512:]
        if bh[:8] != b"EFI PART":
            raise ArtifactError("Backup GPT header missing")
        bs = struct.unpack_from('<I',bh,12)[0]
        if bs != header_size:
            raise ArtifactError("Backup GPT header size mismatch")
        check = bytearray(bh[:bs]); check[16:20] = b"\0"*4
        if binascii.crc32(check)&0xffffffff != struct.unpack_from('<I',bh,16)[0]:
            raise ArtifactError("Backup GPT header checksum mismatch")
        its_lba, other_lba = struct.unpack_from('<QQ',bh,24)
        if its_lba != backup_lba or other_lba != current_lba:
            raise ArtifactError("Backup GPT pointers mismatch")
        backup_entry_lba = struct.unpack_from('<Q',bh,72)[0]
        backup_entry_off = backup_entry_lba * 512 - (total-len(tail))
        if backup_entry_off < 0 or backup_entry_off + count*entry_size > len(tail):
            raise ArtifactError("Backup GPT table outside inspection window")
        backup_entries=tail[backup_entry_off:backup_entry_off+count*entry_size]
        if backup_entries != entries:
            raise ArtifactError("Primary and backup GPT tables differ")
    result=[]
    for idx in range(count):
        ent=entries[idx*128:(idx+1)*128]
        if ent[:16] == b"\0"*16:
            continue
        first,last=struct.unpack_from('<QQ',ent,32)
        name=ent[56:128].decode('utf-16-le','strict').rstrip('\0')
        if first > last or first < first_use or last > last_use or (last+1)*512 > total:
            raise ArtifactError(f"Partition {name or idx} outside usable GPT geometry")
        result.append(dict(name=name,first_lba=first,last_lba=last,bytes=(last-first+1)*512))
    names=[x['name'] for x in result]
    if len(set(names)) != len(names):
        raise ArtifactError("Duplicated GPT partition names")
    missing=PARTS-set(names)
    if missing:
        raise ArtifactError("Missing HAOS Cube partitions: "+", ".join(sorted(missing)))
    ordered=sorted(result,key=lambda x:x['first_lba'])
    if any(a['last_lba'] >= b['first_lba'] for a,b in zip(ordered,ordered[1:])):
        raise ArtifactError("Overlapping GPT partitions")
    return result


def inspect_image(path: Path, max_bytes: int=MAX_RAW_BYTES) -> dict:
    if not re.fullmatch(r"haos_cube2v0eu-[A-Za-z0-9_.-]+\.img\.xz",path.name):
        raise ArtifactError("Image filename does not identify Cube HAOS")
    if not path.is_file():
        raise ArtifactError("Missing disk image")
    compressed_hash=hashlib.sha256()
    raw_hash=hashlib.sha256()
    first=bytearray()
    tail=b""
    size=0
    with path.open('rb') as source:
        while chunk := source.read(CHUNK):
            compressed_hash.update(chunk)
    try:
        with lzma.open(path,'rb') as stream:
            while chunk := stream.read(CHUNK):
                size += len(chunk)
                if size>max_bytes:
                    raise ArtifactError("Raw image exceeds allowed nominal 8GB Cube capacity")
                if len(first)<65536:
                    first.extend(chunk[:65536-len(first)])
                tail=(tail+chunk)[-65536:]
                raw_hash.update(chunk)
    except (lzma.LZMAError, EOFError) as exc:
        raise ArtifactError("XZ decompression or integrity failure") from exc
    if size < 200_000_000 or size % 512 != 0:
        raise ArtifactError("Invalid raw disk image length")
    partitions = gpt_partitions(bytes(first),size,tail)
    return dict(file=path.name,compressed_bytes=path.stat().st_size,raw_bytes=size,
                sha256_compressed=compressed_hash.hexdigest(),sha256_raw=raw_hash.hexdigest(),
                partitions=partitions,gpt_checked=True,full_xz_checked=True,
                hardware_boot_tested=False,rauc_signature_checked=False)


def check(folder: Path) -> dict:
    if not folder.is_dir():
        raise ArtifactError(f"No images folder: {folder}")
    images=sorted(folder.glob('haos_cube2v0eu-*.img.xz'))
    updates=sorted(folder.glob('haos_cube2v0eu-*.raucb'))
    if len(images)!=1 or len(updates)!=1:
        raise ArtifactError(f"Expected exactly one Cube image and update bundle; found {len(images)} / {len(updates)}")
    if not updates[0].is_file() or updates[0].stat().st_size < 100_000:
        raise ArtifactError("Missing or too small Cube RAUC bundle")
    image=inspect_image(images[0])
    update_hash=hashlib.sha256()
    with updates[0].open('rb') as f:
        while chunk := f.read(CHUNK):
            update_hash.update(chunk)
    return dict(checked_path=str(folder),board=BOARD,image=image,
                update_bundle=dict(file=updates[0].name,bytes=updates[0].stat().st_size,
                  sha256=update_hash.hexdigest()),
                note="RAUC signature and physical boot are separate mandatory release gates")


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('images',type=Path,help='Folder containing one matching .img.xz and .raucb')
    p.add_argument('--json-out',type=Path,help='Write release inspection JSON')
    args=p.parse_args()
    try:
        result=check(args.images)
    except (ArtifactError, OSError, EOFError) as exc:
        p.exit(1,f"RELEASE GATE FAILED: {exc}\n")
    out=json.dumps(result,indent=2,ensure_ascii=False)
    if args.json_out:
        args.json_out.write_text(out+'\n')
    print(out)

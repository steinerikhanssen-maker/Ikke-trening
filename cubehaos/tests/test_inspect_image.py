import importlib.util
import lzma
import binascii
import struct
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

PATH = Path(__file__).parents[1] / 'scripts/inspect_image.py'
spec=importlib.util.spec_from_file_location('inspect_image',PATH)
img=importlib.util.module_from_spec(spec);spec.loader.exec_module(img)

PARTITIONS=['hassos-boot','hassos-kernel0','hassos-system0',
            'hassos-kernel1','hassos-system1','hassos-bootstate','hassos-overlay','hassos-data']


def fake_head(disk_size, absent=None):
    data=bytearray(65536)
    data[510:512]=b'\x55\xaa'
    entries=bytearray(128*128)
    index=0
    for name in PARTITIONS:
        if name==absent:continue
        off=index*128;first=2048+index*8192;last=first+8191
        entries[off:off+16]=b'\x11'*16
        entries[off+16:off+32]=bytes([index+1])*16
        struct.pack_into('<QQQ',entries,off+32,first,last,0)
        string=name.encode('utf-16-le')
        entries[off+56:off+56+len(string)]=string
        index+=1
    hdr=bytearray(512)
    hdr[:8]=b'EFI PART'
    struct.pack_into('<I',hdr,8,0x00010000)
    struct.pack_into('<I',hdr,12,92)
    backup_lba=disk_size//512-1
    struct.pack_into('<QQQQ',hdr,24,1,backup_lba,34,backup_lba-33)
    struct.pack_into('<Q',hdr,72,2)
    struct.pack_into('<III',hdr,80,128,128,binascii.crc32(entries)&0xffffffff)
    struct.pack_into('<I',hdr,16,binascii.crc32(hdr[:92])&0xffffffff)
    data[512:1024]=hdr
    data[1024:1024+len(entries)]=entries
    return data



def fake_tail(disk_size, primary):
    entries=primary[1024:1024+128*128]
    tail=bytearray(65536)
    backup_lba=disk_size//512-1
    backup_entry_lba=backup_lba-32
    entry_off=65536-(disk_size-backup_entry_lba*512)
    tail[entry_off:entry_off+len(entries)]=entries
    h=bytearray(512)
    h[:8]=b'EFI PART'
    struct.pack_into('<I',h,8,0x00010000)
    struct.pack_into('<I',h,12,92)
    struct.pack_into('<QQQQ',h,24,backup_lba,1,34,backup_lba-33)
    struct.pack_into('<Q',h,72,backup_entry_lba)
    struct.pack_into('<III',h,80,128,128,binascii.crc32(entries)&0xffffffff)
    struct.pack_into('<I',h,16,binascii.crc32(h[:92])&0xffffffff)
    tail[-512:]=h
    return tail

class ImageTests(unittest.TestCase):
    def test_recognizes_all_required_partitions_and_checksums(self):
        parts=img.gpt_partitions(fake_head(230_000_128),230_000_128)
        self.assertEqual([p['name'] for p in parts],PARTITIONS)

    def test_rejects_missing_partition(self):
        with self.assertRaisesRegex(img.ArtifactError,'Missing HAOS Cube partitions'):
            img.gpt_partitions(fake_head(230_000_128,'hassos-bootstate'),230_000_128)

    def test_rejects_header_crc_damage(self):
        head=fake_head(230_000_128);head[512+16] ^= 1
        with self.assertRaisesRegex(img.ArtifactError,'header checksum'):
            img.gpt_partitions(head,230_000_128)

    def test_rejects_table_crc_damage(self):
        head=fake_head(230_000_128);head[1200] ^= 1
        with self.assertRaisesRegex(img.ArtifactError,'table checksum'):
            img.gpt_partitions(head,230_000_128)

    def test_rejects_wrong_device(self):
        with TemporaryDirectory() as d:
            path=Path(d)/'haos_green-19.0.img.xz';path.write_bytes(b'not a real image')
            with self.assertRaisesRegex(img.ArtifactError,'filename'):
                img.inspect_image(path)

    def test_rejects_empty_artifact_folder(self):
        with TemporaryDirectory() as d:
            with self.assertRaisesRegex(img.ArtifactError,'Expected exactly one'):
                img.check(Path(d))

    def test_reads_entire_xz_not_only_first_bytes(self):
        # Compressed image has valid GPT data and 220MB of zeros. A broken xz
        # footer MUST be detected even when its first 64KiB decompresses.
        size=220*1024*1024
        with TemporaryDirectory() as d:
            path=Path(d)/'haos_cube2v0eu-19.0.dev.img.xz'
            head=fake_head(size)
            tail=fake_tail(size,head)
            with lzma.open(path,'wb',preset=0) as out:
                out.write(head)
                zeros=b'\0'*(1024*1024)
                middle=size-len(head)-len(tail)
                for _ in range(middle//len(zeros)):out.write(zeros)
                out.write(b'\0'*(middle%len(zeros)))
                out.write(tail)
            self.assertEqual(img.inspect_image(path)['raw_bytes'],size)
            damaged=bytearray(tail); damaged[-512+16] ^= 1
            with self.assertRaisesRegex(img.ArtifactError,'Backup GPT header checksum'):
                img.gpt_partitions(head,size,damaged)
            blob=path.read_bytes()
            path.write_bytes(blob[:-20])
            with self.assertRaises((img.ArtifactError,EOFError)):
                img.inspect_image(path)

if __name__=='__main__':unittest.main()

from pathlib import Path
import importlib.util
import tempfile
import unittest

SPEC=importlib.util.spec_from_file_location('release_gate',Path(__file__).parents[1]/'scripts/release_gate.py')
release=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)

class TestReleaseGate(unittest.TestCase):
    def test_missing_image_is_not_verified(self):
        with tempfile.TemporaryDirectory() as temp:
            report=release.inspect(Path(temp))
            self.assertFalse(report['structural_image_validation'])
            self.assertFalse(report['physical_boot_validation'])
            self.assertFalse(report['safe_for_house_handover'])

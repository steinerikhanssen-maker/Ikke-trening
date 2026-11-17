import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

root=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location('sp',root/'scripts/static_preflight.py')
sp=importlib.util.module_from_spec(spec);spec.loader.exec_module(sp)

class StaticTests(unittest.TestCase):
    def test_flags_absent_board(self):
        with TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):sp.preflight(Path(d))

if __name__=='__main__':unittest.main()

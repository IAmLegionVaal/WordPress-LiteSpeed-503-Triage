import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=next((ROOT/'scripts').glob('*.sh'))
BASH=shutil.which('bash')

class Diagnostics(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)
        self.env=dict(os.environ)
        self.env['PATH']=str(self.path)+os.pathsep+os.environ['PATH']

    def mock(self,name,body):
        path=self.path/name
        path.write_text('#!/bin/sh\n'+body+'\n')
        path.chmod(0o755)
        return str(path)

    def run_script(self):
        return subprocess.run([BASH,str(SCRIPT)],env=self.env,capture_output=True,text=True,timeout=10)

    def test_missing_php_is_refused(self):
        self.env['PHP_BIN']=str(self.path/'absent')
        self.assertEqual(self.run_script().returncode,2)

    def test_php_failure_propagates(self):
        self.env['PHP_BIN']=self.mock('php','exit 7')
        self.assertEqual(self.run_script().returncode,7)

    def test_cli_only_warning(self):
        self.env['PHP_BIN']=self.mock('php','[ "$1" = "-r" ] || exit 99; echo "SAPI: cli"')
        result=self.run_script()
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('not proof of LiteSpeed/web SAPI',result.stdout)

    @unittest.skipUnless(shutil.which('php'),'PHP is not installed')
    def test_real_php_cli_output(self):
        self.env['PHP_BIN']=shutil.which('php')
        result=self.run_script()
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('SAPI: cli',result.stdout)
        self.assertIn('memory_limit:',result.stdout)

if __name__ == "__main__": unittest.main()

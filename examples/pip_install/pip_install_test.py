#!/usr/bin/env python3

import os
import subprocess
import unittest
from pathlib import Path

from rules_python.python.runfiles import runfiles


class PipInstallTest(unittest.TestCase):
    maxDiff = None

    def test_entry_point_void_return(self):
        env = os.environ.get("YAMLLINT_ENTRY_POINT")
        self.assertIsNotNone(env)

        r = runfiles.Create()

        # To find an external target, this must use `{workspace_name}/$(rootpath @external_repo//:target)`
        entry_point = Path(
            r.Rlocation("rules_python_pip_install_example/{}".format(env))
        )
        self.assertTrue(entry_point.exists())

        proc = subprocess.run(
            [str(entry_point), "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(proc.stdout.decode("utf-8").strip(), "yamllint 1.26.3")

        # yamllint entry_point is of the form `def run(argv=None):`
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.run(
                [entry_point, "--option-does-not-exist"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        self.assertIn("returned non-zero exit status 2", str(context.exception))

    def test_entry_point_int_return(self):
        env = os.environ.get("SPHINX_BUILD_ENTRY_POINT")
        r = runfiles.Create()

        # To find an external target, this must use `{workspace_name}/$(rootpath @external_repo//:target)`
        entry_point = Path(
            r.Rlocation("rules_python_pip_install_example/{}".format(env))
        )
        self.assertTrue(entry_point.exists())

        proc = subprocess.run(
            [str(entry_point), "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # sphinx-build uses args[0] for its name, only assert the version here
        self.assertTrue(proc.stdout.decode("utf-8").strip().endswith("4.2.0"))

        # sphinx-build entry_point is of the form `def main(argv: List[str] = sys.argv[1:]) -> int:`
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.run(
                [entry_point, "--option-does-not-exist"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        self.assertIn("returned non-zero exit status 2", str(context.exception))

    def test_data(self):
        env = os.environ.get("WHEEL_DATA_CONTENTS")
        self.assertIsNotNone(env)
        self.assertListEqual(
            env.split(" "),
            [
                "external/pip/pypi__s3cmd/s3cmd-2.1.0.data/data/share/doc/packages/s3cmd/INSTALL.md",
                "external/pip/pypi__s3cmd/s3cmd-2.1.0.data/data/share/doc/packages/s3cmd/LICENSE",
                "external/pip/pypi__s3cmd/s3cmd-2.1.0.data/data/share/doc/packages/s3cmd/NEWS",
                "external/pip/pypi__s3cmd/s3cmd-2.1.0.data/data/share/doc/packages/s3cmd/README.md",
                "external/pip/pypi__s3cmd/s3cmd-2.1.0.data/data/share/man/man1/s3cmd.1",
                "external/pip/pypi__s3cmd/s3cmd-2.1.0.data/scripts/s3cmd",
            ],
        )

    def test_dist_info(self):
        env = os.environ.get("WHEEL_DIST_INFO_CONTENTS")
        self.assertIsNotNone(env)
        self.assertListEqual(
            env.split(" "),
            [
                "external/pip/pypi__boto3/boto3-1.14.51.dist-info/DESCRIPTION.rst",
                "external/pip/pypi__boto3/boto3-1.14.51.dist-info/METADATA",
                "external/pip/pypi__boto3/boto3-1.14.51.dist-info/RECORD",
                "external/pip/pypi__boto3/boto3-1.14.51.dist-info/WHEEL",
                "external/pip/pypi__boto3/boto3-1.14.51.dist-info/metadata.json",
                "external/pip/pypi__boto3/boto3-1.14.51.dist-info/top_level.txt",
            ],
        )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python

import os
import shutil
import sys

from impactrun import runconfig
from impactrun.impact_core import ImpactCore
from impactrun.runconfig import inspecdir


def fuzzspecs(specdir=inspecdir):
    sfs = []
    for _, _, filename in os.walk(specdir):
        sfs.extend(filename)
        break

    tfs = []
    specnames = []
    for spec in sfs:

        if not spec.endswith(".json"):
            continue
        specfname = specdir + "/" + spec
        testdir = spec[:-5].lower() + "_tests"  # important, convert specs to all lower case
        tfs.append(testdir)
        specnames.append(spec[:-5].lower())  # convert specs to all lower case
        print(f"Processing {specfname}, generating {testdir}")

        ImpactCore("", specfname, "", runconfig.dfuzzusrname, "", runconfig.dcvconfig, "n", "", True)

        shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), "auth.py"), "tests")
        if os.path.exists(testdir):
            shutil.rmtree(testdir)

        # custom attack_info.json over-write tests/data
        if os.path.exists("mytests/attack_info.json"):
            print("Overwriting attack_info")
            shutil.copy("mytests/attack_info.json", "tests/data/")

        if not os.path.exists("savedattackinfo"):
            os.mkdir("savedattackinfo")
            shutil.copy("tests/data/attack_info.json", "savedattackinfo/attack_info.json")

        os.rename("tests", testdir)
        print(f"Done Processing {specfname}, generating {testdir}")
    print("Done Fuzzing all specs")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("--help") or sys.argv[1].startswith("-help") or sys.argv[1].startswith("help"):
            print("Usage: [Optional name of directory containing json specs, Default: specs]")
            return
        fuzzspecs(sys.argv[1])
    else:
        fuzzspecs()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Honest Cube image gate. Static integrity != hardware boot verification."""
import argparse
import json
import pathlib
import sys
try:
    from inspect_image import check, ArtifactError
except ModuleNotFoundError:
    from scripts.inspect_image import check, ArtifactError

def inspect(path):
    base={"board":"cube2v0eu","structural_image_validation":False,"signed_bundle_validation":False,
          "physical_boot_validation":False,"safe_for_house_handover":False}
    try:
        scan=check(path)
    except (ArtifactError, FileNotFoundError, OSError, EOFError) as err:
        base["error"]=str(err)
        return base
    base["structural_image_validation"]=True
    base["image"]=scan["image"]["file"]
    base["image_hash"]=scan["image"]["sha256_compressed"]
    base["update_bundle"]=scan["update_bundle"]["file"]
    base["remaining_checks"]= ["RAUC signature with trusted certificate", "Cube boot", "Supervisor/Core start", "radio and power-cycle", "30-day soak"]
    return base

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("images",type=pathlib.Path)
    args=ap.parse_args()
    report=inspect(args.images)
    print(json.dumps(report,indent=2,ensure_ascii=False))
    # Deliberately not a passed-release signal until physically tested
    if not report["structural_image_validation"]:
        sys.exit(2)

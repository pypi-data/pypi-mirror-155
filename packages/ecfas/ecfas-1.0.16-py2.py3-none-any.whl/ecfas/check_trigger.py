#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 12:39:41 2022

@author: mirazoki
quality check for trigger
"""
import argparse
import logging
import os
import sys

import pandas as pd

log = logging.getLogger(__name__)

def check_trigger(baseline, outdir):
    bfile = os.path.join(baseline, 'trigg_info.csv')
    if not os.path.exists(bfile):
        log.error(f'Cannot find baseline trigger file(s) {bfile}')
        return False

    tarfile = os.path.join(outdir, 'trigger', 'trigg_info.csv')
    if not os.path.exists(tarfile):
        log.error(f'Cannot find reference trigger file(s) {tarfile}')
        return False

    log.info('Comparing TRIGGERED stations...\n')
    bdat = pd.read_csv(bfile, header=0)
    tdat = pd.read_csv(tarfile, header=0)
    if len(bdat.compare(tdat)) > 0:
        log.error('Differences found in trigger info')
        return False
    log.info('All good')
    return True


def main():
    parser = argparse.ArgumentParser("check_trigger")
    parser.add_argument('-b', '--baseline', metavar='<baseline_dir>', required=True, help='Absolute path to baseline file directory')
    parser.add_argument('-o', '--outputs', metavar='<output_dir>', required=True, help='Absolute path to output data to be checked')
    args = parser.parse_args()

    ok = check_trigger(args.baseline, args.outputs)
    # If any of the checks fail, exit with error flag, which will be picked up by test framework as a fail
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
      

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# padelpy/wrapper.py
# v.0.1.10
# Developed in 2021 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains the `padeldescriptor` function, a wrapper for PaDEL-Descriptor
#

# stdlib. imports
from os.path import abspath, dirname, join
from shutil import which
from subprocess import PIPE, Popen
from time import sleep

# PaDEL-Descriptor is packaged with PaDELPy
_PADEL_PATH = join(
    dirname(abspath(__file__)),
    'PaDEL-Descriptor',
    'PaDEL-Descriptor.jar'
)


def _popen_timeout(command: str, timeout: int) -> tuple:
    ''' Calls PaDEL-Descriptor, with optional subprocess timeout

    Args:
        command (str): command to execute via subprocess.Popen
        timeout (int): if not None, times out after this many seconds

    Returns:
        tuple: (stdout of process, stderr of process)
    '''

    p = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    if timeout is not None:
        for t in range(timeout):
            sleep(1)
            if p.poll() is not None:
                return p.communicate()
        p.kill()
        return (-1, b'PaDEL-Descriptor timed out during subprocess call')
    else:
        return p.communicate()


def padeldescriptor(maxruntime: int = -1, waitingjobs: int = -1,
                    threads: int = -1, d_2d: bool = False, d_3d: bool = False,
                    config: str = None, convert3d: bool = False,
                    descriptortypes: str = None,
                    detectaromaticity: bool = False, mol_dir: str = None,
                    d_file: str = None, fingerprints: bool = False,
                    log: bool = False, maxcpdperfile: int = 0,
                    removesalt: bool = False, retain3d: bool = False,
                    retainorder: bool = False, standardizenitro: bool = False,
                    standardizetautomers: bool = False,
                    tautomerlist: str = None,
                    usefilenameasmolname: bool = False,
                    sp_timeout: int = None,
                    headless: bool = True) -> None:
    ''' padeldescriptor: complete wrapper for PaDEL-Descriptor descriptor/
    fingerprint generation software

    Args:
        maxruntime (int): maximum running time per molecule (in mS); defaults
            to -1 (unlimited)
        waitingjobs (int): maximum number of jobs to store in queue for worker
            threads to process; defaults to -1 (50 * max threads)
        threads (int): maximum number of threads to use; defaults to -1 (equal
            to number of CPU cores)
        d_2d (bool): if `True`, calculates 2-D descriptors
        d_3d (bool): if `True`, calculates 3-D descriptors
        config (str): path to configuration file (optional)
        convert3d (bool): if `True`, converts molecule to 3-D
        descriptortypes (str): path to descriptor types file (optional)
        detectaromaticity (bool): if `True`, removes existing aromaticity
            information and automatically detect aromaticity in the molecule
            before calculation of descriptors
        mol_dir (str): path to directory (or file) containing structural files
        d_file (str): path to file to save calculated descriptors to
        fingerprints (bool): if `True`, calculates fingerprints
        log (bool): if `True`, creates a log file (same as descriptors file,
            with .log extension)
        maxcpdperfile (int): maximum number of compounds to be stored in each
            descriptor file; defaults to 0 (unlimited)
        removesalt (bool): if `True`, removes salt from the molecule
        retain3d (bool): if `True`, retains 3-D coordinates when standardizing
            structure
        retainorder (bool): if `True`, retains order of molecules in
            structural files for descriptor file
        standardizenitro (bool): if `True`, standardizes nitro groups to
            N(:O):O
        standardizetautomers (bool): if `True`, standardizes tautomers
        tautomerlist (str): path to SMIRKS tautomers file (optional)
        usefilenameasmolname (bool): if `True`, uses filename (minus the
            extension) as the molecule name
        headless (bool): if `True`, prevents Padel-splash image from loading. 

    Returns:
        None
    '''

    if which('java') is None:
        raise ReferenceError(
            'Java JRE 6+ not found (required for PaDEL-Descriptor)'
        )
    if headless:
        command = 'java -Djava.awt.headless=true -jar {}'.format(_PADEL_PATH)
    else:
        command = 'java -jar {}'.format(_PADEL_PATH)
    command += ' -maxruntime {}'.format(maxruntime)
    command += ' -waitingjobs {}'.format(waitingjobs)
    command += ' -threads {}'.format(threads)
    command += ' -maxcpdperfile {}'.format(maxcpdperfile)
    if d_2d is True:
        command += ' -2d'
    if d_3d is True:
        command += ' -3d'
    if config is not None:
        command += ' -config {}'.format(config)
    if convert3d is True:
        command += ' -convert3d'
    if descriptortypes is not None:
        command += ' -descriptortypes {}'.format(descriptortypes)
    if detectaromaticity is True:
        command += ' -detectaromaticity'
    if mol_dir is not None:
        command += ' -dir {}'.format(mol_dir)
    if d_file is not None:
        command += ' -file {}'.format(d_file)
    if fingerprints is True:
        command += ' -fingerprints'
    if log is True:
        command += ' -log'
    if removesalt is True:
        command += ' -removesalt'
    if retain3d is True:
        command += ' -retain3d'
    if retainorder is True:
        command += ' -retainorder'
    if standardizenitro is True:
        command += ' -standardizenitro'
    if standardizetautomers is True:
        command += ' -standardizetautomers'
    if tautomerlist is not None:
        command += ' -tautomerlist {}'.format(tautomerlist)
    if usefilenameasmolname is True:
        command += ' -usefilenameasmolname'

    _, err = _popen_timeout(command, sp_timeout)
    if err != b'':
        raise RuntimeError('PaDEL-Descriptor encountered an error: {}'.format(
            err.decode('utf-8')
        ))
    return
 
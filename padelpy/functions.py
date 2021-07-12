#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# padelpy/functions.py
# v.0.1.10
# Developed in 2021 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains various functions commonly used with PaDEL-Descriptor
#

# stdlib. imports
from collections import OrderedDict
from csv import DictReader
from datetime import datetime
from os import remove
from re import compile, IGNORECASE
from time import sleep
import warnings

# PaDELPy imports
from padelpy import padeldescriptor


def from_smiles(smiles, output_csv: str = None, descriptors: bool = True,
                fingerprints: bool = False, timeout: int = 60) -> OrderedDict:
    ''' from_smiles: converts SMILES string to QSPR descriptors/fingerprints

    Args:
        smiles (str, list): SMILES string for a given molecule, or a list of
            SMILES strings
        output_csv (str): if supplied, saves descriptors to this CSV file
        descriptors (bool): if `True`, calculates descriptors
        fingerprints (bool): if `True`, calculates fingerprints
        timeout (int): maximum time, in seconds, for conversion

    Returns:
        list or OrderedDict: if multiple SMILES strings provided, returns a
            list of OrderedDicts, else single OrderedDict; each OrderedDict
            contains labels and values for each descriptor generated for each
            supplied molecule
    '''

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]

    with open('{}.smi'.format(timestamp), 'w') as smi_file:
        if type(smiles) == str:
            smi_file.write(smiles)
        elif type(smiles) == list:
            smi_file.write('\n'.join(smiles))
        else:
            raise RuntimeError('Unknown input format for `smiles`: {}'.format(
                type(smiles)
            ))
    smi_file.close()

    save_csv = True
    if output_csv is None:
        save_csv = False
        output_csv = '{}.csv'.format(timestamp)

    for attempt in range(3):
        try:
            padeldescriptor(
                mol_dir='{}.smi'.format(timestamp),
                d_file=output_csv,
                convert3d=True,
                retain3d=True,
                d_2d=descriptors,
                d_3d=descriptors,
                fingerprints=fingerprints,
                sp_timeout=timeout,
                retainorder=True
            )
            break
        except RuntimeError as exception:
            if attempt == 2:
                remove('{}.smi'.format(timestamp))
                if not save_csv:
                    sleep(0.5)
                    try:
                        remove(output_csv)
                    except FileNotFoundError as e:
                        warnings.warn(e, RuntimeWarning)
                raise RuntimeError(exception)
            else:
                continue

    with open(output_csv, 'r', encoding='utf-8') as desc_file:
        reader = DictReader(desc_file)
        rows = [row for row in reader]
    desc_file.close()

    remove('{}.smi'.format(timestamp))
    if not save_csv:
        remove(output_csv)

    if type(smiles) == list and len(rows) != len(smiles):
        raise RuntimeError('PaDEL-Descriptor failed on one or more mols.' +
                           ' Ensure the input structures are correct.')
    elif type(smiles) == str and len(rows) == 0:
        raise RuntimeError(
            'PaDEL-Descriptor failed on {}.'.format(smiles) +
            ' Ensure input structure is correct.'
        )

    for idx, r in enumerate(rows):
        if len(r) == 0:
            raise RuntimeError(
                'PaDEL-Descriptor failed on {}.'.format(smiles[idx]) +
                ' Ensure input structure is correct.'
            )

    for idx in range(len(rows)):
        del rows[idx]['Name']

    if type(smiles) == str:
        return rows[0]
    return rows


def from_mdl(mdl_file: str, output_csv: str = None, descriptors: bool = True,
             fingerprints: bool = False, timeout: int = 60) -> list:
    ''' from_mdl: converts MDL file into QSPR descriptors/fingerprints;
    multiple molecules may be represented in the MDL file

    Args:
        mdl_file (str): path to MDL file
        output_csv (str): if supplied, saves descriptors/fingerprints here
        descriptors (bool): if `True`, calculates descriptors
        fingerprints (bool): if `True`, calculates fingerprints
        timeout (int): maximum time, in seconds, for conversion

    Returns:
        list: list of dicts, where each dict corresponds sequentially to a
            compound in the supplied MDL file
    '''

    is_mdl = compile(r'.*\.mdl$', IGNORECASE)
    if is_mdl.match(mdl_file) is None:
        raise ValueError('MDL file must have a `.mdl` extension: {}'.format(
            mdl_file
        ))

    save_csv = True
    if output_csv is None:
        save_csv = False
        output_csv = '{}.csv'.format(
            datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        )

    for attempt in range(3):
        try:
            padeldescriptor(
                mol_dir=mdl_file,
                d_file=output_csv,
                convert3d=True,
                retain3d=True,
                retainorder=True,
                d_2d=descriptors,
                d_3d=descriptors,
                fingerprints=fingerprints,
                sp_timeout=timeout
            )
            break
        except RuntimeError as exception:
            if attempt == 2:
                if not save_csv:
                    sleep(0.5)
                    try:
                        remove(output_csv)
                    except FileNotFoundError as e:
                        warnings.warn(e, RuntimeWarning)
                raise RuntimeError(exception)
            else:
                continue

    with open(output_csv, 'r', encoding='utf-8') as desc_file:
        reader = DictReader(desc_file)
        rows = [row for row in reader]
    desc_file.close()
    if not save_csv:
        remove(output_csv)
    if len(rows) == 0:
        raise RuntimeError('PaDEL-Descriptor returned no calculated values.' +
                           ' Ensure the input structure is correct.')
    for row in rows:
        del row['Name']
    return rows

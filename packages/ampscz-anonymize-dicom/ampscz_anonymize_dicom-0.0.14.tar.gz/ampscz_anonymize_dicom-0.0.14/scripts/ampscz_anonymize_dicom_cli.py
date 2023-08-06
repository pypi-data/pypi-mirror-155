#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path
import re
import argparse
import pydicom
import tempfile as tf
from anonymize_dicom.anonymize_dicom import anonymize_dicom


def parse_args(argv):
    '''Parse inputs coming from the terminal'''
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
        eddy_squeeze.
        Visualize extra information from FSL eddy outputs.
        ''')

    argparser.add_argument("--input_dir", "-i",
                           type=str,
                           default='dicom_dir',
                           help='Input dicom directory')

    argparser.add_argument("--id", "-d",
                           type=str,
                           default='ME00001',
                           help='AMPSCZ ID')

    argparser.add_argument("--session", "-s",
                           type=str,
                           default='1',
                           help='Session number')

    argparser.add_argument("--output_dir", "-o",
                           type=str,
                           default='./',
                           help='Output directory')

    args = argparser.parse_args(argv)
    return args


def check_dirs(dicom_root, output_dir):
    if dicom_root.is_dir() and output_dir.is_dir():
        dicom_root_check = True
    else:
        dicom_root_check = False

    return dicom_root_check


def check_name(name):
    if re.match('[A-Z]{2}\d{5}', name):
        name_check = True
    else:
        name_check = False
    return name_check


def get_dicom_info(dicom_root: Path, name, session, output_dir, vars):
    dicoms = 0
    for roott, dirs, files in os.walk(dicom_root):
        for file in files:
            dicoms += 1

    tmpdirname = tf.mkdtemp()
    with tf.TemporaryDirectory() as tmpdirname:
        first_file = True
        for roott, dirs, files in os.walk(dicom_root):
            for file in [x for x in files if not x.startswith('.')]:
                f = pydicom.read_file(Path(roott) / file, force=True)
                full_path = Path(roott) / file
                new_file_loc = Path(tmpdirname) / \
                        f"{f.SeriesNumber}_{f.SeriesDescription}" / file
                Path(new_file_loc).parent.mkdir(exist_ok=True, parents=True)
                for var in vars:
                    if var == 'PatientName':
                        replace_val = name
                    elif var == 'PatientID':
                        if first_file:
                            try:
                                date_row = f.AcquisitionDate
                            except:
                                return
                        year = date_row[:4]
                        month = date_row[4:6]
                        day = date_row[6:]
                        replace_val = f"{name}_MR_{year}_{month}_{day}_{session}"
                        first_file = False
                    elif var == 'PatientBirthDate':
                        replace_val = '19000101'
                    else:
                        replace_val = 'deidentified'
                    setattr(f, var, replace_val)
                f.save_as(new_file_loc)

                # print(new_file_loc)
        out_zip_loc = Path(output_dir) / \
                f"{name}_MR_{year}_{month}_{day}_{session}"

        shutil.make_archive(out_zip_loc, 'zip', tmpdirname)
        shutil.rmtree(tmpdirname)

    return


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

    args.input_dir = Path(args.input_dir)
    args.output_dir = Path(args.output_dir)
    
    # assert inputs
    assert check_name(args.id)
    assert check_dirs(args.input_dir, args.output_dir)

    var_list = ['AccessionNumber',
            'ReferringPhysicianName',
            'PerformingPhysicianName',
            'PatientName',
            'PatientID',
            'PatientBirthDate',
            'PerformedProcedureStepDescription',
            'InstitutionalDepartmentName',
            'InstitutionName',
            'InstitutionAddress']

    get_dicom_info(args.input_dir, args.id, args.session, args.output_dir,
                   var_list)

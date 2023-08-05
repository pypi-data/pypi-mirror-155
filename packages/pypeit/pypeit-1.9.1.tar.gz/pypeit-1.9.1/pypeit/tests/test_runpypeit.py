"""
Module to run tests on scripts
"""
import os
import sys
import glob
import shutil
from IPython.terminal.embed import embed

from configobj import ConfigObj

import pytest

import numpy as np

import matplotlib
matplotlib.use('agg')  # For Travis

from pypeit.scripts.parse_calib_id import ParseCalibID
from pypeit.scripts.setup import Setup
from pypeit.scripts.run_pypeit import RunPypeIt
from pypeit.tests.tstutils import dev_suite_required, data_path
from pypeit import specobjs


@dev_suite_required
def test_run_pypeit_calib_only():
    # Get the directories
    rawdir = os.path.join(os.environ['PYPEIT_DEV'], 'RAW_DATA', 'shane_kast_blue', '600_4310_d55')
    assert os.path.isdir(rawdir), 'Incorrect raw directory'

    master_key = 'A_1_DET01'

    # File list
    all_files = {
        'arcs': ['b1.fits.gz'],
        'flats': ['b11.fits.gz', 'b12.fits.gz', 'b13.fits.gz'],
        'bias': ['b21.fits.gz', 'b22.fits.gz', 'b23.fits.gz'],
    }
    all_masters = [f'MasterArc_{master_key}.fits',
                   f'MasterTiltimg_{master_key}.fits',
                   f'MasterBias_{master_key}.fits',
                   f'MasterTilts_{master_key}.fits',
                   f'MasterEdges_{master_key}.fits.gz',
                   f'MasterFlat_{master_key}.fits',
                   f'MasterWaveCalib_{master_key}.fits']

    # Just get a few files
    for ss, sub_files, masters in zip(range(3),
            [['arcs', 'flats', 'bias'],
             ['arcs', 'bias'],
             ['flats', 'bias']],
            [all_masters,
             [f'MasterArc_{master_key}.fits', f'MasterTiltimg_{master_key}.fits'],
             [f'MasterEdges_{master_key}.fits.gz']]):
        # Grab the subset
        files = []
        for sub_file in sub_files:
            files += all_files[sub_file]
        #
        testrawdir = os.path.join(rawdir, 'TEST')
        if os.path.isdir(testrawdir):
            shutil.rmtree(testrawdir)
        os.makedirs(testrawdir)
        for f in files:
            shutil.copy(os.path.join(rawdir, f), os.path.join(testrawdir, f))

        outdir = os.path.join(os.getenv('PYPEIT_DEV'), 'REDUX_OUT_TEST')

        # For previously failed tests
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)

        # Run the setup
        sargs = Setup.parse_args(['-r', testrawdir, '-s', 'shane_kast_blue', '-c all', '-o',
                                  '--output_path', outdir])
        Setup.main(sargs)

        # Change to the configuration directory and set the pypeit file
        configdir = os.path.join(outdir, 'shane_kast_blue_A')
        pyp_file = os.path.join(configdir, 'shane_kast_blue_A.pypeit')
        assert os.path.isfile(pyp_file), 'PypeIt file not written.'

        # Perform the calib-only reduction
        pargs = RunPypeIt.parse_args([pyp_file, '-c', '-r', configdir])
        RunPypeIt.main(pargs)

        # Test!
        for master_file in masters:
            assert os.path.isfile(os.path.join(configdir, 'Masters', master_file)
                                  ), 'Master File {:s} missing!'.format(master_file)

        # Now test parse_calib_id
        if ss == 0:
            pargs2 = ParseCalibID.parse_args([pyp_file])
            calib_dict = ParseCalibID.main(pargs2)
            assert isinstance(calib_dict, dict)
            assert len(calib_dict) > 0
            assert calib_dict['1'][master_key]['arc']['raw_files'][0] == 'b1.fits.gz'

        # Clean-up
        shutil.rmtree(outdir)
        shutil.rmtree(testrawdir)


def test_run_pypeit():

    # Just get a few files
    testrawdir = data_path('')

    outdir = data_path('REDUX_OUT_TEST')

    # For previously failed tests
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)

    # Run the setup
    sargs = Setup.parse_args(['-r', testrawdir+'b', '-s', 
                              'shane_kast_blue', '-c all', '-o', 
                              '--output_path', outdir])
    Setup.main(sargs)

    # Change to the configuration directory and set the pypeit file
    configdir = os.path.join(outdir, 'shane_kast_blue_A')
    pyp_file = os.path.join(configdir, 'shane_kast_blue_A.pypeit')
    assert os.path.isfile(pyp_file), 'PypeIt file not written.'

    # Try to run with -m and -o
    pargs = RunPypeIt.parse_args([pyp_file, '-o', '-m', '-r', configdir])
    RunPypeIt.main(pargs)

    # TODO: Add some code that will try to open the QA HTML and check that it
    # has the correct PNGs in it.

    # #########################################################
    # Test!!
    # Files exist
    spec1d_file = os.path.join(configdir, 'Science',
                               'spec1d_b27-J1217p3905_KASTb_20150520T045733.560.fits')
    assert os.path.isfile(spec1d_file), 'spec1d file missing'

    # spec1d
    specObjs = specobjs.SpecObjs.from_fitsfile(spec1d_file)
    
    # Check RMS
    assert specObjs[0].WAVE_RMS < 0.02  # difference must be less than 0.02 pixels

    # Flexure
    assert abs(-0.03 - specObjs[0].FLEX_SHIFT_TOTAL) < 0.1  # difference must be less than 0.1 pixels

    # Helio
    assert abs(specObjs[0].VEL_CORR - 0.9999261685542624) < 1.0E-10

    # Now re-use those master files
    pargs = RunPypeIt.parse_args([pyp_file, '-o', '-r', configdir])
    RunPypeIt.main(pargs)

    # Clean-up
    shutil.rmtree(outdir)




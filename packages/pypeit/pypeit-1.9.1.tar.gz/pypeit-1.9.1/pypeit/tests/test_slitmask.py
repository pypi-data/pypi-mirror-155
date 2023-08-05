"""
Module to run tests on PypeItPar classes
"""
import os
import numpy

import pytest
from IPython import embed

from astropy.io import fits

from pypeit.images import buildimage
from pypeit import edgetrace, slittrace, specobjs
from pypeit.spectrographs.keck_deimos import KeckDEIMOSSpectrograph
from pypeit.spectrographs.util import load_spectrograph
from pypeit.tests.tstutils import dev_suite_required, cooked_required, data_path


# Load flats files
def flat_files(instr='keck_deimos'):
    if instr == 'keck_deimos':
        return [os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA', 'keck_deimos', '830G_M_8500', ifile)
                for ifile in ['DE.20100913.57161.fits.gz', 'DE.20100913.57006.fits.gz']]
    elif instr == 'keck_mosfire':
        return [os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA', 'keck_mosfire', 'J_multi', ifile)
                    for ifile in ['m191015_0002.fits', 'm191015_0003.fits', 'm191015_0004.fits']]


@cooked_required
def test_assign_maskinfo_add_missing():
    instr_names = ['keck_deimos', 'keck_mosfire']
    for name in instr_names:
        # Spectrograph
        instrument = load_spectrograph(name)
        par = instrument.default_pypeit_par()
        # working only on detector 3 (det=3 for DEIMOS. For MOSFIRE does not matter because we have only one det)
        det = 3 if name == 'keck_deimos' else 1

        # Built trace image
        traceImage = buildimage.buildimage_fromlist(instrument, det,
                                                    par['calibrations']['traceframe'],
                                                    flat_files(instr=name))

        # load specific config parameters
        par = instrument.config_specific_par(traceImage.files[0])

        # Run edge trace
        edges = edgetrace.EdgeTraceSet(traceImage, instrument, par['calibrations']['slitedges'],
                                       auto=True, debug=False, show_stages=False,qa_path=None)

        slits = edges.get_slits()

        # Test that the maskfile is saved properly
        hdul = fits.open(slits.maskfile)
        det_par = instrument.get_detector_par(det, hdu=hdul)

        if name == 'keck_deimos':
            specobjs_file = os.path.join(os.getenv('PYPEIT_DEV'), 'Cooked', 'Science',
                                         'spec1d_DE.20100913.22358-CFHQS1_DEIMOS_20100913T061231.334.fits')
            sobjs = specobjs.SpecObjs.from_fitsfile(specobjs_file)
            # correct value
            slitid = sobjs[sobjs.MASKDEF_OBJNAME == 'ero89'].SLITID[0]
            true_maskdef_objname = sobjs[sobjs.SLITID == slitid].MASKDEF_OBJNAME[0]
            true_ra = round(sobjs[sobjs.SLITID == slitid].RA[0], 6)
            true_dec = round(sobjs[sobjs.SLITID == slitid].DEC[0], 6)
            true_spat_pixpos = round(sobjs[sobjs.MASKDEF_OBJNAME == 'ero884'].SPAT_PIXPOS[0])
            true_spat_pixpos_2 = round(sobjs[sobjs.MASKDEF_OBJNAME == 'ero191'].SPAT_PIXPOS[0])

        elif name == 'keck_mosfire':
            specobjs_file = os.path.join(os.getenv('PYPEIT_DEV'), 'Cooked', 'Science',
                                         'spec1d_m191014_0170-2M2228_12_MOSFIRE_20191014T095212.598.fits')
            sobjs = specobjs.SpecObjs.from_fitsfile(specobjs_file)
            # correct value
            slitid = sobjs[sobjs.MASKDEF_OBJNAME == '18'].SLITID[0]
            true_maskdef_objname = sobjs[sobjs.SLITID == slitid].MASKDEF_OBJNAME[0]
            true_ra = round(sobjs[sobjs.SLITID == slitid].RA[0], 6)
            true_dec = round(sobjs[sobjs.SLITID == slitid].DEC[0], 6)
            true_spat_pixpos = round(sobjs[sobjs.MASKDEF_OBJNAME == '7'].SPAT_PIXPOS[0])

        # Init at null and remove the force extraction
        idx_remove = []
        for i, sobj in enumerate(sobjs):
            if sobj.MASKDEF_EXTRACT:
                idx_remove.append(i)
            else:
                sobj.MASKDEF_ID = None
                sobj.MASKDEF_OBJNAME = None
                sobj.RA = None
                sobj.DEC = None
                sobj.MASKDEF_EXTRACT = None
        sobjs.remove_sobj(idx_remove)

        # get the dither offset if available
        if name == 'keck_deimos':
            dither_off = None

        elif name == 'keck_mosfire':
            dither_off = instrument.parse_dither_pattern([os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA',
                                                                       'keck_mosfire', 'J_multi',
                                                                       'm191014_0170.fits')])[2][0]

        # get object positions from slitmask design and slitmask offsets
        calib_slits = slittrace.get_maskdef_objpos_offset_alldets(sobjs, [slits], [None],
                                                                  [det_par['platescale']],
                                                                  par['calibrations']['slitedges']['det_buffer'],
                                                                  par['reduce']['slitmask'], dither_off=dither_off)
        # determine if slitmask offsets exist and compute an average offsets over all the detectors
        calib_slits = slittrace.average_maskdef_offset(calib_slits, det_par['platescale'], instrument.list_detectors())
        # slitmask design matching and add undetected objects
        sobjs = slittrace.assign_addobjs_alldets(sobjs, calib_slits, [None],
                                                 [det_par['platescale']], par['reduce']['slitmask'],
                                                 par['reduce']['findobj']['find_fwhm'])

        # Test
        if name == 'keck_deimos':
            # Check if recover the maskdef assignment
            assert sobjs[sobjs.SLITID == slitid].MASKDEF_OBJNAME[0] == true_maskdef_objname, 'Wrong DEIMOS MASKDEF_OBJNAME'
            assert round(sobjs[sobjs.SLITID == slitid].RA[0], 6) == true_ra, 'Wrong object DEIMOS RA'
            assert round(sobjs[sobjs.SLITID == slitid].DEC[0],6) == true_dec, 'Wrong object DEIMOS DEC'
            # Test that undetected objects are found at the correct location (the correct location is
            # verified by visual inspection)
            assert round(sobjs[sobjs.MASKDEF_OBJNAME == 'ero884'].SPAT_PIXPOS[0]) == true_spat_pixpos, \
                'Wrong object (ero884) location on the DEIMOS slit'
            assert round(sobjs[sobjs.MASKDEF_OBJNAME == 'ero191'].SPAT_PIXPOS[0]) == true_spat_pixpos_2, \
                'Wrong object (ero191) location on the DEIMOS slit'
        elif name == 'keck_mosfire':
            # Check if recover the maskdef assignment
            assert sobjs[sobjs.SLITID == slitid].MASKDEF_OBJNAME[0] == true_maskdef_objname, 'Wrong MOSFIRE MASKDEF_OBJNAME'
            assert round(sobjs[sobjs.SLITID == slitid].RA[0], 6) == true_ra, 'Wrong object MOSFIRE RA'
            assert round(sobjs[sobjs.SLITID == slitid].DEC[0],6) == true_dec, 'Wrong object MOSFIRE DEC'
            # Test that undetected object are found at the correct location (the correct location is
            # verified by visual inspection)
            assert round(sobjs[sobjs.MASKDEF_OBJNAME == '7'].SPAT_PIXPOS[0]) == true_spat_pixpos, \
                'Wrong object (7) location on the MOSFIRE slit'

        # Write sobjs
        sobjs.write_to_fits({}, data_path('tst_sobjs.fits'))
        os.remove(data_path('tst_sobjs.fits'))


# @cooked_required
# def test_dith_obs():
#     instr_names = ['keck_deimos']
#     flat_files = [os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA', 'keck_deimos',
#                               '830G_M_9000_dither', ifile)
#                     for ifile in ['DE.20141022.12107.fits', 'DE.20141022.12185.fits',
#                                   'DE.20141022.12263.fits']]
#     for name in instr_names:
#         # Spectrograph
#         instrument = load_spectrograph(name)
#         par = instrument.default_pypeit_par()
#         # working only on detector 3 (det=3 for DEIMOS. For MOSFIRE does not matter because we have only one det)
#         det = 1
#
#         # Built trace image
#         traceImage = buildimage.buildimage_fromlist(instrument, det,
#                                                     par['calibrations']['traceframe'], flat_files)
#
#         # load specific config parameters
#         par = instrument.config_specific_par(traceImage.files[0])
#         # set the slitmask parameter to use the alignment boxes to determine the slitmask_offset
#         par['reduce']['slitmask']['bright_maskdef_id'] = 918850
#
#         # Run edge trace
#         edges = edgetrace.EdgeTraceSet(traceImage, instrument, par['calibrations']['slitedges'],
#                                        auto=True, debug=False, show_stages=False, qa_path=None)
#         slits = edges.get_slits()
#
#         # Test that the maskfile is saved properly
#         hdul = fits.open(slits.maskfile)
#         det_par = instrument.get_detector_par(det, hdu=hdul)
#
#         if name == 'keck_deimos':
#             specobjs_file = os.path.join(os.getenv('PYPEIT_DEV'), 'Cooked', 'Science',
#                                          'spec1d_DE.20141021.35719-GOODSS_DEIMOS_20141021T095514.045.fits')
#
#         sobjs = specobjs.SpecObjs.from_fitsfile(specobjs_file)
#         # Init at null and remove the force extraction
#         idx_remove = []
#         for i, sobj in enumerate(sobjs):
#             if sobj.MASKDEF_EXTRACT:
#                 idx_remove.append(i)
#             else:
#                 sobj.MASKDEF_ID = None
#                 sobj.MASKDEF_OBJNAME = None
#                 sobj.RA = None
#                 sobj.DEC = None
#                 sobj.MASKDEF_EXTRACT = False
#         sobjs.remove_sobj(idx_remove)
#
#         if name == 'keck_deimos':
#             dither_off = None
#
#         # get object positions from slitmask design and slitmask offsets
#         calib_slits = slittrace.get_maskdef_objpos_offset_alldets(sobjs, [slits], [None],
#                                                                   [det_par['platescale']],
#                                                                   par['calibrations']['slitedges']['det_buffer'],
#                                                                   par['reduce']['slitmask'], dither_off=dither_off)
#         # determine if slitmask offsets exist and compute an average offsets over all the detectors
#         calib_slits = slittrace.average_maskdef_offset(calib_slits, det_par['platescale'], instrument.list_detectors())
#         # slitmask design matching and add undetected objects
#         sobjs = slittrace.assign_addobjs_alldets(sobjs, calib_slits, [None],
#                                                  [det_par['platescale']], par['reduce']['slitmask'],
#                                                  par['reduce']['findobj']['find_fwhm'])
#
#         # Test
#         if name == 'keck_deimos':
#             # Check if recover the maskdef assignment
#             assert sobjs[sobjs.SLITID == 1583].MASKDEF_OBJNAME == 'yg_21385', 'Wrong dithered DEIMOS MASKDEF_OBJNAME'
#             assert sobjs[sobjs.SLITID == 1583].RA == 53.11094583, 'Wrong object dithered DEIMOS RA'
#             assert sobjs[sobjs.SLITID == 1583].DEC == -27.72781111, 'Wrong object dithered DEIMOS DEC'
#             assert round(sobjs[sobjs.MASKDEF_OBJNAME == 'yg_21385'].SPAT_PIXPOS[0]) == 1578, \
#                 'Wrong object (yg_21385) location on the dithered DEIMOS slit'


@dev_suite_required
def test_deimosslitmask():
    f = os.path.join(os.environ['PYPEIT_DEV'], 'RAW_DATA', 'keck_deimos', '830G_M_8500',
                     'DE.20100913.22358.fits.gz')
    spec = KeckDEIMOSSpectrograph()
    spec.get_slitmask(f)
    assert spec.slitmask.nslits == 106, 'Incorrect number of slits read!'




import os

from IPython import embed

import numpy as np

from pypeit.images import buildimage
from pypeit.tests.tstutils import dev_suite_required
from pypeit.spectrographs.util import load_spectrograph
from pypeit.edgetrace import EdgeTraceSet


# This test check that `maskdesign_matching` method is properly assigning DEIMOS slit-mask design IDs
# to traced slits

# Load flats files
def flat_files(instr='keck_deimos'):
    if instr == 'keck_deimos':
        return [os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA', 'keck_deimos', '1200G_Cooper', ifile)
                for ifile in ['d0115_0023.fits.gz', 'd0115_0024.fits.gz', 'd0115_0025.fits.gz']]
    elif instr == 'keck_mosfire':
        return [os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA', 'keck_mosfire', 'J_multi', ifile)
                    for ifile in ['m191015_0002.fits', 'm191015_0003.fits', 'm191015_0004.fits']]


@dev_suite_required
def test_maskdef_id():
    instr_names = ['keck_deimos', 'keck_mosfire']
    for name in instr_names:
        # Load instrument
        instrument = load_spectrograph(name)
        par = instrument.default_pypeit_par()

        # working only on detector 1
        det=1

        # Built trace image
        traceImage = buildimage.buildimage_fromlist(instrument, det, par['calibrations']['traceframe'],
                                                    flat_files(instr=name))

        # load specific config parameters
        par = instrument.config_specific_par(traceImage.files[0])
        trace_par = par['calibrations']['slitedges']

        # Run edge trace
        edges = EdgeTraceSet(traceImage, instrument, trace_par, auto=True, debug=False,
                             show_stages=False,qa_path=None)

        slits = edges.get_slits()
        # Check that the `maskdef_id` assigned to the first and last slits is correct
        if name == 'keck_deimos':
            assert slits.maskdef_id[0] == 1098247, 'DEIMOS maskdef_id not found or wrong'
            assert slits.maskdef_id[-1] == 1098226, 'DEIMOS maskdef_id not found or wrong'
            # `maskdef_id` is the slit_id ("dSlitId") from the DEIMOS slit-mask design. If the matching is done
            # correctly these are the slit_id values that the first and last slits should have. These values are
            # coming from a reduction run with DEEP2 IDL-based pipeline.
        elif name == 'keck_mosfire':
            assert slits.maskdef_id[0] == 11, 'MOSFIRE maskdef_id not found or wrong'
            assert slits.maskdef_id[-1] == 1, 'MOSFIRE maskdef_id not found or wrong'
            # `maskdef_id` is the slit_id ("Slit_Number") from the MOSFIRE slit-mask design.
            # The expected values are determined by visual inspection.


@dev_suite_required
def test_add_missing_slits():
    instr_names = ['keck_deimos', 'keck_mosfire']
    for name in instr_names:
        # Load instrument
        instrument = load_spectrograph(name)
        par = instrument.default_pypeit_par()

        # working only on detector 1
        det = 1

        # Built trace image
        traceImage = buildimage.buildimage_fromlist(instrument, det,
                                                    par['calibrations']['traceframe'],
                                                    flat_files(instr=name))

        # load specific config parameters
        par = instrument.config_specific_par(traceImage.files[0])
        trace_par = par['calibrations']['slitedges']

        # Running the EdgeTraceSet steps (one-by-one)

        # Initialize EdgeTraceSet
        edges = EdgeTraceSet(traceImage, instrument, trace_par, auto=False, debug=False,
                             show_stages=False, qa_path=None)
        # Perform the initial edge detection and trace identification
        edges.initial_trace()
        # Initial trace can result in no edges found
        if not edges.is_empty:
            # Refine the locations of the trace using centroids of the
            # features in the Sobel-filtered image.
            edges.centroid_refine()
        # Initial trace can result in no edges found, or centroid
        # refinement could have removed all traces (via `check_traces`)
        if not edges.is_empty:
            # Fit the trace locations with a polynomial
            edges.fit_refine(debug=False)
            # Use the fits to determine if there are any discontinous
            # trace centroid measurements that are actually components
            # of the same slit edge
            edges.merge_traces(debug=False)
        # Check if the PCA decomposition is possible; this should catch
        # long slits
        if edges.par['auto_pca'] and edges.can_pca():
            # Use a PCA decomposition to parameterize the trace
            # functional forms
            edges.pca_refine(debug=False)
            # Use the results of the PCA decomposition to rectify and
            # detect peaks/troughs in the spectrally collapsed
            # Sobel-filtered image, then use those peaks to further
            # refine the edge traces
            edges.peak_refine(rebuild_pca=True, debug=False)

        # Check the values of the traces that will be removed
        if name == 'keck_deimos':
            # Two traces NOT from the same slit
            assert round(edges.edge_fit[edges.pca.reference_row, :][7]) == 458, \
                        'wrong DEIMOS left trace position'
            assert round(edges.edge_fit[edges.pca.reference_row, :][-11]) == 1736, \
                        'wrong DEIMOS right trace position'
            # Two traces from the same slit
            assert round(edges.edge_fit[edges.pca.reference_row, :][9]) == 496, \
                        'wrong DEIMOS left trace position'
            assert round(edges.edge_fit[edges.pca.reference_row, :][10]) == 561, \
                        'wrong DEIMOS right trace position'

            # Remove two left traces and two right traces
            # NOT form the same slit
            indx = np.zeros(edges.ntrace, dtype=bool)
            indx[7] = True
            indx[-11] = True
            # Form the same slit
            indx[9] = True
            indx[10] = True
        elif name == 'keck_mosfire':
            # Two traces NOT from the same slit
            assert round(edges.edge_fit[edges.pca.reference_row, :][0]) == 349, \
                        'wrong MOSFIRE left trace position'
            assert round(edges.edge_fit[edges.pca.reference_row, :][-1]) == 2032, \
                        'wrong MOSFIRE right trace position'
            # Two traces from the same slit
            assert round(edges.edge_fit[edges.pca.reference_row, :][9]) == 973, \
                        'wrong MOSFIRE left trace position'
            assert round(edges.edge_fit[edges.pca.reference_row, :][10]) == 1100, \
                        'wrong MOSFIRE right trace position'

            # Remove two left traces and two right traces
            # NOT form the same slit
            indx = np.zeros(edges.ntrace, dtype=bool)
            indx[0] = True
            indx[-1] = True
            # Form the same slit
            indx[9] = True
            indx[10] = True
        edges.remove_traces(edges.synced_selection(indx, mode='ignore'), rebuild_pca=True)

        # Run slitmask matching algorithm
        edges.maskdesign_matching(debug=False)

        # Sync left and right edges
        edges.sync()

        # Check the values of the traces that have been recovered
        if name == 'keck_deimos':
            # Two traces NOT from the same slit
            assert round(edges.edge_fit[edges.pca.reference_row, :][8]) == 459, \
                        'DEIMOS left trace position not recovered'
            assert round(edges.edge_fit[edges.pca.reference_row, :][-11]) == 1737, \
                        'DEIMOS right trace position not recovered'
            # Two traces from the same slit
            assert round(edges.edge_fit[edges.pca.reference_row, :][10]) == 497, \
                        'DEIMOS left trace position not recovered'
            assert round(edges.edge_fit[edges.pca.reference_row, :][11]) == 561, \
                        'DEIMOS right trace position not recovered'
            # These values are obtained by running PypeIt with the "adding missing traces" functionality.
            # These are within a few pixels (max 4 pixels) from their original values. The correctness of these values
            # was also tested by visual inspection of the EdgeTraceSet image.
        elif name == 'keck_mosfire':
            # Two traces NOT from the same slit
            assert round(edges.edge_fit[edges.pca.reference_row, :][1]) == 348, \
                        'MOSFIRE left trace position not recovered'
            assert round(edges.edge_fit[edges.pca.reference_row, :][-1]) == 2032, \
                        'MOSFIRE right trace position not recovered'
            # Two traces from the same slit
            assert round(edges.edge_fit[edges.pca.reference_row, :][10]) == 973, \
                        'MOSFIRE left trace position not recovered'
            assert round(edges.edge_fit[edges.pca.reference_row, :][11]) == 1101, \
                        'MOSFIRE right trace position not recovered'


@dev_suite_required
def test_overlapped_slits():
    # Load flats frames that have overlapping alignment slits.
    deimos_flats = [os.path.join(os.getenv('PYPEIT_DEV'), 'RAW_DATA', 'keck_deimos',
                                 '1200G_alignslit', ifile)
                        for ifile in ['DE.20110529.11732.fits', 'DE.20110529.11813.fits',
                                      'DE.20110529.11895.fits']]

    # Load instrument
    keck_deimos = load_spectrograph('keck_deimos')
    par = keck_deimos.default_pypeit_par()

    # working only on detector 2
    det = 2

    # Built trace image
    traceImage = buildimage.buildimage_fromlist(keck_deimos, det,
                                                par['calibrations']['traceframe'], deimos_flats)

    # load specific config parameters
    par = keck_deimos.config_specific_par(traceImage.files[0])
    trace_par = par['calibrations']['slitedges']

    # Run edge trace
    edges = EdgeTraceSet(traceImage, keck_deimos, trace_par, auto=True, debug=False,
                         show_stages=False, qa_path=None)

    slits = edges.get_slits()
    # Check that the total number of expected slits and the number of alignment slits are correct.
    assert len(slits.maskdef_designtab['MASKDEF_ID'].data) == 22, \
                'wrong number of slits for this detector'
    assert np.sum(slits.maskdef_designtab['ALIGN'].data) == 3, 'wrong number of alignment slits'
    # These number have been verified by visual inspection.



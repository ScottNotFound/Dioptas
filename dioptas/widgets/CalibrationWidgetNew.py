import os

from PyQt4 import QtGui, QtCore
from pyqtgraph import GraphicsLayoutWidget

from widgets.plot_widgets import MaskImgWidget, CalibrationCakeWidget
from widgets.plot_widgets import SpectrumWidget


class CalibrationWidgetNew(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(CalibrationWidgetNew, self).__init__(*args, **kwargs)

        self.calibration_display_widget = CalibrationDisplayWidget()
        self.calibration_control_widget = CalibrationControlWidget()

        self._main_splitter = QtGui.QSplitter()
        self._main_splitter.addWidget(self.calibration_display_widget)
        self._main_splitter.addWidget(self.calibration_control_widget)
        self._main_splitter.setStretchFactor(0, 2)

        self._layout = QtGui.QHBoxLayout()
        self._layout.addWidget(self._main_splitter)
        self.setLayout(self._layout)

        self.create_shortcuts()

    def create_shortcuts(self):
        self.load_img_btn = self.calibration_control_widget.load_img_btn
        self.load_next_img_btn = self.calibration_control_widget.load_next_img_btn
        self.load_previous_img_btn = self.calibration_control_widget.load_previous_img_btn
        self.filename_txt = self.calibration_control_widget.filename_txt

        self.save_calibration_btn = self.calibration_control_widget.save_calibration_btn
        self.load_calibration_btn = self.calibration_control_widget.load_calibration_btn

        self.integrate_btn = self.calibration_display_widget.calibrate_btn
        self.refine_btn = self.calibration_display_widget.refine_btn
        self.pos_lbl = self.calibration_display_widget.position_lbl

        self.tab_widget = self.calibration_display_widget.tab_widget
        self.ToolBox = self.calibration_control_widget.toolbox

        sv_gb = self.calibration_control_widget.calibration_parameters_widget.start_values_gb
        self.rotate_m90_btn = sv_gb.rotate_m90_btn
        self.rotate_p90_btn = sv_gb.rotate_p90_btn
        self.invert_horizontal_btn = sv_gb.flip_horizontal_btn
        self.invert_vertical_btn = sv_gb.flip_vertical_btn
        self.reset_transformations_btn = sv_gb.reset_transformations_btn
        self.calibrant_cb = sv_gb.calibrant_cb

        refinement_options_gb = self.calibration_control_widget.calibration_parameters_widget.refinement_options_gb
        self.use_mask_cb = refinement_options_gb.use_mask_cb
        self.mask_transparent_cb = refinement_options_gb.mask_transparent_cb
        self.options_automatic_refinement_cb = refinement_options_gb.automatic_refinement_cb
        self.options_num_rings_sb = refinement_options_gb.number_of_rings_sb
        self.options_peaksearch_algorithm_cb = refinement_options_gb.peak_search_algorithm_cb
        self.options_delta_tth_txt = refinement_options_gb.delta_tth_txt
        self.options_intensity_mean_factor_sb = refinement_options_gb.intensity_mean_factor_sb
        self.options_intensity_limit_txt = refinement_options_gb.intensity_limit_txt

        peak_selection_gb = self.calibration_control_widget.calibration_parameters_widget.peak_selection_gb
        self.peak_num_sb = peak_selection_gb.peak_num_sb
        self.automatic_peak_search_rb = peak_selection_gb.automatic_peak_search_rb
        self.select_peak_rb = peak_selection_gb.select_peak_rb
        self.search_size_sb = peak_selection_gb.search_size_sb
        self.automatic_peak_num_inc_cb = peak_selection_gb.automatic_peak_num_inc_cb
        self.clear_peaks_btn = peak_selection_gb.clear_peaks_btn

        self.f2_update_btn = self.calibration_control_widget.fit2d_parameters_widget.update_btn
        self.pf_update_btn = self.calibration_control_widget.pyfai_parameters_widget.update_btn

        self.f2_wavelength_cb = self.calibration_control_widget.fit2d_parameters_widget.wavelength_cb
        self.pf_wavelength_cb = self.calibration_control_widget.pyfai_parameters_widget.wavelength_cb
        self.sv_wavelength_cb = sv_gb.wavelength_cb

        self.f2_distance_cb = self.calibration_control_widget.fit2d_parameters_widget.distance_cb
        self.pf_distance_cb = self.calibration_control_widget.pyfai_parameters_widget.distance_cb
        self.sv_distance_cb = sv_gb.distance_cb

        self.img_view = self.calibration_display_widget.img_widget
        self.cake_view = self.calibration_display_widget.cake_widget
        self.spectrum_view = self.calibration_display_widget.spectrum_widget

    def set_img_filename(self, filename):
        self.filename_txt.setText(os.path.basename(filename))

    def set_start_values(self, start_values):
        sv_gb = self.calibration_control_widget.calibration_parameters_widget.start_values_gb
        sv_gb.distance_txt.setText('%.3f' % (start_values['dist'] * 1000))
        sv_gb.wavelength_txt.setText('%.6f' % (start_values['wavelength'] * 1e10))
        sv_gb.polarization_txt.setText('%.3f' % (start_values['polarization_factor']))
        sv_gb.pixel_height_txt.setText('%.0f' % (start_values['pixel_width'] * 1e6))
        sv_gb.pixel_width_txt.setText('%.0f' % (start_values['pixel_width'] * 1e6))
        return start_values

    def get_start_values(self):
        sv_gb = self.calibration_control_widget.calibration_parameters_widget.start_values_gb
        start_values = {'dist': float(sv_gb.distance_txt.text()) * 1e-3,
                        'wavelength': float(sv_gb.wavelength_txt.text()) * 1e-10,
                        'pixel_width': float(sv_gb.pixel_width_txt.text()) * 1e-6,
                        'pixel_height': float(sv_gb.pixel_height_txt.text()) * 1e-6,
                        'polarization_factor': float(sv_gb.polarization_txt.text())}
        return start_values

    def set_calibration_parameters(self, pyFAI_parameter, fit2d_parameter):
        self.set_pyFAI_parameter(pyFAI_parameter)
        self.set_fit2d_parameter(fit2d_parameter)

    def set_pyFAI_parameter(self, pyfai_parameter):
        pyfai_widget = self.calibration_control_widget.pyfai_parameters_widget
        pyfai_widget.distance_txt.setText('%.6f' % (pyfai_parameter['dist'] * 1000))
        pyfai_widget.poni1_txt.setText('%.6f' % (pyfai_parameter['poni1']))
        pyfai_widget.poni2_txt.setText('%.6f' % (pyfai_parameter['poni2']))
        pyfai_widget.rotation1_txt.setText('%.8f' % (pyfai_parameter['rot1']))
        pyfai_widget.rotation2_txt.setText('%.8f' % (pyfai_parameter['rot2']))
        pyfai_widget.rotation3_txt.setText('%.8f' % (pyfai_parameter['rot3']))
        pyfai_widget.wavelength_txt.setText('%.6f' % (pyfai_parameter['wavelength'] * 1e10))
        pyfai_widget.polarization_txt.setText('%.3f' % (pyfai_parameter['polarization_factor']))
        pyfai_widget.pixel_width_txt.setText('%.4f' % (pyfai_parameter['pixel1'] * 1e6))
        pyfai_widget.pixel_height_txt.setText('%.4f' % (pyfai_parameter['pixel2'] * 1e6))

    def get_pyFAI_parameter(self):
        pyfai_widget = self.calibration_control_widget.pyfai_parameters_widget
        pyfai_parameter = {'dist': float(pyfai_widget.distance_txt.text()) / 1000,
                           'poni1': float(pyfai_widget.poni1_txt.text()),
                           'poni2': float(pyfai_widget.poni2_txt.text()),
                           'rot1': float(pyfai_widget.rotation1_txt.text()),
                           'rot2': float(pyfai_widget.rotation2_txt.text()),
                           'rot3': float(pyfai_widget.rotation3_txt.text()),
                           'wavelength': float(pyfai_widget.wavelength_txt.text()) / 1e10,
                           'polarization_factor': float(pyfai_widget.polarization_txt.text()),
                           'pixel1': float(pyfai_widget.pixel_width_txt.text()) / 1e6,
                           'pixel2': float(pyfai_widget.pixel_height_txt.text()) / 1e6}
        return pyfai_parameter

    def set_fit2d_parameter(self, fit2d_parameter):
        fit2d_widget = self.calibration_control_widget.fit2d_parameters_widget
        fit2d_widget.distance_txt.setText('%.4f' % (fit2d_parameter['directDist']))
        fit2d_widget.center_x_txt.setText('%.3f' % (fit2d_parameter['centerX']))
        fit2d_widget.center_y_txt.setText('%.3f' % (fit2d_parameter['centerY']))
        fit2d_widget.tilt_txt.setText('%.6f' % (fit2d_parameter['tilt']))
        fit2d_widget.rotation_txt.setText('%.6f' % (fit2d_parameter['tiltPlanRotation']))
        fit2d_widget.wavelength_txt.setText('%.4f' % (fit2d_parameter['wavelength'] * 1e10))
        fit2d_widget.polarization_txt.setText('%.3f' % (fit2d_parameter['polarization_factor']))
        fit2d_widget.pixel_width_txt.setText('%.4f' % (fit2d_parameter['pixelX']))
        fit2d_widget.pixel_height_txt.setText('%.4f' % (fit2d_parameter['pixelY']))

    def get_fit2d_parameter(self):
        fit2d_widget = self.calibration_control_widget.fit2d_parameters_widget
        fit2d_parameter = {'directDist': float(fit2d_widget.distance_txt.text()),
                           'centerX': float(fit2d_widget.center_x_txt.text()),
                           'centerY': float(self.f2_center_y_txt.text()),
                           'tilt': float(fit2d_widget.tilt_txt.text()),
                           'tiltPlanRotation': float(fit2d_widget.rotation_txt.text()),
                           'wavelength': float(fit2d_widget.wavelength_txt.text()) / 1e10,
                           'polarization_factor': float(fit2d_widget.polarization_txt.text()),
                           'pixelX': float(fit2d_widget.pixel_width_txt.text()),
                           'pixelY': float(fit2d_widget.pixel_height_txt.text())}
        return fit2d_parameter


class CalibrationDisplayWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(CalibrationDisplayWidget, self).__init__(*args, **kwargs)

        self._layout = QtGui.QVBoxLayout()

        self.img_layout_widget = GraphicsLayoutWidget()
        self.cake_layout_widget = GraphicsLayoutWidget()
        self.spectrum_layout_widget = GraphicsLayoutWidget()

        self.img_widget = MaskImgWidget(self.img_layout_widget)
        self.cake_widget = CalibrationCakeWidget(self.cake_layout_widget)
        self.spectrum_widget = SpectrumWidget(self.spectrum_layout_widget)

        self.tab_widget = QtGui.QTabWidget()
        self.tab_widget.addTab(self.img_layout_widget, 'Image')
        self.tab_widget.addTab(self.cake_layout_widget, 'Cake')
        self.tab_widget.addTab(self.spectrum_layout_widget, 'Cake')
        self._layout.addWidget(self.tab_widget)

        self._status_layout = QtGui.QHBoxLayout()
        self.calibrate_btn = QtGui.QPushButton("Calibrate")
        self.refine_btn = QtGui.QPushButton("Refine")
        self.position_lbl = QtGui.QLabel("position_lbl")

        self._status_layout.addWidget(self.calibrate_btn)
        self._status_layout.addWidget(self.refine_btn)
        self._status_layout.addSpacerItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding,
                                                            QtGui.QSizePolicy.Minimum))
        self._status_layout.addWidget(self.position_lbl)
        self._layout.addLayout(self._status_layout)

        self.setLayout(self._layout)
        self.style_widgets()

    def style_widgets(self):
        self.calibrate_btn.setMinimumWidth(140)
        self.refine_btn.setMinimumWidth(140)


class CalibrationControlWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(CalibrationControlWidget, self).__init__(*args, **kwargs)

        self._layout = QtGui.QVBoxLayout()

        self._file_layout = QtGui.QHBoxLayout()
        self.load_img_btn = QtGui.QPushButton("Load File")
        self.load_previous_img_btn = QtGui.QPushButton("<")
        self.load_next_img_btn = QtGui.QPushButton(">")

        self._file_layout.addWidget(self.load_img_btn)
        self._file_layout.addWidget(self.load_previous_img_btn)
        self._file_layout.addWidget(self.load_next_img_btn)

        self._layout.addLayout(self._file_layout)

        self.filename_txt = QtGui.QLineEdit()
        self._layout.addWidget(self.filename_txt)

        self.toolbox = QtGui.QToolBox()
        self.calibration_parameters_widget = CalibrationParameterWidget()
        self.pyfai_parameters_widget = PyfaiParametersWidget()
        self.fit2d_parameters_widget = Fit2dParametersWidget()

        self.toolbox.addItem(self.calibration_parameters_widget, "Calibration Parameters")
        self.toolbox.addItem(self.pyfai_parameters_widget, 'pyFAI Parameters')
        self.toolbox.addItem(self.fit2d_parameters_widget, 'Fit2d Parameters')
        self._layout.addWidget(self.toolbox)

        self._bottom_layout = QtGui.QHBoxLayout()
        self.load_calibration_btn = QtGui.QPushButton('Load Calibration')
        self.save_calibration_btn = QtGui.QPushButton('Save Calibration')
        self._bottom_layout.addWidget(self.load_calibration_btn)
        self._bottom_layout.addWidget(self.save_calibration_btn)
        self._layout.addLayout(self._bottom_layout)

        self.setLayout(self._layout)


class CalibrationParameterWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(CalibrationParameterWidget, self).__init__(*args, **kwargs)

        self._layout = QtGui.QVBoxLayout()

        self.start_values_gb = StartValuesGroupBox()
        self.peak_selection_gb = PeakSelectionGroupBox()
        self.refinement_options_gb = RefinementOptionsGroupBox()

        self._layout.addWidget(self.start_values_gb)
        self._layout.addWidget(self.peak_selection_gb)
        self._layout.addWidget(self.refinement_options_gb)

        self.setLayout(self._layout)


class StartValuesGroupBox(QtGui.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(StartValuesGroupBox, self).__init__('Start values', *args, **kwargs)

        self._layout = QtGui.QVBoxLayout()

        self._grid_layout1 = QtGui.QGridLayout()

        self._grid_layout1.addWidget(LabelAlignRight('Distance:'), 0, 0)
        self.distance_txt = NumberTextField('200')
        self.distance_cb = QtGui.QCheckBox()
        self.distance_cb.setChecked(True)
        self._grid_layout1.addWidget(self.distance_txt, 0, 1)
        self._grid_layout1.addWidget(QtGui.QLabel('mm'), 0, 2)
        self._grid_layout1.addWidget(self.distance_cb, 0, 3)

        self._grid_layout1.addWidget(LabelAlignRight('Wavelength:'), 1, 0)
        self.wavelength_txt = NumberTextField('0.3344')
        self.wavelength_cb = QtGui.QCheckBox()
        self._grid_layout1.addWidget(self.wavelength_txt, 1, 1)
        self._grid_layout1.addWidget(QtGui.QLabel('A'), 1, 2)
        self._grid_layout1.addWidget(self.wavelength_cb, 1, 3)

        self._grid_layout1.addWidget(LabelAlignRight('Polarization:'), 2, 0)
        self.polarization_txt = NumberTextField('0.99')
        self._grid_layout1.addWidget(self.polarization_txt, 2, 1)

        self._grid_layout1.addWidget(LabelAlignRight('Pixel width:'), 3, 0)
        self.pixel_width_txt = NumberTextField('72')
        self._grid_layout1.addWidget(self.pixel_width_txt, 3, 1)
        self._grid_layout1.addWidget(QtGui.QLabel('um'))

        self._grid_layout1.addWidget(LabelAlignRight('Pixel height:'), 4, 0)
        self.pixel_height_txt = NumberTextField('72')
        self._grid_layout1.addWidget(self.pixel_height_txt, 4, 1)
        self._grid_layout1.addWidget(QtGui.QLabel('um'))

        self._grid_layout1.addWidget(LabelAlignRight('Calibrant:'), 5, 0)
        self.calibrant_cb = CleanLooksComboBox()
        self._grid_layout1.addWidget(self.calibrant_cb, 5, 1, 1, 2)

        self._grid_layout2 = QtGui.QGridLayout()

        self.rotate_p90_btn = QtGui.QPushButton('Rotate +90')
        self.rotate_m90_btn = QtGui.QPushButton('Rotate -90')
        self._grid_layout2.addWidget(self.rotate_p90_btn, 1, 0)
        self._grid_layout2.addWidget(self.rotate_m90_btn, 1, 1)

        self.flip_horizontal_btn = QtGui.QPushButton('Flip horizontal')
        self.flip_vertical_btn = QtGui.QPushButton('Flip vertical')
        self._grid_layout2.addWidget(self.flip_horizontal_btn, 2, 0)
        self._grid_layout2.addWidget(self.flip_vertical_btn, 2, 1)

        self.reset_transformations_btn = QtGui.QPushButton('Reset transformations')
        self._grid_layout2.addWidget(self.reset_transformations_btn, 3, 0, 1, 2)

        self._layout.addLayout(self._grid_layout1)
        self._layout.addLayout(self._grid_layout2)

        self.setLayout(self._layout)


class PeakSelectionGroupBox(QtGui.QGroupBox):
    def __init__(self):
        super(PeakSelectionGroupBox, self).__init__('Peak Selection')

        self._layout = QtGui.QGridLayout()
        self._layout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding,
                                               QtGui.QSizePolicy.Minimum), 0, 0)
        self._layout.addWidget(LabelAlignRight('Current Ring Number:'), 0, 1, 1, 2)
        self.peak_num_sb = SpinBoxAlignRight()
        self.peak_num_sb.setValue(1)
        self.peak_num_sb.setMinimum(1)
        self._layout.addWidget(self.peak_num_sb, 0, 3)

        self._layout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding,
                                               QtGui.QSizePolicy.Minimum), 1, 0, 1, 2)
        self.automatic_peak_num_inc_cb = QtGui.QCheckBox('automatic increase')
        self.automatic_peak_num_inc_cb.setChecked(True)
        self._layout.addWidget(self.automatic_peak_num_inc_cb, 1, 2, 1, 2)

        self.automatic_peak_search_rb = QtGui.QRadioButton('automatic peak search')
        self.automatic_peak_search_rb.setChecked(True)
        self.select_peak_rb = QtGui.QRadioButton('single peak search')
        self._layout.addWidget(self.automatic_peak_search_rb, 2, 0, 1, 4)
        self._layout.addWidget(self.select_peak_rb, 3, 0, 1, 4)

        self._layout.addWidget(LabelAlignRight('Search size:'), 4, 0)
        self.search_size_sb = SpinBoxAlignRight()
        self.search_size_sb.setValue(10)
        self.search_size_sb.setMaximumWidth(50)
        self._layout.addWidget(self.search_size_sb, 4, 1, 1, 2)
        self._layout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding,
                                               QtGui.QSizePolicy.Minimum), 4, 2, 1, 2)

        self.clear_peaks_btn = QtGui.QPushButton("Clear All Peaks")
        self._layout.addWidget(self.clear_peaks_btn, 5, 0, 1, 4)

        self.setLayout(self._layout)


class RefinementOptionsGroupBox(QtGui.QGroupBox):
    def __init__(self):
        super(RefinementOptionsGroupBox, self).__init__('Refinement Options')

        self._layout = QtGui.QGridLayout()

        self.automatic_refinement_cb = QtGui.QCheckBox('automatic refinement')
        self.automatic_refinement_cb.setChecked(True)
        self._layout.addWidget(self.automatic_refinement_cb, 0, 0, 1, 2)

        self.use_mask_cb = QtGui.QCheckBox('use mask')
        self._layout.addWidget(self.use_mask_cb, 1, 0)

        self.mask_transparent_cb = QtGui.QCheckBox('transparent')
        self._layout.addWidget(self.mask_transparent_cb, 1, 1)

        self._layout.addWidget(LabelAlignRight('Peak Search Algorithm:'), 2, 0)
        self.peak_search_algorithm_cb = CleanLooksComboBox()
        self.peak_search_algorithm_cb.addItems(['Massif', 'Blob'])
        self._layout.addWidget(self.peak_search_algorithm_cb, 2, 1)

        self._layout.addWidget(LabelAlignRight('Delta 2Th:'), 3, 0)
        self.delta_tth_txt = NumberTextField('0.1')
        self._layout.addWidget(self.delta_tth_txt, 3, 1)

        self._layout.addWidget(LabelAlignRight('Intensity Mean Factor:'), 4, 0)
        self.intensity_mean_factor_sb = DoubleSpinBoxAlignRight()
        self.intensity_mean_factor_sb.setValue(3.0)
        self._layout.addWidget(self.intensity_mean_factor_sb, 4, 1)

        self._layout.addWidget(LabelAlignRight('Intensity Limit:'), 5, 0)
        self.intensity_limit_txt = NumberTextField('55000')
        self._layout.addWidget(self.intensity_limit_txt, 5, 1)

        self._layout.addWidget(LabelAlignRight('Number of rings:'), 6, 0)
        self.number_of_rings_sb = SpinBoxAlignRight()
        self.number_of_rings_sb.setValue(15)
        self._layout.addWidget(self.number_of_rings_sb, 6, 1)

        self.setLayout(self._layout)


class PyfaiParametersWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(PyfaiParametersWidget, self).__init__(*args, **kwargs)

        self._layout = QtGui.QGridLayout()

        self._layout.addWidget(LabelAlignRight('Distance:'), 0, 0)
        self.distance_txt = NumberTextField()
        self.distance_cb = QtGui.QCheckBox()
        self.distance_cb.setChecked(True)
        self._layout.addWidget(self.distance_txt, 0, 1)
        self._layout.addWidget(QtGui.QLabel('mm'), 0, 2)
        self._layout.addWidget(self.distance_cb, 0, 3)

        self._layout.addWidget(LabelAlignRight('Wavelength:'), 1, 0)
        self.wavelength_txt = NumberTextField()
        self.wavelength_cb = QtGui.QCheckBox()
        self._layout.addWidget(self.wavelength_txt, 1, 1)
        self._layout.addWidget(QtGui.QLabel('A'), 1, 2)
        self._layout.addWidget(self.wavelength_cb, 1, 3)

        self._layout.addWidget(LabelAlignRight('Polarization:'), 2, 0)
        self.polarization_txt = NumberTextField()
        self._layout.addWidget(self.polarization_txt, 2, 1)

        self._layout.addWidget(LabelAlignRight('PONI:'), 3, 0)
        self.poni1_txt = NumberTextField()
        self._layout.addWidget(self.poni1_txt, 3, 1)
        self._layout.addWidget(QtGui.QLabel('m'), 3, 2)

        self.poni2_txt = NumberTextField()
        self._layout.addWidget(self.poni2_txt, 4, 1)
        self._layout.addWidget(QtGui.QLabel('m'), 4, 2)

        self._layout.addWidget(LabelAlignRight('Rotations'), 5, 0)
        self.rotation1_txt = NumberTextField()
        self.rotation2_txt = NumberTextField()
        self.rotation3_txt = NumberTextField()
        self._layout.addWidget(self.rotation1_txt, 5, 1)
        self._layout.addWidget(self.rotation2_txt, 6, 1)
        self._layout.addWidget(self.rotation3_txt, 7, 1)
        self._layout.addWidget(QtGui.QLabel('rad'), 5, 2)
        self._layout.addWidget(QtGui.QLabel('rad'), 6, 2)
        self._layout.addWidget(QtGui.QLabel('rad'), 7, 2)

        self._layout.addWidget(LabelAlignRight('Pixel width:'), 8, 0)
        self.pixel_width_txt = NumberTextField()
        self._layout.addWidget(self.pixel_width_txt, 8, 1)
        self._layout.addWidget(QtGui.QLabel('um'))

        self._layout.addWidget(LabelAlignRight('Pixel height:'), 9, 0)
        self.pixel_height_txt = NumberTextField()
        self._layout.addWidget(self.pixel_height_txt, 9, 1)
        self._layout.addWidget(QtGui.QLabel('um'))

        self.update_btn = QtGui.QPushButton('update')
        self._layout.addWidget(self.update_btn, 10, 0, 1, 4)

        self._layout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding),
                             11, 0, 1, 4)

        self.setLayout(self._layout)


class Fit2dParametersWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(Fit2dParametersWidget, self).__init__(*args, **kwargs)

        self._layout = QtGui.QGridLayout()

        self._layout.addWidget(LabelAlignRight('Distance:'), 0, 0)
        self.distance_txt = NumberTextField()
        self.distance_cb = QtGui.QCheckBox()
        self.distance_cb.setChecked(True)
        self._layout.addWidget(self.distance_txt, 0, 1)
        self._layout.addWidget(QtGui.QLabel('mm'), 0, 2)
        self._layout.addWidget(self.distance_cb, 0, 3)

        self._layout.addWidget(LabelAlignRight('Wavelength:'), 1, 0)
        self.wavelength_txt = NumberTextField()
        self.wavelength_cb = QtGui.QCheckBox()
        self._layout.addWidget(self.wavelength_txt, 1, 1)
        self._layout.addWidget(QtGui.QLabel('A'), 1, 2)
        self._layout.addWidget(self.wavelength_cb, 1, 3)

        self._layout.addWidget(LabelAlignRight('Polarization:'), 2, 0)
        self.polarization_txt = NumberTextField()
        self._layout.addWidget(self.polarization_txt, 2, 1)

        self._layout.addWidget(LabelAlignRight('Center X:'), 3, 0)
        self.center_x_txt = NumberTextField()
        self._layout.addWidget(self.center_x_txt, 3, 1)
        self._layout.addWidget(QtGui.QLabel('px'), 3, 2)

        self._layout.addWidget(LabelAlignRight('Center Y:'), 4, 0)
        self.center_y_txt = NumberTextField()
        self._layout.addWidget(self.center_y_txt, 4, 1)
        self._layout.addWidget(QtGui.QLabel('px'), 4, 2)

        self._layout.addWidget(LabelAlignRight('Rotation:'), 5, 0)
        self.rotation_txt = NumberTextField()
        self._layout.addWidget(self.rotation_txt, 5, 1)
        self._layout.addWidget(QtGui.QLabel('deg'), 5, 2)

        self._layout.addWidget(LabelAlignRight('Tilt:'), 6, 0)
        self.tilt_txt = NumberTextField()
        self._layout.addWidget(self.tilt_txt, 6, 1)
        self._layout.addWidget(QtGui.QLabel('deg'), 6, 2)

        self._layout.addWidget(LabelAlignRight('Pixel width:'), 8, 0)
        self.pixel_width_txt = NumberTextField()
        self._layout.addWidget(self.pixel_width_txt, 8, 1)
        self._layout.addWidget(QtGui.QLabel('um'))

        self._layout.addWidget(LabelAlignRight('Pixel height:'), 9, 0)
        self.pixel_height_txt = NumberTextField()
        self._layout.addWidget(self.pixel_height_txt, 9, 1)
        self._layout.addWidget(QtGui.QLabel('um'))

        self.update_btn = QtGui.QPushButton('update')
        self._layout.addWidget(self.update_btn, 10, 0, 1, 4)

        self._layout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding),
                             11, 0, 1, 4)

        self.setLayout(self._layout)


class NumberTextField(QtGui.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(NumberTextField, self).__init__(*args, **kwargs)
        self.setValidator(QtGui.QDoubleValidator())
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


class LabelAlignRight(QtGui.QLabel):
    def __init__(self, *args, **kwargs):
        super(LabelAlignRight, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


class CleanLooksComboBox(QtGui.QComboBox):
    cleanlooks = QtGui.QStyleFactory.create('cleanlooks')

    def __init__(self, *args, **kwargs):
        super(CleanLooksComboBox, self).__init__(*args, **kwargs)
        self.setStyle(CleanLooksComboBox.cleanlooks)


class SpinBoxAlignRight(QtGui.QSpinBox):
    def __init__(self, *args, **kwargs):
        super(SpinBoxAlignRight, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight)


class DoubleSpinBoxAlignRight(QtGui.QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        super(DoubleSpinBoxAlignRight, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = CalibrationWidgetNew()
    widget.show()
    widget.setWindowState(widget.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
    widget.activateWindow()
    widget.raise_()
    app.exec_()

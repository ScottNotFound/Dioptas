# -*- coding: utf-8 -*-
# Dioptas - GUI program for fast processing of 2D X-ray diffraction data
# Principal author: Clemens Prescher (clemens.prescher@gmail.com)
# Copyright (C) 2014-2019 GSECARS, University of Chicago, USA
# Copyright (C) 2015-2018 Institute for Geology and Mineralogy, University of Cologne, Germany
# Copyright (C) 2019 DESY, Hamburg, Germany
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ..utility import QtTest
import os
import gc

from mock import MagicMock
import numpy as np

from ..utility import click_button, enter_value_into_text_field
from ...controller.integration import JcpdsEditorController
from ...model.DioptasModel import DioptasModel
from ...widgets.integration import IntegrationWidget

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')
jcpds_path = os.path.join(data_path, 'jcpds')


class JcpdsEditorControllerTest(QtTest):
    # SETUP
    #######################
    def setUp(self) -> None:
        self.model = DioptasModel()
        self.model.calibration_model.is_calibrated = True
        self.model.calibration_model.pattern_geometry.wavelength = 0.31E-10
        self.model.calibration_model.integrate_1d = MagicMock(return_value=(self.model.calibration_model.tth,
                                                                            self.model.calibration_model.int))

        self.phase_model = self.model.phase_model

        self.widget = IntegrationWidget()

        self.controller = JcpdsEditorController(self.widget, self.model)
        self.model.pattern_model.load_pattern(os.path.join(data_path, 'pattern_001.xy'))

        self.jcpds_widget = self.controller.jcpds_widget
        self.phase_widget = self.widget.phase_widget

        self.load_phases()
        self.controller.active = True

        self.setup_selected_row(5)
        click_button(self.phase_widget.edit_btn)

    def tearDown(self) -> None:
        del self.controller
        del self.widget
        self.model.delete_configurations()
        del self.model
        gc.collect()

    # Utility Functions
    #######################
    def load_phase(self, filename):
        self.model.phase_model.add_jcpds(os.path.join(jcpds_path, filename))

    def load_phases(self):
        self.load_phase('ar.jcpds')
        self.load_phase('ag.jcpds')
        self.load_phase('au_Anderson.jcpds')
        self.load_phase('mo.jcpds')
        self.load_phase('pt.jcpds')
        self.load_phase('re.jcpds')

    def setup_selected_row(self, ind):
        self.phase_widget.get_selected_phase_row = MagicMock(return_value=ind)

    def send_phase_tw_select_signal(self, ind):
        self.phase_widget.phase_tw.currentCellChanged.emit(ind, 0, 0, 0)

    # Tests
    #######################
    def test_edit_button_shows_correct_phase(self):
        self.assertEqual(self.jcpds_widget.filename_txt.text(), self.phase_model.phases[5].filename)

    def test_selection_changed_shows_correct_phase(self):
        self.send_phase_tw_select_signal(3)
        self.assertEqual(self.jcpds_widget.filename_txt.text(), self.phase_model.phases[3].filename)

    def test_updating_the_gui_after_external_change(self):
        previous_a = self.jcpds_widget.lattice_eos_a_txt.text()
        self.phase_model.set_pressure(5, 20)
        self.assertNotEqual(previous_a, self.jcpds_widget.lattice_eos_a_txt.text())

    def test_updating_volume_after_changing_a(self):
        previous_volume = self.jcpds_widget.lattice_volume_txt.text()
        self.jcpds_widget.lattice_a_sb.setValue(3)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_volume_txt.text())

    def test_updating_volume_after_changing_c(self):
        previous_volume = self.jcpds_widget.lattice_volume_txt.text()
        self.jcpds_widget.lattice_c_sb.setValue(3)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_volume_txt.text())

    def test_updating_volume_after_changing_ca_ratio(self):
        previous_volume = self.jcpds_widget.lattice_volume_txt.text()
        self.jcpds_widget.lattice_c_sb.setValue(3)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_volume_txt.text())

    def test_updating_k0_parameter(self):
        self.phase_model.set_pressure(5, 30)
        previous_volume = self.jcpds_widget.lattice_eos_volume_txt.text()
        enter_value_into_text_field(self.jcpds_widget.eos_K_txt, 300)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_eos_volume_txt.text())

    def test_updating_kp_parameter(self):
        self.phase_model.set_pressure(5, 30)
        previous_volume = self.jcpds_widget.lattice_eos_volume_txt.text()
        enter_value_into_text_field(self.jcpds_widget.eos_Kp_txt, 5)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_eos_volume_txt.text())



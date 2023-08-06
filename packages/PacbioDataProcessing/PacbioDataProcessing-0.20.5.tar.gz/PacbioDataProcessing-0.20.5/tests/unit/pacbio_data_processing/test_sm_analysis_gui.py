#######################################################################
#
# Copyright (C) 2021, 2022 David Palao
#
# This file is part of PacBioDataProcessing.
#
#  PacBioDataProcessing is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PacBio data processing is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PacBioDataProcessing. If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import unittest
from unittest.mock import patch, MagicMock
import sys
from contextlib import contextmanager
from collections.abc import Iterator


from pacbio_data_processing.sm_analysis_gui import main_gui
from pacbio_data_processing.constants import (
    MISSING_GOOEY_ERROR_TEMPLATE, SM_ANALYSIS_GUI_EXE
)


@contextmanager
def replace_gui_module() -> Iterator[MagicMock]:
    mocked_gui_module = MagicMock()
    try:
        real_gui_module = sys.modules["pacbio_data_processing.ui.gui"]
    except KeyError:
        real_gui_module = None
    sys.modules["pacbio_data_processing.ui.gui"] = mocked_gui_module
    yield mocked_gui_module
    if real_gui_module is None:
        del sys.modules["pacbio_data_processing.ui.gui"]
    else:
        sys.modules["pacbio_data_processing.ui.gui"] = real_gui_module


@patch("pacbio_data_processing.sm_analysis_gui._main")
@patch("pacbio_data_processing.ui.gui.parse_input_sm_analysis")
class MainGUIFunctionTestCase(unittest.TestCase):
    def test_parses_cl(self, pparse_gui, pmain):
        main_gui()
        pparse_gui.assert_called_once_with()

    def test_calls_main(self, pparse_gui, pmain):
        main_gui()
        pmain.assert_called_once_with(pparse_gui.return_value)


class HighLevelErrorsTestCase(unittest.TestCase):
    def test_main_gui_does_not_crashes_if_exception(self):
        with replace_gui_module() as mgui:
            mgui.parse_input_sm_analysis.side_effect = Exception("jo ja")
            with self.assertLogs() as cm:
                main_gui()
            self.assertEqual(cm.output, ["CRITICAL:root:jo ja"])

    def test_gooey_module_missing(self):
        err_msg = "No module named 'gooey'"
        with replace_gui_module() as pgui:
            with self.assertLogs() as cm:
                with patch("builtins.__import__") as pimport:
                    pimport.side_effect = ModuleNotFoundError(
                        err_msg, name="gooey")
                    main_gui()
                self.assertEqual(
                    cm.output,
                    ["CRITICAL:root:"+MISSING_GOOEY_ERROR_TEMPLATE.format(
                        msg=err_msg, program=SM_ANALYSIS_GUI_EXE)
                     ]
                )
            pgui.parse_input_sm_analysis.assert_not_called()

    def test_other_module_missing(self):
        err_msg = "No module named 'guli'"
        with replace_gui_module() as pgui:
            with self.assertLogs() as cm:
                with patch("builtins.__import__") as pimport:
                    pimport.side_effect = ModuleNotFoundError(
                        err_msg, name="guli")
                    main_gui()
                self.assertEqual(
                    cm.output,
                    ["CRITICAL:root:No module named 'guli'"]
                )
            pgui.parse_input_sm_analysis.assert_not_called()

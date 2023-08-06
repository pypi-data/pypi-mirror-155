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

from .errors import high_level_handler, MissingGooeyError
from .sm_analysis import _main


@high_level_handler
def main_gui():
    """Entry point for ``sm-analysis-gui`` executable."""
    try:
        from .ui.gui import parse_input_sm_analysis
    except ModuleNotFoundError as e:
        if e.name == "gooey":
            raise MissingGooeyError(e.msg, name=e.name)
        else:
            raise
    config = parse_input_sm_analysis()
    _main(config)

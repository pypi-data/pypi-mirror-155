#######################################################################
#
# Copyright (C) 2021, 2022 David Palao
#
# This file is part of PacBio data processing.
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


import logging
from functools import wraps

from .constants import (
    EXIT_CODE_FAILURE, MISSING_GOOEY_ERROR_TEMPLATE, SM_ANALYSIS_GUI_EXE
)


class SMAPipelineError(Exception):
    ...


class MissingGooeyError(ModuleNotFoundError):
    def __str__(self):
        return MISSING_GOOEY_ERROR_TEMPLATE.format(
            msg=self.msg, program=SM_ANALYSIS_GUI_EXE
        )


def high_level_handler(func):
    @wraps(func)
    def func_wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.critical(str(e))
            return EXIT_CODE_FAILURE
    return func_wrapped

# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.AST.
#
# SENAITE.AST is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2020-2022 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from bika.lims.interfaces import IGuardAdapter
from bika.lims.interfaces import ISubmitted
from bika.lims.interfaces import IVerified
from senaite.ast import utils
from senaite.ast.config import DISK_CONTENT_KEY
from senaite.ast.config import ZONE_SIZE_KEY
from zope.interface import implementer


class BaseGuardAdapter(object):

    def __init__(self, context):
        self.context = context

    def guard(self, action):
        func_name = "guard_{}".format(action)
        func = getattr(self, func_name, None)
        if func:
            return func()

        # No guard intercept here
        return True


@implementer(IGuardAdapter)
class SampleGuardAdapter(BaseGuardAdapter):
    """AST-like analyses are set as 'Internal', but 'submit' and 'verify' guards
    from senaite.core dismiss internal analyses.
    "Final" analyses with AST category for each Microorganism and antibiotic
    are automatically created once the intermediate AST analyses are submitted
    (diameter zone, content, etc.).
    """

    def guard_submit(self):
        """Returns true when results for valid AST analyses have been submitted
        """
        # Get the valid AST-like analyses
        analyses = utils.get_ast_analyses(self.context)
        submitted = map(ISubmitted.providedBy, analyses)
        if all(submitted):
            # All AST-like analyses have been submitted
            return True

        return False

    def guard_verify(self):
        """Returns true if all valid AST analyses have been verified.
        """
        analyses = utils.get_ast_analyses(self.context)
        verified = map(IVerified.providedBy, analyses)
        if all(verified):
            # All AST-like analyses have been verified
            return True

        return False


@implementer(IGuardAdapter)
class AnalysisGuardAdapter(BaseGuardAdapter):
    """Guard for objects from IAnalysis type
    """

    def guard_submit(self):
        """AST-like analyses have antibiotics as interim fields. Do not allow
        the submission unless all interim field values are non-empty
        """
        if not utils.is_ast_analysis(self.context):
            # Not an AST analysis
            return True

        # Check that all interim fields have non-empty values
        keyword = self.context.getKeyword()
        for interim in self.context.getInterimFields():

            if utils.is_extrapolated_interim(interim):
                # Skip extrapolated interims
                continue

            if keyword in [ZONE_SIZE_KEY, DISK_CONTENT_KEY]:
                # Negative values are not permitted
                value = interim.get("value")
                value = api.to_float(value, default=-1)
                if value < 0:
                    return False

        # No empties
        return True

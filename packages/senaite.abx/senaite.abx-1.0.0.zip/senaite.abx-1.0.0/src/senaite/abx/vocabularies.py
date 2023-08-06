# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.ABX.
#
# SENAITE.ABX is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
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
from senaite.core.catalog import SETUP_CATALOG
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class AntibioticClassesVocabulary(object):
    """Vocabulary of pre-defined Antibiotic classes
    """

    def __call__(self, context):
        """Returns a SimpleVocabulary of antibiotic classes
        """
        query = {
            "portal_type": "AntibioticClass",
            "is_active": True,
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }
        items = []
        brains = api.search(query, SETUP_CATALOG)
        for brain in brains:
            uid = api.get_uid(brain)
            title = api.get_title(brain)
            items.append(SimpleTerm(uid, uid, title))

        return SimpleVocabulary(items)


AntibioticClassesVocabularyFactory = AntibioticClassesVocabulary()

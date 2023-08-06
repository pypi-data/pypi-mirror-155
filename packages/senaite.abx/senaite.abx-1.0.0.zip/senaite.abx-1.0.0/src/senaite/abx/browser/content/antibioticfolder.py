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

import collections

from bika.lims import _ as _c
from bika.lims import api
from bika.lims.utils import get_link_for
from plone.memoize import view
from senaite.abx import messageFactory as _
from senaite.app.listing import ListingView
from senaite.core.catalog import SETUP_CATALOG


class AntibioticFolderView(ListingView):
    """Antibiotics listing view
    """

    def __init__(self, context, request):
        super(AntibioticFolderView, self).__init__(context, request)

        self.catalog = SETUP_CATALOG

        self.contentFilter = {
            "portal_type": "Antibiotic",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }

        self.context_actions = {
            _c("Add"): {
                "url": "++add++Antibiotic",
                "icon": "add.png"
            }
        }

        self.show_select_column = True
        self.categories = []
        self.show_categories = True
        self.expand_all_categories = False

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _c("Title"),
                "index": "sortable_title"
            }),
            ("abbreviation", {
                "title": _("Abbreviation"),
            }),
            ("category", {
                "title": _("Class"),
            }),
            ("Description", {
                "title": _c("Description"),
                "index": "Description"
            }),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _c("Active"),
                "contentFilter": {"is_active": True},
                "transitions": [],
                "columns": self.columns.keys(),
            }, {
                "id": "inactive",
                "title": _c("Inactive"),
                "contentFilter": {'is_active': False},
                "transitions": [],
                "columns": self.columns.keys(),
            }, {
                "id": "all",
                "title": _c("All"),
                "contentFilter": {},
                "columns": self.columns.keys(),
            },
        ]

    @view.memoize
    def get_categories(self):
        """Returns a list of available categories
        """
        query = {
            "portal_type": "AntibioticClass",
            "sort_on": "sortable_title",
            "sort_order": "ascending"
        }
        brains = api.search(query)
        return map(api.get_title, brains)

    def update(self):
        """Update hook
        """
        # Group the items by category (AntibioticClass)
        self.categories = self.get_categories()
        super(AntibioticFolderView, self).update()

    def before_render(self):
        """Before template render hook
        """
        super(AntibioticFolderView, self).before_render()

    def folderitem(self, obj, item, index):
        """Service triggered each time an item is iterated in folderitems.
        The use of this service prevents the extra-loops in child objects.
        :obj: the instance of the class to be foldered
        :item: dict containing the properties of the object to be used by
            the template
        :index: current index of the item
        """
        obj = api.get_object(obj)
        antibiotic_class = obj.antibiotic_class
        item["replace"]["Title"] = get_link_for(obj)
        item["abbreviation"] = obj.abbreviation
        item["category"] = _("Other")
        if antibiotic_class:
            item["category"] = api.get_title(antibiotic_class)
            item["replace"]["category"] = get_link_for(antibiotic_class)
        return item

    def get_children_hook(self, parent_uid, child_uids=None):
        """Hook to get the children of an item
        """
        super(AntibioticFolderView, self).get_children_hook(
            parent_uid, child_uids=child_uids)

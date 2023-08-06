# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.MICROORGANISM.
#
# SENAITE.MICROORGANISM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
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
from senaite.app.listing import ListingView
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.p3compat import cmp
from senaite.microorganism import messageFactory as _
from senaite.microorganism.config import GRAM_STAIN_OPTIONS
from senaite.microorganism.config import SHAPE_OPTIONS


class MicroorganismFolderView(ListingView):
    """Microorganisms listing view
    """

    def __init__(self, context, request):
        super(MicroorganismFolderView, self).__init__(context, request)

        self.categories = []
        self.show_categories = True
        self.pagesize = 999999  # hide batching controls

        self.catalog = SETUP_CATALOG
        self.contentFilter = {
            "portal_type": "Microorganism",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }

        self.context_actions = {
            _c("Add"): {
                "url": "++add++Microorganism",
                "icon": "add.png"}
            }

        self.show_select_column = True

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _c("Title"),
                "index": "sortable_title"
            }),
            ("gram_stain", {
                "title": _("Gram stain")
            }),
            ("shape", {
                "title": _("Shape"),
            }),
            ("glass", {
                "title": _("GLASS"),
                "type": "boolean",
            }),
            ("mro", {
                "title": _("MRO"),
                "type": "boolean",
            }),
            ("mro_phenotype", {
                "title": _("MRO phenotype")
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

    def folderitem(self, obj, item, index):
        """Service triggered each time an item is iterated in folderitems.
        The use of this service prevents the extra-loops in child objects.
        :obj: the instance of the class to be foldered
        :item: dict containing the properties of the object to be used by
            the template
        :index: current index of the item
        """
        item["replace"]["Title"] = get_link_for(obj)

        obj = api.get_object(obj)
        item["gram_stain"] = self.get_gram_stain_title(obj.gram_stain)
        item["shape"] = self.get_shape_title(obj.shape)
        item["glass"] = obj.glass
        item["mro"] = obj.multi_resistant
        item["mro_phenotype"] = obj.mro_phenotype
        item["class"]["mro"] = "center"
        item["class"]["glass"] = "center"
        item["Description"] = obj.description

        # Group into categories
        self.categorize(obj, item)

        return item

    def categorize(self, obj, item):
        """Assigns the category to the item passed-in so the items of the
        listing are displayed in categories/groups
        """
        uncategorized = _("Uncategorized")

        def sort_category(a, b):
            # Uncategorized always comes first
            if a == uncategorized:
                return -1
            if b == uncategorized:
                return 1

            a = a.lower().strip()
            b = b.lower().strip()
            return cmp(a, b)

        # Get the category name
        category = self.get_category_title(obj, default=uncategorized)

        # Add the category if not yet in there
        if category not in self.categories:
            self.categories.append(category)

            # Sort the categories
            self.categories = sorted(self.categories, cmp=sort_category)

        item["category"] = category

    def get_category_title(self, microorganism, default=None):
        """Returns the category title of the microorganism passed-in
        """
        category = microorganism.category
        if category:
            category = category[0]
            return self.get_obj_title(category, default=default)
        return default

    @view.memoize
    def get_obj_title(self, obj_uid, default=None):
        if api.is_uid(obj_uid):
            obj = api.get_object_by_uid(obj_uid)
            return api.get_title(obj) or default
        return default

    @view.memoize
    def get_gram_stain_title(self, gram_stain_value):
        """Returns the title of the gram satin value passed-in
        """
        return dict(GRAM_STAIN_OPTIONS).get(gram_stain_value, "")

    @view.memoize
    def get_shape_title(self, shape_value):
        """Returns the title of the shape value passed-in
        """
        return dict(SHAPE_OPTIONS).get(shape_value, "")

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

from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.schema import UIDReferenceField
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidgetFactory
from senaite.microorganism import messageFactory as _
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IMicroorganismBehavior(model.Schema):

    gram_stain = schema.Choice(
        title=_(u"Gram stain"),
        vocabulary="senaite.microorganism.vocabularies.gram_stains",
        required=False,
    )

    shape = schema.Choice(
        title=_(u"Shape"),
        vocabulary="senaite.microorganism.vocabularies.shapes",
        required=False,
    )

    glass = schema.Bool(
        title=_(u"GLASS organism"),
        description=_(
            "Whether this is an infectious organism included in the Global "
            "Antimicrobial Resistance Surveillance System (GLASS) for the "
            "the collection, analysis and sharing of Antimicrobial Resistance "
            "(AMR) data at a global level"
        ),
        required=False,
    )

    multi_resistant = schema.Bool(
        title=_(u"MRO Organism"),
        description=_(
            "Whether this organism is considered multi resistant (MRO)",
        ),
        required=False,
    )

    mro_phenotype = schema.TextLine(
        title=_(u"MRO phenotype"),
        required=False,
    )

    category = UIDReferenceField(
        title=_(u"Category / Group"),
        description=_(
            u"The category or group this microorganism belongs to"
        ),
        allowed_types=("MicroorganismCategory", ),
        multi_valued=False,
        required=False,
    )

    directives.widget(
        "category",
        UIDReferenceWidgetFactory,
        catalog=SETUP_CATALOG,
        query={
            "portal_type": "MicroorganismCategory",
            "is_active": True,
            "sort_on": "title",
            "sort_order": "ascending",
        },
        display_template="<a href='${url}'>${title}</a>",
        columns=[
            {
                "name": "title",
                "width": "30",
                "align": "left",
                "label": _(u"Title"),
            }, {
                "name": "description",
                "width": "70",
                "align": "left",
                "label": _(u"Description"),
            },
        ],
        limit=15,
    )


@implementer(IMicroorganismBehavior)
@adapter(IDexterityContent)
class Microorganism(object):

    def __init__(self, context):
        self.context = context

    def _get_gram_stain(self):
        return getattr(self.context, "gram_stain")

    def _set_gram_stain(self, value):
        self.context.gram_stain = value

    gram_stain = property(_get_gram_stain, _set_gram_stain)

    def _get_shape(self):
        return getattr(self.context, "shape")

    def _set_shape(self, value):
        self.context.shape = value

    shape = property(_get_shape, _set_shape)

    def _get_glass(self):
        return getattr(self.context, "glass", False)

    def _set_glass(self, value):
        self.context.glass = value

    glass = property(_get_glass, _set_glass)

    def _get_multi_resistant(self):
        return getattr(self.context, "multi_resistant", False)

    def _set_multi_resistant(self, value):
        self.context.multi_resistant = value

    multi_resistant = property(_get_multi_resistant, _set_multi_resistant)

    def _get_mro_phenotype(self):
        return getattr(self.context, "mro_phenotype")

    def _set_mro_phenotype(self, value):
        self.context.mro_phenotype = value

    mro_phenotype = property(_get_mro_phenotype, _set_mro_phenotype)

    def _get_category(self):
        return getattr(self.context, "category")

    def _set_category(self, value):
        self.context.category = value

    category = property(_get_category, _set_category)

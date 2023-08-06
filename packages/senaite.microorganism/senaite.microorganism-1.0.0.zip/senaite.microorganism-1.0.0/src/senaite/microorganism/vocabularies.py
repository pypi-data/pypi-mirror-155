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

from senaite.microorganism.config import GRAM_STAIN_OPTIONS
from senaite.microorganism.config import SHAPE_OPTIONS
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class GramStainsVocabulary(object):
    """Vocabulary of pre-defined Gram Stains
    """

    def __call__(self, context):
        """Returns a SimpleVocabulary of gram stains
        """
        items = map(lambda g: SimpleTerm(g[0], title=g[1]), GRAM_STAIN_OPTIONS)
        return SimpleVocabulary(items)


GramStainsVocabularyFactory = GramStainsVocabulary()


@implementer(IVocabularyFactory)
class ShapesVocabulary(object):
    """Vocabulary of pre-defined Shapes
    """

    def __call__(self, context):
        """Returns a SimpleVocabulary of microorganism shapes
        """
        items = map(lambda g: SimpleTerm(g[0], title=g[1]), SHAPE_OPTIONS)
        return SimpleVocabulary(items)


ShapesVocabularyFactory = ShapesVocabulary()

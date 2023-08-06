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

from senaite.microorganism import messageFactory as _

# Gram stain options
# List of (value, title) tuples
GRAM_STAIN_OPTIONS = [
    ("gram+", _("Gram-positive")),
    ("gram-", _("Gram-negative")),
]

# Microorganism shape options
# List of (value, title) tuples
# Three basic shapes: coccus, rod or bacillus, and spiral.
SHAPE_OPTIONS = [
    # The cocci are spherical or oval bacteria
    ("coccus", _("Coccus")),
    # Cocci have one of several distinct arrangements based on their planes of
    # division: diplococci, staphylococci, streptococci, sarcina, tetrad
    ("coccus.diplococci", _("Diplococci")),
    ("coccus.staphylococci", _("Staphylococci")),
    ("coccus.streptococci", _("Streptococci")),
    ("coccus.sarcina", _("Sarcina")),
    ("coccus.tetrad", _("Tetrad")),

    # Bacilli (or rod) are rod-shaped bacteria
    ("rod", _("Rod")),
    # Bacilli all divide in one plane producing a bacillus, streptobacillus, or
    # coccobacillus arrangement
    ("rod.bacillus", _("Bacillus")),
    ("rod.streptobacilli", _("Streptobacilli")),
    ("rod.coccobacilli", _("Coccobacilli")),

    # Spirals come in one of three forms, a vibrio, a spirillum, or a spirochete
    ("spiral", _("Spiral")),
    ("spiral.vibrio", _("Vibrio")),
    ("spiral.spirillum", _("Spirillum"))
]

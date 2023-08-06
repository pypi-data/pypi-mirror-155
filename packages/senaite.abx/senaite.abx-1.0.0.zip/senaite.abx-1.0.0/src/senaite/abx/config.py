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

from senaite.abx import messageFactory as _

# List of default antibiotics classes to create on install
ANTIBIOTIC_CLASSES = [
    _("Aminoglycosides"),
    _("Carbapenems"),
    _("Cephalosporins"),
    _("Fluoroquinolones"),
    _("Macrolides"),
    _("Monobactams"),
    _("Penicillins"),
    _("Tetracyclines"),
    _("Other"),
]

# List of default antibiotics to create on install
# Tuples of (antibiotic name, antibiotic properties)
ANTIBIOTICS = [
    # Penicillins
    ("Penicillin", {
        "abbreviation": "P",
        "antibiotic_class": _("Penicillins")
    }),
    ("Oxacillin", {
        "abbreviation": "Ox",
        "antibiotic_class": _("Penicillins")
    }),
    ("Ampicillin", {
        "abbreviation": "Am",
        "antibiotic_class": _("Penicillins")
    }),
    ("Ampicillin Sulbactam", {
        "abbreviation": "Ams",
        "antibiotic_class": _("Penicillins")
    }),
    ("Piperacillin", {
        "abbreviation": "Pi",
        "antibiotic_class": _("Penicillins")
    }),

    # Cephalosporins
    ("Cefazolin", {
        "abbreviation": "Cfz",
        "antibiotic_class": _("Cephalosporins")
    }),
    ("Ceftriaxone", {
        "abbreviation": "Cax",
        "antibiotic_class": _("Cephalosporins")
    }),
    ("Cefepime", {
        "abbreviation": "Pime",
        "antibiotic_class": _("Cephalosporins")
    }),
    ("Cefuroxime", {
        "abbreviation": "Cxm",
        "antibiotic_class": _("Cephalosporins")
    }),
    ("Cefotaxime", {
        "abbreviation": "Cft",
        "antibiotic_class": _("Cephalosporins")
    }),
    ("Ceftazidime", {
        "abbreviation": "Caz",
        "antibiotic_class": _("Cephalosporins")
    }),

    # Fluoroquinolones
    ("Ciprofloxacin", {
        "abbreviation": "Cp",
        "antibiotic_class": _("Fluoroquinolones")
    }),
    ("Levofloxacin", {
        "abbreviation": "Levo",
        "antibiotic_class": _("Fluoroquinolones")
    }),
    ("Moxifloxacin", {
        "abbreviation": "Mox",
        "antibiotic_class": _("Fluoroquinolones")
    }),

    # Aminoglycosides
    ("Amikacin", {
        "abbreviation": "Amk",
        "antibiotic_class": _("Aminoglycosides")
    }),
    ("Gentamicin", {
        "abbreviation": "Gm",
        "antibiotic_class": _("Aminoglycosides")
    }),
    ("Tobramycin", {
        "abbreviation": "To",
        "antibiotic_class": _("Aminoglycosides")
    }),

    # Monobactams
    ("Aztreonam", {
        "abbreviation": "Azt",
        "antibiotic_class": _("Monobactams")
    }),
    # Carbapenems
    ("Ertapenem", {
        "abbreviation": "Ert",
        "antibiotic_class": _("Carbapenems")
    }),
    ("Imienem", {
        "abbreviation": "Imp",
        "antibiotic_class": _("Carbapenems")
    }),
    ("Meropenem", {
        "abbreviation": "Mer",
        "antibiotic_class": _("Carbapenems")
    }),

    # Macrolides
    ("Azithromycin", {
        "abbreviation": "Azi",
        "antibiotic_class": _("Macrolides")
    }),
    ("Clarithromycin", {
        "abbreviation": "Cla",
        "antibiotic_class": _("Macrolides")
    }),
    ("Erythromycin", {
        "abbreviation": "E",
        "antibiotic_class": _("Macrolides")
    }),
    ("Clindamycin", {
        "abbreviation": "Cdm",
        "antibiotic_class": _("Macrolides")
    }),

    # Other
    ("Vancomycin", {
        "abbreviation": "Va",
        "antibiotic_class": _("Other")
    }),
    ("Rifampin", {
        "abbreviation": "Rif",
        "antibiotic_class": _("Other")
    }),
    ("Linezolid", {
        "abbreviation": "Lzd",
        "antibiotic_class": _("Other")
    }),
    ("Tetracycline", {
        "abbreviation": "Te",
        "antibiotic_class": _("Other")
    }),
    ("Trimethoprim", {
        "abbreviation": "Ts",
        "antibiotic_class": _("Other")
    }),
]

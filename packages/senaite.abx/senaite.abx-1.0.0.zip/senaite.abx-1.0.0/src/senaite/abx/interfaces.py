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

from bika.lims.interfaces import IDoNotSupportSnapshots
from senaite.core.interfaces import IHideActionsMenu
from senaite.lims.interfaces import ISenaiteLIMS
from zope.interface import Interface


class ISenaiteABXLayer(ISenaiteLIMS):
    """Zope 3 browser Layer interface specific for senaite.abx
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """


class IAntibiotic(Interface):
    """Marker interface for Antibiotic content
    """


class IAntibioticClass(Interface):
    """Marker interface for AntibioticClass content
    """


class IAntibioticClassFolder(IHideActionsMenu, IDoNotSupportSnapshots):
    """Marker interface for AntibioticClassFolder content
    """


class IAntibioticFolder(IHideActionsMenu, IDoNotSupportSnapshots):
    """Marker interface for AntibioticFolder content
    """

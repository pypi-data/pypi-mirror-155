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
from plone.registry.interfaces import IRegistry
from senaite.abx import logger
from senaite.abx import PRODUCT_NAME
from senaite.abx import PROFILE_ID
from senaite.abx.config import ANTIBIOTIC_CLASSES
from senaite.abx.config import ANTIBIOTICS
from zope.component import getUtility

# Tuples of (folder_id, folder_name, type)
SETUP_FOLDERS = [
    ("antibiotic_classes", "Antibiotic classes", "AntibioticClassFolder"),
    ("antibiotics", "Antibiotics", "AntibioticFolder"),
]


def setup_handler(context):
    """Generic setup handler
    """
    if context.readDataFile("{}.txt".format(PRODUCT_NAME)) is None:
        return

    logger.info("{} setup handler [BEGIN]".format(PRODUCT_NAME.upper()))
    portal = context.getSite()

    # Setup folders (Antibotic folder, etc.)
    add_setup_folders(portal)

    # Configure visible navigation items
    setup_navigation_types(portal)

    # Setup initial data
    setup_antibiotic_classes(portal)
    #setup_antibiotics(portal)

    logger.info("{} setup handler [DONE]".format(PRODUCT_NAME.upper()))


def add_setup_folders(portal):
    """Adds the initial folders in setup
    """
    logger.info("Adding setup folders ...")

    setup = api.get_setup()
    pt = api.get_tool("portal_types")
    ti = pt.getTypeInfo(setup)

    # Disable content type filtering
    ti.filter_content_types = False

    for folder_id, folder_name, portal_type in SETUP_FOLDERS:
        if setup.get(folder_id) is None:
            logger.info("Adding folder: {}".format(folder_id))
            setup.invokeFactory(portal_type, folder_id, title=folder_name)

    # Enable content type filtering
    ti.filter_content_types = True

    logger.info("Adding setup folders [DONE]")


def setup_navigation_types(portal):
    """Add additional types for navigation
    """
    logger.info("Setup navigation types ...")
    registry = getUtility(IRegistry)
    key = "plone.displayed_types"
    display_types = registry.get(key, ())

    new_display_types = set(display_types)
    to_display = map(lambda f: f[2], SETUP_FOLDERS)
    new_display_types.update(to_display)
    registry[key] = tuple(new_display_types)
    logger.info("Setup navigation types [DONE]")


def setup_antibiotic_classes(portal):
    """Setup default antibiotic classes if do not exist yet
    """
    logger.info("Setup default antibiotic classes ...")

    # Get the titles of the existing classes first
    folder = api.get_setup().get("antibiotic_classes")
    existing = map(api.get_title, folder.objectValues())

    # Create the antibiotic classes
    for ac in ANTIBIOTIC_CLASSES:
        if ac in existing:
            logger.warn("Antibiotic class {} already exists [SKIP]".format(ac))
            continue

        logger.info("Adding antibiotic class: {}".format(ac))
        api.create(folder, "AntibioticClass", title=ac)

    # Don't know why yet, but after adding the antibiotic classes, the folder
    # looses the title
    folder.title = "Antibiotic classes"
    folder.reindexObject()

    logger.info("Setup default antibiotic classes [DONE]")


def setup_antibiotics(portal):
    """Setup default antibiotics if do not exist yet
    """
    logger.info("Setup default antibiotics ...")

    # Get the titles of the existing antibiotics first
    folder = api.get_setup().get("antibiotics")
    existing = map(api.get_title, folder.objectValues())

    def get_antibiotic_class(name):
        query = {
            "portal_type": "AntibioticClass",
            "title": name,
        }
        brains = api.search(query)
        if len(brains) == 1:
            return api.get_object(brains[0])
        return None

    # Create the antibiotic classes
    for name, props in ANTIBIOTICS:
        if name in existing:
            logger.warn("Antibiotic {} already exists [SKIP]".format(name))
            continue

        logger.info("Adding antibiotic: {}".format(name))

        # Get the antibiotic class by name
        a_class_name = props.get("antibiotic_class")
        a_class = get_antibiotic_class(a_class_name)
        if not a_class:
            logger.error("Antibiotic class missing: '{}' [SKIP]".format(
                a_class_name))
            continue

        obj = api.create(folder, "Antibiotic", title=name)
        obj.antibiotic_class = api.get_uid(a_class)
        obj.abbreviation = props.get("abbreviation")
        obj.reindexObject()

    # After adding the antibiotic, the folder looses the title
    folder.title = "Antibiotics"
    folder.reindexObject()
    logger.info("Setup default antibiotics [DONE]")


def pre_install(portal_setup):
    """Runs before the first import step of the *default* profile
    This handler is registered as a *pre_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} pre-install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)  # noqa
    portal = context.getSite()  # noqa

    logger.info("{} pre-install handler [DONE]".format(PRODUCT_NAME.upper()))


def post_install(portal_setup):
    """Runs after the last import step of the *default* profile
    This handler is registered as a *post_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)  # noqa
    portal = context.getSite()  # noqa

    logger.info("{} install handler [DONE]".format(PRODUCT_NAME.upper()))


def post_uninstall(portal_setup):
    """Runs after the last import step of the *uninstall* profile
    This handler is registered as a *post_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} uninstall handler [BEGIN]".format(PRODUCT_NAME.upper()))

    # https://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py
    profile_id = "profile-{}:uninstall".format(PRODUCT_NAME)
    context = portal_setup._getImportContext(profile_id)  # noqa
    portal = context.getSite()  # noqa

    logger.info("{} uninstall handler [DONE]".format(PRODUCT_NAME.upper()))

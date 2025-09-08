#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# translation_utils.py - Utilities for translation support
#
import gettext

# Configure the translation text domain for comm-ashyterm
gettext.textdomain("comm-layout-changer")

# Export _ directly as the translation function
_ = gettext.gettext

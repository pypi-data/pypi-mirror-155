# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

from typing import List

sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../arthurai/'))
sys.path.append(os.path.abspath("../sphinx_ext"))


# -- Project information -----------------------------------------------------

project = 'ArthurAI SDK'
copyright = '2022, ArthurAI'
author = 'ArthurAI'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              # note: autodoc has native typehint support now but result isn't as pretty and it mis-orders permissions
              'sphinx_autodoc_typehints',
              'autosummary_permissions']
              # DO NOT UNCOMMENT unless testing! our autosummary_permissions extension will setup regular autosummary
              # 'sphinx.ext.autosummary']

# these are the defaults but to be explicit
autosummary_generate = True
autosummary_imported_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# The light_logo and dark_logo properties take a file path relative to the _static folder
html_theme_options = {
    "light_logo": "images/light-mode-logo.svg",
    "dark_logo": "images/dark-mode-logo.svg",
    "dark_css_variables": {
        "color-brand-primary": "#AC37F6",
        "color-brand-content": "#AC37F6",
        "color-problematic": "#AC37F6",
    },
    "light_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#7C4DFF",
        "color-problematic": "#7C4DFF",
    },
    "sidebar_hide_name": True,

}

# Custom CSS file in case we want to add more styling
html_css_files = [
    'css/custom_styles.css'
]

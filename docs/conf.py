"""Sphinx configuration."""
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

# Project information
project = "django-htmx-tools"
copyright = "2025, Howie Weiner"
author = "Howie Weiner"

# The full version, including alpha/beta/rc tags
release = "0.1.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output options
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Autodoc settings
autodoc_member_order = "bersource"
autodoc_typehints = "description"

# Napoleon settings (for Google/NumPy style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": ("https://docs.djangoproject.com/en/stable/", "https://docs.djangoproject.com/en/stable/_objects/"),
}

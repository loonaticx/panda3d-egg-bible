# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Panda3D egg bible'
copyright = '2023, Loonatic'
author = 'Loonatic'

# release = '0.1'
# version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    # 'sphinx_gallery.gen_gallery'
    'myst_parser',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'pydata_sphinx_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# syntax highlighter
pygments_style = 'sphinx'

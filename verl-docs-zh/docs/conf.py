# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'verl 中文文档'
copyright = '2026, verl 中文文档（社区翻译，非官方）'
author = 'verl 中文文档翻译组'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []

# 中文界面
language = 'zh_CN'

# -- MyST Parser（支持 Markdown）----------------------------------------------

source_suffix = {
    '.md': 'markdown',
}

# 为标题自动生成锚点（支持中文锚点链接，深度 4 级）
myst_heading_anchors = 4

myst_enable_extensions = [
    'colon_fence',
    'tasklist',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = 'verl 中文文档'
html_show_sourcelink = False
html_show_sphinx = False

# ReadTheDocs 主题选项
html_theme_options = {
    'navigation_depth': 4,          # 左侧导航展开深度
    'collapse_navigation': False,   # 不折叠导航
    'sticky_navigation': True,      # 导航随页面滚动
    'titles_only': False,
    'logo_only': False,
}

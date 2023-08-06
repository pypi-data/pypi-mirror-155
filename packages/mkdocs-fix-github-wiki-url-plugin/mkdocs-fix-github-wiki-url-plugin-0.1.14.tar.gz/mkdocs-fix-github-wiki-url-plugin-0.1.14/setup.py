from setuptools import setup, find_packages

description = 'A mkdocs plugin that makes edit-this-page links work correctly for Github Wiki.'
long_description = description

with open("README.md", 'r') as f:
  long_description = f.read()

setup(
  name='mkdocs-fix-github-wiki-url-plugin',
  version='0.1.14',
  description=description,
  long_description=long_description,
  long_description_content_type='text/markdown',
  keywords='mkdocs',
  url='https://github.com/xiaoxiao921/mkdocs-fix-github-wiki-url-plugin',
  author='Quentin Escarbajal',
  author_email='xiaoxiao921@hotmail.fr',
  license='MIT',
  python_requires='>=3.6',
  install_requires=[
    'mkdocs>=1.1.0'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only'
  ],
  entry_points={
    'mkdocs.plugins': [
      'mkdocs-fix-github-wiki-url-plugin = mkdocs_fix_github_wiki_url_plugin.plugin:MkDocsFixGithubWikiUrlPlugin'
    ]
  }
)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ontorunner',
 'ontorunner.converters',
 'ontorunner.pipes',
 'ontorunner.post',
 'ontorunner.pre']

package_data = \
{'': ['*']}

install_requires = \
['CairoSVG>=2.5.2,<3.0.0',
 'OGER>=1.5,<2.0',
 'click>=8.1.3,<9.0.0',
 'dframcy>=0.1.6,<0.2.0',
 'kgx>=1.5.8,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scispacy==0.5.0',
 'six>=1.16.0,<2.0.0',
 'spacy>=3.2.0,<3.3.0',
 'textdistance[extras]>=4.2.2,<5.0.0']

entry_points = \
{'console_scripts': ['onto-util = ontorunner.pre.util:cli',
                     'ontoger = ontorunner.oger_module:cli',
                     'ontospacy = ontorunner.spacy_module:main']}

setup_kwargs = {
    'name': 'ontorunner',
    'version': '0.1.1',
    'description': 'This is a wrapper project around various entity recognition (NER) tools.',
    'long_description': '# ontoRunNER\n\nThis is a wrapper project around the following named entity recognition (NER) tools:\n - [OGER](https://github.com/OntoGene/OGER).\n - [spaCy](https://spacy.io)\n   - using [sciSpaCy](https://scispacy.apps.allenai.org) pipeline \n   namely the CRAFT corpus (`en_ner_craft_md`) used by default. Others can be used as listed [here](https://github.com/allenai/scispacy#available-models)\n\n## Documentation\n\n[ontoRunNER using Sphinx](https://monarch-initiative.github.io/ontorunner/index.html)\n',
    'author': 'Harshad Hegde',
    'author_email': 'hhegde@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

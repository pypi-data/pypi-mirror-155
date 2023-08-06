# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weighted_metapath2vec']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.1,<5.0.0',
 'gensim>=4.1,<5.0',
 'networkx>=2.8,<3.0',
 'scikit-learn>=1.0,<2.0']

setup_kwargs = {
    'name': 'weighted-metapath2vec',
    'version': '0.1.3',
    'description': 'A weighted alternative to metapath2vec for heterogenous graph embedding',
    'long_description': "# Weighted Metapath2vec\n\nWeighted is a Python package to embed heterogenous graph nodes using a weighted alternative of Metapath2vec technique. The embedding can be used for downstream machine learning tasks.\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\n## Installation\n\n```\npip install wmetapath2vec\n```\n\n## Usage\n\n```python\nfrom wmetapath2vec import WeightedMetapath2VecModel\n\n...  # Load a networkx graph as G\n\nmetapaths = [\n    ['Article', 'Author', 'Article'],\n    ['Author', 'Article', 'Author']\n]\n\nmodel = WeightedMetapath2VecModel(G,\n                                  metapaths,\n                                  walk_length=3,\n                                  n_walks_per_node=20,\n                                  embedding_dim=128)\n\nnode_embeddings = model.fit_transform()\n\n...  # downstream task\n```\n",
    'author': 'Morteza Ansarinia',
    'author_email': 'ansarinia@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/morteza/wmetapath2vec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)

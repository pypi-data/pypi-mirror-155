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
    'version': '0.1.4',
    'description': 'A weighted alternative to metapath2vec for heterogenous graph embedding',
    'long_description': "# Weighted-Metapath2Vec\n\n**Weighted-Metapath2Vec** is a Python package to embed heterogeneous graphs.\nThe algorithm uses a weighted alternative to Metapath2vec to compute the embeddings.\nThe embeddings can be used for downstream machine learning.\n\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\n## Installation\n\n```bash\npip install weighted-metapath2vec\n```\n\n## Usage\n\n```python\nfrom weighted_metapath2vec import WeightedMetapath2VecModel\n\n...  # Load a networkx graph as G\n\nmetapaths = [\n    ['Article', 'Author', 'Article'],\n    ['Author', 'Article', 'Author']\n]\n\nmodel = WeightedMetapath2VecModel(G,\n                                  metapaths,\n                                  walk_length=3,\n                                  n_walks_per_node=20,\n                                  embedding_dim=128)\n\nnode_embeddings = model.fit_transform()\n\n...  # downstream task\n```\n\n## Contributing\n\nUse GitHub to fork and submit pull requests.\n\n## License\n\nMIT License. See the [LICENSE](LICENSE) file.\n",
    'author': 'Morteza Ansarinia',
    'author_email': 'ansarinia@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/morteza/weighted-metapath2vec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)

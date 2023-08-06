# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neat_ml_schema', 'neat_ml_schema.src.neat_ml_schema.datamodel']

package_data = \
{'': ['*'],
 'neat_ml_schema': ['project/docs/*',
                    'project/docs/types/*',
                    'project/excel/*',
                    'project/graphql/*',
                    'project/jsonld/*',
                    'project/jsonschema/*',
                    'project/owl/*',
                    'project/prefixmap/*',
                    'project/protobuf/*',
                    'project/shacl/*',
                    'project/shex/*',
                    'project/sqlschema/*',
                    'src/data/examples/*',
                    'src/docs/*',
                    'src/schema/*']}

install_requires = \
['linkml-runtime>=1.1.24,<2.0.0', 'pytest>=7.1.2,<8.0.0', 'tox>=3.25.0,<4.0.0']

extras_require = \
{':extra == "docs"': ['linkml>=1.2.11,<2.0.0']}

setup_kwargs = {
    'name': 'neat-ml-schema',
    'version': '0.1.9',
    'description': 'A linkml based schema for the neat-ml project.',
    'long_description': '# Neat-ml schema\n\nNeat-ml schema defines the schema in the form of a [YAML file](https://github.com/Knowledge-Graph-Hub/neat-ml-schema/blob/main/neat_ml_schema/src/schema/neat_ml_schema.yaml) for data going into graph ML pipelines (specifically [NEAT](https://github.com/Knowledge-Graph-Hub/neat-ml)). This project itself is generated using the command `linkml-ws new` derived from the [linkML](https://github.com/linkml/linkml) project.\n\n[Documentation](https://knowledge-graph-hub.github.io/neat-ml-schema/)\n',
    'author': 'Harshad Hegde',
    'author_email': 'hhegde@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://knowledge-graph-hub.github.io/neat_ml_schema/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

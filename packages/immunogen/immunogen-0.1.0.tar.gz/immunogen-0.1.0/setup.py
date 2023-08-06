# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['immunogen',
 'immunogen.data',
 'immunogen.data.pickles',
 'immunogen.eplets',
 'immunogen.immunogenicity',
 'immunogen.utils']

package_data = \
{'': ['*'],
 'immunogen.data': ['class_ii_sequences/*',
                    'eplets/*',
                    'haplotype_frequencies/*']}

install_requires = \
['numpy>=1.22.4,<2.0.0', 'pandas>=1.4.0,<2.0.0', 'parameterized>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'immunogen',
    'version': '0.1.0',
    'description': 'ImmunoGen is the package for HLA and Immunogenicity computing with Python.',
    'long_description': 'Immunogenicity Utilities is the package for HLA and Immunogenicity computing with Python.\n\nIt provides:\n\n- low-to-high conversion\n\n- calculation of Type 1 and Type II AMS, EMS, and HMS\n\n    - both with DQ and without\n    - both with ABO consideration and without\n- useful eplet functions\n- and much more\n',
    'author': 'Robert C. Green II',
    'author_email': 'greenr@bgsu.edu',
    'maintainer': 'Michael Terry',
    'maintainer_email': 'mterry@bgsu.edu',
    'url': 'https://gitlab.com/immunogen/immunogen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.9',
}


setup(**setup_kwargs)

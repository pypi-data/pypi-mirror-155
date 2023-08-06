# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ezconda', 'ezconda.experimental', 'ezconda.files']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1',
 'importlib-metadata>=4.11.4,<5.0.0',
 'rich>=10.11.0',
 'tomlkit>=0.9.0',
 'typer[all]>=0.4.0']

entry_points = \
{'console_scripts': ['ezconda = ezconda.main:app']}

setup_kwargs = {
    'name': 'ezconda',
    'version': '0.7.0',
    'description': 'Create, Manage, Re-create conda environments & specifications with ease.',
    'long_description': '# EZconda\n\n![EZconda](https://github.com/SarthakJariwala/ezconda/blob/2945291bc9ef123cb52e9c6436906ac0728b0451/docs/logo.png)\n\n<p align="center">\n    <a href="https://github.com/SarthakJariwala/ezconda/actions?workflow=Tests">\n        <img src="https://github.com/SarthakJariwala/ezconda/workflows/Tests/badge.svg">\n    </a>\n    <a href="https://codecov.io/gh/SarthakJariwala/ezconda">\n        <img src="https://codecov.io/gh/SarthakJariwala/ezconda/branch/main/graph/badge.svg">\n    </a>\n    <a href="https://anaconda.org/conda-forge/ezconda">\n        <img alt="Conda (channel only)" src="https://img.shields.io/conda/vn/conda-forge/ezconda">\n    </a>\n    <a href="https://ezconda.sarthakjariwala.com">\n        <img src="https://github.com/SarthakJariwala/ezconda/workflows/Docs/badge.svg">\n    </a>\n</p>\n\n<p align="center">\n    <em><b>Create, Manage, Re-create</b> conda environments & specifications with ease.</em>\n</p>\n\n---\n\n**EZconda** is a command line interface application that helps practitioners create and manage `conda` environment and related specifications with ease.\n\n> It provides an easy to use higher level abstraction for creating and managing reproducible `conda` environments.\n\n## Key Features\n\n- **Environment Management** : Create and manage `conda` environments with ease.\n\n- **Specifications Management** : Add and remove packages from the <abbr title="commonly known as environment.yml file">specifications file</abbr> as you install & remove them.\n    \n    > _**No manual file edits! No exporting entire environments!**_\n\n- **Reproducible Environments** : Auto lock current environment state and re-create it exactly anywhere!\n\n- **Easy & Intuitive** : Intuitive commands and autocompletions by default.\n\n- **Fast & Reliable Environment Resolution** : Get fast and reliable environment solves by default.\n\n    > *EZconda* uses `mamba` by default, but you can easily switch between `mamba` and `conda`.\n\n- **Built-in Good Practices & Guardrails** : Enables the user to follow good practices, by default.\n\n## Requirements\n\n- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installation\n\n## Installation\n\nThe recommended way to install **EZconda** is using `conda` or `mamba` in the `base` environment : \n\n### Using `conda`: \n\n```console\n$ conda install ezconda -c conda-forge -n base\n```\n\n### Using `mamba`:\n\n```console\n$ mamba install ezconda -c conda-forge -n base\n```\n\n## A Minimal Example\n\n### Create a new environment\n\nCreate a new environment with `Python 3.9` installed -\n\n<div class="termy">\n\n```console\n$ ezconda create -n ds-proj python=3.9\n\n// Creates ds-proj with Python=3.9 installed\n```\n\n</div>\n\n**EZconda** creates the `conda` environment as well as a specifications file `ds-proj.yml` (named after the environment name) -\n\n```YAML title="ds-proj.yml" hl_lines="1 5" \nname: ds-proj\nchannel:\n    - defaults\ndependencies:\n    - python=3.9\n```\n\n### Install packages\n\nAs you install packages, the specifications file is also updated accordingly.\n\n<div class="termy">\n\n```console\n$ ezconda install -n ds-proj -c conda-forge numpy pandas scipy\n\n// Installs numpy, scipy, pandas from conda-forge channel\n```\n\n</div>\n\n```YAML title="ds-proj.yml" hl_lines="3 7-9" \nname: ds-proj\nchannel:\n    - conda-forge\n    - defaults\ndependencies:\n    - python=3.9\n    - numpy\n    - pandas\n    - scipy\n```\n\nThe `conda-forge` channel was also added to the specifications along with the packages.\n\n### Remove packages\n\nThe specifications file is also updated when you remove packages.\n\n<div class="termy">\n\n```console\n$ ezconda remove -n ds-proj pandas\n\n// Removes pandas from ds-proj\n```\n\n</div>\n\n```YAML title="ds-proj.yml" hl_lines="7 8" \nname: ds-proj\nchannel:\n    - conda-forge\n    - defaults\ndependencies:\n    - python=3.9\n    - numpy\n    - scipy\n```\n\n> Informed Package Removal:\n    If you try to remove a package that is a dependency for an installed package, **EZconda** will inform you before removing the package. See [docs](https://ezconda.sarthakjariwala.com/user_guide/remove_packages) for more details.\n\n### Sync environment with changes\n\nLet\'s say you are working with collaborators and they update the specifications file (`ds-proj.yml`) with a new dependency. Now, your local conda environment is out of sync with the new dependencies. \n\nTo bring it back in sync, you can use the `sync` command.\n\n<div class="termy">\n\n```console\n$ ezconda sync -n ds-proj --with specfile\n\n// Syncs ds-proj environment with new changes in specifications file (ds-proj.yml)\n```\n</div>\n\n> Sync changes:\n    Learn more about syncing environments in the [user guide](https://ezconda.sarthakjariwala.com/user_guide/sync_env).\n\n### Re-create environment\n\nAs you create, install and remove packages, in addition to the specifications file, **EZconda** also generates and maintains a lock file.\n\nYou can use this lock file to reproducibly re-create an environment.\n\n> Lock file:\n    You can learn more about [reproducible environments](https://ezconda.sarthakjariwala.com/design_decisions/reproducible_environments) and [lock file](https://ezconda.sarthakjariwala.com/design_decisions/lockfile) in docs.\n\n<div class="termy">\n\n```console\n$ ezconda create --file ds-proj-darwin-x86_64.lock\n\n// Creates a new environment \'ds-proj-darwin-x86_64.lock\'\n```\n</div>\n\n\n## Summary\n\nIn summary, **EZconda** provides an easy to use higher level abstraction for creating and managing reproducible `conda` environments.\n\nTo learn more, check out the [User Guide](https://ezconda.sarthakjariwala.com/user_guide/create_new_env)\n\n---\n\n## Contributing Guidelines\n\n<!-- TODO Add contributing guidelines -->\n\n### Run tests\n\n```bash\ndocker-compose up --build test\n```\n\n### Local iterative development\n\n```bash\ndocker-compose build dev && docker-compose run dev bash\n```',
    'author': 'Sarthak Jariwala',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

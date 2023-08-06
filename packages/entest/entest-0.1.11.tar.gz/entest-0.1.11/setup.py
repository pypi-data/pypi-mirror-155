# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entest']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['entest = entest.cli:main']}

setup_kwargs = {
    'name': 'entest',
    'version': '0.1.11',
    'description': 'Write dependent integration tests. See my pycon talk.',
    'long_description': '# Entest\nSee `tests/example.py`.\n\nTo have a test implicitly depend on all other tests use `run_last` flag. This is the case for teardown of critical resources for example users. To skip these tests use `--skip-teardown` or set `ENTEST_SKIP_TEARDOWN` environment variable.\n\nTo have all tests implicitly depend on a given test place it closer to the root of the graph.\nUse `setup_setup` to take advantage of `depends_on` default behavior. (i.e. for the first decorated function in a module `TEST_ROOT` is taken do be the previous test)\n\nTo have a test depend on another test NOT being run use `without` flag. This is usefull for testing error flows.\n\nOptionally install `rich` for nicer output.\n\n## Contributing\nPlease do not maintain a fork! Make a pull request and if it is not obviously bad I will merge it in a timely manner.\n\nI would like to change a lot of things structure-wise, but API will stay the same. In particular:\n- `depends_on` decorator with kwargs `previous`, `run_last` and `without`.\n- `STATUS` classificator. I see how it can be misused easily, but I will still ship this footgun.\n\n## Run tests\n```\nentest --graph\nentest\nentest --skip-teardown\nentest --env env_name tests/spam_users.py\n```\n',
    'author': 'Peteris Ratnieks',
    'author_email': 'peteris.ratnieks@zealid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/peteris-zealid/entest',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

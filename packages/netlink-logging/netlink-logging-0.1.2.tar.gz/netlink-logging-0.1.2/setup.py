# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logging']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'netlink-logging',
    'version': '0.1.2',
    'description': 'A wrapper around logging and logzero',
    'long_description': '# netlink-logging\n\n_Part of the NetLink Python Tools_\n\nA small wrapper around python logging and [logzero](https://logzero.readthedocs.io/en/latest/).\n\n## Features\n\n- Log to a logfile automatically (same name as the top-level script, `_input_` for console)\n- Additional levels:\n  - `TRACE` (`5`)\n  - `VERBOSE` (`15`)\n  - `SUCCESS` (`25`)\n- Timestamps are in UTC and use format `%Y-%m-%d %H:%M:%S`\n- Uncaught Exceptions are logged as `CRITICAL`\n\n## Installation\n\n```bash\npip install netlink-logging\n```\n\n## Usage\n\n```python\nfrom netlink.logging import logger \n\nlogger.trace(\'A TRACE entry.\')\nlogger.debug(\'A DEBUG entry.\')\nlogger.verbose(\'A VERBOSE entry.\')\nlogger.info(\'An INFO entry.\')\nlogger.success(\'A SUCCESS entry.\')\nlogger.warning(\'A WARNING entry.\')\nlogger.error(\'An ERROR entry.\')\nlogger.critical(\'A CRITICAL entry.\')\n```\n\nresults in\n\n``` \n[D 2022-02-32 26:27:28 <input>:…] A DEBUG entry.\n[V 2022-02-32 26:27:28 <input>:…] A VERBOSE entry.\n[I 2022-02-32 26:27:28 <input>:…] An INFO entry.\n[S 2022-02-32 26:27:28 <input>:…] A SUCCESS entry.\n[W 2022-02-32 26:27:28 <input>:…] A WARNING entry.\n[E 2022-02-32 26:27:28 <input>:…] An ERROR entry.\n[C 2022-02-32 26:27:28 <input>:…] A CRITICAL entry.\n```\n\n## Additional Methods\n\n### `set_file`\n\nUse `set_file` to change the file that is logged to:\n\n```\nlogger.set_file([filename, \n                    [formatter,] \n                    [mode,] \n                    [max_bytes,] \n                    [backup_count,] \n                    [encoding,] \n                    [log_level,] \n                    [disable_stderr_logger]])\n```\n\n#### Parameters\n\n- **filename** (optional, `str`)\n\n  Must be provided, if any other parameter is provided. If not provided, or set to `None` logging to file is disabled.\n\n- **formatter** (optional, `logging.Formatter`)\n  \n  Formatter to use for logging to file. Defaults to `[K time module:line number] (message`, where \n  - **K** is the first letter of the logging level\n  - **time** is `%Y-%m-%d %H:%M:%S` in UTC\n  - **module** and **line number show the location in code\n  - **message** as provided in call\n\n- **mode** (optional, `str`)\n\n  Mode to open the file with. Defaults to `a`.\n\n- **max_bytes** (optional, `int`)\n  \n   Size of the logfile when rollover should occur. If set to `0`, rollover never occurs. Defaults to `100 MB`. \n\n- **backup_count** (optional, `int`)\n\n  Number of backups to keep. If set to 0, rollover never occurs. Defaults to `5`.\n\n- **encoding** (optional, `str`)\n \n  Used to open the file with that encoding. Defaults to `utf-8`.\n\n- **log_level** (optional, `int`)\n\n  Set a custom logging level for the file logger. Defaults to the current logging level.\n\n- **disable_stderr_logger** (optional, `bool`)\n\n  Should the default stderr logger be disabled. Defaults to `False`.\n\n\n### `set_level`\n\nThe current logging level can be set without additional imports:\n\n```python\nfrom netlink.logging import logger\n\nlogger.set_level(ERROR)\n```\n\n\n## Roadmap\n\nAn additional feature that is considered would log **every** Exception raised.\n\n## License\n\n### MIT License\n\nCopyright (c) 2022 Bernhard Radermacher\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink-consulting/netlink-logging',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

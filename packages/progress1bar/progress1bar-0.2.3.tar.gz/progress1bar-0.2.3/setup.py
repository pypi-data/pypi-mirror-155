#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'progress1bar',
        version = '0.2.3',
        description = 'A simple ANSI-based progress bar',
        long_description = "# progress1bar #\n[![build](https://github.com/soda480/progress1bar/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/progress1bar/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/soda480/progress1bar/branch/main/graph/badge.svg?token=6zIZLnSJ0T)](https://codecov.io/gh/soda480/progress1bar)\n[![Code Grade](https://api.codiga.io/project/25921/status/svg)](https://app.codiga.io/public/project/25921/progress1bar/dashboard)\n[![complexity](https://img.shields.io/badge/complexity-Simple:%205-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/progress1bar.svg)](https://badge.fury.io/py/progress1bar)\n[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)\n\nA simple ANSI-based progress bar.\n\n## Installation\n```bash\npip install progress1bar\n```\n\n### `ProgressBar`\n\n```\nProgressBar(total=None, fill=None, regex=None, completed_message=None, clear_alias=False)\n```\n\n<details><summary>Documentation</summary>\n\n> `total` - An integer for the total number of items the progress bar will show that need to be completed.\n\n> `fill` - A dictionary whose key values are integers that dictate the number of leading zeros the progress bar should add to the `total` and `completed` values; this is optional and should be used to format the progress bar appearance. The supported key values are `max_total` and `max_completed`.\n\n> `regex` - A dictionary whose key values are regular expressions for `total`, `count` and `alias`. The regular expressions will be checked against the log messages intercepted from the executing function, if matched the value will be used to assign the attribute for the respective progress bar. The `total` and `count` key values are required, the `alias` key value is optional.\n\n> `completed_message` - A string to designate the message the progress bar should display when complete. Default is 'Processing complete'\n\n> `clear_alias` - A boolean to designate if the progress bar should clear the alias when complete.\n\n**Attributes**\n\n> `count` - An integer attribute to increment that designates the current count. When count reaches total the progress bar will show complete.\n\n> `alias` - A string attribute to set the alias of the progress bar.\n\n**Functions**\n\n> **reset()**\n>> Reset the progress bar so that it can be used again. It will maintain and show the number of times the progress bar has been used.\n\n</details>\n\n\n### Examples\n\nVarious [examples](https://github.com/soda480/progress1bar/tree/master/examples) are included to demonstrate the progress1bar package. To run the examples, build the Docker image and run the Docker container using the instructions described in the [Development](#development) section.\n\n#### [example1](https://github.com/soda480/progress1bar/tree/master/examples/example1.py)\n\nThe `ProgressBar` class is used to display function execution as a progress bar. Use it as a context manager, and simply set the `.total` and `.count` attributes accordingly. Here is an example:\n\n<details><summary>Code</summary>\n\n```Python\nimport time\nfrom progress1bar import ProgressBar\n\nwith ProgressBar(total=250) as pb:\n    for _ in range(pb.total):\n        pb.count += 1\n        # simulate work\n        time.sleep(.01)\n```\n\n</details>\n\n![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example1.gif)\n\n#### [example2](https://github.com/soda480/progress1bar/tree/master/examples/example2.py)\n\nConfigure `ProgressBar` to display the item that is currently being processd by setting the `alias` attribute, specify fill dictionary parameter to ensure the progress bar digits are displayed uniformly:\n\n<details><summary>Code</summary>\n\n```Python\nimport names\nfrom progress1bar import ProgressBar\n\nprint('Processing names...')\ncompleted_message = 'Done processing all names'\nfill = {'max_total': 999}\nwith ProgressBar(total=500, completed_message=completed_message, fill=fill, clear_alias=True) as pb:\n    for _ in range(pb.total):\n        pb.alias = names.get_full_name()\n        # simulate work\n        pb.count += 1\n```\n\n</details>\n\n![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example2.gif)\n\n#### [example3](https://github.com/soda480/progress1bar/tree/master/examples/example3.py)\n\nConfigure `ProgressBar` to use regular expressions to determine the `total`, `count` and `alias` attributes:\n\n<details><summary>Code</summary>\n\n```Python\nimport time\nimport random\nimport logging\nimport names\nfrom progress1bar import ProgressBar\n\nlogger = logging.getLogger(__name__)\n\nTOTAL_ITEMS = 325\n\ndef process_message(pb, message):\n    pb.match(message)\n    logger.debug(message)\n\nregex = {\n    'total': r'^processing total of (?P<value>\\d+)$',\n    'count': r'^processed .*$',\n    'alias': r'^processor is (?P<value>.*)$'\n}\nfill = {\n    'max_total': TOTAL_ITEMS\n}\nwith ProgressBar(regex=regex, fill=fill) as pb:\n    last_name = names.get_last_name()\n    process_message(pb, f'processor is {last_name}')\n    total = random.randint(50, TOTAL_ITEMS)\n    process_message(pb, f'processing total of {total}')\n    for _ in range(total):\n        process_message(pb, f'processed {names.get_full_name()}')\n        time.sleep(.01)\n```\n\n</details>\n\n![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example3.gif)\n\n#### [example4](https://github.com/soda480/progress1bar/tree/master/examples/example4.py)\n\nConfigure `ProgressBar` to show and reuse progress for several iterations:\n\n<details><summary>Code</summary>\n\n```Python\nimport time\nimport random\nimport names\nfrom progress1bar import ProgressBar\n\nTOTAL_ITEMS = 150\nTOTAL_NAMES = 7\n\nfill = {\n    'max_total': TOTAL_ITEMS,\n    'max_completed': TOTAL_NAMES\n}\nprint(f'This progress bar will execute {TOTAL_NAMES} iterations of varying counts and keep track of how many have been completed ...')\nwith ProgressBar(fill=fill) as pb:\n    total_names = 0\n    while True:\n        pb.alias = names.get_last_name()\n        pb.total = random.randint(50, TOTAL_ITEMS)\n        for _ in range(pb.total):\n            names.get_full_name()\n            pb.count += 1\n            time.sleep(.01)\n        total_names += 1  \n        if total_names == TOTAL_NAMES:\n            pb.alias = ''\n            break\n        pb.reset()\n```\n\n</details>\n\n![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example4.gif)\n\n## Development ##\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```sh\ndocker image build \\\n-t \\\nprogress1bar:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\nprogress1bar:latest \\\n/bin/bash\n```\n\nExecute the build:\n```sh\npyb -X\n```\n",
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/progress1bar',
        project_urls = {},

        scripts = [],
        packages = ['progress1bar'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'cursor',
            'colorama'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )

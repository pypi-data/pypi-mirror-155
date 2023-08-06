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
        name = 'mppbar',
        version = '0.1.1',
        description = 'A multi-processing enabled progress bar.',
        long_description = '# mppbar\n[![build](https://github.com/soda480/mppbar/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/mppbar/actions/workflows/main.yml)\n[![Code Grade](https://api.codiga.io/project/33815/status/svg)](https://app.codiga.io/public/project/33815/mppbar/dashboard)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/mppbar.svg)](https://badge.fury.io/py/mppbar)\n[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)\n\nThe mppbar module provides a convenient way to scale execution of a function across multiple input values by distributing the input across a number of background processes, it displays the execution status of each background process using a [progress bar](https://pypi.org/project/progress1bar/).\n\nThe MPpbar class is a subclass of [MPmq](https://pypi.org/project/mpmq/) and the primary benefit of using `mppbar` is that the function being scaled requires minimal modification (if at all) since the multiprocessing and progress bar are completely abstracted. The progress bar is initialized and updated through the interception and processing of the messages logged within the function. The log messages in the function must use f-string style formatting.\n\n\n### Installation\n```bash\npip install mppbar\n```\n\n### `MPpbar class`\n```\nMPpbar(function, process_data=None, shared_data=None, processes_to_start=None, regex=None, fill=None)\n```\n\n<details><summary>Documentation</summary>\n\n> `function` - The function to execute. It should accept two positional arguments; the first argument is the dictionary containing the input data for the respective process see `process_data` below, the second argument is the shared dictionary sent to all proceses see `shared_data` below.\n\n> `process_data` - A list of dictionaries where each dictionary describes the input data that will be sent to the respective process executing the function; the length of the list dictates the total number of processes that will be executed.\n\n> `shared_data` - A dictionary containing arbitrary data that will be sent to all processes.\n\n> `processes_to_start` - The number of processes to initially start; this represents the number of concurrent processes that will be running. If the total number of processes is greater than this number then the remaining processes will be queued and executed to ensure this concurrency is maintained. Defaults to the length of the `process_data` lsit.\n\n> `regex` - A dictionary whose key values are regular expressions for `total`, `count` and `alias`. The regular expressions will be checked against the log messages intercepted from the executing function, if matched the value will be used to assign the attribute for the respective progress bar. The `total` and `count` key values are required, the `alias` key value is optional.\n\n> `fill` - A dictionary whose key values are integers that dictate the number of leading zeros the progress bar should add to the `total`, `index` and `completed` values; this is optional and should be used to format the progress bar appearance. The supported key values are `max_total`, `max_index` and `max_completed`.\n\n> **execute(raise_if_error=False)**\n>> Start execution the process’s activity. If `raise_if_error` is set to True, an exception will be raised if the function encounters an error during execution.\n\n</details>\n\n### Examples\n\n#### [example1](https://github.com/soda480/mppbar/blob/main/examples/example1.py)\n\nDistribute work across multiple processes with all executing concurrently, each displays a progress bar showing its execution status.\n\n<details><summary>Code</summary>\n\n```Python\nimport time, random, logging\nimport names\nfrom mppbar import MPpbar\nlogger = logging.getLogger(__name__)\n\ndef do_work(data, *args):\n    # log our intentions - messages will be intercepted as designated by MPpbar regex\n    logger.debug(f\'processor is {names.get_last_name()}\')\n    total = data[\'total\']\n    logger.debug(f\'processing total of {total}\')\n    for index in range(total):\n        # simulae work by sleeping\n        time.sleep(random.choice([.1, .2, .4]))\n        logger.debug(f\'processed item {index}\')\n    return total\n\ndef main():\n    # designate 6 processes total - each getting a different total\n    process_data = [{\'total\': random.randint(8, 16)} for item in range(6)]\n    # supply regex to intercept and set values for total count and alias\n    regex = {\n        \'total\': r\'^processing total of (?P<value>\\d+)$\',\n        \'count\': r\'^processed item \\d+$\',\n        \'alias\': r\'^processor is (?P<value>.*)$\',\n    }\n    print(\'>> Processing items...\')\n    pbars =  MPpbar(function=do_work, process_data=process_data, regex=regex, timeout=1)\n    results = pbars.execute()\n    # add up totals from all processes\n    print(f">> {len(process_data)} workers processed a total of {sum(result for result in results)} items")\n\nif __name__ == \'__main__\':\n    main()\n```\n\n</details>\n\n![example1](https://raw.githubusercontent.com/soda480/mppbar/main/docs/images/example1.gif)\n\n#### [example2](https://github.com/soda480/mppbar/blob/main/examples/example2.py)\n\nDistribute work across multiple processes but only a subset are executing concurrently, each displays a progress bar showing its execution status. Useful if you can only afford to run a few processes concurrently.\n\n<details><summary>Code</summary>\n\n```Python\nimport time, random, logging\nimport names\nfrom mppbar import MPpbar\nlogger = logging.getLogger(__name__)\n\ndef do_work(data, *args):\n    # log our intentions - messages will be intercepted as designated by MPpbar regex\n    logger.debug(f\'processor is {names.get_last_name()}\')\n    total = data[\'total\']\n    logger.debug(f\'processing total of {total}\')\n    for index in range(total):\n        # simulae work by sleeping\n        time.sleep(random.choice([.1, .2, .4]))\n        logger.debug(f\'processed item {index}\')\n    return total\n\ndef main():\n    # designate 6 processes total - each getting a different total\n    process_data = [{\'total\': random.randint(8, 16)} for item in range(6)]\n    # supply regex to intercept and set values for total count and alias\n    regex = {\n        \'total\': r\'^processing total of (?P<value>\\d+)$\',\n        \'count\': r\'^processed item \\d+$\',\n        \'alias\': r\'^processor is (?P<value>.*)$\',\n    }\n    # designate fill factor for total - to make progress bar look nicer\n    fill = {\n        \'max_total\': 100\n    }\n    print(\'>> Processing items...\')\n    # set concurrency to 3 - max of 3 processes will be running at any given time\n    pbars =  MPpbar(function=do_work, process_data=process_data, regex=regex, fill=fill, processes_to_start=3, timeout=1)\n    results = pbars.execute()\n    # add up totals from all processes\n    print(f">> {len(process_data)} workers processed a total of {sum(result for result in results)} items")\n\nif __name__ == \'__main__\':\n    main()\n```\n\n</details>\n\n![example2](https://raw.githubusercontent.com/soda480/mppbar/main/docs/images/example2.gif)\n\n#### [example3](https://github.com/soda480/mppbar/blob/main/examples/example3.py)\n\nDistribute alot of work across a small set of processes using a thread-safe queue, each process gets work off the queue until there is no more work, all processes reuse a progress bar to show its execution status. Useful if you have alot of data to distribute across a small set of processes.\n\n<details><summary>Code</summary>\n\n```Python\nimport time, random, logging\nfrom multiprocessing import Queue\nfrom queue import Empty\nimport names\nfrom mppbar import MPpbar\nlogger = logging.getLogger(__name__)\n\ndef do_work(total):\n    # log our intentions - messages will be intercepted as designated by MPpbar regex\n    logger.debug(f\'processor is {names.get_last_name()}\')\n    logger.debug(f\'processing total of {total}\')\n    for index in range(total):\n        # simulae work by sleeping\n        time.sleep(random.choice([.001, .003, .005]))\n        logger.debug(f\'processed item {index}\')\n    return total\n\ndef prepare_queue():\n    # create queue to add all the work that needs to be done\n    queue = Queue()\n    for _ in range(100):\n        queue.put({\'total\': random.randint(40, 99)})\n    return queue\n\ndef run_q(data, *args):\n    queue = data[\'queue\']\n    result = 0\n    while True:\n        try:\n            # get work from queue\n            total = queue.get(timeout=1)[\'total\']\n            # process the work\n            result += do_work(total)\n            # this allows us to reset progress bar\n            logger.debug(\'reset-mppbar\')\n        except Empty:\n            logger.debug(\'reset-mppbar-complete\')\n            break\n    return result\n\ndef main():\n    queue = prepare_queue()\n    # designate 3 processes total - each getting reference to the queue\n    process_data = [{\'queue\': queue} for item in range(3)]\n    # supply regex to intercept and set values for total count and alias\n    regex = {\n        \'total\': r\'^processing total of (?P<value>\\d+)$\',\n        \'count\': r\'^processed item \\d+$\',\n        \'alias\': r\'^processor is (?P<value>.*)$\',\n    }\n    print(\'>> Processing items...\')\n    pbars =  MPpbar(function=run_q, process_data=process_data, regex=regex, timeout=1)\n    results = pbars.execute()\n    # add up totals from all processes\n    print(f">> {len(process_data)} workers processed a total of {sum(result for result in results)} items")\n\nif __name__ == \'__main__\':\n    main()\n```\n\n</details>\n\n![example3](https://raw.githubusercontent.com/soda480/mppbar/main/docs/images/example3.gif)\n\n\n### Development\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```sh\ndocker image build \\\n-t \\\nmppbar:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\nmppbar:latest \\\n/bin/bash\n```\n\nExecute the build:\n```sh\npyb -X\n```\n',
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

        url = 'https://github.com/soda480/mppbar',
        project_urls = {},

        scripts = [],
        packages = ['mppbar'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'mpmq==0.3.0',
            'cursor==1.3.5',
            'colorama==0.4.5',
            'progress1bar==0.2.2'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )

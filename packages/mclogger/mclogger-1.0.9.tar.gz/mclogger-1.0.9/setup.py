# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mclogger']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'coloredlogs>=15.0,<16.0', 'tailer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['mclogger = mclogger.__main__:main']}

setup_kwargs = {
    'name': 'mclogger',
    'version': '1.0.9',
    'description': 'MCLogger that shows log records on screen in color and in a log file',
    'long_description': '# MCLogger: Multi color logger to log to screen and file\n\n\n\n## MCLogger to log to file AND to the console\n\n### What problem does this solve?\nA challenge for web-server applications (e.g. such as Flask) is to decipher what\'s going on from a long logging window.  The standard loggers are all single color console test which you have to trawl through manually one by one.\n\nMCLogger helps to solve this by colorising the debug, info, warning, into different colors so that it is much easier to read.  The logger will output to both on screen and also a file\n\n### How does it do this?\nMCLogger builds on the logging library and adds console color libraries to add colors to debug, info, error, warning entries\n\n* DEBUG - blue\n* WARNING - yellow\n* ERROR - red\n* INFO - cyan\n\n### How to install?\nMCLogger is avaialble through PyPi and you may use pip:\n\n```\n\tpip install mclogger\n```\n\nOr, through git:\n```\n\tgit clone https://github.com/pub12/mclogger.git\n```\n\n\n\n### How to use the logger?\nThe logger is super easy to use.  You need to simply create an instance and add a file/filepath for the logfile\n\n```\nfrom mclogger import MCLogger\n\nfilename = \'log_file.txt\'\nlogger = MultiLogger(filename).getLogger()\n\nlogger.debug("hello world - debug")\nlogger.info("hello world - info")\nlogger.error("hello world - error")\nlogger.warning("hello world - warning")\n```\nOutput will be:\n![Output for mclogger](https://github.com/pub12/mclogger/blob/master/readme/mclogger.png)\n\n### Class Methods overview\n\n- #### getLogger(*filename*):\n\tGenerates the log instance which can be called with .debug(*message*); .info(*message*); .error(*message*); .info(*message*) which will be displayed in color format.\n\n\tFormat of the output message will be: \n\t\t"`<current server timestamp> [<Filename and line number - function name()>] [<DEBUG | INFO | WARN | ERROR >] - < Message >`"\n\n\t- *filename* - filename with optional relative of optional filepath - e.g. `temp/log_file.txt`\n\n- #### read_log_file(*last_n_rows = 20*):\n\tReturn in an array the `last_n_rows` in an array in the order listed within the file.  This will include the color codes for the message\n\n\t- *last_n_rows* - Number of lines to read\n\n- #### read_log_file_as_text(*last_n_rows = 20*):\n\tReturn in an array the `last_n_rows` in an array in the order listed within the file.  This will have color codes removed\n\n\t- *last_n_rows* - Number of lines to read',
    'author': 'Pubs Abayasiri',
    'author_email': 'pubudu.abayasiri@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pubs12/mlogger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)

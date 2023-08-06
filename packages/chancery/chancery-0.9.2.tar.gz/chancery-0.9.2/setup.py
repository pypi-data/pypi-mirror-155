# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chancery']

package_data = \
{'': ['*']}

install_requires = \
['needly>=2.5.61,<3.0.0']

entry_points = \
{'console_scripts': ['chancery = chancery.chancery:main']}

setup_kwargs = {
    'name': 'chancery',
    'version': '0.9.2',
    'description': 'Chancery is a simple text editor with predefined openQA snippets.',
    'long_description': "Chancery\n########\n\n**Chancery** is a very simple text editor for `openQA <https://open.qa>`_, i.e. allows to type text, save and open files. However, its main purpose is to speed up the development of openQA test scripts so it does not specialize in text typing in the first place. Its main strength is that it comes with a library of openQA command snippets that you can quickly insert using the *menu items* or *keyboard shortcuts*.   \n\nThe current version (0.9) offers almost all snippets that are most frequently used in Fedora openQA scripts. The future versions will provide more and more snippets until the whole openQA `TestApi <http://open.qa/api/testapi/>`_ is covered. If you are new to openQA scripting, you might want to read the `openQA TestApi <http://open.qa/api/testapi/>`_ to understand, how specific methods (snippets) work and what you can expect from them. \n\nHow to use the application\n==========================\n\n* Type in the text area.\n* Insert snippets at a cursor position using **Quick actions**, **Menu**, or **keyboard shortcuts**.\n\nHow to start with openQA scripting\n==================================\n\n1. Each script needs to be enclosed in the `sub {}` structure, or it will not work in the openQA engine. The **Create file layout** button in the **Quick actions** will insert the snippet for you.\n\n2. Each script needs to have a subroutine called `test_flags` to set test flags for the script. The **Set test flags** button in the **Quick actions** will insert the snippet for you with all the test flags switched off. To switch on the flag, change its value to `1`. Note, that some of the test flags contradict each other, such as `no_rollback` or `always_rollback` so pay attention to the settings. You can also delete the unused flags for better readability.\n\nHow to work with snippets\n=========================\n\nObligatory arguments\n--------------------\nUsually, the methods use **obligatory arguments**, further called *arguments*. These are presented as **perl variables**, such as `$needlematch` or `$text`. \nYou can either define these variables previously, or replace the references with expected values.\n\nNon-obligatory arguments\n------------------------\n\nThe testAPI methods use various configuration options. When these are left out, the method then works with the default settings, which is mostly fine.\nThe snippets, however, provide all such configuration variables using the default values so they can be modified to suit the users' needs without having to consult the documentation all the time. If you *do not need to alter an option* you can leave it as is, or delete it from the snippet for better readability. \n\nHow to report bugs\n==================\n\nIf you think you have found a bug, report it in the project's issues.\n",
    'author': 'Lukáš Růžička',
    'author_email': 'lruzicka@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

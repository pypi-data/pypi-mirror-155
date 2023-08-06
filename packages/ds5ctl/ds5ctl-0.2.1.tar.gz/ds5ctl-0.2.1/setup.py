# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ds5ctl']

package_data = \
{'': ['*']}

install_requires = \
['dearpygui>=1.6.2,<2.0.0',
 'hidapi>=0.11.2,<0.12.0',
 'mopyx>=1.1.1,<2.0.0',
 'pytest>=7.0,<8.0']

entry_points = \
{'console_scripts': ['ds5ctl = ds5ctl.gui:run_gui']}

setup_kwargs = {
    'name': 'ds5ctl',
    'version': '0.2.1',
    'description': 'Some reference implementations of DS5-related I/O',
    'long_description': '# ds5ctl\n\nA GUI tool for configuring a DualSense 5 controller (currently only supports direct USB connection)\n\n![Example of GUI](https://user-images.githubusercontent.com/33840/174457044-a3320871-bc76-4f20-9f62-ef854517712e.png)\n\n![Example recording after sending to controller](https://user-images.githubusercontent.com/33840/174456917-81cdcd86-f37e-483c-976f-c6381d1b6469.gif)\n\n\n# Installation\n\n```shell\npip install ds5ctl\n```\n\n\n# Usage\n\nTo run the GUI:\n\n```shell\nds5ctl\n\n# Or\npython -m ds5ctl\n```\n\nTo send commands to the controller, press the Send button at the bottom. This will emit all currently-configured controls. Though all sliders and controls are shown (such as Haptics Left/Right or Lightbar Colour), emitting them will have no effect on the controller unless the appropriate Control flags are also checked.\n\nTo send haptics to the device, ensure `DS5_MODE` Operating Mode is checked, and modify the Haptics sliders. The controller appears to spin the motors for 5 seconds before desisting automatically.\n\nTo change the adaptive trigger effects, ensure `DS5_MODE` Operating Mode is checked, as well as `TRIGGER_EFFECTS_RIGHT` and/or `TRIGGER_EFFECTS_LEFT` (depending on which sides you wish to modify), then using the trigger effects panes to modify the effect.\n',
    'author': 'Zach Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theY4Kman/ds5ctl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

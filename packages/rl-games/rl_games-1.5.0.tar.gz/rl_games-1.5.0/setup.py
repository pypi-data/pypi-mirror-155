# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rl_games',
 'rl_games.algos_torch',
 'rl_games.common',
 'rl_games.common.layers',
 'rl_games.common.transforms',
 'rl_games.distributed',
 'rl_games.envs',
 'rl_games.envs.diambra',
 'rl_games.envs.test',
 'rl_games.interfaces',
 'rl_games.networks']

package_data = \
{'': ['*'],
 'rl_games': ['configs/*',
              'configs/atari/*',
              'configs/brax/*',
              'configs/dm_control/*',
              'configs/ma/*',
              'configs/minigrid/*',
              'configs/mujoco/*',
              'configs/openai/*',
              'configs/procgen/*',
              'configs/smac/*',
              'configs/smac/runs/*',
              'configs/test/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'gym[classic_control]>=0.23.0,<0.24.0',
 'opencv-python>=4.5.5,<5.0.0',
 'psutil>=5.9.0,<6.0.0',
 'ray>=1.11.0,<2.0.0',
 'setproctitle>=1.2.2,<2.0.0',
 'tensorboard>=2.8.0,<3.0.0',
 'tensorboardX>=2.5,<3.0',
 'wandb>=0.12.11,<0.13.0']

extras_require = \
{'atari': ['ale-py>=0.7,<0.8', 'AutoROM[accept-rom-license]>=0.4.2,<0.5.0'],
 'brax': ['brax>=0.0.13,<0.0.14', 'jax>=0.3.13,<0.4.0'],
 'envpool': ['envpool>=0.6.1,<0.7.0'],
 'mujoco': ['mujoco-py>=2.1.2,<3.0.0']}

setup_kwargs = {
    'name': 'rl-games',
    'version': '1.5.0',
    'description': '',
    'long_description': None,
    'author': 'Denys Makoviichuk',
    'author_email': 'trrrrr97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)

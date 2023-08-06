# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_splitview']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2', 'Pillow>=9.1.0', 'ipykernel>=6.13.0', 'ipython>=7.0.0']

setup_kwargs = {
    'name': 'jupyter-splitview',
    'version': '0.0.7',
    'description': 'Making before/after image sliders in JupyterLab',
    'long_description': 'Jupyter Splitview\n=================\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kolibril13/jupyter-splitview/HEAD?labpath=example_notebook.ipynb)\n[![JupyterLight](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://kolibril13.github.io/jupyter-splitview/)  \nA cell magic that displays images in splitview using https://github.com/NUKnightLab/juxtapose.  \n*NOTE: Still work in progress, there will be breaking changes.*\n*Note: JupyterLite example is still work in progress\n## Installation\n```py\npip install jupyter-splitview\n```\n## Example\n```py\nimport jupyter_splitview\n```\n\n```py\n%%splity\n\nfrom skimage import data\nfrom skimage.util import random_noise\nimport matplotlib.pyplot as plt\n\nimg = data.chelsea()\nnoisy_img = random_noise(img, var=0.02)\n\nfig, ax1 = plt.subplots()\nax1.axis("off")\nax1.imshow(img)\n\nfig, ax2 = plt.subplots()\nax2.axis("off")\nax2.imshow(noisy_img)\n```\n\n<img src="https://user-images.githubusercontent.com/44469195/173762859-61c12c6b-7d50-4a63-9a51-8b78b43b4b03.png" style="width: 350px;"/>\n\nNote: The split view widget is still responsive after closing and reopening the notebook without running the cell again.\n\nAnother example:\n```py\n%%splity --position 73% --height auto\n\nimport matplotlib.pyplot as plt\nimport numpy as np\n\narray1 = np.full((15, 30), 10)\narray2 = np.random.randint(0, 10, size=(15, 30))\nfig, ax1 = plt.subplots(figsize=(5, 10))\nax1.imshow(array1)\nfig, ax2 = plt.subplots(figsize=(5, 10))\nax2.imshow(array2)\n```\n<img src="https://user-images.githubusercontent.com/44469195/173763087-e76be74b-57e4-4861-ae0a-6c307021b785.png" style="width: 300px;"/>\n\n\n## Notebook arguments\n\n* `--position 73%` will set the slider start position to 73%.\n*  The height of the widget. \n* `--height 220` will set the height to 220 pixel. \n* When `--height`is not provided, the default height of the widget is 300 pixel.\n* `--height auto` will set the height by the value of the first image\'s resolution in vertical direction.\n* The widget\'s width will always be adjusted automatically. \n\n## Notebook formatting\nFormatting with black can be done this way: \n1. `pip install \'black[jupyter]\'`\n2. `black --python-cell-magics splity splitview_magic.ipynb`\n\n\n## Developer Installation\n\n1. `git clone --recurse https://github.com/kolibril13/jupyter-splitview`\n(Note: In case that the repo was already cloned e.g. with the GitHub Desktop client, the  GitHub submodule has to be loaded via `git submodule update --init --recursive`)\n2. `poetry install`\n\n## Changelog\n\n## Milestones \n\n* Handle cases where n ≠ 2 images. Currently: All further img are ignored.\n* implement tests, find out how to test a magic class\n\n* Idea: Second option without using cell magic:\n```python\nfrom splitview import Splity # (does not yet exist)\nmy_splity = Splity(left_layer=img1, right_layer=img2)\ndisplay(my_splity)\n```\n\n## 0.0.8 (Work in Progress)\n\n\n* Make this work also in VSCode notebooks, [see this issue](https://github.com/NUKnightLab/juxtapose/issues/178).\n\n\n## 0.0.7\n\n* Rewrite of the import of JavaScript and CSS to make it more robust when closing and opening the notebook\n* First attempt to add a JupyterLite example.\n## 0.0.6 \n\nFix poetry workflow\n\n## 0.0.5 \n\n* Ship the javascript directly with the package, so no internet connection is required\n* use jinja2 to save HTML in separate file\n* load stylesheet and javascript only once in the beginning, and not in every cell that contains the splitview widget.\n\n## 0.0.4 \n\n* New `--height` parameter\n\n## 0.0.3\n\n* default slider position\n* updated minimal example\n* internal code restructuring and formatting\n* Handle import in non jupyter context\n\n### 0.0.2 \n* save images in base64 strings and don\'t load images to disk (increases package security).\n### 0.0.1\n\n* First release\n\n\n',
    'author': 'kolibril13',
    'author_email': '44469195+kolibril13@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

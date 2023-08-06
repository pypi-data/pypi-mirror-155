# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cupcake',
 'cupcake.config',
 'cupcake.config.languages',
 'cupcake.editor',
 'cupcake.editor.autocomplete',
 'cupcake.editor.find_replace',
 'cupcake.editor.language',
 'cupcake.editor.language.languages',
 'cupcake.editor.linenumbers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cupcake-editor',
    'version': '0.5.1',
    'description': 'Embeddable code editor for tkinter',
    'long_description': "# Cupcake: Embeddable Code Editor\nCupcake is an Embeddable Modern Code editor for python tkinter applications. It comes with features such as **Autocompletions**, **Minimap** and **Semantic Syntax highlighting**. Cupcake is written in pure python with the tkinter library. It is the the code editor which powers [Biscuit](https://github.com/billyeatcookies/Biscuit). See a good list of the code editor's [features](#features).\n\n<table>\n    <td>\n        <img src=https://user-images.githubusercontent.com/70792552/162617435-a9145e3e-e380-4afd-8e78-cbeedeb1bd24.gif />\n    </td>\n    <td>\n        <img src=https://user-images.githubusercontent.com/70792552/162617464-65169951-fc20-44f3-9f24-a7d80cb6eb10.gif />\n    </td>\n</table>\n\n<!-- ![something](.github/res/screenshot.png) -->\n\n## Installation\nCupcake can be installed by running:\n```\npip install cupcake-editor\n```\nCupcake requires Python 3.10+ to run.\n\n## Quick start\nHere is a quick example of embedding cupcake in your project:\n```py\nimport tkinter as tk\nfrom cupcake import Editor \n\nroot = tk.Tk()\nroot.minsize(800, 600)\n\neditor = Editor(root)\neditor.pack(expand=1, fill=tk.BOTH)\n\nroot.mainloop()\n```\n\n## Examples!\nExamples demonstrating how to use cupcake are in the [examples](./examples) directory. You can learn how to integrate the editor to your app with these. You can run the examples like `python -m examples.hello`\n\n## Features\n\n- [x] Syntax Highlighting\n- [x] Auto completions\n- [x] Auto Indentation\n- [x] Minimap\n- [x] Find Replace\n- [ ] Extendable language support\n- [ ] Code Debugging\n- [ ] Language Detection\n- [ ] Code Folding\n\n\n### Contributing\nThank you if you are considering to contribute to Cupcake. See [contributing](./CONTRIBUTING.md) for further details such as coding guides and editing tools used.\n",
    'author': 'Billy',
    'author_email': 'billydevbusiness@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

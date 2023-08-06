# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quantum_viz']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'ipython>=8.0.3,<9.0.0', 'varname>=0.8.1,<0.9.0']

extras_require = \
{'qiskit': ['qiskit-terra>=0.19.1,<1']}

setup_kwargs = {
    'name': 'quantum-viz',
    'version': '1.0.4',
    'description': 'quantum-viz.js Python tools',
    'long_description': '# quantum-viz\n\n`quantum-viz` is the Python package companion of [quantum-viz.js](https://github.com/microsoft/quantum-viz.js), a JavaScript package that supports visualizing any arbitrary quantum gate, classical control logic and collapsed grouped blocks of gates using JSON-formatted input data. `quantum-viz` contains a Jupyter widget and will also include support for translating quantum circuits written in common quantum programming libraries to JSON using the `quantum-viz.js` JSON schema.\n\n![quantum-viz screenshot](https://user-images.githubusercontent.com/4041805/137234877-6a529652-a3b9-48c6-9d3c-c2b9d1e11855.gif)\n\n## Installation\n\nYou can install the *quantum-viz.js widget* via `pip` from PyPI:\n\n```bash\npip install quantum-viz\n```\n\n## Example\n\nTo use the quantum-viz widget, run the below example code in a [Jupyter notebook](https://jupyter.org/) cell:\n\n```python\nfrom quantum_viz import Viewer\n\n# Create a quantum circuit that prepares a Bell state\ncircuit = {\n    "qubits": [{ "id": 0 }, { "id": 1, "numChildren": 1 }],\n    "operations": [\n        {\n            "gate": \'H\',\n            "targets": [{ "qId": 0 }],\n        },\n        {\n            "gate": \'X\',\n            "isControlled": "True",\n            "controls": [{ "qId": 0 }],\n            "targets": [{ "qId": 1 }],\n        },\n        {\n            "gate": \'Measure\',\n            "isMeasurement": "True",\n            "controls": [{ "qId": 1 }],\n            "targets": [{ "type": 1, "qId": 1, "cId": 0 }],\n        },\n    ],\n}\n\nwidget = Viewer(circuit)\nwidget # Display the widget\n```\n\n![quantum-viz example](https://user-images.githubusercontent.com/4041805/137230540-b523dc76-29c7-48e2-baa3-34d4ee0a17a1.PNG)\n\n## Qiskit Integration\n\nBy installing the optional `[qiskit]` dependency, you can leverage Qiskit\'s `QuantumCircuit` APIs\nto define the circuit and render it using the `Viewer` widget on Jupyter, for example:\n\n```python\nfrom qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit\nfrom quantum_viz import Viewer\n\nqr = QuantumRegister(3, \'q\')\nanc = QuantumRegister(1, \'ancilla\')\ncr = ClassicalRegister(3, \'c\')\nqc = QuantumCircuit(qr, anc, cr)\n\n\nqc.h(qr[0:3])\nqc.x(anc[0])\nqc.h(anc[0])\nqc.cx(qr[0:3], anc[0])\nqc.h(qr[0:3])\nqc.barrier(qr)\nqc.measure(qr, cr)\n\nViewer(qc)\n```\n\nOptionally, you can also import the `display` method from `quantum_viz.utils` to render the circuit on a new browser window:\n\n```python\nfrom quantum_viz.utils import display\ndisplay(qc)\n```\n\n## Contributing\n\nCheck out our [contributing guidelines](./CONTRIBUTING.md) to find out how you can contribute to quantum-viz.\n',
    'author': 'Microsoft Corporation',
    'author_email': 'que-contacts@microsoft.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/microsoft/quantum-viz.js',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

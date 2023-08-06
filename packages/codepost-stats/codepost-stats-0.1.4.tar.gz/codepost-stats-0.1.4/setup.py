# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['codepost_stats',
 'codepost_stats.analyzers',
 'codepost_stats.analyzers.abstract']

package_data = \
{'': ['*']}

install_requires = \
['codepost>=0.2.25,<0.3.0', 'tqdm>=4.48.2,<5.0.0']

setup_kwargs = {
    'name': 'codepost-stats',
    'version': '0.1.4',
    'description': 'A system to compile statistics automatically from a course on the codePost platform.',
    'long_description': '# codePost Statistics Compiler\n\n![pytest](https://github.com/jlumbroso/codepost-stats/workflows/pytest/badge.svg)\n [![codecov](https://codecov.io/gh/jlumbroso/codepost-stats/branch/master/graph/badge.svg?token=KVGWAVZKW1)](https://codecov.io/gh/jlumbroso/codepost-stats)\n [![Documentation Status](https://readthedocs.org/projects/codepost-stats/badge/?version=latest)](https://codepost-stats.readthedocs.io/en/latest/?badge=latest)\n [![Downloads](https://pepy.tech/badge/codepost-stats)](https://pepy.tech/project/codepost-stats)\n [![Run on Repl.it](https://repl.it/badge/github/jlumbroso/codepost-stats)](https://repl.it/github/jlumbroso/codepost-stats)\n [![Stargazers](https://img.shields.io/github/stars/jlumbroso/codepost-stats?style=social)](https://github.com/jlumbroso/codepost-stats)\n\nA system to compile statistics automatically from a course on the codePost platform.\n\n## Installation\n\nThe package is available on PyPI as slacktivate and so is available the usual way, i.e.,\n```shell\n$ pip install codepost-stats\n```\n\n## Example\n\n```python\nimport codepost\n\nimport codepost_stats\nimport codepost_stats.analyzers.abstract.simple\nimport codepost_stats.analyzers.standard\nimport codepost_stats.event_loop\n\n# Login\ncodepost.configure_api_key("<CODEPOST_API_TOKEN>")\n\n# Create Course Analyzer Event Loop\ncael = codepost_stats.event_loop.CourseAnalyzerEventLoop(\n    course_name="COS126",\n    course_term="S2020",\n)\n\n# Create Analyzer\nclass SubmissionsGradedCounter(codepost_stats.analyzers.abstract.simple.CounterAnalyzer):\n    _name = "submissions.graded"\n    \n    def _event_submission(\n        self,\n        assignment: codepost.models.assignments.Assignments,\n        submission: codepost.models.submissions.Submissions,\n    ):\n        # if no grader, nothing to do\n        if submission.grader is None:\n            return\n        \n        # if not finalized, do not want to count it\n        if not submission.isFinalized:\n            return\n        \n        # increase number of graded submission for grader by 1\n        self._delta_counter(\n            name=submission.grader,\n            subcat=assignment.name,\n            delta=1,\n        )\n        \nsgc = SubmissionsGradedCounter()\n\n# Add the analyzer we just created\ncael.register(sgc)\n\n# Add a few standard analyzers\ncael.register(codepost_stats.analyzers.standard.CustomCommentsCounter)\ncael.register(codepost_stats.analyzers.standard.RubricCommentsCounter)\n\n# Run the aggregation of stats\ncael.run()\n\n# Extract statistics per user\nstatistics_per_user = {\n    name: cael.get_by_name(name)\n    for name in cael.names\n}\n```\nand the `statistics_per_user` variable would be a dictionary of the form:\n```json\n{\n  "grader1@princeton.edu": {\n    "submissions.graded": {\n      "hello": 5,\n      "loops": 6,\n      "nbody": 0,\n      "sierpinski": 8,\n      "programming-exam-1": 6,\n      "hamming": 0,\n      "lfsr": 2,\n      "guitar": 5,\n      "markov": 6,\n      "tspp": 4,\n      "atomic": 29\n    },\n    "comments.counter.custom": {\n      "hello": 9,\n      "loops": 6,\n      "nbody": 0,\n      "sierpinski": 14,\n      "programming-exam-1": 6,\n      "hamming": 0,\n      "lfsr": 4,\n      "guitar": 8,\n      "markov": 14,\n      "tspp": 7,\n      "atomic": 36\n    },\n    "comments.counter.rubric": {\n      "hello": 7,\n      "loops": 15,\n      "nbody": 0,\n      "sierpinski": 13,\n      "programming-exam-1": 8,\n      "hamming": 0,\n      "lfsr": 6,\n      "guitar": 10,\n      "markov": 17,\n      "tspp": 13,\n      "atomic": 38\n    }\n  },\n  "grader2@princeton.edu": {\n      /* ... grader2@princeton.edu\'s statistics here ... */\n  },\n  /* ... more graders ... */\n}\n```\n\n## License\n\nThis project is licensed [under the LGPLv3 license](https://www.gnu.org/licenses/lgpl-3.0.en.html),\nwith the understanding that importing a Python modular is similar in spirit to dynamically linking\nagainst it.\n\n- You can use the library/CLI `codepost-stats` in any project, for any purpose,\n  as long as you provide some acknowledgement to this original project for\n  use of the library (for open source software, just explicitly including\n  `codepost-stats` in the dependency such as a `pyproject.toml` or `Pipfile`\n  is acknowledgement enough for me!).\n\n- If you make improvements to `codepost-stats`, you are required to make those\n  changes publicly available.\n\n',
    'author': 'Jérémie Lumbroso',
    'author_email': 'lumbroso@cs.princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jlumbroso/codepost-stats',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_deps_scanner']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0',
 'python-gitlab>=2.6.0',
 'requests>=2.25.1',
 'toml>=0.10.2']

entry_points = \
{'console_scripts': ['comment-gitlab = poetry_deps_scanner.comment_gitlab:main',
                     'scan-deps = poetry_deps_scanner.scan_deps:main']}

setup_kwargs = {
    'name': 'poetry-deps-scanner',
    'version': '1.1.0',
    'description': 'Analyse poetry dependencies and comment on gitlab',
    'long_description': '# Poetry dependencies scanner & gitlab commenter\n\nThis project consists of two scripts.\n\nOne analyses the `poetry.lock` and `pyproject.toml` files\nit receives and produces an output listing the outdated\npackages.\n\nThe other takes an input and posts it as a comment on a Gitlab\nmerge request.\n\nHere\'s how we use them:\n\n```yaml\n# .gitlab-ci.yml\n\nscan-deps:\n  stage: test\n  image: deps-scanner\n  allow_failure: true\n  script:\n    - scan-deps poetry.lock pyproject.toml | comment-gitlab\n  only:\n    - merge_requests\n```\n\nThe `deps-scanner` image is built from the Dockerfile in this repository.\n\nHere\'s an example of what the output looks like in a merge request for\nthis repository:\n\n![Comment screenshot](img/comment-screenshot.png)\n\n## Installation\n\n```bash\npython -m pip install poetry-deps-scanner\n```\n\n## Dependencies analysis\n\nThe following snippet is an example output the first script may produce:\n\n```\ndirect devpi command-log: current=0.0.28 -> latest=0.0.29\ndirect pypi  django: current=3.1.9 -> latest=3.2.1\ndirect pypi  semver: current=3.0.0.dev2 -> latest=2.13.0\ntrans. pypi  idna: current=2.10 -> latest=3.1\n```\n\nThe first column indicates whether the package is a direct or transitive\ndependency:\n* `direct` means the package is a direct dependency.\n* `trans.` means the package is a transitive dependency: the dependency\n  of a direct dependency or of a transitive dependency.\n\nThis is computed by using the `pyproject.toml` if given. If this file is\nnot provided on the command line, the column will be omitted.\n\nA dependency is considered direct if it is present in the `pyproject.toml`.\n\nThe second column indicates whether the package comes from PyPi or\na devpi instance.\n\n## Gitlab comment\n\nThe `comment_gitlab.py` script requires some environment variables\nto properly work:\n\n* `BOT_USERNAME`: The username for the bot user\n* `BOT_TOKEN`: A Gitlab access token for the bot user\n  (see https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)\n* `CI_SERVER_URL`: The URL of the Gitlab instance where to post\n* `CI_PROJECT_ID`: The ID of the project containing the MR to post on\n* `CI_MERGE_REQUEST_IID`: The IID of the merge request to comment on\n\nThe last three variables are automatically populated by Gitlab CI when\nrunning a job as part of a detached pipeline (for a merge request). Notice\nthe `only: [merge_requests]` in the `.gitlab-ci.yml` above.\n\nOf course, you can also provide them manually to integrate with any other build\nsystem.\n\nIf a comment from the bot user already exists, it will be replaced,\nin order to reduce the noise. In other words, there will be at most one\ncomment from the bot on a given merge request. It will contain the results of\nthe latest check.\n\n## Build the docker image outside ITSF\n\nThe Dockerfile inside the repository references images from our internal\nDocker registry proxy. You can easily build it on your own by removing\nthe `nexus.itsf.io:5005/` prefix.\n\n```bash\n# on Ubuntu\nsed -i \'s/nexus.itsf.io:5005\\///g\' Dockerfile\n# on macOS\nsed -e \'s/nexus.itsf.io:5005\\///g\' -i "" Dockerfile\n# then\ndocker build -t deps-scanner .\n```\n',
    'author': 'Gabriel Augendre',
    'author_email': 'gabriel.augendre@itsfactory.fr',
    'maintainer': 'Gabriel Augendre',
    'maintainer_email': 'gabriel.augendre@itsfactory.fr',
    'url': 'https://github.com/itsolutionsfactory/poetry-deps-scanner/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)

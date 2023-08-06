# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web_youtube_dl', 'web_youtube_dl.app', 'web_youtube_dl.services']

package_data = \
{'': ['*'], 'web_youtube_dl.app': ['static/*', 'templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'Werkzeug>=1.0.1,<2.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'fastapi>=0,<1',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'janus>=0.5.0,<0.6.0',
 'musicbrainzngs>=0.7.1,<0.8.0',
 'mutagen>=1.45.1,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pytube>=12.0.0,<13.0.0',
 'uvicorn>=0.17.0,<0.18.0',
 'websockets>=10.3,<11.0']

entry_points = \
{'console_scripts': ['web-youtube-dl-cli = '
                     'web_youtube_dl.app.main:cli_download',
                     'web-youtube-dl-web = web_youtube_dl.app.main:run_app']}

setup_kwargs = {
    'name': 'web-youtube-dl',
    'version': '0.3.0',
    'description': 'A web version of youtube-dl',
    'long_description': ".. image:: https://badge.fury.io/py/web-youtube-dl.svg\n    :target: https://badge.fury.io/py/web-youtube-dl\n    :alt: PyPi Package\n\n.. image:: https://img.shields.io/pypi/pyversions/web-youtube-dl\n    :target: https://pypi.org/project/web-youtube-dl/\n    :alt: Compatible Python Versions\n\n\nAbout\n=====\n\nThis is a project that builds on pytube to provide a simple web-interface \nfor downloading audio from Youtube. It's primary purpose is to provide a LAN \nHTTP accessible method of saving audio to a local device.\n\nThis project is built using python's asyncio libraries and packages include \nFastAPI, janus, and uvicorn. It's also an example of how to work with pytube's \npython sdk and enable asynchronous downloads in the context of a web-app. \n\nFiles are downloaded using an API endpoint and then retrived from the application's \nstatic files directory using Javascript's fetch API. Download progress is presented \nvia a websocket connection.\n\n\nInstallation\n============\n\n.. code-block:: bash\n\n    pip install web-youtube-dl\n\n\nRunning\n=======\n\nCLI\n---\n\nInstalling this project will give you access to two CLI tools, each with a\nseparate purpose:\n\n* | **web-youtube-dl-cli**\n  | Useful for simply downloading the highest possible quality audio of a song. \n  | Simply provide the URL and an .mp3 will be downloaded to current working\n  | directory or to the value of the *YT_DOWNLOAD_PATH* environment variable \n\n* | **web-youtube-dl-web**\n  |  Useful for running the web service on the local machine. It will \n  |  listen to all local network connections on port 5000 (or whatever port is\n  |  defined in the environment variable *YT_DOWNLOAD_PORT*).\n\n\nDocker\n------\n\nThis project can optionally be run and managed as a Docker container.\n\nBuild the Docker image\n^^^^^^^^^^^^^^^^^^^^^^\n\n.. code-block:: bash\n\n    docker build . -t  web-youtube-dl:latest --force-rm\n\nOr, using the project's Makefile\n\n.. code-block:: bash\n\n    make image\n\nRun the service\n^^^^^^^^^^^^^^^\n\nWhen running the service via Docker, you can configure where it stores downloaded \nsongs by default and the port the service listens on by setting the appropriate \nenvironment variables.\n\nTo configure the port, set the environment variable *YT_DOWNLOAD_PORT* to some \nother numerical value.\n\nTo configure the download path, set the environment variable *YT_DOWNLOAD_PATH* \nto some other filesystem path. Note that an unprivileged user must have access \nto writing to this location. By default, this is set to *tmp* and does not \nreally need to be changed.\n\n.. code-block:: bash\n\n    docker-compose up -d\n\nOr, using the project's Makefile\n\n.. code-block:: bash\n\n    make compose\n\nEnhancements\n^^^^^^^^^^^^\nTrack progress beyond YT download\n- tie into ffmpeg\n- tie into metadata extraction",
    'author': 'Uriel Mandujano',
    'author_email': 'uriel.mandujano14@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

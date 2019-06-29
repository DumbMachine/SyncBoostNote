import os
import platform

from setuptools import find_packages, setup

with open('./requirements.txt') as f:
    required = f.read().splitlines()


setup(name="syncboostnote",
      version="0.1a",
      install_requires=required,
      packages=find_packages(exclude=["tests"]),
      scripts=[],
      description="CLI tool to help syncing BoostNote notes.",
      long_description="A simple CLI, created in Python, to help users to Sync their notes created in BoostNote Application with their Github Account. Along with syncing, it also creates a repo with a beautiful layout and interface to consume the notes on mobile devices.",
      author="Ratin Kumar",
      author_email="ratin.kumar.2k@gmail.com",
      maintainer="Ratin Kumar (@DumbMachine)",
      maintainer_email="ratin.kumar.2k@gmail.com",
      url="https://github.com/DumbMachine/syncboostnote",
      download_url="https://github.com/DumbMachine/syncboostnote/releases",
      license="GNU-gpl3",
      test_suite="tests",
      # setup_requires = ["pytest-runner"],
      # tests_require = ["pytest"],
      classifiers=[
          #   "Development Status :: 1 - Planning",
          #   "Development Status :: 2 - Pre-Alpha",
          #   "Development Status :: 3 - Alpha",
          "Development Status :: 4 - Beta",
          #   "Development Status :: 5 - Production/Stable",
          #   "Development Status :: 6 - Mature",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Operating System :: MacOS",
          "Operating System :: POSIX",
          "Operating System :: Unix",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Topic :: Software Development",
          "Topic :: Utilities",
      ],
      entry_points={
          'console_scripts': [
              'syncboostnote = syncboostnote.cli:run_as_command',
          ],
      },
      platforms="Any",
      )

![CI](https://github.com/andreasdomanowski/sage-graph-assessment/actions/workflows/python.yml/badge.svg) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# Assessing Graph Properties
This repository contains a simple ad-hoc script for assessing properties on graphs with SageMath.
Either install Sage globally or build the docker image.
For now and the sake of simplicity, manipulate the dockerfile and rebuild to change the arguments.

# Usage
1) Clone the repository
   1) via SSH: `git clone --recursive git@github.com:andreasdomanowski/sage-graph-assessment.git`
   2) via HTTPS: `git clone --recursive https://github.com/andreasdomanowski/sage-graph-assessment.git`
2) Run the task and assessment server. You need to either install SageMath and Python3 globally or build a Docker image
   1) via global installation
      1) `sudo apt install sagemath`
      2) `sage assessment-task-server/minimalWebserver.py`
   2) via Docker
      1) `docker build -t sage-assessment-minimal-example:latest assessment-task-server/.`
      2) `docker run -d -p 8889:8889 sage-assessment-minimal-example`
3) Run the modeling editor
   1) Traverse into the folder *Apollon/*
   2) `yarn install`
   3) `yarn start`
   4) Go to http://localhost:8888

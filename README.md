[![Build Status](https://travis-ci.org/bertini36/profiler.svg?branch=master)](https://travis-ci.org/bertini36/profiler)
[![Requirements Status](https://requires.io/github/bertini36/profiler/requirements.svg?branch=master)](https://requires.io/github/bertini36/profiler/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/bertini36/profiler/badge.svg?branch=master)](https://coveralls.io/github/bertini36/profiler?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

<h3 align="center">
    bertini36/profiler 📖
</h3>
<p align="center">
  <a href="#-environment-setup" target="_blank">
    Installation
  </a>&nbsp;&nbsp;•&nbsp;
  <a href="https://github.com/bertini36/profiler/blob/master/Makefile" target="_blank">
    Commands
  </a>&nbsp;&nbsp;•&nbsp;
  <a href="https://github.com/bertini36/profiler/blob/master/src/settings.py" target="_blank">
    Algorithm settings
  </a>&nbsp;&nbsp;•&nbsp;
  <a href="https://albertopou.dev/blog/profiling-on-social-networks" target="_blank">
    Post
  </a>
</p>
<p align="center">
Profiler tries to identify main topics in personal Twitter timelines using
<a href="http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf">LDA
 topic models algorithm</a> in a easy way for simple exploratory purposes
</p>

## ⚙️ Environment Setup

### 🐳 Required tools

1. [Install Docker and Docker Compose](https://www.docker.com/get-started)
2. Clone this project: `git clone https://github.com/bertini36/profiler`
3. Move to the project folder: `profiler`

### 🚀 Usage

1. Install all the dependencies and bring up the project with Docker executing: `make build`
2. `cp .env-sample .env`
3. Add your Twitter keys at `.env`
4. If you require it, customize some algorithm technical configs at `src/settings.py`
5. Run an inference: `make run timelines=pablocasado_ topics=3`
6. ☕
7. HTML outputs will be generated at `output` folder. Open them with your navigator

### 📈 Results screenshot

<p align="center"><img src="https://github.com/bertini36/profiler/blob/master/img/photo.png"/></p>

<br />
<p align="center">&mdash; Built with :heart: from Mallorca &mdash;</p>

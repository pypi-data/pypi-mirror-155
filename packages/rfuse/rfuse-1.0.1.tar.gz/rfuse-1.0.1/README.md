# Fuse
![](https://img.shields.io/github/downloads/eliran-turgeman/fuse/total)
![](https://img.shields.io/github/license/eliran-turgeman/fuse)
![](https://img.shields.io/github/commit-activity/w/eliran-turgeman/fuse/main)

Fuse is a content aggregation CLI tool written in Python.

Currently supports Reddit and Medium as sources.

# Installation
`pip install Fuse-Con`

View PyPi project at https://pypi.org/project/Fuse-Con/

# Basic Usage
`python ./src/main.py --reddit --sub programming --hot --limit 3`
* Note: To use reddit as a source you need to generate a key for Reddit's API, follow this guide on [reddit's github](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) and then set `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` as environment variables or pass these keys through the CLI with the arguments `reddit_id` and `reddit_secret`.

![Capture](https://user-images.githubusercontent.com/50831652/167022584-efdd95c6-0d78-463a-a468-dc08dd7989ae.JPG)

`python ./src/main.py --medium --tag programming`

![Capture](https://user-images.githubusercontent.com/50831652/167022796-ac13ad37-dd1a-4c74-b0dc-0c04bfa923fd.JPG)

Note: limit is 10 by default.


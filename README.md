MathAppData
===
[![Build Status](https://travis-ci.org/NonameDev/MathAppData.svg?branch=master)](https://travis-ci.org/NonameDev/MathAppData) [![Coverage Status](https://coveralls.io/repos/NonameDev/MathAppData/badge.svg?branch=master)](https://coveralls.io/r/NonameDev/MathAppData?branch=master)

This repository holds the data that is used by MathApp.

Pipeline
---
This repository consists of two stages beta and master. All changes should be merged into the beta branch. Travis will then run all the test and regenerate the images for the equations. If nothing fails, all changes will be published to the master branch

DPI Sizes
---
Four different versions of each image is generated in order to have approriate image sized for devices with different screen densities. The four different dpi levels are shown below
### ldpi
![ldpi image example](./imgs/ldpi/eqn_0.png "ldpi image example")
### mdpi
![mdpi image example](./imgs/mdpi/eqn_0.png "mdpi image example")
### hdpi
![hdpi image example](./imgs/hdpi/eqn_0.png "hdpi image example")
### xhdpi
![xhdpi image example](./imgs/xhdpi/eqn_0.png "xhdpi image example")

# Data dumping directory introduction

This directory is for dumping data.

All the data can be downloaded from [google drive](https://drive.google.com/drive/folders/1dkDeHlwOVbmgXcDazZvO6TFEZ6V_7WUu). If you have a good internet, you can directly download the complete large zip file such as `train.zip`. In case you suffer from downloading large fiels, we also split each data set into small chunks, which can be found in the directory ending with `_chunks`, such as `train_chunks`. After downloading, please run the following command to each set to merge those chunks together:

After downloading is finished, please make the file structured as following:

```
OpenCOOD # root of your OpenCOOD
├── opv2v_data_dumping # the downloaded opv2v data
│   ├── train
│   ├── validate
│   ├── test
│   ├── test_culvercity
├── opencood # the core codebase
```
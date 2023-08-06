# runner

* [中文说明](README_CN.md)

## introduction

`runner` is a `configurable` quick launcher for `starting (running)` commonly used `commands (programs)`.
It comes with a `log` output interface, which is convenient for users to `view (color)` and `save` log. And the log output in a special format can also drive the program to draw a `progress bar`.

![main-ui](https://i.ibb.co/CtZ55GP/main.png)

## install

pip install -r requirements.txt

only tested on the `windwos` platform, recommended to use the `python 3.7` version.

## start up

- python runner.py - run from codebase
- runner - run after install

## configure

### main configuration file

config.json
```json
{
    "maxLogLines": 1000,        // max lines to view
    "maxStdout": 40960,         // max block of stdout 
    "defaultEncoding": "gbk",   // default stdout encodding
    "configs": [                // sub configuration item
        {
            "file": "runner_common.json",   // sub configuration file
            "title": "通用(测试)"            // title in ui
        }
    ]
}
```

### sub configuration file

runner_xxxx.json
```json
[
    {
        "title": "change codepage to gbk(use with caution)",  // title in ui
        "cmd": "cmd /c  chcp 936",          // command ling
        "encoding": "gbk",                  // output encoding
        "qss": "color: rgb(150, 0, 0);",    // ui styles in qss format
        "cwd": ""                           // current working directory
    }
]
```

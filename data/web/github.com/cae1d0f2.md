---
domain: github.com
fetch_date: '2026-05-18T12:36:31.248481'
status: ok
url: https://github.com/sh-aidev/distil-whisper
---

A clean and simple PyTorch implementation of distil whisper speech to text in live mode.

This repository contains a clean and simple pytorch implementation of distil whisper speech to text taking live input from the microphone. In config we can provide required mic details for our code to work. The code is written in a modular way so that it can be easily understood and modified. The code is written in a way that it can be easily integrated with other projects. Also once the text prediction is done, it is sent to redis server for further processing using redis pub sub communication.

- Live Speech to Text
- Redis Pub Sub Communication
- Modular Code
- Easy to Integrate

The directory structure of new project looks like this:

```
├── configs
│ └── config.toml
├── internal
│ ├── app.py
│ ├── core
│ │ ├── audio_src.py
│ │ ├── __init__.py
│ │ └── stt.py
│ ├── __init__.py
│ ├── server
│ │ ├── __init__.py
│ │ └── pubsub.py
│ └── utils
│ ├── config.py
│ ├── __init__.py
│ ├── logger.py
│ ├── models.py
│ ├── noise_check.py
│ ├── textformat.py
│ └── util.py
├── logs
│ └── server.log
├── main.py
├── pylogger
│ ├── __init__.py
│ └── logger.py
├── README.md
└── requirements.txt
```


```
git clone https://github.com/sh-aidev/distil-whisper.git
cd distil-whisper
```

`code .`

**NOTE**: Once repo in opened in vscode, it will ask to open in container. Click on reopen in container. It will take some time to build the container.

`python3 -m pip install -r requirements.txt`

`python3 get_source_mic.py`

Which ever Mic you want to select, copy the name of that mic and paste it in config.toml file.

`NOTE`

: If you are using docker, you need to run the above command inside the docker container. If your desired mic is not listed, try restarting system and then run the command. Also, to get the mic sample rate, you can run the below command in the terminal and updated the sample rate in config.toml file respectively.

`pactl list sources | grep -A 10 alsa_input`

```
python3 main.py
# NOTE: If you are running the code for the first time, make sure to correctly provide mic details in config.toml file like name, sample rate, etc.
# Also, it is possible that noise threshold for you mic could be different. So, you can play around with the value to get the best result.
```

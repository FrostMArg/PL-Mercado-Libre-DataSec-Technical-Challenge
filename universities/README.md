
# Universities


## How to run this project?
To execute these commands, remember to be positioned in the root folder of the project.
```
cd universities/
```

This project was implemented using python 3.11. If you have installed that python version (or any version above 3.7) you can just run the following commands:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
There is also a Dockerfile present and you can execute it using docker with the following commands

```bash
docker build -t universities .
docker run universities
```

## Dependencies
This project only uses the `requests` library to query the hackerrank API
# TrueWay Geocoding API on RapidAPI

## Install
### using pip
```
pip install trueway_geocoding_rapidapi
```
### using poetry
```
poetry add trueway_geocoding_rapidapi
```

## Build
### Windows
```
git clone https://github.com/dankaprogg/trueway_geocoding_rapidapi.git

cd trueway_geocoding_rapidapi
py -m venv venv
cd venv/Scripts/ && activate && cd ../../
pip install -r requirements.txt
py setup.py sdist bdist_wheel install
```
### Linux
```
git clone https://github.com/dankaprogg/trueway_geocoding_rapidapi.git

cd trueway_geocoding_rapidapi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 setup.py sdist bdist_wheel install
```
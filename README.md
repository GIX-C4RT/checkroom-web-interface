# checkroom-web-interface
A web interface for our equipment management system

## Design Descisions
Flask for the backend. Sticking with Python (as opposed to Node.js) to keep our tech stack smaller.
Sticking with Flask because it's simpler than Django and the rest of the team is already familiar with it.

In the current design the front end and back end are tightly coupled, with the backend generating the HTML for the front end. Ideally, the application logic (back end) would be entirely seperate from the display logic (front end). In the future, we might use a static website as the frontend and create a true RESTful API that only delivers JSON for the backend.

## Architecture
Flask app backend that renders a website frontend.

## Instructions
### Installation
#### Ubuntu
```
sudo apt install python3 python3-pip # install Python 3
python3 -m pip install --upgrade pip # update pip
cd # go to home directory
mkdir robotics # make robotics directory
cd robotics # go to robotics directory
git clone https://github.com/GIX-C4RT/checkroom-web-interface.git # clone the repo
cd checkroom-web-interface # go to checkroom-web-interface directory
python3 -m venv .venv # create virtual environment
source .venv/bin/activate # activate the virtual environment
pip install flask, numpy, opencv-contrib-python # install dependencies
flask init-db # initialize the database
```

### Runnning
#### Ubuntu
```
source run.bash # run the web app backend
```

## Dependencies
* Python 3
* Flask
* OpenCV
* Numpy

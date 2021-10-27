# checkroom-web-interface
A web interface for our equipment management system

## Design Descisions
Flask for the backend. Sticking with Python (as opposed to Node.js) to keep our tech stack smaller.
Sticking with Flask because it's simpler than Django and the rest of the team is already familiar with it.

In the current design the front end and back end are tightly coupled, with the backend generating the HTML for the front end. Ideally, the application logic (back end) would be entirely seperate from the display logic (front end). In the future, we might use a static website as the frontend and create a true RESTful API that only delivers JSON for the backend.

## Architecture
Flask app backend that renders a website frontend.

## Running
### Ubuntu
```
sudo apt install python3 # install Python 3
pip install flask # install flask
git clone https://github.com/GIX-C4RT/checkroom-web-interface.git # clone the repo
cd checkroom-web-interface # navigate to the new repo folder
flask init-db # initialize the database
source run.bash # run the web app backend
```

## Dependencies
* Python 3
* Flask

## Running
To run the app, run the approprate run script from your terminal (run.bash, run.bat, run.ps1).

### LookupError: unknown encoding: cp65001
See here: https://stackoverflow.com/questions/35176270/python-2-7-lookuperror-unknown-encoding-cp65001

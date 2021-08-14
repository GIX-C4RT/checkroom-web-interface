# checkroom-web-interface
A web interface for our equipment management system

## Design Descisions
Flask for the backend. Sticking with Python (as opposed to Node.js) to keep our tech stack smaller.
Sticking with Flask because it's simpler than Django and the rest of the team is already familiar with it.

In the current design the front end and back end are tightly coupled, with the backend generating the HTML for the front end. Ideally, the application logic (back end) would be entirely seperate from the display logic (front end). In the future, we might use a static website as the frontend and create a true RESTful API that only delivers JSON for the backend.

## Architecture
Flask app backend that renders a website frontend.

## Running
1. Clone this repo
2. Install the dependencies (possibly in a virtual environment)
3. Initialize the database (flask init-db)
4. Run the appropriate run script for your shell (run.bash,bat,ps1)

## Dependencies
* Python 3.9
* Flask

## Running
To run the app, run the approprate run script from your terminal (run.bash, run.bat, run.ps1).

### LookupError: unknown encoding: cp65001
See here: https://stackoverflow.com/questions/35176270/python-2-7-lookuperror-unknown-encoding-cp65001

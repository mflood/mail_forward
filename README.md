# mail_forward


## Starting up the service

### Running flask app locally in developer mode

> To run flask locally in non-production mode:

```bash
# Download the repo
git clone https://github.com/mflood/mail_forward

# Go into the flask_app directory
cd mail_forward/flask_app

# Set up the virtual environment
# (requires python3)
./setup.sh

# Start the flask server in developer mode
./run_flask_bare.sh
```

> Open a browser to [127.0.0.1:5000](127.0.0.1:5000)
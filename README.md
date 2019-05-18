# mail_forward

## Testing
```bash
# Download the repo
git clone https://github.com/mflood/mail_forward

# Go into the flask_app directory
cd mail_forward/flask_app

# Set up the virtual environment
# (requires python3)
./setup.sh

# Run pylint
./run_pylint.sh

# Run tests
./run_tests.sh

# Run tests with coverage
./run_coverage.sh
```


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

# set env variables for mailgun and mandrill
# or use noop as default service provider
vim envs.sh
source envs.sh

# Start the flask server in developer mode
./run_flask_bare.sh
```

> Open a browser to [http://127.0.0.1:5000](http://127.0.0.1:5000/)

### Running flask app locally in production mode with gunicorn

> To run flask locally using gunicorn

```bash
# Download the repo
git clone https://github.com/mflood/mail_forward

# Go into the flask_app directory
cd mail_forward/flask_app

# Set up the virtual environment
# (requires python3)
./setup.sh

# set env variables for mailgun and mandrill
# or use noop as default service provider
vim envs.sh
source envs.sh

# Start the flask server in developer mode
./run_flask_gunicorn.sh
```

> Open a browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Running flask app in a docker container

> To deploy and run the app in a docker container

```bash
# Download the repo
git clone https://github.com/mflood/mail_forward

# Go into the repo's root directory

cd mail_forward

# Build the docker image

./docker_build.sh

# Set enviroment variables for mailgun and mandrill

vim docker.env

# Run the docker image

./docker_run.sh
```

> Ensure the docker image is running

```bash
docker ps
```

> Find the image IP address
    
```bash
docker inspect <container id>
```

> Open a browser to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

> Note: We're running the docker version on 8000 instead of 5000

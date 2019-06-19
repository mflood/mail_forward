# mail_forward

Brightwheel Coding Challenge

## Language / Framework

> For this POC, I used python/flask since I am comfortable with Python and have used flask a few times before.  For testing I chose pytest since it easily works with flask apps and I like the fixtures features.  
> 
> For deployment, I chose 3 options.  First, running flask in developer mode, for just getting things up and running while developing. Second, running in production mode using gunicorn. Finally, I provide running within docker as an option since I have not used it before and decided to take this opportunity to learn.
> 
> Internally, I initially chose to use **requests** for making the API calls because the mailgun documentation used that. I soon discovered that it also has nice mock features that work with pytest, so it turned out to be a good choice.
> 
> Likewise, I got lucky with **html2text** as the first module I found that seemed to work nicely for converting HTML to text.


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

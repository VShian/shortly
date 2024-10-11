# Shortly

## Setup

Create virtual environment

```
python3 -m pip install virtualenv
python3 -m virtualenv env
source env/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run database migrations

```
python manage.py migrate
```

## Run local server

```
python manage.py runserver
```

## Deployment (Ubuntu)

Install supervisor

```
sudo apt update && sudo apt install supervisor
```

Install production dependencies

```
pip install -r requirements-prod.txt
```

Copy supervisor.conf file in to `/etc/supervisor/conf.d/`

_Note:_ Verify and update `command` and `directory` values in conf file if required

```
sudo cp supervisor.conf /etc/supervisor/conf.d/shortly.conf
```

Run start servers cript

```
./start-server.sh
```

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

## API
Endpoint: `/api/short-url`

#### **Examples:**

<details>
  <summary>  
    Create a new short URL
  </summary>

POST `/api/short-url`

Request

    {
        "url": "https://google.com"
    }

Response:

    {
        "short_url": "http://ip/r/64x/",
        "short_key": "64x",
        "url": "https://google.com"
    }

Status: 201

</details>

<details>
<summary>Get short URL by short key</summary>

GET `/api/short-url/64x`

Response:

    {
        "short_url": "http://ip/r/64x/",
        "short_key": "64x",
        "url": "https://google.com"
    }

Status: 200

</details>

<details>

<summary>Get short URL by URL (using POST data)</summary>

POST `/api/short-url`

_Note:_ This will create new short URL if it doesn't exist already. Use two GET methods if you don't want to create object when it does not exist.

Request:

    {
        "url": "https://google.com"
    }

Response:

    {
        "short_url": "http://ip/r/64x/",
        "short_key": "64x",
        "url": "https://google.com"
    }

Status: 200

</details>

<details>
<summary>Get short URL by URL (using GET query params)</summary>

GET `/api/short-url?url=https://google.com`

Response:

    {
        "short_url": "http://ip/r/64x/",
        "short_key": "64x",
        "url": "https://google.com"
    }

Status: 200
</details>

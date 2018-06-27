# A Bokeh starter app with Flask.


A non-trivial skeleton for an integrated flask-bokeh app running [bokeh sliders example](https://github.com/bokeh/bokeh/blob/master/examples/app/sliders.py) and [the Full Stack Python bokeh bars example](https://www.fullstackpython.com/blog/responsive-bar-charts-bokeh-flask-python-3.html).

Running on bokeh 0.13

To run:
* In one terminal:  `export FLASK_APP=application.py`, `flask run`.
* In another: `bokeh serve app/bokeh/sliders.py app/bokeh/bars.py --allow-websocket-origin=localhost:5000`



## Running through Nginx with SSL

To run behind a reverse proxy with SSL, we must direct flask traffic to gunicorn running on localhost:8000 and bokeh traffic to the bokeh server on localhost:5006. We also must change the addresses called with `server_document` in the route files, set up supervisor to run the servers, and we should copy the bokeh static assets into our application's static folder.

To get the bokeh plots to the 5006 server, we will prefix the bokeh app names in our routes with `/bokeh_plots`, we can then strip off the prefix in the Nginx config file.

#### 1) Change bokeh routes:
currently we call
`script = server_document("http://localhost:5006/bars")`
We now want to call
`script = server_document("https://example.com/bokeh_script/bars")`

#### 2) Nginx Config:
```
# redirect HTTP traffic to HTTPS
server {
    listen      80;
    server_name _;
    return      301 https://$server_name$request_uri;
}

server {
    listen      443 default_server;
    server_name _;

    # add Strict-Transport-Security to prevent man in the middle attacks
    add_header Strict-Transport-Security "max-age=31536000";

    ssl on;

    # SSL installation details will vary by platform
    ssl_certificate /home/ubuntu/application/certs/cert.pem;
    ssl_certificate_key /home/ubuntu/application/certs/key.pem;

    # enables all versions of TLS, but not SSLv2 or v3 which are deprecated.
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    # disables all weak ciphers
    ssl_ciphers "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GC$

    ssl_prefer_server_ciphers on;

    # All bokeh plots are prefixed with some unique route, in this case 'bokeh_plots'
    # Here we will collect these, strip off the prefix, and send the result to the bokeh server
    # Sends https://example.com/bokeh_plots/sliders ⇒ http://localhost:5006/sliders
    location /bokeh_plots  {
        rewrite  ^/bokeh_plots/(.*)  /$1 break;
        proxy_pass http://127.0.0.1:5006;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host:$server_port;
        proxy_buffering off;
    }

    # All traffic other than static and bokeh_plots goes to the gunicorn server
    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }


    location /static {
        # handle static files directly, without forwarding to the application
        alias /home/ubuntu/application/app/static;
        expires 30d;
    }
}
```

#### 3) Supervisor
We will want to run the bokeh and gunicorn servers with Supervisor. Bokeh serve needs to include the --use-xheaders tag to allow SSL.
```
; supervisor config file

[program:bokeh_apps]
command=/path/to/bokeh serve sliders.py bars.py --allow-websocket-origin=example.com --port=5006 --use-xheaders
directory=/home/ubuntu/application/app/bokeh
autostart=true
autorestart=true
startretries=3
numprocs=1
process_name=%(program_name)s_%(process_num)02d
stderr_logfile=/var/log/app-bokeh.err.log
stdout_logfile=/var/log/app-bokeh.out.log
user=ubuntu
environment=USER="ubuntu",HOME="/home/ubuntu",PATH="/path/to/env/bin"

[program:application]
command=/path/to/gunicorn application:app
directory=/home/ubuntu/application
stderr_logfile=/var/log/app-gunicorn.err.log
stdout_logfile=/var/log/app-gunicorn.out.log
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
environment=USER="ubuntu",HOME="/home/ubuntu",PATH="/path/to/env/bin"
```

# Authenticating Bokeh Sessions
Clearly if we put some effort into building something with user logins we won't want some regular old alices and bobs just navigating to example.com/bokeh_plots/plot and bypassing our lovely authentication system. To solve this we will serve bokeh with `--session-ids external-signed` [as documented here](https://bokeh.pydata.org/en/latest/docs/reference/command/subcommands/serve.html). 

This ensures that a valid session_id is present before doing anything, rather than just creating one at random on page startup. We will also serve with `--disable-index` which disables the otherwise handy index page of served plots.

We will need to change the route file again, now using server_session instead of server_document so we can include a generated session_id. It may now look something like this:
```
from bokeh.embed import server_session
from bokeh.util import session_id

from flask import render_template

from app.bokeh import bp


@bp.route('/sliders')
def sliders():
    s_id = session_id.generate_session_id()
    script = server_session(session_id=s_id, url="https://example.com/bokeh_plots/sliders")
    return render_template('base.html', plot_script=script)
```

Finally we will need to set 2 environment variables for both processes: `BOKEH_SECRET_KEY` and `BOKEH_SIGN_SESSIONS`. The secret key is used to generate and verify the session_id and SIGN_SESSIONS to indicate that it should be externally signed. This can be achieved first by generating a key with `bokeh secret` and then by adding both into the supervisor config file:

```environment=USER="ubuntu",HOME="/home/ubuntu",PATH="/home/ubuntu/anaconda3/envs/venv/bin",BOKEH_SECRET_KEY=asdfghjklpoiuytrewq,BOKEH_SIGN_SESSIONS=true```

# A Bokeh starter app with Flask.

A combination of [the Flask sliders example](https://github.com/bokeh/bokeh/blob/master/examples/app/sliders.py) and [the Full Stack Python bokeh/flask example](https://www.fullstackpython.com/blog/responsive-bar-charts-bokeh-flask-python-3.html).

Written as a not-quite-trivial example of getting a couple of these things running on a flask server to be later integrated into a full app.

Running on bokeh 0.12.13.

To run:
* In one terminal: `python app.py`.
* In another: `bokeh serve sliders.py bars.py --allow-websocket-origin=localhost:5000`

Currently still specifying the .py files to run, want to throw a directory at it really.
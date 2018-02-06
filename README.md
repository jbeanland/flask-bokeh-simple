# A Bokeh starter app with Flask.

A combination of [the Flask sliders example](https://github.com/bokeh/bokeh/blob/master/examples/app/sliders.py) and [the Full Stack Python bokeh/flask example](https://www.fullstackpython.com/blog/responsive-bar-charts-bokeh-flask-python-3.html).

Written as a not-quite-trivial example of getting one or two of these things running on a flask server to be later integrated into a full app.

Running on bokeh 0.12.13, so there's a good chance things will change soon enough.

To run:
* In one terminal: `python app.py`.
* In another: either `bokeh serve sliders.py --allow-websocket-origin=localhost:5000` or `bokeh serve bars.py --allow-websocket-origin=localhost:5000` depending on which one is wanted. 
* In app.py, in the `index` function, comment out the appropriate line to allow either `bars` or `sliders` to be received. (Not very elegant but will do for the time being).

Since this is a first version, only one can run at a time. Next job is to extend it to run multiple plots.
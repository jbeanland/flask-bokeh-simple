from flask import render_template
from bokeh.embed import server_document

from app.bokeh import bp


@bp.route('/')
@bp.route('/bars')
def bars():
    script = server_document("http://localhost:5006/bars")
    return render_template('base.html', plot_script=script)


@bp.route('/sliders')
def sliders():
    script = server_document("http://localhost:5006/sliders")
    return render_template('base.html', plot_script=script)

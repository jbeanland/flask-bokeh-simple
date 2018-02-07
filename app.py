from flask import Flask, render_template
from bokeh.embed import server_document

app = Flask(__name__)

@app.route('/')
@app.route('/bars')
def bars():
    script  = server_document("http://localhost:5006/bars")
    return render_template('base.html',plot_script=script)


@app.route('/sliders')
def sliders():
    script  = server_document("http://localhost:5006/sliders")
    return render_template('base.html',plot_script=script)


if __name__ == "__main__":
    app.run(debug=True)

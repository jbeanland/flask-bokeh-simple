from flask import Flask, render_template
from bokeh.embed import server_document

app = Flask(__name__)

@app.route("/")
def index():
    # script  = server_document("http://localhost:5006/sliders")
    script  = server_document("http://localhost:5006/bars")
    return render_template('chart.html',plot_script=script)

if __name__ == "__main__":
    app.run(debug=True)

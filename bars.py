import random
from bokeh.models import LinearAxis, Grid
from bokeh.models.glyphs import VBar
from bokeh.models.widgets import Slider
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import column
from config import Config

# Set up data
data_days = list(range(1, Config.BARS_MAX_DAYS+1))
data_bugs = [random.randint(1,100) for i in range(1, Config.BARS_MAX_DAYS + 1)]

x = data_days[:Config.BARS_DEFAULT_DAYS]
y = data_bugs[:Config.BARS_DEFAULT_DAYS]

source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
x_name='x'; y_name='y'; title='Bugs found per day'

plot = figure(title=title,
    plot_width=1200, plot_height=300,
    h_symmetry=False, v_symmetry=False, min_border=0,
    toolbar_location='above',
    sizing_mode='scale_width', outline_line_color='#666666'
    )

glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8, fill_color='#e12127')
plot.add_glyph(source, glyph)

xaxis=LinearAxis()
yaxis=LinearAxis()

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
plot.toolbar.logo = None
plot.min_border_top = 0
plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = '#999999'
plot.yaxis.axis_label = 'Bugs Found'
plot.ygrid.grid_line_alpha = .1
plot.xaxis.axis_label = "Days after app deployment"
plot.xaxis.major_label_orientation = 1

# Set up widget
bar_slider = Slider(title='Number of Days', value=Config.BARS_DEFAULT_DAYS, start=1, end=100, step=1)

# create callback function
def update_days(attrname, old, new):
    x = data_days[:bar_slider.value]
    y = data_bugs[:bar_slider.value]

    source.data = dict(x=x, y=y)

# listen for calllback function
bar_slider.on_change('value', update_days)

# set up layouts and add to document
curdoc().add_root(column([plot, bar_slider]))
curdoc().title = 'Chart'

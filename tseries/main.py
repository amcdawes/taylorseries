'''
A bokeh-based interface that demonstrates the Taylor series.
'''

import numpy as np

import numpy.random as random
import time
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput, Paragraph
from bokeh.plotting import figure

from scipy.interpolate import approximate_taylor_polynomial
from scipy import sin

xvals = np.linspace(-10,10)

def fitfunc(x):
    """Function to fit with Taylor series."""
    return sin(x)

yf = fitfunc(xvals)

x0 = 0
n = 2
scale = 0.5
tfit = approximate_taylor_polynomial(fitfunc,x0,n,scale)
yt = tfit(xvals)

# create bokeh data sources for the two graphs
fsource = ColumnDataSource(data=dict(x=xvals, y=yf))
tsource = ColumnDataSource(data=dict(x=xvals, y=yt))

# Set up plot
plot = figure(plot_height=400, plot_width=600, title="Series Approximation",
              tools="crosshair,pan,reset,save,wheel_zoom",y_range=[-2,2],x_range=[-6,6])

# colors are dark for use in the dark optics labs
#plot.background_fill_color = "black"
#plot.border_fill_color = "black"

# First plot
plot.line(x='x', y='y', source=fsource)

# Second plot
plot.line(x='x', y='y', source=tsource, color="red")


# Set up widgets to control scale of plots
# TODO change these to actual range sliders
n_slider = Slider(title="series order n", value=2, start=1, end=10, step=1)
x0_slider = Slider(title="expansion point x_0", value=0.0, start=-1.0, end=1.0, step=0.1)


def update_data():

    tfit = approximate_taylor_polynomial(fitfunc,x0,n,scale)
    yt = tfit(xvals - x0)

    tsource.data = dict(x=xvals, y=yt)
    fsource.data = dict(x=xvals, y=yf)

def update_values(attrname, old, new):
    global n
    global x0

    # Get the current slider values
    n = n_slider.value
    x0 = x0_slider.value


# Add on_change listener to each widget that we're using:
for w in [n_slider, x0_slider]:
    w.on_change('value', update_values)


# Set up layouts and add to document
controls = widgetbox(n_slider, x0_slider)

# build the app document, this is just layout control and arranging the interface
curdoc().add_root(row(controls, plot, width=1800))
curdoc().title = "Taylor Series"

# set the callback to pull the data every 100 ms:
curdoc().add_periodic_callback(update_data, 100)

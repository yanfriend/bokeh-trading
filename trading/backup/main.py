from math import pi

from numpy import asarray, cumprod, convolve, exp, ones
from numpy.random import lognormal, gamma, uniform
import random
from bokeh.models.widgets import Button

from bokeh.layouts import row, column, gridplot
from bokeh.models import ColumnDataSource, Slider, Select, Range1d
from bokeh.plotting import curdoc, figure
from bokeh.driving import count
from bokeh.models.widgets import PreText # use tables https://github.com/bokeh/bokeh/blob/master/bokeh/models/widgets/tables.py

BUFSIZE = 200
MA12, MA26, EMA12, EMA26 = '12-tick Moving Avg', '26-tick Moving Avg', '12-tick EMA', '26-tick EMA'

source = ColumnDataSource(dict(
    time=[], low=[], high=[], open=[], close=[],
    color=[],
    time1=[], noop=[]
))



p2 = figure(plot_height=250, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="right")
p2.x_range.follow = "end"
p2.x_range.follow_interval = 100
p2.x_range.range_padding = 0


p = figure(
    # width=800,
    plot_width=1000,
    plot_height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset", x_axis_type=None,
           y_axis_location="right",
    x_range = p2.x_range
)
# p.x_range.follow = "end"
# p.x_range.follow_interval = 100
# p.x_range.range_padding = 0

# p.line(x='time', y='average', alpha=0.2, line_width=3, color='navy', source=source)
# p.line(x='time', y='ma', alpha=0.8, line_width=2, color='orange', source=source)
p.segment(x0='time', y0='low', x1='time', y1='high', line_width=2, color='black', source=source)
p.segment(x0='time', y0='open', x1='time', y1='close', line_width=8, color='color', source=source)
# p.line(x='time1', y='noop', line_width=10, color='color', source=source)

# p.segment(x0='time', y0='high', x1='time', y1='low', color='black', source=source)


# p2.line(x='time', y='noop', line_width=10, color='color', source=source)


# p2 = figure(plot_height=250, x_range=p.x_range, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="right")
# p2.line(x='time', y='macd', color='red', source=source)
# p2.line(x='time', y='macd9', color='blue', source=source)
# p2.segment(x0='time', y0=0, x1='time', y1='macdh', line_width=6, color='black', alpha=0.5, source=source)

mean = Slider(title="mean", value=0, start=-0.01, end=0.01, step=0.001)
stddev = Slider(title="stddev", value=0.04, start=0.01, end=0.1, step=0.01)
mavg = Select(value=MA12, options=[MA12, MA26, EMA12, EMA26])

stats = PreText(text='', width=500)

def _create_prices(t):
    # last_average = 100 if t == 0 else source.data['average'][-1]
    returns = asarray(lognormal(mean.value, stddev.value, 1))
    rnd = random.randint(1, 10)
    average = rnd * cumprod(returns)
    high = rnd * exp(abs(gamma(1, 0.03, size=1)))
    low = rnd / exp(abs(gamma(1, 0.03, size=1)))
    delta = high - low
    open = low + delta * uniform(0.05, 0.95, size=1)
    close = low + delta * uniform(0.05, 0.95, size=1)
    return open[0], high[0], low[0], close[0] # , average[0]


@count()
def update(t):
    print 'ttttttttttttttttttt', t

    open, high, low, close = _create_prices(t)
    color = "green" if open < close else "red"

    stats.text = str(close)

    new_data = dict(
        time=[t],
        open=[open],
        high=[high],
        low=[low],
        close=[close],
        # average=[average],
        color=[color],
        time1=[t+1],
        noop=[(high+low)/2]
    )

    print new_data
    source.stream(new_data, 300)

    # p.x_range = Range1d(max(1,t+1-900), t+1) # not work


curdoc().title = "Trading"

# curdoc().add_periodic_callback(update, 50)

button = Button(label='Next Bar')
button.on_click(update)

curdoc().add_root(row(
    column(
        # row(mean, stddev, mavg),
        # gridplot([[p]], toolbar_location="left", plot_width=1200)),
        gridplot([[p], [p2]], toolbar_location="left", plot_width=1000)),
    column(stats, button)
)
)

for _ in xrange(69):  # number in chartgame.com
    update()

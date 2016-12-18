from numpy import asarray, cumprod, convolve, exp, ones
from numpy.random import lognormal, gamma, uniform
import random

from bokeh.layouts import row, column, gridplot
from bokeh.models import ColumnDataSource, Slider, Select
from bokeh.plotting import curdoc, figure
from bokeh.driving import count
from bokeh.models.widgets import Button
from bokeh.models.widgets import PreText


source = ColumnDataSource(dict(
    time=[], average=[], low=[], high=[], open=[], close=[], color=[], # todo, remove average
    volume=[],
    trade_time=[], trade_price=[]
))

p_aux = figure(plot_height=50, tools="xpan,xwheel_zoom,xbox_zoom,reset", x_axis_type=None, y_axis_location="right")
p_aux.x_range.follow = "end"
p_aux.x_range.follow_interval = 100
p_aux.x_range.range_padding = 0
p_aux.line(x='time', y=0, color='green', source=source)

p_main = figure(plot_height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="right")
p_main.segment(x0='time', y0='low', x1='time', y1='high', line_width=2, color='black', source=source)
p_main.segment(x0='time', y0='open', x1='time', y1='close', line_width=8, color='color', source=source)

# position_line = p_main.line([],[], line_width=1)
# ds_pos = position_line.data_source

# p_main.circle(x='trade_time', y='trade_price', size=20, color="navy", alpha=0.5, source=source)
p_main.circle(x='trade_time', y='trade_price', size=20, color="navy", alpha=0.5, source=source)


p_vol = figure(plot_height=150, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="right")
p_vol.segment(x0='time', y0=0, x1='time', y1='volume', line_width=8, color="color", source=source)

stats = PreText(text='', width=500)

def _create_prices(t):
    last_average = 100 if t==0 else source.data['average'][-1]
    returns = asarray(lognormal(0, 0.04, 1))
    average =  last_average * cumprod(returns)
    high = average * exp(abs(gamma(1, 0.03, size=1)))
    low = average / exp(abs(gamma(1, 0.03, size=1)))
    delta = high - low
    open = low + delta * uniform(0.05, 0.95, size=1)
    close = low + delta * uniform(0.05, 0.95, size=1)
    return open[0], high[0], low[0], close[0], average[0]

@count()
def update(t):
    open, high, low, close, average = _create_prices(t)
    volume = random.randint(100, 1000)

    color = "green" if open < close else "red"

    nan = float('nan')

    trade_time=t
    if t==60:
        trade_price=close
    else:
        trade_price='NaN' # nan

    new_data = dict(
        time=[t],
        # time1=[t-1],
        open=[open],
        high=[high],
        low=[low],
        close=[close],
        average=[average],
        color=[color],
        volume=[volume],

        trade_time=[trade_time],
        trade_price=[trade_price],
    )
    stats.text = str(close)

    source.stream(new_data, 69)

    # ds_pos.data['x'].append(t) # this way has issues.
    # ds_pos.data['y'].append(100)
    # ds_pos.trigger('data', ds_pos.data, ds_pos.data)
    #




button = Button(label='Next Bar')
button.on_click(update)

curdoc().add_root(row(
    column(
        gridplot([[p_main], [p_vol], [p_aux]], toolbar_location="left", plot_width=1000)),
    column(stats, button)
)
)

# curdoc().add_periodic_callback(update, 300)
curdoc().title = "iTrade"

for _ in xrange(69):  # number in chartgame.com
    update()

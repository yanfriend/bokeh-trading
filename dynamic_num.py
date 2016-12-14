from bokeh.plotting import figure, curdoc
from bokeh.palettes import RdYlBu3
from bokeh.models.widgets import Button
from bokeh.layouts import column
import numpy as np

# create a plot and style its properties
p = figure(x_range=(0, 100),
y_range=(0, 100),
toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None
# add a text renderer to out plot (no data yet)
r = p.text(x=[], y=[], text=[], text_color=[],
text_font_size="20pt",
text_baseline="middle",
text_align="center")

i = 0
rnd = np.random.random
ds = r.data_source
def callback():
 global i
 ds.data['x'].append(rnd()*70 + 15)
 ds.data['y'].append(rnd()*70 + 15)
 ds.data['text_color'].append(RdYlBu3[i%3])
 ds.data['text'].append(str(i))
 ds.trigger('data', ds.data, ds.data)
 i = i + 1
# add a button widget and configure with the
# call back
button = Button(label='Press Me')
button.on_click(callback)
# put everything a layout & to the document
curdoc().add_root(column(button, p))

# to run: bokeh serve --show  test2.py

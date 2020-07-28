import bokeh
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
import forecast
import numpy as np

def plot_forecast(x,json_output,quantity,units,color):
    
    h = bokeh.models.tools.HoverTool(
        tooltips=[
            (quantity, '$y{1.f}'+f'{units}'),
            ('Time (UTC)','@x{%I %p %F}'),
        ],

        formatters={
            '@x'        : 'datetime', # use 'datetime' formatter for '@date' field
                                         # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    
    p = bokeh.models.tools.PanTool()
    s = bokeh.models.tools.SaveTool()

    fig = figure(x_axis_type='datetime', title=f'{quantity} ({units})', x_range=(x[1], x[120]),
                 tools = [h,p,s],
                 height=300,width=600, toolbar_location="below",)


    fig.varea(x=x[1:],
              y1 = forecast.c_to_f(np.array(json_output['forecast'][quantity.lower()]['min_poss'][1:],dtype=float)),
              y2 = forecast.c_to_f(np.array(json_output['forecast'][quantity.lower()]['max_poss'][1:],dtype=float)),
              fill_color='#D1D1D1',
              alpha=0.5
             )

    fig.line(x=x[1:],y=forecast.c_to_f(np.array(json_output['forecast'][quantity.lower()]['best_guess'][1:],dtype=float)),
             line_color=color,line_width=3,)

    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_width = 0.5

    output_file(f'{quantity.lower()}.html')

    show(fig)
#from motion_detector import df
import motion_detector
from bokeh.plotting import figure,show,output_file

p = figure(x_axis_type = "datetime",height = 100, width = 500, title = "Motion Graph",toolbar_location = "above")
p.yaxis.minor_tick_line_color = None
p.ygrid[0].grid_line_alpha = 0


p.quad(left = motion_detector.df["start"], right = motion_detector.df["end"], top = 1, bottom = 0, color = "green")

output_file("Motion_graph.html")
show(p)

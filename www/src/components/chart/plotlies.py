# Description: Plotly chart components.

from components.chart.plotly.area_line_chart import AreaLineChart
from components.chart.plotly.bar_chart import BarChart
from components.chart.plotly.line_chart import LineChart
from components.chart.plotly.pie_chart import PieChart
from components.chart.chart_model import ChartModel

charts = {
    "ChartModel": ChartModel,
    "AreaLineChart": AreaLineChart,
    "BarChart": BarChart,
    "LineChart": LineChart,
    "PieChart": PieChart,
}

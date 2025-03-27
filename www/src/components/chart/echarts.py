# Description: EChart components.

from components.chart.echart.bar_chart import BarChart
from components.chart.echart.line_chart import LineChart
from components.chart.echart.pie_chart import PieChart
from components.chart.chart_model import ChartModel

charts = {
    "ChartModel": ChartModel,
    "LineChart": LineChart,
    "BarChart": BarChart,
    "PieChart": PieChart,
}

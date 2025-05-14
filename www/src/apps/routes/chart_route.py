import pandas as pd
from flask import Blueprint, json, render_template, request
from pathlib import Path
from apps.service import chart_service
from apps.model.response.chart_response import ChartResponse
from components import echart as ec

template_path = Path(__file__).parent.parent / "templates"
echart_route = Blueprint('echart', __name__, template_folder=template_path)

# Echarts

@echart_route.route("/<chart_id>", methods=['POST', 'GET'])
def show_echart(chart_id):
    ''' show echart chart '''
    try:
        _database = json.loads(request.form.get('database'))
        _endpoint = request.form.get('link', '')
        chart_response = chart_service.get_chart_data(_endpoint, _database.get('customer_code',''), _database.get('dbid',0))
        if chart_response.status_code == 200:
            ds_json = chart_response.json()
            if ds_json:
                ds_json["chart_model"]["id"] = chart_id 
                chart_info = ChartResponse(**ds_json) 
                chart_model = ec.ChartModel(id=chart_id, type=chart_info.chart_model.type, title=chart_info.chart_model.title, x_axis=chart_info.chart_model.x_axis, y_axis=chart_info.chart_model.y_axis)
                df = pd.DataFrame(chart_info.data)

                if chart_info.chart_model.type == "line":
                    chart = ec.LineChart(chart_model, df)
                    html = chart.render(horizontal=False, show_label=False)
                elif chart_info.chart_model.type =="bar":
                    chart = ec.BarChart(chart_model, df)
                    html = chart.render(horizontal=False, show_label=False)
                else: 
                    chart = ec.PieChart(chart_model, df)
                    html = chart.render(donut=True)
                return render_template("chart_detail.html", graph_html=html, title=chart.chart_model.title)
            else:
                return render_template("error.html")
        
    except Exception as e:
        return render_template("error.html", title=f"Error{e}")

# import pandas as pd
# from flask import Blueprint, render_template, request
# from pathlib import Path
# from components import echart as ec
# from components.chart.chart_model import ChartModel, ChartSize
# from sample.fake_data import FakeData
# 0
# template_path = Path(__file__).parent.parent / "templates"
# echart_route = Blueprint('echart', __name__, template_folder=template_path)

# # Echarts
# @echart_route.route("/<chart_id>")
# def show_echart(chart_id):
#     ''' show echart chart '''
#     try:
#         # Lấy dữ liệu giả từ FakeData thay vì gọi API
#         df = FakeData.generate_data(2023, 2025)
        
#         # Chuẩn bị dữ liệu cho các loại biểu đồ khác nhau
#         chart_type = request.args.get("type", "line")  # Mặc định là biểu đồ đường
        
#         # Xác định các tham số của biểu đồ dựa trên loại biểu đồ
#         if chart_type == "line":
#             # Tạo dữ liệu cho biểu đồ đường theo thời gian
#             # Tính trung bình Revenue và Cost theo từng tháng
#             df['Month'] = df['Date'].dt.strftime('%Y-%m')
#             monthly_data = df.groupby('Month')[['Revenue', 'Cost']].mean().reset_index()
            
#             chart_model = ChartModel(
#                 id=chart_id,
#                 type="line",
#                 title="Doanh thu và Chi phí theo tháng",
#                 x_axis="Month",
#                 y_axis=["Revenue", "Cost"],
#                 show_title=True,
#                 show_legend=True,
#                 show_grid=True,
#                 size=ChartSize(width=800, height=400)
#             )
            
#             chart = ec.LineChart(chart_model, monthly_data)
#             html = chart.render(horizontal=False, show_label=False)
            
#         elif chart_type == "bar":
#             # Tạo dữ liệu cho biểu đồ cột theo thành phố
#             city_data = df.groupby('City')[['Revenue', 'Cost']].sum().reset_index()
            
#             chart_model = ChartModel(
#                 id=chart_id,
#                 type="bar",
#                 title="Tổng doanh thu và Chi phí theo Thành phố",
#                 x_axis="City",
#                 y_axis=["Revenue", "Cost"],
#                 show_title=True,
#                 show_legend=True,
#                 show_grid=True,
#                 size=ChartSize(width=800, height=400)
#             )
            
#             chart = ec.BarChart(chart_model, city_data)
#             html = chart.render(horizontal=False, show_label=False)
            
#         else:  # pie chart
#             # Tạo dữ liệu cho biểu đồ tròn theo sản phẩm
#             item_data = df.groupby('Item')['Revenue'].sum().reset_index()
            
#             chart_model = ChartModel(
#                 id=chart_id,
#                 type="pie",
#                 title="Tỷ lệ doanh thu theo Sản phẩm",
#                 x_axis="Item",
#                 y_axis=["Revenue"],
#                 show_title=True,
#                 show_legend=True,
#                 show_grid=True,
#                 size=ChartSize(width=800, height=400)
#             )
            
#             chart = ec.PieChart(chart_model, item_data)
#             html = chart.render(donut=True)
        
#         return render_template("chart_detail.html", graph_html=html, title=chart_model.title)
#     except Exception as e:
#         return render_template("error.html", title="Error", error=str(e))
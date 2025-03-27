# Description: Line chart component using Plotly library
import plotly.express as px
from components.chart.plotly.base_chart import Chart


class LineChart(Chart):

    def render(self):
        try:
            x_column = self.chart_model.x_axis
            y_columns = self.chart_model.y_axis

            # Tạo DataFrame con chỉ chứa các cột cần thiết
            required_columns = [x_column] + y_columns
            filtered_df = self.data[required_columns]

            fig = px.line(filtered_df, x=x_column, y=y_columns, title=self.chart_model.title)
            fig.update_layout(
                showlegend=self.chart_model.show_legend,
                title= self.chart_model.title if self.chart_model.show_title else None,
                xaxis=dict(showgrid=self.chart_model.show_grid),
                yaxis=dict(showgrid=self.chart_model.show_grid)
            )
            self.html = fig.to_html(full_html=False)
            return self.html
        except Exception as e:
            raise e
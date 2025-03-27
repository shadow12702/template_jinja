# This file contains the AreaLineChart class which is responsible for rendering area line charts using Plotly.
import plotly.express as px

from components.chart.plotly.base_chart import Chart

class AreaLineChart(Chart):
    def render(self, stacked=False, color_map=None):
        try:
            x_column = self.chart_model.x_axis
            y_columns = self.chart_model.y_axis

            # create a sub DataFrame containing only the required columns
            required_columns = [x_column] + y_columns
            filtered_df = self.data[required_columns]

            # format data for area chart
            df_long = filtered_df.melt(id_vars=[x_column], value_vars=y_columns, var_name="Series", value_name="Value")

            # Build area chart
            fig = px.area(df_long, x=x_column, y="Value", color="Series", title=self.chart_model.title)

            # change color
            if color_map:
                fig.update_traces(marker=dict(colors=[color_map.get(series, None) for series in df_long["Series"]]))

            # update layout
            fig.update_layout(
                showlegend=self.chart_model.show_legend,
                title=self.chart_model.title if self.chart_model.show_title else None,
                xaxis=dict(showgrid=self.chart_model.show_grid),
                yaxis=dict(showgrid=self.chart_model.show_grid),
                barmode="stack" if stacked else "overlay"
            )

            self.html = fig.to_html(full_html=False)
            return self.html
        except Exception as e:
            raise e

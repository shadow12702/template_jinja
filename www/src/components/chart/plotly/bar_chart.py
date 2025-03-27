# Description: Bar chart component using Plotly library.
import plotly.express as px
from components.chart.plotly.base_chart import Chart

class BarChart(Chart):

    def render(self, stacked:bool=False, horizontal:bool=False):
        try:
            x_column = self.chart_model.x_axis
            y_columns = self.chart_model.y_axis

            # get required columns
            required_columns = [x_column] + y_columns
            new_df = self.data.groupby(x_column)[y_columns].sum().reset_index()
            new_df = new_df[required_columns]

            # Format data for bar chart
            if len(y_columns) > 1:
                new_df = new_df.melt(id_vars=[x_column], value_vars=y_columns, var_name="Series", value_name="Value")

            # Chart orientation and barmode
            orientation = "h" if horizontal else "v"  #(vertical) or (horizontal)
            barmode = "stack" if stacked else "group"  # Stack or Group

            # Build chart
            fig = px.bar(new_df, 
                         x=x_column if not horizontal else "Value",
                         y="Value" if not horizontal else x_column,
                         color="Series" if len(y_columns) > 1 else None,
                         title=self.chart_model.title,
                         orientation=orientation)

            # update layout
            fig.update_layout(
                barmode=barmode, 
                showlegend=self.chart_model.show_legend,
                title=self.chart_model.title if self.chart_model.show_title else None,
                xaxis=dict(showgrid=self.chart_model.show_grid),
                yaxis=dict(showgrid=self.chart_model.show_grid)
            )

            self.html = fig.to_html(full_html=False)
            return self.html
        except Exception as e:
            raise e

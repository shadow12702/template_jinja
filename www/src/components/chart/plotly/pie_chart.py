# Description: Pie chart using Plotly

import pandas as pd
import plotly.express as px

from components.chart.plotly.base_chart import Chart

class PieChart(Chart):

    def render(self, color_map=None, threshold=0.05, group_other_name="Others"):
        try:
            if len(self.chart_model.y_axis) != 1:
                raise ValueError("Pie chart requires exactly one y_axis (value).")

            category_col = self.chart_model.x_axis
            value_col = self.chart_model.y_axis[0]

            # Tạo DataFrame con chỉ chứa các cột cần thiết
            new_df = self.data.groupby(category_col)[value_col].sum().reset_index()
            total = new_df[value_col].sum()
            new_df["percentage"] = new_df[value_col] / total

            # Group small values into "Others"
            mask = new_df["percentage"] < threshold
            others_value = new_df.loc[mask, value_col].sum()

            if others_value > 0:
                new_df = new_df.loc[~mask]
                new_df = new_df.concat([new_df, pd.DataFrame({category_col: [group_other_name], value_col: [others_value]})], ignore_index=True)
            
            # Build Pie Chart
            fig = px.pie(new_df, names=category_col, values=value_col, title=self.chart_model.title)

            # change the color of the pie chart
            if color_map:
                fig.update_traces(marker=dict(colors=[color_map.get(cat, None) for cat in new_df[category_col]]))

            self.html = fig.to_html(full_html=False)
            return self.html
        except Exception as e:
            raise e

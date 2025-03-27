import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts
from components.chart.echart.base_chart import Chart

class PieChart(Chart):

    def render(self, threshold =0.05, donut:bool=False, group_other_name:str="Others", show_label:bool=False):
        try:
            if len(self.chart_model.y_axis) != 1:
                raise ValueError("Pie chart requires exactly one y_axis (value).")
            
            category_col = self.chart_model.x_axis
            value_col = self.chart_model.y_axis[0]

            # Create a DataFrame with only the required columns
            new_df = self.data.groupby(category_col)[value_col].sum().reset_index()
            total = new_df[value_col].sum()
            new_df["percentage"] = new_df[value_col] / total

            # Group small values into "Others"
            mask = new_df["percentage"] < threshold
            others_value = new_df.loc[mask, value_col].sum()

            if others_value > 0:
                new_df = new_df.loc[~mask]
                new_df = new_df.concat([new_df, pd.DataFrame({category_col: [group_other_name], value_col: [others_value]})], ignore_index=True)
                
            data_present = new_df[[category_col, value_col]].values.tolist()
            # Create a Pie chart
            pie = Pie(init_opts=opts.InitOpts(width="100%", height=f"{self.chart_model.size.height}px"))
            pie.add("", data_present, 
                    radius = ["40%", "75%"] if donut else "55%",
                    label_opts=opts.LabelOpts(is_show=show_label, 
                                            #   formatter="{b}: {d}%"
                                              ),
                )
            pie.set_global_opts(title_opts=opts.TitleOpts(title=self.chart_model.title if self.chart_model.show_title else ""),
                                legend_opts=opts.LegendOpts(is_show=self.chart_model.show_legend))
            self.html = pie.render_embed()
            
                # div_style=f"{self.chart_model.size.width}px", f"{self.chart_model.size.height}px")
            return self.html
        except Exception as e:
            raise e
from pyecharts.charts import Bar
from pyecharts import options as opts
from components.chart.echart.base_chart import Chart

class BarChart(Chart):

    def render(self, stacked=False, horizontal=False, show_label:bool=False):
        try:
            bar = Bar(init_opts=opts.InitOpts(width=f"100%", height=f"{self.chart_model.size.height}px"))
            new_df = self.data.groupby(self.chart_model.x_axis)[self.chart_model.y_axis].sum().reset_index()
            categories = new_df[self.chart_model.x_axis].to_list()
            
            bar.add_xaxis(categories)
            for column in self.chart_model.y_axis:
                bar.add_yaxis(column, new_df[column].to_list(), stack='stacked' if stacked else None,
                                label_opts=opts.LabelOpts(is_show=show_label),)   
            if horizontal:
                bar.reversal_axis()
            
            bar.set_global_opts(title_opts=opts.TitleOpts(title=self.chart_model.title),
                                toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                            feature={"dataView": {"readOnly": True},
                                                                    "magicType": {"show": True, 
                                                                                    "title": ["Biểu đồ đường", "Biểu đồ cột", "Xếp chồng"],
                                                                                    "type": ["line", "bar","stack"]},
                                                                    }),
                                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                                legend_opts=opts.LegendOpts(is_show=self.chart_model.show_legend),
                                xaxis_opts=opts.AxisOpts(is_show=self.chart_model.show_grid),
                                yaxis_opts=opts.AxisOpts(is_show=self.chart_model.show_grid))
            self.html = bar.render_embed()
            return self.html
        except Exception as e:
            raise e
        
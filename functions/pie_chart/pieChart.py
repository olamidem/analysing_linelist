import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
import streamlit.components.v1 as components


def pie_chart_value(art_start):
    male = art_start.query('Sex == "M"')
    female = art_start.query('Sex == "F"')
    pieChart = {'Name': ['MALE', 'FEMALE'],
                'values': [male['Sex'].count(), female['Sex'].count()]}
    pieChart = pd.DataFrame(pieChart)
    return pieChart


def pie_chart_display(pieChart):
    p = (
        Pie(init_opts=opts.InitOpts(width="900px", height="500px"))
            .add(
            "",
            [list(z) for z in zip(pieChart['Name'], pieChart['values'])],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Tx_New by Sex"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="10%", pos_right="%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)", font_size=15)
                             )
            .render_embed()
    )
    components.html(p, width=900, height=500)
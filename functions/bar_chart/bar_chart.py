from pyecharts.charts import Bar
from pyecharts import options as opts
import streamlit.components.v1 as components

def bar_chart_display(female, male):
    age_disaggregation = ['<1', '1-4', '5-9', '10-14',
                          '15-19', '20-24', '25-29',
                          '30-34', '35-39', '40-44', '45-49', '50+']
    c = (
        Bar()
            .add_xaxis(age_disaggregation)
            .add_yaxis("MALE", male, gap="15%")
            .add_yaxis("FEMALE", female, gap="15%")
            .set_global_opts(title_opts=opts.TitleOpts(title="Sex and Age Group", subtitle="CURRENT AGE"))
            .render_embed()
    )
    components.html(c, height=500, width=1000)
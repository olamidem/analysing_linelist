import streamlit.components.v1 as components
from pyecharts import options as opts
from pyecharts.charts import Bar


def bar_chart_display(female, male):
    age_disaggregation = ['<1', '1-4', '5-9', '10-14',
                          '15-19', '20-24', '25-29',
                          '30-34', '35-39', '40-44', '45-49', '50+']
    c = (
        Bar()
            .add_xaxis(age_disaggregation)
            .add_yaxis("MALE", male, gap="15%")
            .add_yaxis("FEMALE", female, gap="15%")
            .extend_axis(
            # yaxis=opts.AxisOpts(
            #     name="Percentage %",
            #     type_="value",
            #     min_=0,
            #     max_=100,
            #     position="right",
            #     axisline_opts=opts.AxisLineOpts(
            #         linestyle_opts=opts.LineStyleOpts(color="green")
            #     ),
            #     axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            #     splitline_opts=opts.SplitLineOpts(
            #         is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            #     ),
            # )
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Sex and Age Group", subtitle="CURRENT AGE"))
            .render_embed()
    )

    components.html(c, height=500, width=1000)


def pregnant_breastfeeding_barchart(breastfeeding, pregnant):
    age_disaggregation = ['15-19', '20-24', '25-29',
                          '30-34', '35-39', '40-44', '45-49', '50+']
    pregnant_breastfeeding = (
        Bar()
            .add_xaxis(age_disaggregation)
            .add_yaxis("PREGNANT", pregnant, gap="15%", color='rgb(23, 108, 54)')
            .add_yaxis("BREASTFEEDING", breastfeeding, gap="15%", color='rgb(148, 124, 45)')
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Sex and Age Group", subtitle="Current Pregnancy Status"))
            .render_embed()
    )
    components.html(pregnant_breastfeeding, height=500, width=1000)


def bar_chart_suppressed_vl(female, male):
    age_disaggregation = ['<1', '1-4', '5-9', '10-14',
                          '15-19', '20-24', '25-29',
                          '30-34', '35-39', '40-44', '45-49', '50+']
    c = (
        Bar()
            .add_xaxis(age_disaggregation)
            .add_yaxis("MALE", male, gap="15%")
            .add_yaxis("FEMALE", female, gap="15%")
            .extend_axis(
            yaxis=opts.AxisOpts(
                name="Percentage %",
                type_="value",
                min_=0,
                max_=100,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="green")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Sex and Age Group", subtitle="CURRENT AGE"))

            .render_embed()
    )

    components.html(c, height=500, width=1000)

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie

def pieChart_values(Current_TB_Status_count, cd4_count_result, ipt_screening, pbs_count, tbDocumented_result_count,
                    transferIn_count, tx_new_count):
    pieChart = {'Name': ["TX_NEW", "TRANSFER IN", "PBS", "CD4 COUNT", "TB SCREENING",
                         "TB SUSPECT", "DOCUMENTED TB RESULTS"],
                'values': [tx_new_count, transferIn_count, pbs_count, cd4_count_result,
                           ipt_screening, Current_TB_Status_count, tbDocumented_result_count]}
    pieChart = pd.DataFrame(pieChart)
    return pieChart

def pieChart_dsiplay(pieChart):
    p = (
        Pie(init_opts=opts.InitOpts(width="900px", height="500px"))
            .add(
            "",
            [list(z) for z in zip(pieChart['Name'], pieChart['values'])],
            radius=["40%", "75%"],
        )
        #     .set_global_opts(
        #     title_opts=opts.TitleOpts(title="TREATMENT NEW"),
        #     # legend_opts=opts.LegendOpts(orient="vertical", pos_top="10%", pos_right="%"),
        # )

            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=15)

                             )
            .render_embed()
    )
    return p

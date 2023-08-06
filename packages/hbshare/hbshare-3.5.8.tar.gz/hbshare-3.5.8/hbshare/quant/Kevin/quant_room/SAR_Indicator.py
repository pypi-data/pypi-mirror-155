"""
SAR Indicator
"""
import pandas as pd
import numpy as np
import talib
import hbshare as hbs
from pyecharts import options as opts
from pyecharts.charts import Kline, Scatter
from pyecharts.commons.utils import JsCode


color_function = """
        function (params) {
            if (params.data.sign > 0) {
                return 'green';
            } else 
            return 'red';
        }
        """


def plot_kline(df):
    kline = (
        Kline(init_opts=opts.InitOpts(width="1600px", height="600px"))
        .add_xaxis(xaxis_data=list(df.index))
        .add_yaxis(
            series_name="klines",
            y_axis=df[['TOPEN', 'TCLOSE', 'LOW', 'HIGH']].values.tolist(),
            itemstyle_opts=opts.InitOpts())
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True, pos_bottom=10, pos_left="center"),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    xaxis_index=[0],
                    range_start=80,
                    range_end=100),
                opts.DataZoomOpts(
                    is_show=True,
                    type_="slider",
                    xaxis_index=[0],
                    pos_top="85%",
                    range_start=80,
                    range_end=100)
            ],
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color="rgba(245, 245, 245, 0.8)",
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color="#000")
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=5,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": "#00da3c"},
                    {"value": -1, "color": "#ec0000"}
                ]
            ),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                link=[{"xAxisIndex": "all"}],
                label=opts.LabelOpts(background_color="#777")
            ),
            brush_opts=opts.BrushOpts(
                x_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX"
            )))

    tmp = data.rename(columns={"sar": "value"})[['value', 'sign']].to_dict(orient="records")

    scatter = (
        Scatter(init_opts=opts.InitOpts(width="1600px", height="600px"))
        .add_xaxis(xaxis_data=list(df.index))
        .add_yaxis(
            series_name="sar",
            # y_axis=df['sar'].values.tolist(),
            y_axis=tmp,
            symbol_size=6,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
        )
        .set_series_opts()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    xaxis_index=[0],
                    range_start=80,
                    range_end=100),
                opts.DataZoomOpts(
                    is_show=True,
                    type_="slider",
                    xaxis_index=[0],
                    pos_top="85%",
                    range_start=80,
                    range_end=100)
            ]))

    kline.overlap(scatter).render('D:\\kline.html')


# 数据,以日线做实验
start_date = '20211231'
end_date = '20220616'
ticker = '688006'

sql_script = "SELECT SYMBOL, TDATE, TOPEN, TCLOSE, HIGH, LOW FROM finchina.CHDQUOTE WHERE " \
             "SYMBOL = {} and TDATE >= {} and TDATE <= {}".format(ticker, start_date, end_date)
data = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])
data['TDATE'] = data['TDATE'].astype(str)
sar = talib.SAR(data.HIGH, data.LOW)
data['sar'] = sar
data = data.set_index('TDATE').dropna()[['TOPEN', 'TCLOSE', 'LOW', 'HIGH', 'sar']].round(2)

# color
sign_list = []
for i in range(data.shape[0]):
    t_date = data.index[i]
    if i == 0:
        sign = 1 if data.loc[t_date, 'sar'] > data.loc[t_date, 'HIGH'] else -1
        sign_list.append(sign)
        continue
    else:
        pre_sign = sign_list[i - 1]
        if pre_sign == 1:
            sign = 1 if data.loc[t_date, 'sar'] > data.loc[t_date, 'HIGH'] else -1
        else:
            sign = 1 if data.loc[t_date, 'sar'] > data.loc[t_date, 'HIGH'] else -1
        sign_list.append(sign)

data['sign'] = sign_list

plot_kline(data)

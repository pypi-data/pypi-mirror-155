"""
alpha标的超额回测模块
"""
import pandas as pd
import numpy as np
from datetime import datetime
import os
import hbshare as hbs
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_trading_day_list
from Arbitrage_backtest import cal_annual_return, cal_annual_volatility, cal_sharpe_ratio, cal_max_drawdown
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params, style_names, industry_names
from plotly.offline import plot as plot_ly
import statsmodels.api as sm
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
plt.style.use('seaborn')


class AlphaBacktest:
    def __init__(self, data_path, start_date, end_date, mode="ratio"):
        self.data_path = data_path
        self.start_date = start_date
        self.end_date = end_date
        self.mode = mode
        self._load_data()

    def _load_data(self):
        data_with_header = pd.read_excel(
            os.path.join(self.data_path, r"指增-{}.xlsx".format(self.end_date)), sheet_name='原始净值')
        data = pd.read_excel(
            os.path.join(self.data_path, "指增-{}.xlsx".format(self.end_date)), sheet_name='原始净值', header=1)
        data['t_date'] = data['t_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        data.index = data['t_date']
        cols = data_with_header.columns.tolist()

        trading_day_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")

        data_param = []
        type_list = [x for x in cols if not x.startswith('Unnamed')]
        for i in range(len(type_list) - 1):
            if type_list[i] in ['量价（500）', '机器学习', '基本面']:
                s_index, e_index = cols.index(type_list[i]), cols.index(type_list[i + 1])
                data_slice = data[data.columns[s_index: e_index]]
                data_slice = data_slice[data_slice.index >= self.start_date].reindex(trading_day_list)
                data_param.append(data_slice)
            else:
                pass

        self.nav_data = pd.concat(data_param, axis=1).dropna(how='all', axis=0).sort_index()

        nav_df = self.nav_data.copy()
        nav_df['trade_date'] = nav_df.index
        nav_df['month'] = nav_df['trade_date'].apply(lambda x: datetime.strptime(x, '%Y%m%d').month)
        nav_df['next_month'] = nav_df['month'].shift(-1)
        nav_df.iloc[-1, -1] = nav_df['month'].tolist()[-1]

        self.month_list = nav_df[nav_df['month'] != nav_df['next_month']]['trade_date'].tolist()

        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format('000905', self.start_date, self.end_date)
        index_data = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data']).set_index('TRADEDATE')['TCLOSE']
        self.index_nav = index_data.reindex(self.nav_data.index)

        sql_script = "SELECT * FROM factor_return where trade_date >= {} and trade_date <= {}".format(
            self.start_date, self.end_date)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        factor_data = pd.pivot_table(
            data, index='trade_date', columns='factor_name', values='factor_ret').sort_index()[
            ['size', 'beta', 'momentum']]
        self.factor_data = (1 + factor_data).cumprod().reindex(self.nav_data.index)

        self.fund_date = pd.read_excel(os.path.join(self.data_path, r"fund_date.xlsx"), dtype={"start_date": str})

    def _counting_num(self):
        df = self.nav_data.copy()
        df['trade_date'] = df.index
        df['month'] = df['trade_date'].apply(lambda x: datetime.strptime(x, '%Y%m%d').month)
        df['next_month'] = df['month'].shift(-1)
        df.iloc[-1, -1] = df['month'].tolist()[-1]
        quarter_list = df[(df['month'] != df['next_month']) & (df['month'].isin([3, 6, 9, 12]))]['trade_date'].tolist()

        df = self.nav_data.copy()
        num_list = []
        for i in range(len(quarter_list) - 2):
            start_date, end_date = quarter_list[i], quarter_list[i + 2]
            period_data = df.loc[start_date: end_date, :].dropna(axis=1)
            num_list.append(period_data.shape[1])

        count_df = pd.DataFrame(index=quarter_list[1: -1], data=num_list, columns=['number'])

        return count_df

    @staticmethod
    def _regression(y, x):
        return sm.OLS(y, sm.add_constant(x)).fit().resid

    @staticmethod
    def _single_period_calc(ret, factor_ret, rf=0.015):
        annual_return = ret.apply(cal_annual_return, axis=0)
        annual_vol = ret.apply(cal_annual_volatility, axis=0)
        sharpe_ratio = (annual_return - rf) / annual_vol

        f_ret = sm.add_constant(np.array(factor_ret))
        resid = ret.apply(lambda x: sm.OLS(x, f_ret).fit().resid)
        alpha = (1 + resid).prod() - 1

        max_drawdown = (1 + ret).cumprod().apply(cal_max_drawdown, axis=0)

        factor = annual_return.to_frame('ret').merge(
            sharpe_ratio.to_frame('sharpe'), left_index=True, right_index=True).merge(
            alpha.to_frame('s_ret'), left_index=True, right_index=True).merge(
            max_drawdown.to_frame('max_drawdown'), left_index=True, right_index=True)

        return factor

    @staticmethod
    def _calc_group_weight(factor_series, group_num=5):
        n = factor_series.shape[0]
        p_list = [round((n / group_num) * i, 1) for i in range(0, group_num + 1)]
        group_df = pd.DataFrame(index=factor_series.index, columns=['group_{}'.format(i) for i in range(1, group_num + 1)])
        group_df = pd.merge(
            factor_series.to_frame('factor'), group_df, left_index=True, right_index=True).sort_values(by='factor')

        for i in range(len(p_list) - 1):
            point1, point2 = p_list[i], p_list[i + 1]
            tmp1 = group_df.index[np.floor(point1).astype(int)]
            if i == len(p_list) - 2:
                tmp2 = group_df.index[np.floor(point2).astype(int) - 1]
            else:
                tmp2 = group_df.index[np.floor(point2).astype(int)]
            group_df.loc[tmp1: tmp2, 'group_{}'.format(i + 1)] = 1.

        for i in range(1, len(p_list) - 1):
            point = p_list[i]
            tmp = group_df.index[np.floor(point).astype(int)]
            t_values = round(point - int(point), 2)
            group_df.loc[tmp, 'group_{}'.format(i)] = t_values
            group_df.loc[tmp, 'group_{}'.format(i + 1)] = round(1 - t_values, 1)

        group_df = group_df.fillna(0.)

        return group_df

    def calculate_factor(self, start_date, calc_period, hold_period):
        """
        start_date: 有效数据的起始时间点
        calc_period: 回溯区间长度
        hold_period: 持有区间长度
        """
        nav_df = self.nav_data.copy()
        reb_list = [x for x in self.month_list if x >= start_date][::hold_period]

        # 实际运行起始
        tmp = self.fund_date.set_index('fund_name')
        for name in tmp.index.tolist():
            e_date = tmp.loc[name, "start_date"]
            if nav_df.index.tolist().index(e_date) != 0:
                t_index = nav_df.index.tolist().index(e_date) - 1
                nav_df.loc[: nav_df.index.tolist()[t_index], name] = np.NAN
            else:
                pass

        # 异常值剔除
        include_list = [x for x in nav_df.columns if x not in [
            '聚宽一号', '无量1期', '思勰投资-中证500指数增强1号', '希格斯水手2号', '龙旗红旭500指数增强']]
        nav_df = nav_df[include_list]

        factor_list = []
        group_ret_list = []
        group_ret_list2 = []
        corr_list = []
        group_num = 5
        for reb_date in reb_list:
            s_date = self.month_list[self.month_list.index(reb_date) - calc_period]
            if self.month_list.index(reb_date) + hold_period >= len(self.month_list):
                e_date = self.month_list[-1]
            else:
                e_date = self.month_list[self.month_list.index(reb_date) + hold_period]
            # data check
            period_data = nav_df.loc[s_date: e_date].dropna(axis=1)

            calc_data = period_data.loc[s_date: reb_date]
            bm_data = self.index_nav.loc[s_date: reb_date]
            assert (calc_data.shape[0] == bm_data.shape[0])
            excess_ret = calc_data.pct_change().dropna().sub(bm_data.pct_change().dropna().squeeze(), axis=0)
            factor_ret = self.factor_data.pct_change().dropna().reindex(excess_ret.index)

            factor_ret = factor_ret[['size']]

            factor = self._single_period_calc(excess_ret, factor_ret)
            factor['fund_name'] = factor.index
            factor['reb_date'] = reb_date
            factor.reset_index(drop=True, inplace=True)
            # factor1 = factor.copy()

            # group weight
            # factor['calmar'] = factor['ret'] / factor['max_drawdown'].abs()
            factor_series = factor.set_index('fund_name')['s_ret']
            weight_df = self._calc_group_weight(factor_series, group_num)
            print(reb_date, weight_df.shape[0])

            # holding ret
            future_data = period_data.loc[reb_date: e_date]
            bm_data_fu = self.index_nav.loc[reb_date: e_date]
            assert (future_data.shape[0] == bm_data_fu.shape[0])
            excess_fu = future_data.pct_change().fillna(0.).sub(bm_data_fu.pct_change().fillna(0.).squeeze(), axis=0)
            excess_df = (1 + excess_fu).cumprod().T.reindex(weight_df.index).T
            group_nav = excess_df.dot(weight_df[weight_df.columns[1:]])
            group_nav = group_nav / group_nav.iloc[0]
            group_ret = group_nav.pct_change().dropna()

            a = ((1 + excess_fu).prod() - 1).to_frame('excess')
            a = pd.merge(factor, a, left_on='fund_name', right_index=True)
            corr_list.append(a['ret'].corr(a['excess']))
            # print(reb_date, a['ret'].corr(a['excess']))

            group_ret_list.append(group_ret)
            group_ret_list2.append(((1 + group_ret).prod() - 1).to_frame(reb_date).T)
            factor_list.append(factor)

        factor_df = pd.concat(factor_list)
        group_ret_all = pd.concat(group_ret_list)
        (1 + group_ret_all).cumprod().plot.line()

        # annual_alpha = group_ret_all.apply(cal_annual_return, axis=0)
        year_alpha = pd.DataFrame(
            index=['2019', '2020', '2021'], columns=['group_{}'.format(i) for i in range(1, group_num + 1)])
        year_alpha.loc['2019'] = (1 + group_ret_all[:"20191227"]).prod() - 1
        year_alpha.loc['2020'] = (1 + group_ret_all["20200103": "20201231"]).prod() - 1
        year_alpha.loc['2021'] = (1 + group_ret_all["20210108":]).prod() - 1

        return factor_df, group_ret_all

    def run(self, start_date):
        nav_df = self.nav_data.copy()
        reb_list = [x for x in self.month_list if x >= start_date][::3]

        # 实际运行起始
        tmp = self.fund_date.set_index('fund_name')
        for name in tmp.index.tolist():
            e_date = tmp.loc[name, "start_date"]
            if nav_df.index.tolist().index(e_date) != 0:
                t_index = nav_df.index.tolist().index(e_date) - 1
                nav_df.loc[: nav_df.index.tolist()[t_index], name] = np.NAN
            else:
                pass

        # 异常值剔除
        include_list = [x for x in nav_df.columns if x not in [
            '聚宽一号', '无量1期', '思勰投资-中证500指数增强1号', '希格斯水手2号', '龙旗红旭500指数增强']]
        nav_df = nav_df[include_list]

        factor_list = []
        group_ret_list = []
        group_num = 4
        weight_list = []
        for reb_date in reb_list:
            s_date = self.month_list[self.month_list.index(reb_date) - 6]
            pre_date = self.month_list[self.month_list.index(reb_date) - 3]
            if self.month_list.index(reb_date) + 3 >= len(self.month_list):
                e_date = self.month_list[-1]
            else:
                e_date = self.month_list[self.month_list.index(reb_date) + 3]
            # data check
            period_data = nav_df.loc[s_date: e_date].dropna(axis=1)

            calc_data = period_data.loc[s_date: reb_date]
            bm_data = self.index_nav.loc[s_date: reb_date]
            assert (calc_data.shape[0] == bm_data.shape[0])
            excess_ret = calc_data.pct_change().dropna().sub(bm_data.pct_change().dropna().squeeze(), axis=0)
            factor_ret = self.factor_data.pct_change().dropna().reindex(excess_ret.index)

            factor_ret = factor_ret[['size']]
            # 6个月因子
            factor = self._single_period_calc(excess_ret, factor_ret)
            factor['fund_name'] = factor.index
            factor['reb_date'] = reb_date
            factor.reset_index(drop=True, inplace=True)
            factor1 = factor.copy()
            # 3个月因子
            factor = self._single_period_calc(excess_ret.loc[pre_date:][1:], factor_ret.loc[pre_date:][1:])
            factor['fund_name'] = factor.index
            factor['reb_date'] = reb_date
            factor.reset_index(drop=True, inplace=True)
            factor2 = factor.copy()
            factor2.rename(columns={"ret": "ret_3M"}, inplace=True)

            factor = pd.merge(factor1, factor2[['fund_name', 'ret_3M']], on='fund_name')
            list1 = factor[factor['max_drawdown'] >= factor['max_drawdown'].quantile(0.25)]['fund_name'].tolist()
            tmp = factor[factor['fund_name'].isin(list1)]
            selected_name = tmp[tmp['sharpe'] >= tmp['sharpe'].quantile(0.66)]['fund_name'].tolist()

            # group weight
            # factor['calmar'] = factor['ret'] / factor['max_drawdown'].abs()
            factor_series = factor.set_index('fund_name')['max_drawdown']
            weight_df = self._calc_group_weight(factor_series, group_num)
            print(reb_date, weight_df.shape[0], len(selected_name))

            weight_df.loc[selected_name, 'port'] = 1.0
            weight_df['port'] = weight_df['port'].fillna(0.)

            tmp = weight_df.copy()
            tmp['date'] = reb_date
            weight_list.append(tmp[tmp['port'] == 1][['date', 'port']])

            # holding ret
            future_data = period_data.loc[reb_date: e_date]
            bm_data_fu = self.index_nav.loc[reb_date: e_date]
            assert (future_data.shape[0] == bm_data_fu.shape[0])
            excess_fu = future_data.pct_change().fillna(0.).sub(bm_data_fu.pct_change().fillna(0.).squeeze(), axis=0)
            excess_df = (1 + excess_fu).cumprod().T.reindex(weight_df.index).T
            group_nav = excess_df.dot(weight_df[weight_df.columns[1:]])
            group_nav = group_nav / group_nav.iloc[0]
            group_ret = group_nav.pct_change().dropna()

            # a = ((1 + excess_fu).prod() - 1).to_frame('excess')
            # a = pd.merge(factor, a, left_on='fund_name', right_index=True)
            # print(reb_date, a['ret'].corr(a['excess']))

            group_ret_list.append(group_ret)
            factor_list.append(factor)

        factor_df = pd.concat(factor_list)
        group_ret_all = pd.concat(group_ret_list)
        (1 + group_ret_all).cumprod().plot.line()

        # annual_alpha = group_ret_all.apply(cal_annual_return, axis=0)
        year_alpha = pd.DataFrame(
            index=['2019', '2020', '2021'], columns=['group_{}'.format(i) for i in range(1, group_num + 1)] + ['port'])
        year_alpha.loc['2019'] = (1 + group_ret_all[:"20191227"]).prod() - 1
        year_alpha.loc['2020'] = (1 + group_ret_all["20200103": "20201231"]).prod() - 1
        year_alpha.loc['2021'] = (1 + group_ret_all["20210108":]).prod() - 1

        return factor_df, group_ret_all

    # def run(self):
    #     nav_df = self.nav_data.copy()
    #
    #     nav_df['trade_date'] = nav_df.index
    #     nav_df['month'] = nav_df['trade_date'].apply(lambda x: datetime.strptime(x, '%Y%m%d').month)
    #     nav_df['next_month'] = nav_df['month'].shift(-1).fillna(0.).astype(int)
    #     nav_df.loc[nav_df['month'] != nav_df['next_month'], 'isMonthEnd'] = 1
    #     month_list = nav_df[nav_df['isMonthEnd'] == 1].index.tolist()
    #     cols = [x for x in nav_df.columns if x not in ['trade_date', 'month', 'next_month', 'isMonthEnd']]
    #
    #     ret_df = []
    #     for i in range(6, len(month_list) - 1, 3):
    #         if i + 3 > len(month_list) - 1:
    #             start_date, pre_date, t_date, future_date = month_list[i - 6], month_list[i - 3], \
    #                                                         month_list[i], month_list[-1]
    #         else:
    #             start_date, pre_date, t_date, future_date = month_list[i - 6], month_list[i - 3], \
    #                                                         month_list[i], month_list[i + 3]
    #         period_df = nav_df.loc[start_date: future_date, cols].dropna(how='any', axis=1)
    #         quarter_ret = period_df.loc[[start_date, pre_date, t_date, future_date]].pct_change().dropna().T
    #
    #         quantile_df = quarter_ret.rank() / quarter_ret.shape[0]
    #         # 剔除连续两个季度处于前25%分位的管理人
    #         selected_df = quantile_df[(quantile_df[pre_date] < 0.75) | (quantile_df[t_date] < 0.75)]
    #
    #         # print(t_date, period_df.shape[1], selected_df.shape[0])
    #
    #         # 前一个季度超额排名前50%
    #         selected_df = selected_df[selected_df[t_date] >= 0.50]
    #         # selected_df = selected_df.sort_values(by=t_date, ascending=False)[:10]
    #         tmp = period_df.loc[t_date: future_date] / period_df.loc[t_date]
    #         port_ret = tmp[selected_df.index].mean(axis=1).pct_change().dropna()
    #         # 对照组1
    #         group1 = quarter_ret[quarter_ret[t_date] < quarter_ret[t_date].quantile(0.5)]
    #         group1_ret = tmp[group1.index].mean(axis=1).pct_change().dropna()
    #         # 对照组2
    #         group2 = quarter_ret[quarter_ret[t_date] >= quarter_ret[t_date].quantile(0.5)]
    #         group2_ret = tmp[group2.index].mean(axis=1).pct_change().dropna()
    #         # 对照组3
    #         group3_ret = tmp.mean(axis=1).pct_change().dropna()
    #
    #         period_ret = port_ret.to_frame('port').merge(
    #             group1_ret.to_frame('group1'), left_index=True, right_index=True).merge(
    #             group2_ret.to_frame('group2'), left_index=True, right_index=True).merge(
    #             group3_ret.to_frame('group3'), left_index=True, right_index=True)
    #
    #         ret_df.append(period_ret)
    #
    #     ret_df = pd.concat(ret_df).sort_index()
    #
    #     # 中证500
    #     sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
    #                  "and JYRQ >= {} and JYRQ <= {}".format('000905', nav_df.index[0], nav_df.index[-1])
    #     res = hbs.db_data_query('readonly', sql_script, page_size=5000)
    #     data = pd.DataFrame(res['data']).rename(columns={"TCLOSE": "benchmark"}).set_index(
    #         'TRADEDATE')['benchmark']
    #     benchmark_ret = data.reindex(nav_df.index).pct_change().dropna().reindex(ret_df.index)
    #
    #     excess_return = ret_df.sub(benchmark_ret.squeeze(), axis=0)
    #
    #     (1 + excess_return).cumprod().plot.line(title="excess return compare line")
    #
    #     excess_nav = (1 + excess_return).cumprod()
    #     performance_df = pd.DataFrame(
    #         index=excess_nav.columns, columns=["累计超额", "超额年化", "超额年化波动", "最大回撤",
    # #                                            "Sharpe比率", "Calmar比率", "投资胜率", "平均损益比"])
    #     performance_df.loc[:, "累计超额"] = excess_nav.iloc[-1] - 1
    #     performance_df.loc[:, "超额年化"] = excess_return.apply(cal_annual_return, axis=0)
    #     performance_df.loc[:, '超额年化波动'] = excess_return.apply(cal_annual_volatility, axis=0)
    #     performance_df.loc[:, "最大回撤"] = excess_nav.apply(cal_max_drawdown, axis=0)
    #     performance_df.loc[:, "Sharpe比率"] = excess_return.apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)
    #     performance_df['Calmar比率'] = performance_df['超额年化'] / performance_df['最大回撤'].abs()
    #     performance_df.loc[:, "投资胜率"] = excess_return.apply(lambda x: x.gt(0).sum() / len(x), axis=0)
    #     performance_df.loc[:, "平均损益比"] = excess_return.apply(lambda x: x[x > 0].mean() / x[x < 0].abs().mean(), axis=0)
    #     # 格式处理
    #     performance_df['累计超额'] = performance_df['累计超额'].apply(lambda x: format(x, '.2%'))
    #     performance_df['超额年化'] = performance_df['超额年化'].apply(lambda x: format(x, '.2%'))
    #     performance_df['超额年化波动'] = performance_df['超额年化波动'].apply(lambda x: format(x, '.2%'))
    #     performance_df['最大回撤'] = performance_df['最大回撤'].apply(lambda x: format(x, '.2%'))
    #     performance_df['Sharpe比率'] = performance_df['Sharpe比率'].round(2)
    #     performance_df['Calmar比率'] = performance_df['Calmar比率'].round(2)
    #     performance_df['投资胜率'] = performance_df['投资胜率'].apply(lambda x: format(x, '.2%'))
    #     performance_df['平均损益比'] = performance_df['平均损益比'].round(2)
    #
    #     performance_df = performance_df.T
    #     performance_df.index.name = "指标名称"
    #     performance_df = performance_df.reset_index()
    #     fig = ff.create_table(performance_df)
    #     fig.layout.autosize = False
    #     fig.layout.width = 400
    #     fig.layout.height = 400
    #
    #     plot_ly(fig, filename="D:\\123.html", auto_open=False)
    #
    #     tmp = excess_nav['group2'].to_frame("超额")
    #     tmp['trade_date'] = tmp.index
    #     tmp['trade_dt'] = tmp['trade_date'].apply(lambda x: datetime.strptime(x, "%Y%m%d"))
    #     tmp['month'] = tmp['trade_dt'].apply(lambda x: x.month)
    #     tmp['year'] = tmp['trade_dt'].apply(lambda x: x.year)
    #     month_end = tmp[tmp['month'].shift(-1) != tmp['month']]['trade_date'].tolist()
    #
    #     month_excess = tmp.reindex(month_end)['超额'].pct_change().dropna()
    #     month_excess = pd.merge(month_excess, tmp[['month', 'year']], left_index=True, right_index=True)
    #     month_excess = pd.pivot_table(month_excess, index='year', columns='month', values='超额').sort_index()
    #     month_excess = month_excess.T.reindex(np.arange(1, 13)).sort_index().T
    #     month_excess.columns = [str(x) + '月' for x in month_excess.columns]
    #     month_excess['全年'] = (1 + month_excess.fillna(0.)).prod(axis=1) - 1
    #     for i in range(len(month_excess.index)):
    #         values = month_excess.iloc[i].values
    #         month_excess.iloc[i, :] = [format(x, '.2%') if x == x else x for x in values]
    #
    #     month_excess.to_csv('D:\\456.csv', encoding="gbk")


if __name__ == '__main__':
    # AlphaBacktest("D:\\量化产品跟踪\\指数增强", '20161230', '20220520').run()
    # f_df, g_ret = AlphaBacktest("D:\\量化产品跟踪\\指数增强", '20161230', '20220520').calculate_factor('20181228', 3, 3)
    AlphaBacktest("D:\\量化产品跟踪\\指数增强", '20161230', '20220602').run('20181228')
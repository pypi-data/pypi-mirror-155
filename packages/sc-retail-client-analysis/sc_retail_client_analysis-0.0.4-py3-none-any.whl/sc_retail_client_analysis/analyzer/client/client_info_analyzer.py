#  The MIT License (MIT)
#
#  Copyright (c) 2022. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging
import os
from datetime import datetime

import numpy as np
import pandas as pd
from config42 import ConfigManager

from sc_retail_client_analysis.analyzer.base.base_analyzer import BaseAnalyzer


class ClientInfoAnalyzer(BaseAnalyzer):
    """
    零售客群分析
    """

    def __init__(self, *, config: ConfigManager):
        super().__init__(config=config)
        self._key_enabled = "retail.client.client_info.enabled"
        self._key_business_type = "retail.client.client_info.business_type"
        self._key_export_column_list = "retail.client.client_info.sheet_config.export_column_list"
        self._age_series: pd.Series = None
        self._gender_series: pd.Series = None

    def _read_config(self, *, config: ConfigManager):
        super()._read_config(config=config)
        self._src_filepath = config.get("retail.client.client_info.source_file_path")
        self._target_avg_asset_filename = config.get("retail.client.client_info.target_avg_asset_filename")
        self._target_contrib_filename = config.get(
            "retail.client.client_info.target_contrib_filename")
        self._target_contrib_per_acct_filename = config.get(
            "retail.client.client_info.target_contrib_per_acct_filename")
        self._target_contrib_monthly_filename = config.get(
            "retail.client.client_info.target_contrib_monthly_filename")
        self._target_contrib_monthly_per_acct_filename = config.get(
            "retail.client.client_info.target_contrib_monthly_per_acct_filename")
        self._target_cross_sales_filename = config.get("retail.client.client_info.target_cross_sales_filename")
        self._target_prod_sales_rate_filename = config.get("retail.client.client_info.target_prod_sales_rate_filename")
        self._target_asset_balance_filename = config.get("retail.client.client_info.target_asset_balance_filename")
        # Sheet名称
        self._sheet_name = config.get("retail.client.client_info.sheet_name")
        # 表头行索引
        self._header_row = config.get("retail.client.client_info.sheet_config.header_row")
        # 管理资产年日均列索引
        self._average_asset_column = config.get("retail.client.client_info.sheet_config.average_asset_column")
        self._age_column = config.get("retail.client.client_info.sheet_config.age_column")
        self._gender_column = config.get("retail.client.client_info.sheet_config.gender_column")
        self._whole_contrib_column = config.get("retail.client.client_info.sheet_config.whole_contrib_column")
        self._gz_column = config.get("retail.client.client_info.sheet_config.gz_column")
        # 管理资产余额列索引
        self._asset_balance_column = config.get("retail.client.client_info.sheet_config.asset_balance_column")

        # # 信用卡客户
        # credit_column: 42
        self._credit_column = config.get("retail.client.client_info.sheet_config.credit_column")
        # # 快捷支付
        # fast_payment_column: 58
        self._fast_payment_column = config.get("retail.client.client_info.sheet_config.fast_payment_column")
        # # 呼啦商户
        # hula_column: 60
        self._hula_column = config.get("retail.client.client_info.sheet_config.hula_column")
        # # 净储蓄存款月日均
        # monthly_saving_avg_column: 18
        self._monthly_saving_avg_column = config.get("retail.client.client_info.sheet_config.monthly_saving_avg_column")
        # # 定期存款余额
        # fixed_deposit_column: 37
        self._fixed_deposit_column = config.get("retail.client.client_info.sheet_config.fixed_deposit_column")
        # # 结构性存款余额
        # structural_deposit_column: 31
        self._structural_deposit_column = config.get("retail.client.client_info.sheet_config.structural_deposit_column")
        # # 大额存单余额
        # large_deposit_column: 32
        self._large_deposit_column = config.get("retail.client.client_info.sheet_config.large_deposit_column")
        # # 零售贷款余额
        # retail_loan_column: 20
        self._retail_loan_column = config.get("retail.client.client_info.sheet_config.retail_loan_column")
        # # 理财产品余额
        # finance_prod_column: 24
        self._finance_prod_column = config.get("retail.client.client_info.sheet_config.finance_prod_column")
        # # 非货基金余额
        # fund_column: 38
        self._fund_column = config.get("retail.client.client_info.sheet_config.fund_column")
        # # 代销信托余额
        # trust_column: 39
        self._trust_column = config.get("retail.client.client_info.sheet_config.trust_column")
        # # 贵金属余额
        # precious_metal_column: 40
        self._precious_metal_column = config.get("retail.client.client_info.sheet_config.precious_metal_column")

        # 信用卡签约
        self._credit_sign_column_name = config.get("retail.client.client_info.sheet_config.credit_sign_column_name")
        self._fast_payment_sign_column_name = config.get(
            "retail.client.client_info.sheet_config.fast_payment_sign_column_name")
        self._hula_sign_column_name = config.get("retail.client.client_info.sheet_config.hula_sign_column_name")
        self._payment_and_clear_sign_column_name = config.get(
            "retail.client.client_info.sheet_config.payment_and_clear_sign_column_name")
        self._deposit_sales_column_name = config.get("retail.client.client_info.sheet_config.deposit_sales_column_name")
        self._retail_loan_sales_column_name = config.get(
            "retail.client.client_info.sheet_config.retail_loan_sales_column_name")
        self._finance_sales_column_name = config.get("retail.client.client_info.sheet_config.finance_sales_column_name")
        self._fund_sales_column_name = config.get("retail.client.client_info.sheet_config.fund_sales_column_name")
        self._trust_sales_column_name = config.get("retail.client.client_info.sheet_config.trust_sales_column_name")
        self._precious_metal_sales_column_name = config.get(
            "retail.client.client_info.sheet_config.precious_metal_sales_column_name")
        self._cross_sales_column_name = config.get("retail.client.client_info.sheet_config.cross_sales_column_name")

        # 管理资产年日均分布
        self._average_asset_splits: list = config.get("retail.client.client_info.sheet_config.average_asset_splits")
        self._average_asset_splits.append(np.Inf)
        self._age_splits: list = config.get("retail.client.client_info.sheet_config.age_splits")
        self._whole_contrib_splits: list = config.get(
            "retail.client.client_info.sheet_config.whole_contrib_splits")
        self._whole_contrib_splits.insert(0, -np.Inf)
        self._whole_contrib_splits.append(np.Inf)
        # 日期格式
        date_format = '%Y%m%d'
        date_date = config.get("retail.client.client_info.data_date")
        self._data_date = datetime.strptime(date_date, date_format)
        self._total_month = self._data_date.month
        self._data_total_month: list = config.get("retail.client.client_info.data_total_month")
        self._cross_sales_splits: list = config.get("retail.client.client_info.sheet_config.cross_sales_splits")

        # 储蓄存款创利金额
        # saving_profit_column: 69
        self._saving_profit_column = config.get("retail.client.client_info.sheet_config.saving_profit_column")
        # 零售贷款创利金额
        # retail_loan_profit_column: 64
        self._retail_loan_profit_column = config.get("retail.client.client_info.sheet_config.retail_loan_profit_column")
        # 非息资产中收金额
        # non_interest_profit_column: 71
        self._non_interest_profit_column = config.get(
            "retail.client.client_info.sheet_config.non_interest_profit_column")
        # 理财中收金额
        # finance_profit_column: 65
        self._finance_profit_column = config.get("retail.client.client_info.sheet_config.finance_profit_column")
        # 基金中收金额
        # fund_profit_column: 66
        self._fund_profit_column = config.get("retail.client.client_info.sheet_config.fund_profit_column")
        # 保险中收金额
        # insurance_profit_column: 67
        self._insurance_profit_column = config.get("retail.client.client_info.sheet_config.insurance_profit_column")
        # 信托中收金额
        # trust_profit_column: 67
        self._trust_profit_column = config.get("retail.client.client_info.sheet_config.trust_profit_column")
        # 贵金属中收金额
        # precious_metal_profit_column: 68
        self._precious_metal_profit_column = config.get(
            "retail.client.client_info.sheet_config.precious_metal_profit_column")

    def _read_src_file(self) -> pd.DataFrame:
        logging.getLogger(__name__).info("读取源文件：{}".format(self._src_filepath))
        data = pd.read_excel(
            self._src_filepath,
            sheet_name=self._sheet_name,
            header=self._header_row,
        )
        self._average_asset_column_name = data.columns[self._average_asset_column]
        self._asset_balance_column_name = data.columns[self._asset_balance_column]
        self._age_column_name = data.columns[self._age_column]
        self._gender_column_name = data.columns[self._gender_column]
        self._whole_contrib_column_name = data.columns[self._whole_contrib_column]
        self._gz_column_name = data.columns[self._gz_column]
        # # 信用卡客户
        # credit_column: 42
        self._credit_column_name = data.columns[self._credit_column]
        # # 快捷支付
        # fast_payment_column: 58
        self._fast_payment_column_name = data.columns[self._fast_payment_column]
        # # 呼啦商户
        # hula_column: 60
        self._hula_column_name = data.columns[self._hula_column]
        # # 净储蓄存款月日均
        # monthly_saving_avg_column: 18
        self._monthly_saving_avg_column_name = data.columns[self._monthly_saving_avg_column]
        # # 定期存款余额
        # fixed_deposit_column: 37
        self._fixed_deposit_column_name = data.columns[self._fixed_deposit_column]
        # # 结构性存款余额
        # structural_deposit_column: 31
        self._structural_deposit_column_name = data.columns[self._structural_deposit_column]
        # # 大额存单余额
        # large_deposit_column: 32
        self._large_deposit_column_name = data.columns[self._large_deposit_column]
        # # 零售贷款余额
        # retail_loan_column: 20
        self._retail_loan_column_name = data.columns[self._retail_loan_column]
        # # 理财产品余额
        # finance_prod_column: 24
        self._finance_prod_column_name = data.columns[self._finance_prod_column]
        # # 非货基金余额
        # fund_column: 38
        self._fund_column_name = data.columns[self._fund_column]
        # # 代销信托余额
        # trust_column: 39
        self._trust_column_name = data.columns[self._trust_column]
        # # 贵金属余额
        # precious_metal_column: 40
        self._precious_metal_column_name = data.columns[self._precious_metal_column]

        # 储蓄存款创利金额
        # saving_profit_column: 69
        self._saving_profit_column_name = data.columns[self._saving_profit_column]
        # 零售贷款创利金额
        # retail_loan_profit_column: 64
        self._retail_loan_profit_column_name = data.columns[self._retail_loan_profit_column]
        # 非息资产中收金额
        # non_interest_profit_column: 71
        self._non_interest_profit_column_name = data.columns[self._non_interest_profit_column]
        # 理财中收金额
        # finance_profit_column: 65
        self._finance_profit_column_name = data.columns[self._finance_profit_column]
        # 基金中收金额
        # fund_profit_column: 66
        self._fund_profit_column_name = data.columns[self._fund_profit_column]
        # 保险中收金额
        # insurance_profit_column: 67
        self._insurance_profit_column_name = data.columns[self._insurance_profit_column]
        # 信托中收金额
        # trust_profit_column: 67
        self._trust_profit_column_name = data.columns[self._trust_profit_column]
        # 贵金属中收金额
        # precious_metal_profit_column: 68
        self._precious_metal_profit_column_name = data.columns[self._precious_metal_profit_column]

        return data

    def _pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        if data.empty:
            return data
        data = self._avg_asset_analysis(data)
        data = self._whole_contrib_analysis(data)
        data = self._whole_contrib_avg_analysis(data)
        data = self._contrib_per_acct_analysis(data)
        data = self._contrib_avg_per_acct_analysis(data)
        data = self._cross_sales_analysis(data)
        data = self._prod_sales_rate_analysis(data)
        data = self._asset_balance_overall_analysis(data)
        return data

    def _common_split_analysis(self, data_splits, full_key_name, full_data, filter_data_mapping: dict, right=False):
        segments = pd.cut(full_data, data_splits, include_lowest=not right, right=right)
        series = pd.value_counts(segments, sort=False)
        zero_series = series.copy()
        zero_series[:] = 0
        series_list = list()
        column_names = list()
        column_names.append(full_key_name)
        series_list.append(series)
        for key, value in filter_data_mapping.items():
            column_name = key
            column_names.append(column_name)
            filter_data = value
            if not filter_data.empty:
                segments = pd.cut(filter_data, data_splits, include_lowest=not right, right=right)
                series = pd.value_counts(segments, sort=False)
                series_list.append(series)
            else:
                series_list.append(zero_series)

        # 合并成一个data frame
        merged_df = pd.concat(series_list, axis=1)
        merged_df.columns = column_names
        return merged_df.T

    def _avg_asset_split_analysis(self, data):
        if data.empty:
            return None
        splits = self._average_asset_splits
        full_key_name = '全量'
        column_name = self._average_asset_column_name
        full_data = data[column_name]
        filter_data_mapping: dict = dict()

        criterion_gz = data[self._gz_column_name].map(lambda x: x == 1)
        criterion_not_gz = data[self._gz_column_name].map(lambda x: x != 1)
        data_gz = data[criterion_gz].copy()
        filter_data_mapping['广州'] = data_gz[column_name]

        data_other = data[criterion_not_gz].copy()
        filter_data_mapping['其他'] = data_other[column_name]

        return self._common_split_analysis(splits, full_key_name, full_data, filter_data_mapping)

    def _avg_asset_analysis(self, data):
        target_filename_full_path = os.path.join(self._target_directory, self._target_avg_asset_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename_full_path):
            logging.getLogger(__name__).info("删除AUM输出文件：{} ".format(target_filename_full_path))
            try:
                os.remove(target_filename_full_path)
            except Exception as e:
                logging.getLogger(__name__).error("删除AUM文件 {} 失败：{} ".format(target_filename_full_path, e))
                return
        logging.getLogger(__name__).info("输出AUM文件：{} ".format(target_filename_full_path))
        result = data
        if result.empty:
            logging.getLogger(__name__).error("零售AUM无数据")
            return result
        with pd.ExcelWriter(target_filename_full_path) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._avg_asset_split_analysis(result)
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[self._gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[self._gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._avg_asset_split_analysis(data_male)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._avg_asset_split_analysis(data_female)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(self._age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[self._age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._avg_asset_split_analysis(data_criterion)
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(
                excel_writer=excel_writer,
                sheet_name="零售AUM",
            )

        return result

    def _whole_contrib_analysis(self, data):
        target_filename = os.path.join(self._target_directory, self._target_contrib_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info("删除本年创利输出文件：{} ".format(target_filename))
            try:
                os.remove(target_filename)
            except Exception as e:
                logging.getLogger(__name__).error("删除本年创利文件 {} 失败：{} ".format(target_filename, e))
                return
        logging.getLogger(__name__).info("输出本年创利文件：{} ".format(target_filename))
        result = data
        if result.empty:
            logging.getLogger(__name__).error("本年创利无数据")
            return result
        with pd.ExcelWriter(target_filename) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._whole_contrib_split_analysis(result)
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[self._gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[self._gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._whole_contrib_split_analysis(data_male)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._whole_contrib_split_analysis(data_female)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(self._age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[self._age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._whole_contrib_split_analysis(data_criterion)
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(
                excel_writer=excel_writer,
                sheet_name="本年创利",
            )

        return result

    def _whole_contrib_split_analysis(self, data):
        if data.empty:
            return None
        splits = self._whole_contrib_splits
        full_key_name = '全量'
        column_name = self._whole_contrib_column_name
        full_data = data[column_name]
        filter_data_mapping: dict = dict()

        criterion_gz = data[self._gz_column_name].map(lambda x: x == 1)
        criterion_not_gz = data[self._gz_column_name].map(lambda x: x != 1)
        data_gz = data[criterion_gz].copy()
        filter_data_mapping['广州'] = data_gz[column_name]

        data_other = data[criterion_not_gz].copy()
        filter_data_mapping['其他'] = data_other[column_name]

        return self._common_split_analysis(splits, full_key_name, full_data, filter_data_mapping, True)

    def _whole_contrib_avg_analysis(self, data):
        target_filename = os.path.join(self._target_directory,
                                       self._target_contrib_monthly_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info("删除月均创利输出文件：{} ".format(target_filename))
            try:
                os.remove(target_filename)
            except Exception as e:
                logging.getLogger(__name__).error(
                    "删除月均创利文件 {} 失败：{} ".format(target_filename, e))
                return
        logging.getLogger(__name__).info("输出月均创利文件：{} ".format(target_filename))
        result = data
        if result.empty:
            logging.getLogger(__name__).error("月均创利无数据")
            return result
        with pd.ExcelWriter(target_filename) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._whole_contrib_avg_split_analysis(result)
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[self._gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[self._gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._whole_contrib_avg_split_analysis(data_male)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._whole_contrib_avg_split_analysis(data_female)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(self._age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[self._age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._whole_contrib_avg_split_analysis(data_criterion)
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(
                excel_writer=excel_writer,
                sheet_name="月均创利",
            )

        return result

    def _whole_contrib_avg_split_analysis(self, data):
        if data.empty:
            return None
        splits = self._whole_contrib_splits
        full_key_name = '全量'
        column_name = self._whole_contrib_column_name
        full_data = data[column_name] / self._data_total_month
        filter_data_mapping: dict = dict()

        criterion_gz = data[self._gz_column_name].map(lambda x: x == 1)
        criterion_not_gz = data[self._gz_column_name].map(lambda x: x != 1)
        data_gz = data[criterion_gz].copy()
        filter_data_mapping['广州'] = data_gz[column_name] / self._data_total_month

        data_other = data[criterion_not_gz].copy()
        filter_data_mapping['其他'] = data_other[column_name] / self._data_total_month

        return self._common_split_analysis(splits, full_key_name, full_data, filter_data_mapping, right=True)

    def _contrib_per_acct_analysis(self, data):
        target_filename = os.path.join(self._target_directory, self._target_contrib_per_acct_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info("删除本年户均创利输出文件：{} ".format(target_filename))
            try:
                os.remove(target_filename)
            except Exception as e:
                logging.getLogger(__name__).error("删除本年户均创利文件 {} 失败：{} ".format(target_filename, e))
                return
        logging.getLogger(__name__).info("输出本年户均创利文件：{} ".format(target_filename))

        result = data
        if result.empty:
            logging.getLogger(__name__).error("本年户均创利无数据")
            return result
        with pd.ExcelWriter(target_filename) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._contrib_per_acct_split_analysis(result)
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[self._gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[self._gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._contrib_per_acct_split_analysis(data_male)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._contrib_per_acct_split_analysis(data_female)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(self._age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[self._age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._contrib_per_acct_split_analysis(data_criterion)
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(
                excel_writer=excel_writer,
                sheet_name="本年户均创利",
            )

        return result

    def _contrib_per_acct_split_analysis(self, data):
        if data.empty:
            return None
        splits = self._whole_contrib_splits
        filter_data_mapping: dict = dict()

        column_list = list()
        column_list.append(self._saving_profit_column_name)
        column_list.append(self._retail_loan_profit_column_name)
        column_list.append(self._non_interest_profit_column_name)
        column_list.append(self._finance_profit_column_name)
        column_list.append(self._fund_profit_column_name)
        column_list.append(self._insurance_profit_column_name)
        column_list.append(self._trust_profit_column_name)
        column_list.append(self._precious_metal_profit_column_name)
        df_list = list()
        for column_name in column_list:
            full_key_name = column_name
            full_data = data[column_name]
            df = self._common_split_analysis(splits, full_key_name, full_data, filter_data_mapping)
            df_list.append(df)

        # 合并成一个data frame
        merged_all_df = pd.concat(df_list)
        return merged_all_df

    def _contrib_avg_per_acct_analysis(self, data):
        target_filename = os.path.join(self._target_directory, self._target_contrib_monthly_per_acct_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info("删除月均户均创利输出文件：{} ".format(target_filename))
            try:
                os.remove(target_filename)
            except Exception as e:
                logging.getLogger(__name__).error("删除月均户均创利文件 {} 失败：{} ".format(target_filename, e))
                return
        logging.getLogger(__name__).info("输出月均户均创利文件：{} ".format(target_filename))

        result = data
        if result.empty:
            logging.getLogger(__name__).error("月均户均创利无数据")
            return result
        with pd.ExcelWriter(target_filename) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._contrib_avg_per_acct_split_analysis(result)
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[self._gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[self._gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._contrib_avg_per_acct_split_analysis(data_male)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._contrib_avg_per_acct_split_analysis(data_female)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(self._age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[self._age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._contrib_avg_per_acct_split_analysis(data_criterion)
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(
                excel_writer=excel_writer,
                sheet_name="本年户均创利",
            )

        return result

    def _contrib_avg_per_acct_split_analysis(self, data):
        if data.empty:
            return None
        splits = self._whole_contrib_splits
        filter_data_mapping: dict = dict()

        column_list = list()
        column_list.append(self._saving_profit_column_name)
        column_list.append(self._retail_loan_profit_column_name)
        column_list.append(self._non_interest_profit_column_name)
        column_list.append(self._finance_profit_column_name)
        column_list.append(self._fund_profit_column_name)
        column_list.append(self._insurance_profit_column_name)
        column_list.append(self._trust_profit_column_name)
        column_list.append(self._precious_metal_profit_column_name)
        df_list = list()
        for column_name in column_list:
            full_key_name = column_name
            full_data = data[column_name] / self._data_total_month
            df = self._common_split_analysis(splits, full_key_name, full_data, filter_data_mapping)
            df_list.append(df)

        # 合并成一个data frame
        merged_all_df = pd.concat(df_list)
        return merged_all_df

    def _cross_sales_column_analysis(self, data):
        # 信用卡签约
        data[self._credit_sign_column_name] = data[self._credit_column_name]
        sign_mapping = {'已签约': 1, '未签约': 0, '曾经签约': 0}
        data = data.replace({self._credit_sign_column_name: sign_mapping})
        data[self._credit_sign_column_name].fillna(0, inplace=True)

        # 快捷支付签约
        data[self._fast_payment_sign_column_name] = data[self._fast_payment_column_name]
        data = data.replace({self._fast_payment_sign_column_name: sign_mapping})
        data[self._fast_payment_sign_column_name].fillna(0, inplace=True)
        data[self._fast_payment_sign_column_name] = data[self._fast_payment_sign_column_name].astype('int64')
        # 呼啦签约
        data[self._hula_sign_column_name] = data[self._hula_column_name]
        data = data.replace({self._hula_sign_column_name: sign_mapping})
        data[self._hula_sign_column_name].fillna(0, inplace=True)
        data[self._hula_sign_column_name] = data[self._hula_sign_column_name].astype('int64')
        # 支付结算签约，快捷支付=已签约 || 呼啦商户=已签约
        data[self._payment_and_clear_sign_column_name] = \
            data[self._fast_payment_sign_column_name] | data[self._hula_sign_column_name]

        # 储蓄营销,净储蓄存款月日均+定期存款余额+结构性存款余额+大额存单余额>0，则储蓄营销=1
        data[self._deposit_sales_column_name] = \
            data[self._monthly_saving_avg_column_name] + \
            data[self._fixed_deposit_column_name] + \
            data[self._structural_deposit_column_name] + \
            data[self._large_deposit_column_name]
        data[self._deposit_sales_column_name] = data[self._deposit_sales_column_name] > 0
        true_false_mapping = {True: 1, False: 0}
        data = data.replace({self._deposit_sales_column_name: true_false_mapping})

        data[self._retail_loan_sales_column_name] = data[self._retail_loan_column_name] > 0
        data = data.replace({self._retail_loan_sales_column_name: true_false_mapping})

        data[self._finance_sales_column_name] = data[self._finance_prod_column_name] > 0
        data = data.replace({self._finance_sales_column_name: true_false_mapping})

        data[self._fund_sales_column_name] = data[self._fund_column_name] > 0
        data = data.replace({self._fund_sales_column_name: true_false_mapping})

        data[self._trust_sales_column_name] = data[self._trust_column_name] > 0
        data = data.replace({self._trust_sales_column_name: true_false_mapping})

        data[self._precious_metal_sales_column_name] = data[self._precious_metal_column_name] > 0
        data = data.replace({self._precious_metal_sales_column_name: true_false_mapping})

        # 交叉营销度=信用卡签约+支付结算签约+储蓄营销+零贷营销+理财营销+基金营销+信托营销+贵金属营销
        data[self._cross_sales_column_name] = \
            data[self._credit_sign_column_name] + \
            data[self._payment_and_clear_sign_column_name] + \
            data[self._deposit_sales_column_name] + \
            data[self._retail_loan_sales_column_name] + \
            data[self._finance_sales_column_name] + \
            data[self._fund_sales_column_name] + \
            data[self._trust_sales_column_name] + \
            data[self._precious_metal_sales_column_name]

        return data

    def _cross_sales_split_analysis(self, data):
        if data.empty:
            return None
        splits = self._cross_sales_splits
        full_key_name = '全量'
        column_name = self._cross_sales_column_name
        full_data = data[column_name]
        filter_data_mapping: dict = dict()

        criterion_gz = data[self._gz_column_name].map(lambda x: x == 1)
        criterion_not_gz = data[self._gz_column_name].map(lambda x: x != 1)
        data_gz = data[criterion_gz].copy()
        filter_data_mapping['广州'] = data_gz[column_name]

        data_other = data[criterion_not_gz].copy()
        filter_data_mapping['其他'] = data_other[column_name]

        return self._common_split_analysis(splits, full_key_name, full_data, filter_data_mapping)

    def _cross_sales_analysis(self, data):
        target_filename = os.path.join(self._target_directory, self._target_cross_sales_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info("删除交叉营销输出文件：{} ".format(target_filename))
            try:
                os.remove(target_filename)
            except Exception as e:
                logging.getLogger(__name__).error("删除交叉营销文件 {} 失败：{} ".format(target_filename, e))
                return
        logging.getLogger(__name__).info("输出交叉营销文件：{} ".format(target_filename))

        result = self._cross_sales_column_analysis(data)
        if result.empty:
            logging.getLogger(__name__).error("交叉营销无数据")
            return result
        with pd.ExcelWriter(target_filename) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._cross_sales_split_analysis(result)
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[self._gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[self._gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._cross_sales_split_analysis(data_male)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._cross_sales_split_analysis(data_female)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(self._age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[self._age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._cross_sales_split_analysis(data_criterion)
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(
                excel_writer=excel_writer,
                sheet_name="交叉营销",
            )

        return result

    def _prod_sales_rates_analysis(self, data_splits, data):
        column_list = list()
        column_list.append(self._credit_sign_column_name)
        column_list.append(self._payment_and_clear_sign_column_name)
        column_list.append(self._deposit_sales_column_name)
        column_list.append(self._retail_loan_sales_column_name)
        column_list.append(self._finance_sales_column_name)
        column_list.append(self._fund_sales_column_name)
        column_list.append(self._trust_sales_column_name)
        column_list.append(self._precious_metal_sales_column_name)

        rate_list = list()
        index_list = list()
        for column_name in column_list:
            sign_data = data[column_name]
            segments = pd.cut(sign_data, data_splits,
                              include_lowest=True, right=False)
            groupby = sign_data.groupby(segments)
            aggre = groupby.agg(['count'])
            rates = aggre / aggre.agg(['sum']).loc['sum', 'count']
            # [1,2)的区间的占比
            rate = rates.iloc[1, 0] * 100
            rate_list.append(rate)
            index_list.append(column_name)
        series = pd.Series(rate_list, index=index_list)
        return series

    def _prod_sales_rate_common_split_analysis(self, data_splits, full_key_name, full_data, filter_data_mapping: dict):
        series = self._prod_sales_rates_analysis(data_splits, full_data)
        zero_series = series.copy()
        zero_series[:] = 0
        series_list = list()
        column_names = list()
        column_names.append(full_key_name)
        series_list.append(series)
        for key, value in filter_data_mapping.items():
            column_name = key
            column_names.append(column_name)
            filter_data = value
            if not filter_data.empty:
                series = self._prod_sales_rates_analysis(data_splits, filter_data)
                series_list.append(series)
            else:
                series_list.append(zero_series)

        # 合并成一个data frame
        merged_df = pd.concat(series_list, axis=1)
        merged_df.columns = column_names
        return merged_df.T

    def _prod_sales_rate_split_analysis(self, data):
        if data.empty:
            return None
        splits = [0, 1, 2]
        full_key_name = '全量'
        full_data = data
        filter_data_mapping: dict = dict()

        criterion_gz = data[self._gz_column_name].map(lambda x: x == 1)
        criterion_not_gz = data[self._gz_column_name].map(lambda x: x != 1)
        data_gz = data[criterion_gz].copy()
        filter_data_mapping['广州'] = data_gz

        data_other = data[criterion_not_gz].copy()
        filter_data_mapping['其他'] = data_other

        return self._prod_sales_rate_common_split_analysis(splits, full_key_name, full_data, filter_data_mapping)

    def _prod_sales_rate_analysis(self, data):
        target_filename = os.path.join(self._target_directory, self._target_prod_sales_rate_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info("删除产品营销率输出文件：{} ".format(target_filename))
            try:
                os.remove(target_filename)
            except Exception as e:
                logging.getLogger(__name__).error("删除产品营销率文件 {} 失败：{} ".format(target_filename, e))
                return
        logging.getLogger(__name__).info("输出产品营销率文件：{} ".format(target_filename))

        result = data
        if result.empty:
            logging.getLogger(__name__).error("交叉营销率无数据")
            return result
        with pd.ExcelWriter(target_filename) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._prod_sales_rate_split_analysis(result)
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[self._gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[self._gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._prod_sales_rate_split_analysis(data_male)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._prod_sales_rate_split_analysis(data_female)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(self._age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[self._age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._prod_sales_rate_split_analysis(data_criterion)
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(
                excel_writer=excel_writer,
                sheet_name="交叉营销率",
            )

        return result

    def _asset_balance_analysis(self, data_splits, data):
        segments = pd.cut(data, data_splits, include_lowest=True, right=False)
        groupby = data.groupby(segments).agg(['sum'])
        series = groupby.squeeze()
        return series

    def _asset_balance_common_split_analysis(self, data_splits, full_key_name, full_data, filter_data_mapping: dict):
        series = self._asset_balance_analysis(data_splits, full_data)
        zero_series = series.copy()
        zero_series[:] = 0
        series_list = list()
        column_names = list()
        column_names.append(full_key_name)
        series_list.append(series)
        for key, value in filter_data_mapping.items():
            column_name = key
            column_names.append(column_name)
            filter_data = value
            if not filter_data.empty:
                series = self._asset_balance_analysis(data_splits, filter_data)
                series_list.append(series)
            else:
                series_list.append(zero_series)

        # 合并成一个data frame
        merged_df = pd.concat(series_list, axis=1)
        merged_df.columns = column_names
        return merged_df.T

    def _asset_balance_split_analysis(self, data):
        if data.empty:
            return None
        splits = self._average_asset_splits
        full_key_name = '全量'
        column_name = self._asset_balance_column_name
        full_data = data[column_name]
        filter_data_mapping: dict = dict()

        criterion_gz = data[self._gz_column_name].map(lambda x: x == 1)
        criterion_not_gz = data[self._gz_column_name].map(lambda x: x != 1)
        data_gz = data[criterion_gz].copy()
        filter_data_mapping['广州'] = data_gz[column_name]

        data_other = data[criterion_not_gz].copy()
        filter_data_mapping['其他'] = data_other[column_name]

        return self._asset_balance_common_split_analysis(splits, full_key_name, full_data, filter_data_mapping)

    def _asset_balance_overall_analysis(self, data):
        target_filename = os.path.join(self._target_directory, self._target_asset_balance_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info("删除管理资产余额输出文件：{} ".format(target_filename))
            try:
                os.remove(target_filename)
            except Exception as e:
                logging.getLogger(__name__).error("删除管理资产余额文件 {} 失败：{} ".format(target_filename, e))
                return
        logging.getLogger(__name__).info("输出管理资产余额文件：{} ".format(target_filename))

        result = data
        if result.empty:
            logging.getLogger(__name__).error("管理资产余额无数据")
            return result
        with pd.ExcelWriter(target_filename) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._asset_balance_split_analysis(result)
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[self._gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[self._gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._asset_balance_split_analysis(data_male)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._asset_balance_split_analysis(data_female)
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(self._age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[self._age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._asset_balance_split_analysis(data_criterion)
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(
                excel_writer=excel_writer,
                sheet_name="管理资产余额",
            )

        return result

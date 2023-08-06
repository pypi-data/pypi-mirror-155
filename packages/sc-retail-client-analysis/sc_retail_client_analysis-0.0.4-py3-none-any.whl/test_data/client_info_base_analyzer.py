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

import pandas as pd

from test_data import BaseAnalyzer


class ClientInfoBaseAnalyzer(BaseAnalyzer):
    """
    零售客群分析基类
    """

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

    def _split_analysis(self, *, data, data_splits, data_column_name, ):
        if data.empty:
            return None
        splits = data_splits
        column_name = data_column_name
        full_key_name = '全量'
        full_data = data[column_name]
        filter_data_mapping: dict = dict()

        criterion_gd = data[self._gd_column_name].map(lambda x: x == 1)
        criterion_not_gd = data[self._gd_column_name].map(lambda x: x != 1)
        data_gd = data[criterion_gd].copy()
        filter_data_mapping['广东'] = data_gd[column_name]

        criterion_gz = data[self._gz_column_name].map(lambda x: x == 1)
        criterion_not_gz = data[self._gz_column_name].map(lambda x: x != 1)
        data_gz = data[criterion_gz].copy()
        filter_data_mapping['广州'] = data_gz[column_name]

        criterion_hn = data[self._hn_column_name].map(lambda x: x == 1)
        criterion_not_hn = data[self._hn_column_name].map(lambda x: x != 1)
        data_hn = data[criterion_hn].copy()
        filter_data_mapping['湖南'] = data_hn[column_name]

        data_other = data[criterion_not_gd & criterion_not_gz & criterion_not_hn].copy()
        filter_data_mapping['其他'] = data_other[column_name]

        return self._common_split_analysis(splits, full_key_name, full_data, filter_data_mapping)

    def _analysis(self, *, target_filename, data, data_splits, data_column_name,
                  gender_column_name, age_column_name, age_splits
                  ):
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info("删除输出文件：{} ".format(target_filename))
            try:
                os.remove(target_filename)
            except Exception as e:
                logging.getLogger(__name__).error("删除文件 {} 失败：{} ".format(target_filename, e))
                return
        logging.getLogger(__name__).info("输出文件：{} ".format(target_filename))
        result = data
        if result.empty:
            logging.getLogger(__name__).error("零售无数据")
            return result
        with pd.ExcelWriter(target_filename) as excel_writer:
            # 全量
            df_list = list()
            keys = list()
            merged_df = self._split_analysis(
                data=result,
                data_splits=data_splits,
                data_column_name=data_column_name,
            )
            if merged_df is None:
                return result
            zero_df = merged_df.copy()
            zero_df.loc[:, :] = 0
            df_list.append(merged_df)
            keys.append('全量')
            # 按性别拆分
            criterion_male = result[gender_column_name].map(lambda x: x == '男性')
            criterion_female = result[gender_column_name].map(lambda x: x == '女性')
            data_male = result[criterion_male].copy()
            keys.append('男性')
            if not data_male.empty:
                merged_df = self._split_analysis(
                    data=data_male,
                    data_splits=data_splits,
                    data_column_name=data_column_name,
                )
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)
            data_female = result[criterion_female].copy()
            keys.append('女性')
            if not data_female.empty:
                merged_df = self._split_analysis(
                    data=data_female,
                    data_splits=data_splits,
                    data_column_name=data_column_name,
                )
                if merged_df is not None:
                    df_list.append(merged_df)
                else:
                    df_list.append(zero_df)
            else:
                df_list.append(zero_df)

            # 按年龄拆分
            age_intervals = pd.arrays.IntervalArray.from_breaks(age_splits, closed='left')
            for age_interval in age_intervals:
                criterion = result[age_column_name].map(lambda x: age_interval.left <= x < age_interval.right)
                data_criterion = result[criterion].copy()
                name = f"{age_interval.left}<= 年龄 <{age_interval.right}"
                keys.append(name)
                if not data_criterion.empty:
                    merged_df = self._split_analysis(
                        data=data_criterion,
                        data_splits=data_splits,
                        data_column_name=data_column_name,
                    )
                    if merged_df is not None:
                        df_list.append(merged_df)
                    else:
                        df_list.append(zero_df)
                else:
                    df_list.append(zero_df)
            merged_all_df = pd.concat(df_list, keys=keys)
            merged_all_df.to_excel(excel_writer=excel_writer, )

        return result

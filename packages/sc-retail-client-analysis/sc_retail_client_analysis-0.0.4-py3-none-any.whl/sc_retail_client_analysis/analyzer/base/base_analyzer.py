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

#  The MIT License (MIT)
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
#
import logging
import os

import pandas as pd
from config42 import ConfigManager


class BaseAnalyzer:
    """
    分析基础类
    """

    def __init__(self, *, config: ConfigManager):
        self._config = config
        # 业务类型
        self._key_business_type = None
        self._business_type = None
        self._key_enabled = None
        self._read_config(config=config)

    def _enabled(self):
        """
        是否启用分析
        :return: 是否启用分析
        """
        # 配置不存在默认不启用分析
        enabled_config = self._config.get(self._key_enabled)
        return False if enabled_config is None else enabled_config

    def get_business_type(self) -> str:
        """
        业务类型
        :return: 业务类型
        """
        return self._business_type

    def _read_config(self, *, config: ConfigManager):
        """
        读取配置，初始化相关变量
        """
        # 生成的目标Excel文件存放路径
        self._target_directory = self._config.get("retail.target_directory")
        # 目标文件名称
        self._target_detail_filename = self._config.get("retail.target_detail_filename")

    def _read_src_file(self) -> pd.DataFrame:
        """
        读取Excel或CSV文件，获取DataFrame
        :return: DataFrame
        """
        return pd.DataFrame()

    def _rename_target_columns(self, *, data: pd.DataFrame) -> pd.DataFrame:
        """
        重命名DataFrame相关列

        :param data: 原DataFrame
        :return: 重命名相关列后的DataFrame
        """
        return data

    def _pre_pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        """
        在数据透视之前做的操作

        :param data: 原DataFrame
        :return: 操作后的DataFrame
        """
        return data

    def _pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        """
        对DataFrame进行数据透视

        :param data: 原DataFrame
        :return: 数据透视后的DataFrame
        """
        return data

    def _after_pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        """
        在数据透视之后做的操作

        :param data: 原DataFrame
        :return: 操作后的DataFrame
        """
        return data

    def _merge_with_manifest(self, *, manifest_data: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        """
        与花名册合并

        :param manifest_data: 花名册数据，左边表
        :param data: 待合并DataFrame，右边表
        :return: 与花名册合并后的DataFrame
        """
        return data

    def _drop_duplicated_columns(self, *, data: pd.DataFrame) -> pd.DataFrame:
        """
        删除重复列

        :param data: 原始DataFrame
        :return: 删除重复列后的DataFrame
        """
        return data

    def analysis(self) -> pd.DataFrame:
        """
        主分析流程分析

        """
        self._business_type = self._config.get(self._key_business_type)
        # 如果未启用，则直接返回上一次的分析数据
        if not self._enabled():
            # 处理缺少配置的情况下日志记录不到具体分析类型的问题
            business_type = self._business_type
            if business_type is None:
                business_type = self._key_business_type
            logging.getLogger(__name__).info("{} 分析未启用".format(business_type))
            return pd.DataFrame()
        # 读取业务类型
        logging.getLogger(__name__).info("开始分析 {} 数据".format(self._business_type))
        # 读取Excel或CSV文件，获取DataFrame
        try:
            data = self._read_src_file()
        except FileNotFoundError as e:
            logging.getLogger(__name__).error("{} 分析失败：{}".format(self._business_type, e))
            # 文件不存在，则直接返回上一次的分析数据
            return pd.DataFrame()
        # 重命名DataFrame相关列
        data = self._rename_target_columns(data=data)
        # 在数据透视之前做的操作
        data = self._pre_pivot_table(data=data)
        # 对DataFrame进行数据透视
        data = self._pivot_table(data=data)
        # 在数据透视之后做的操作
        if not data.empty:
            data = self._after_pivot_table(data=data)
        # 删除重复列
        data = self._drop_duplicated_columns(data=data)
        # 输出原始分析报告
        # self.write_detail_report(data)
        logging.getLogger(__name__).info("完成分析 {} 数据".format(self._business_type))
        return data

    def write_detail_report(self, data: pd.DataFrame):
        # 如果未启用，则直接返回
        if not self._enabled():
            return
        # 读取源文件失败
        if data is None:
            return
        target_detail_filename_full_path = os.path.join(self._target_directory, self._target_detail_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_detail_filename_full_path):
            logging.getLogger(__name__).info("删除明细输出文件：{} ".format(target_detail_filename_full_path))
            try:
                os.remove(target_detail_filename_full_path)
            except Exception as e:
                logging.getLogger(__name__).error("删除明细文件 {} 失败：{} ".format(target_detail_filename_full_path, e))
                return
        logging.getLogger(__name__).info("输出明细文件：{} ".format(target_detail_filename_full_path))
        with pd.ExcelWriter(target_detail_filename_full_path) as excel_writer:
            data.to_excel(
                excel_writer=excel_writer,
                index=False,
                sheet_name=self._business_type,
            )

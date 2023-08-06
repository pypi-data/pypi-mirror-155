import json
import os.path

import chardet
import requests

from docparser.core.behavior_base import BehaviorBase
from docparser.core.tools import Tools


class TextRepairBehavior(BehaviorBase):
    class_index = 0

    def data_processing(self, ref_data, data: list, error: list, config: dict, logger, additional) -> dict:

        conf = config.get("text_repair")

        if 'file' not in additional or conf is None:
            return additional

        sub_conf = conf.get('subs')

        if sub_conf is None:
            return additional

        sub_conf = [Tools.init_regex(item) for item in sub_conf]

        parse_file = self.__convert(additional, conf)

        if parse_file:

            encoding = self.get_encoding(parse_file)
            with open(parse_file, 'r', encoding=encoding, errors='ignore') as f:
                lines = f.readlines()

            if lines and isinstance(lines, list):
                for line in lines:
                    for sub in sub_conf:
                        res = Tools.match_value(line, sub)
                        if res is not None and isinstance(res, dict):
                            for k, v in res.items():
                                data[k] = v
                                if k == conf.get('stop'):
                                    return additional

        return additional

    def __convert(self, additional, conf):

        file = additional.get('file')
        file_suffix = os.path.splitext(file)
        if file_suffix[1].lower() != '.xlsx':
            return None
        pdf_url = conf.get("pdf_api")
        url_params = {"filepaths": [f'{file_suffix[0]}.pdf'], "doctype": 'txt'}
        header = {
            "Content-type": "application/json"
        }
        try:

            response = requests.post(pdf_url, headers=header, data=json.dumps(url_params), timeout=20)
            if response.ok:
                res_content = response.json()
                if res_content.get("status") and len(res_content.get("files")) > 0:
                    return list(res_content.get("files").values())[0]
        except Exception:
            return None

    def get_encoding(self, file):
        """
        推断文件编码
        : return： 编码名称
        """
        f3 = open(file=file, mode='rb')  # 以二进制模式读取文件
        file_data = f3.read()  # 获取文件内容
        # print(file_data)
        f3.close()  # 关闭文件
        result = chardet.detect(file_data)
        encode = result['encoding']
        # gb2312的编码需要转成gbk或者gb18030处理
        if str(encode).upper() == 'GB2312':
            return 'gbk'
        return encode

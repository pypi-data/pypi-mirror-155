import pytest

from docparser.doc_parser_factory import DocParserFactory

config = {
    "id": "AN_CMA_",
    "parse": {
        "id": "CMA",
        "name": "CMA config",
        "kv": {
            "VESSEL": {
                "position_pattern": [
                    "^VESSEL:"
                ],
                "value_pattern": [
                    "(?P<Vessel>[\\w\\W]*?)(?:\\r\\n|\\n|$)"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "VesselName",
                        "key": "Vessel"
                    }
                ]
            },
            "VOYAGE": {
                "position_pattern": [
                    "^VOYAGE:"
                ],
                "value_pattern": [
                    "VOYAGE\\s*:\\s*(?P<VOYAGE>[\\w\\W]*)"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "VoyageNo",
                        "key": "VOYAGE"
                    }
                ]
            },
            "POD ETA": {
                "position_pattern": [
                    "^POD ETA"
                ],
                "value_pattern": [
                    "POD\\s*ETA\\s*:\\s*(?P<ETA>\\d+/\\d+/\\d+)(?:\\r\\n|\\n)"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "EstimatedArrivalDate",
                        "key": "ETA"
                    }
                ]
            },
            "DeliveryPlaceName": {
                "position_pattern": [
                    "^OPERATIONAL LOAD PORT"
                ],
                "value_pattern": [
                    "[\\w\\W]*(?:\\n|\\r\\n|)(?P<DELIVERY>.*)"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "DeliveryPlaceName",
                        "key": "DELIVERY"
                    }
                ]
            },
            "DestinationPortName": {
                "position_pattern": [
                    "[\\w\\W]*?OPERATIONAL DISCH. PORT[\\w\\W]*"
                ],
                "value_pattern": [
                    "[^\\n]*?(?:\\n)(?P<DestinationPortName>[^\\n]*?)(?:\\n|$)",
                    "[^\\n]*(?P<DestinationPortName>.*)$"
                ],
                "repeat_count": 1,
                "find_mode": "h",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "DestinationPortName",
                        "key": "DestinationPortName"
                    }
                ]
            },
            "BillOfLadingsId": {
                "position_pattern": [
                    "^Please clear your cargo",
                    "Please Pay freight against "
                ],
                "value_pattern": [
                    "[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4}\\s*[a-zA-Z]{3,}\\d{5,}[a-zA-Z]*)\\s*((Waybill)|(Negotiable))",
                    "[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4,}\\d{5,}[a-zA-Z]*)\\s*"
                ],
                "repeat_count": 1,
                "find_mode": "default",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "BillOfLadingsId",
                        "key": "billoflading"
                    }
                ]
            },
            "BillOfLadingsId1": {
                "position_pattern": [
                    "^Please[\\w\\W]*BILL\\s*TYPE$",
                    "^SCAC\\s{2,}B/L\\s*#$"
                ],
                "value_pattern": [
                    "(?P<billoflading>[a-zA-Z]{4,}\\s*[a-zA-Z]*\\d{5,}[a-zA-Z]*)$"
                ],
                "repeat_count": 1,
                "find_mode": "v",
                "separator_mode": "regex",
                "is_split_cell": 0,
                "split_pattern": [
                    ""
                ],
                "action": [
                    {
                        "keyword": "BillOfLadingsId",
                        "key": "billoflading"
                    }
                ]
            }
        },
        "table": {
            "containers": {
                "position_pattern": [
                    "^CONTAINER\\s*#"
                ],
                "separator": " ",
                "find_mode": "v",
                "separator_mode": "regex",
                "column": [
                    "ContainerNo"
                ],
                "behaviors": [
                    {
                        "over_action": "row",
                        "value_pattern": [
                            "(?P<col_1>([a-zA-Z]{4,}\\d{7,}\\s*)*)"
                        ],
                        "action": []
                    }
                ]
            }
        },
        "data_type_format": {
            "VoyageNo": {
                "data_type": "str",
                "filter": "r([/\\s])"
            },
            "EstimatedArrivalDate": {
                "data_type": "time",
                "format": "%m/%d/%Y",
                "filter": ""
            },
            "BillOfLadingsId": {
                "data_type": "str",
                "filter": "(\\s)"
            }
        },
        "text_repair": {
            "pdf_api": "http://www.baidu.com",
            "stop":"DestinationPortName",
            "subs": [
                ['VESSEL\\s*:\\s*(?P<VesselName>[\\w\\W]*?)\\s*VOYAGE\\s*:\\s*'],
                ["OPERATIONAL\\s*DISCH\\.\\s*PORT\\s*:\\s*(?P<DestinationPortName>[\\w\\W]*)$"],
            ],
        },
        # "address_repair": {
        #     "db": {
        #         "pub": {
        #             "user": "co",
        #             "pwd": "Co&23@2332$22",
        #             "server": "db.uat.com:1433",
        #             "database": "CO_PUB"
        #         }
        #     },
        #     "repairs": [
        #         {
        #             "key": "DeliveryPlaceName",
        #             "db_key": "pub",
        #             "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
        #             "column": [
        #                 0,
        #                 1,
        #                 2,
        #                 3
        #             ],
        #             "value": 4,
        #             "mapping": "DeliveryPlaceId",
        #             "old_val_handle": "empty"
        #         },
        #         {
        #             "key": "DestinationPortName",
        #             "db_key": "pub",
        #             "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
        #             "column": [
        #                 0,
        #                 1,
        #                 2,
        #                 3
        #             ],
        #             "value": 4,
        #             "mapping": "DestinationPortId",
        #             "old_val_handle": "empty"
        #         }
        #     ]
        # }
    }
}


class TestExcelDocumentParser:

    def test_excel_file_parse(self):
        """
        单文件测试
        :return:
        """
        factory = DocParserFactory.create("excel2",
                                          r"C:\Users\APing\Desktop\temp\noa-cmacgm-notice-of-arrival-oocl-chongqing-0upc4w1ma-3859949797819000.xlsx",
                                          config['parse'])
        result, errors = factory.parse()

        print(result, errors)


if __name__ == '__main__':
    pytest.main("-q --html=report.html")

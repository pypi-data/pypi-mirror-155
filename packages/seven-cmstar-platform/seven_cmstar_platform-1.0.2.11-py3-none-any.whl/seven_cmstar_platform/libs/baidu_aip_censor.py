# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/9/3 16:15
:LastEditTime: 2021/9/3 16:15
:LastEditors: SunYiTan
:Description: 百度内容审核
"""
import logging

from aip import AipContentCensor


class BaiduAipCensor:
    """
    百度内容审核：https://cloud.baidu.com/doc/ANTIPORN/s/gk3h6xfxl
    """

    def __init__(self, app_id, api_key, secret_key):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key

    def image_censor(self, url):
        """
        内容审核平台-图像, 图片参数为远程url图片
        :param url:
        :return:
            {'conclusion': '不合规', 'log_id': 16306575473448430, 'data': [{'msg': '存在百度官方违禁图不合规', 'conclusion': '不合规', 'subType': 0, 'conclusionType': 2, 'type': 0}], 'conclusionType': 2}
            {'conclusion': '合规', 'log_id': 16306576034770551, 'isHitMd5': False, 'conclusionType': 1}
        """
        client = AipContentCensor(self.app_id, self.api_key, self.secret_key)
        result = client.imageCensorUserDefined(url)
        # print(result)
        if result.__contains__("conclusionType"):
            if result["conclusionType"] == 1:
                # 合规
                return True, ""
            elif result["conclusionType"] == 2:
                # 不合规
                logging.getLogger("log_error").error(f"违禁图片，url：{url}，result：{result}")
                for data_dict in result["data"]:
                    return False, data_dict["msg"]
                return False, "图片存在违禁内容"
            elif result["conclusionType"] == 3:
                # 疑似
                return True, ""
            else:
                # 4 审核失败
                logging.getLogger("log_error").error(f"图片审核失败，url：{url}，result：{result}")
                return True, ""
        else:
            # 失败
            logging.getLogger("log_error").error(f"图片审核失败，url：{url}，result：{result}")
            return True, ""

    def text_censor(self, text: str):
        """
        内容审核平台-文本
        :param text:
        :return:
            {'conclusion': '不合规', 'log_id': 16318607791718580, 'data': [{'msg': '存在暴恐违禁不合规', 'conclusion': '不合规', 'hits': [{'wordHitPositions': [], 'probability': 0.9854951, 'datasetName': '百度默认文本反作弊库', 'words': [], 'modelHitPositions': [[0, 2, 0.9855]]}], 'subType': 1, 'conclusionType': 2, 'type': 12}, {'msg': '存在政治敏感不合规', 'conclusion': '不合规', 'hits': [{'wordHitPositions': [{'positions': [[0, 2]], 'label': '300101', 'keyword': '江泽民'}], 'probability': 1.0, 'datasetName': '百度默认文本反作弊库', 'words': ['江泽民'], 'modelHitPositions': [[0, 2, 0.9999]]}], 'subType': 3, 'conclusionType': 2, 'type': 12}], 'isHitMd5': False, 'conclusionType': 2}
            {'conclusion': '合规', 'log_id': 16318609705518401, 'isHitMd5': False, 'conclusionType': 1}
        """
        if not text:
            return True, ""

        client = AipContentCensor(self.app_id, self.api_key, self.secret_key)
        result = client.textCensorUserDefined(text)
        # print(result)
        if result.__contains__("conclusionType"):
            if result["conclusionType"] == 1:
                # 合规
                return True, ""
            elif result["conclusionType"] == 2:
                # 不合规
                logging.getLogger("log_error").error(f"违禁文本，text：{text}，result：{result}")
                for data_dict in result["data"]:
                    return False, data_dict["msg"]
                return False, "存在违禁词不合规"
            elif result["conclusionType"] == 3:
                # 疑似
                return True, ""
            else:
                # 4 审核失败
                logging.getLogger("log_error").error(f"文本审核失败，text：{text}，result：{result}")
                return True, ""
        else:
            # 失败
            logging.getLogger("log_error").error(f"文本审核失败，text：{text}，result：{result}")
            return True, ""

    def video_censor(self, video_name, video_url):
        """
        内容审核平台-视频
        :param text:
        :return:
            {"log_id": 15832318739570011, "conclusionType": 2, "conclusion": "不合规", "isHitMd5": false, "msg": "未命中视频黑库", "frames": [{"conclusionType": 2, "conclusion": "不合规", "frameTimeStamp": 0, "frameUrl": "http://bj.bcebos.com/v1/aip-web/2877d59d-414c-4b4f-9b99-9a125b6b2055?authorization=bce-auth-v1%2Ff86a2044998643b5abc89b59158bad6d%2F2020-03-03T10%3A37%3A56Z%2F-1%2F%2F8801a8dc24914caf2ea3d1c360d24002ccbbffb99c3f74d35a1257d07ea15529", "frameThumbnailUrl": "http://bj.bcebos.com/v1/aip-web/84e15149-2f91-4033-bff5-b7c6078107ed?authorization=bce-auth-v1%2Ff86a2044998643b5abc89b59158bad6d%2F2020-03-03T10%3A37%3A56Z%2F-1%2F%2Fa90ef9833579b3503863aea51a47e40ab2cd269a9354d8b0f4730c44803170f5", "data": [{"conclusionType": 2, "conclusion": "不合规", "type": 5, "subType": 1, "msg": "存在公众人物不合规", "stars": [{"probability": 0.96015228271484, "name": "圆圆"}]}]}], "conclusionTypeGroupInfos": [{"msg": "存在watermark不合规", "typeInfo": {"type": "广告检测"}, "subTypeInfoList": [{"subType": "watermark", "timestamp": 0}]}]}
            {'conclusion': '合规', 'log_id': 16318609705518401, 'isHitMd5': False, 'conclusionType': 1}
        """
        ext_id = video_url  # 视频在用户平台的唯一ID，方便人工审核结束时数据推送，用户利用此ID唯一锁定一条平台资源，若无可填写视频Url

        client = AipContentCensor(self.app_id, self.api_key, self.secret_key)
        result = client.videoCensorUserDefined(video_name, video_url, ext_id)
        # print(result)

        frame_url = ""
        if result.__contains__("frames"):
            for frame_dict in result["frames"]:
                frame_url = frame_dict["frameUrl"]
                break

        if result.__contains__("conclusionType"):
            if result["conclusionType"] == 1:
                # 合规
                return True, "", frame_url
            elif result["conclusionType"] == 2:
                # 不合规
                logging.getLogger("log_error").error(f"违禁视频，url：{video_url}，result：{result}")
                for frame_dict in result["frames"]:
                    if frame_dict["conclusionType"] == 2:
                        for data_dict in frame_dict["data"]:
                            if data_dict["conclusionType"] == 2:
                                return False, data_dict["msg"], frame_url
                return False, "视频存在违禁内容", frame_url
            elif result["conclusionType"] == 3:
                # 疑似
                return True, "", frame_url
            else:
                # 4 审核失败
                logging.getLogger("log_error").error(f"视频审核失败，url：{video_url}，result：{result}")
                return False, "视频审核失败", frame_url
        else:
            # 失败
            logging.getLogger("log_error").error(f"视频审核失败，url：{video_url}，result：{result}")
            return True, "视频审核失败，请稍后重试哦", frame_url

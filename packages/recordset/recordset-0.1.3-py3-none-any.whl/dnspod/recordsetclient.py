import logging

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client, models

import utils.logger as logger
from commons.config import get_env


class RecordSetClient:

    def __init__(self, profile=None):
        self.headers = {
            "X-TC-TraceId": "ffe0c072-8a5d-4e17-8887-a8a60252abca"
        }
        profile = profile if profile != None else "default"
        self.DOMAIN = get_env(profile, "domain")
        self.SECRET_ID = get_env(profile, 'secret_id')
        self.SECRET_KEY = get_env(profile, 'secret_key')
        self.REGION = get_env(profile, "region")  # "ap-guangzhou"

    def valid(self, value, subdomain):
        if value is None:
            logger.log_r("value could not null")
            exit()
        if subdomain is None:
            logger.log_r("subdomain could not null")
            exit()
        pass

    def run(self, method, value=None, subdomain=None, record_type=None):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
            cred = credential.Credential(self.SECRET_ID, self.SECRET_KEY)

            # 实例化一个http选项，可选的，没有特殊需求可以跳过。
            http_profile = HttpProfile()
            client_profile = ClientProfile()
            set_client_profile(client_profile, http_profile)

            # 实例化要请求产品(以cvm为例)的client对象，clientProfile是可选的。
            client = dnspod_client.DnspodClient(cred, self.REGION, client_profile)

            if method == "del":
                resp = self.describe_record_list(client)
                logging.debug(resp.to_json_string(indent=2))
                self.delete_record(client, value, subdomain, resp)

            if method == "add":
                req_add = models.CreateRecordRequest()
                self.valid(value, subdomain)
                resp_add = self.add_record_about_vpn(value, subdomain, record_type, client, req_add)
                print("record add succeed, info:\n", resp_add.to_json_string(indent=2))

            if method == "list":
                resp = self.describe_record_list(client)
                print(resp.to_json_string(indent=2))

        except TencentCloudSDKException as err:
            print(err)

    def describe_record_list(self, client):
        # 实例化一个cvm实例信息查询请求对象,每个接口都会对应一个request对象。
        req = models.DescribeRecordListRequest()
        req.Domain = self.DOMAIN
        # python sdk支持自定义header如 X-TC-TraceId、X-TC-Canary，可以按照如下方式指定，header必须是字典类型的
        req.headers = self.headers
        resp = client.DescribeRecordList(req)
        return resp

    def add_record_about_vpn(self, value, subdomain, record_type, client, req_add):
        req_add.Domain = self.DOMAIN
        req_add.SubDomain = subdomain
        req_add.Value = value
        req_add.RecordLine = "默认"
        req_add.RecordType = record_type if record_type is None else "A"
        resp_add = client.CreateRecord(req_add)
        return resp_add

    def delete_record(self, client, value, subdomain, resp):
        for record in resp.RecordList:
            if value is None:
                if subdomain is None:
                    logger.log_r("please enter your subdomain")
                    exit()
                if record.Name == subdomain:
                    self.delete_record_by_id(client, record.RecordId)
            elif value == record.Value:
                self.delete_record_by_id(client, record.RecordId)

    def delete_record_by_id(self, client, record_id):
        req_del = models.DeleteRecordRequest()
        req_del.RecordId = record_id
        req_del.Domain = self.DOMAIN
        resp_del = client.DeleteRecord(req_del)
        print("delete record succeed, info:", resp_del.to_json_string(indent=2))


def set_client_profile(client_profile, http_profile):
    http_profile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
    http_profile.keepAlive = True  # 状态保持，默认是False
    http_profile.reqMethod = "GET"  # get请求(默认为post请求)
    http_profile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
    http_profile.endpoint = "dnspod.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)
    client_profile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
    client_profile.language = "en-US"  # 指定展示英文（默认为中文）
    client_profile.httpProfile = http_profile


if __name__ == '__main__':
    RecordSetClient()

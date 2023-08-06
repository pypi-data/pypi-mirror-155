#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'andy.hu'
__mtime__ = '2021/12/28'

"""
import os
from qcloud_cos import CosConfig, CosS3Client

from clife_svc.libs.http_request import ClientRequest

from clife_svc.libs.log import klogger


class TxyCos:

    def __init__(self, cos_region=ClientRequest.COS_REGION, cos_secret_id=ClientRequest.COS_SECRET_ID,
                 cos_secret_key=ClientRequest.COS_SECRET_KEY):
        self.cos_client = self._create_txy_client(cos_region, cos_secret_id, cos_secret_key)

    def _create_txy_client(self, cos_region, cos_secret_id, cos_secret_key):
        """
        腾讯云上传client对象
        """

        try:
            config = CosConfig(Region=cos_region, Secret_id=cos_secret_id,
                               Secret_key=cos_secret_key,
                               )
            client = CosS3Client(config)

            klogger.info('_create_txy_client success')
            return client
        except Exception as e:
            raise Exception('_create_txy_client error:{}'.format(e))

    def cos_upload(self, file_apath: str, cos_key_dir: str, cos_bucket=ClientRequest.COS_BUCKET, retry=2):
        """
        :param file_apath:
        :param cos_key_dir:
        :param cos_bucket
        :param retry:
        :return:
        """
        if os.path.isfile(file_apath):
            while retry > 0:
                retry -= 1
                try:
                    cos_key = '{}/'.format(cos_key_dir) + os.path.split(file_apath)[1]
                    resp = self.cos_client.upload_file(
                        Bucket=cos_bucket,
                        LocalFilePath=file_apath,
                        Key=cos_key,
                        PartSize=20,
                        MAXThread=10
                    )
                    etag = resp.get('ETag', '')
                    if etag:
                        klogger.info('cos_upload success')
                        return {'cos_etag': etag, 'cos_key': cos_key}
                except Exception as e:
                    klogger.error('upload file error:{}'.format(e))

        else:
            raise Exception('file not exist:{}'.format(file_apath))

    def cos_object_exists(self, cos_key, cos_bucket=ClientRequest.COS_BUCKET):
        """
        判断cos文件是否存在
        :param cos_key:
        :param cos_bucket
        :return: bool
        """
        status = self.cos_client.object_exists(
            Bucket=cos_bucket,
            Key=cos_key
        )
        return status

    def cos_get_object(self, cos_key, save_file, cos_bucket=ClientRequest.COS_BUCKET, retry=2):
        """
        通过 cos_key 下载文件
        :return: save_file
        """
        while retry > 0:
            retry -= 0
            try:
                resp = self.cos_client.get_object(
                    Bucket=cos_bucket,
                    Key=cos_key,
                )

                body = resp['Body']
                body.get_stream_to_file(save_file)
                klogger.info('cos_get_object success:{}'.format(save_file))
                return save_file
            except Exception as e:
                klogger.error('cos_get_object error:{}'.format(e))
                raise e

    def cos_get_presigned_download_url(self, cos_key, bucket=ClientRequest.COS_BUCKET, expired=600, params={}, headers={}):
        """
        生成预签名的url,通过 url 下载文件,url有效期
        :param cos_key:
        :param bucket:
        :param expired: 秒
        :return:
        """
        url = self.cos_client.get_presigned_download_url(bucket, cos_key, Expired=expired, Params=params,
                                                         Headers=headers)
        return url

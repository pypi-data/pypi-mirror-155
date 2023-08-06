from .client import Client
from .bucket import Bucket
from .config import JSS_CONFIG
import json
import hashlib
import re


class Jss:

    def __init__(self, end_point, access_key, secret_key):
        """创建一个 jss 客户端实例
             @public
             :param {string} endpoint 所要连接的 endpoint 地址
             :param {string} accessKey 字符串 accessKey
             :param {string} secretKey 字符串 secretKey
             @example
             jss=new jss('storage.jd.com','your-accessKey-here','your-secretKey-here');
        """

        if not (isinstance(end_point, str) and end_point.strip()):
            if 'end_point' not in JSS_CONFIG or len(JSS_CONFIG['end_point']) == 0:
                raise ValueError('endpoint cannot be empty')
            else:
                end_point = JSS_CONFIG['end_point']
        if not (isinstance(access_key, str) and access_key.strip()):
            if 'access_key' not in JSS_CONFIG or len(JSS_CONFIG['access_key']) == 0:
                raise ValueError('access key cannot be empty')
            else:
                access_key = JSS_CONFIG['access_key']
        if not (isinstance(secret_key, str) and end_point.strip()):
            if 'secret_key' not in JSS_CONFIG or len(JSS_CONFIG['secret_key']) == 0:
                raise ValueError('secret key cannot be empty')
            else:
                secret_key = JSS_CONFIG['secret_key']

        self.endpoint = end_point
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = Client(end_point, access_key, secret_key)

    def bucket(self, name):
        """新建一个 Bucket 对象, 该对象封装了对 Bucket 的操作
             @public
             :param {string} bucketName bucket的名字;
             :returns {Bucket} 新建的 Bucket 对象
             @example
             bucket=jss.bucket('bucket-name')
        """

        return Bucket(self.client, name)

    def list_buckets(self):
        """列出所有 bucket
             @public
             :returns [{Bucket}]
             @example
             bucket=jss.list_bucket()
        """

        request = {
            'method': 'GET',
            'uri': '/'
        }
        res = self.client.execute(request)
        res.raise_for_status()
        json_text = json.loads(res.text)
        return json_text['Buckets']

    def has_bucket(self, bucket_name):
        """ 判断bucket是否存在
             @public
             :param {string} bucket_name bucket的名字;
             :returns [{Bucket}]
             @example
             bucket=jss.has_bucket('your_bucket_name')
        """
        if not (isinstance(bucket_name, str) and bucket_name.strip()):
            raise ValueError('参数 name 必须为非空字符串')

        bucket_list = self.list_buckets()
        has_bucket_flag = False
        for item in bucket_list:
            if item['Name'] == bucket_name:
                has_bucket_flag = True
                break
        return has_bucket_flag

    def _encode_post_data(self, js_data):
        encode_data = []
        if not isinstance(js_data, dict):
            encode_data.extend([self._encode_post_data(i) for i in js_data])
            return encode_data
        for values in js_data.values():
            if isinstance(values, dict):
                encode_data.extend(self._encode_post_data(values))
            elif isinstance(values, list):
                for i in values:
                    if isinstance(i, dict):
                        encode_data.extend(self._encode_post_data(i))
                    else:
                        i = re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039\u002e])", "", str(i))
                        if i == "":
                            continue
                        encode_data.append(i)
            else:
                values = re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039\u002e])", "", str(values))
                if values == "":
                    continue
                encode_data.append(values)
        return encode_data    

    def save_data(self, url, post_data, resp, bucket_name="pfinder-data-bucket"):
        if post_data is None:
            file_name = '/'.join(url.split("/")[-2:])
        else:
            file_name = url.split("/")[-1] + '/' + '/'.join(self._encode_post_data(post_data))
        resp = self.bucket(bucket_name).object(file_name).put_data(json.dumps(resp), file_name)
        if resp.status_code != 200:
            raise OverflowError("Save data into oss error!")
        return True

    def get_data(self, url, post_data, bucket_name="pfinder-data-bucket"):
        if post_data is None:
            file_name = '/'.join(url.split("/")[-2:])
        else:
            file_name = url.split("/")[-1] + '/' + '/'.join(self._encode_post_data(post_data))
        resp = self.bucket(bucket_name).object(file_name).get().content
        data = json.loads(resp)
        return data

    def has_data(self, url, post_data, bucket_name="pfinder-data-bucket"):
        if post_data is None:
            file_name = '/'.join(url.split("/")[-2:])
        else:
            file_name = url.split("/")[-1] + '/' + '/'.join(self._encode_post_data(post_data))
        has_file_flag = self.bucket(bucket_name).object(file_name).exist()
        return has_file_flag

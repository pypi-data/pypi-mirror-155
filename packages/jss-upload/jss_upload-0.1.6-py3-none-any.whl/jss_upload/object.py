import os
import urllib.parse
from requests import codes
from hashlib import md5
import logging
import json
import io

log = logging.getLogger(__name__)


class Object:
    """
    Object 是京东云存储中的基本实体，由键(Key)，数据(Data)和元数据(Metadata)三部分组成。关于数据(Data)，
    京东云存储并不关心其内容具体是什么。而元数据(Metadata)则是一组键值(Key-Value)的组合，包括数据的长度，创建时间，MD5 值等
    """

    def __init__(self, client, bucket, key):
        """创建一个 Object 实例
             @public
             :param {Client} client Client 实例
             :param {Bucket} bucket Bucket 实例
             :param {string} key Bucket 名称
        """

        if not (isinstance(key, str) and key.strip()):
            raise ValueError('name cannot be empty')
        self.key = key
        self.client = client
        self.bucket = bucket

    def get(self, headers=None):
        """下载一个资源并读取其内容
             @public
             :returns {Response.Body} 成功时 statusCode 为 200, 获得文件内容
             @example
             jss.bucket('your-bucket-name').object('your-object-name').get()
        """
        bucket_name = self.bucket.name
        object_key = self.key

        request = {
            'method': 'GET',
            'uri': '/' + bucket_name + '/' + object_key
        }
        if headers:
            request['headers'] = headers
        try:
            return self.client.execute(request)
        except Exception as e:
            logging.error("JSS: get object failed" + repr(e), stack_info=True)
            raise ConnectionError('JSS: get object failed!' + repr(e))

    def put_data(self, body_data, file_new_name):
        """以data方式上传或替换一个资源
             @public
             :param {string} data_body 要上传资源的raw data
             :param {string} file_new_name 下载时文件的保存名称
             :returns 成功时 statusCode 为 200, 返回的Body为空;
             @example
             jss.bucket('pro-test').object('123.html').put(your_data_variable, '123.html')
        """
        bucket_name = self.bucket.name
        object_key = file_new_name
        headers = {
            'content-type': '',
            'Content-Disposition': "attachment; filename={func_result}".format(
                func_result=urllib.parse.quote(file_new_name, safe='~()*!.\''))
        }
        request = {
            'method': 'PUT',
            'uri': '/' + bucket_name + '/' + object_key,
            'headers': headers,
            'body': body_data.encode(encoding='UTF-8')
        }
        try:
            return self.client.execute(request)
        except Exception as e:
            logging.error("JSS: put_data failed" + repr(e), stack_info=True)
            raise ConnectionError("put data failed" + repr(e))

    def put_file(self, file_with_path, file_new_name):
        """以本地文件形式上传或替换一个资源
             @public
             :param {string} file_with_path 要上传资源的本地路径
             :param {string} file_new_name 下载时文件的保存名称
             :returns {Promise.<Response.body>} resolve，成功时 statusCode 为 200, 返回的Body为空;
             @example
             jss.bucket('pro-test').object('123.html').put_file('/file/folder/123.html', '123.html')
        """
        bucket_name = self.bucket.name
        object_key = file_new_name

        if not (isinstance(file_with_path, str) and file_with_path.strip()):
            raise ValueError('参数 path 必须为非空字符串')

        if file_new_name is None:
            file_new_name = object_key

        if not os.path.exists(file_with_path):
            raise IOError('can not find file')

        headers = {
            'content-type': '',
            'Content-Disposition': "attachment; filename={func_result}".format(
                func_result=urllib.parse.quote(file_new_name, safe='~()*!.\''))
        }
        with open(file_with_path) as fh:
            data_body = fh.read()

            request = {
                'method': 'PUT',
                'uri': '/' + bucket_name + '/' + object_key,
                'headers': headers,
                'body': data_body.encode(encoding='UTF-8')
            }
            try:
                return self.client.execute(request)
            except Exception as e:
                logging.error("JSS: put_file failed" + repr(e), stack_info=True)
                raise ConnectionError("put file failed" + repr(e))

    def init_multipart_upload(self):
        """初始化分块上传任务
             @public
             :returns {string} upload_id 返回分块上传的任务id
        """
        bucket_name = self.bucket.name
        object_key = self.key

        request = {
            'method': 'POST',
            'uri': '/' + bucket_name + '/' + object_key + '?uploads'
        }
        res = self.client.execute(request)
        res.raise_for_status()
        json_text = json.loads(res.text)
        return json_text['UploadId']

    def upload_part(self, upload_id, part_number, input_stream):
        """上传分块数据
             @public
             :param {string} upload_id: 分块上传任务id
             :param {int} part_number: 自定义分块编号, e.g., 1, 2, 3...
             :returns {dict} headers 返回该分块的头文件信息，其中etag等信息需要用在complete_multipart_upload
        """
        if not (isinstance(upload_id, str) and upload_id.strip()):
            raise ValueError('upload_id 必须是非空字符串')
        if not (isinstance(part_number, int)):
            raise ValueError('part_number 必须是非空整数')
        bucket_name = self.bucket.name
        object_key = self.key

        request = {
            'method': 'PUT',
            'uri': '/' + bucket_name + '/' + object_key + '?partNumber=' + str(part_number) + '&uploadId=' + upload_id,
            'body': input_stream
        }
        res = self.client.execute(request)
        res.raise_for_status()
        return res.headers

    def complete_multipart_upload(self, upload_id, parts):
        """完成分块上传任务
             @public
             :param {string} upload_id: 分块上传任务id
             :param {List} parts: 分块信息，例子:
             parts = [{'PartNumber' : '1',
                        'ETag': "xxxxxxx"}]
             :returns {dict} 成功则返回Object的信息
        """
        if not (isinstance(upload_id, str) and upload_id.strip()):
            raise ValueError('upload_id 必须是非空字符串')

        bucket_name = self.bucket.name
        object_key = self.key

        headers = {
            'content-type': 'application/json'
        }
        part_body = {'Part': parts}
        request = {
            'method': 'POST',
            'uri': '/' + bucket_name + '/' + object_key + '?uploadId=' + upload_id,
            'headers': headers,
            'body': json.dumps(part_body)
        }
        res = self.client.execute(request)
        res.raise_for_status()
        json_text = json.loads(res.text)
        return json_text

    def abort_multipart_upload(self, upload_id):
        """终止分块上传任务
             @public
             :param {string} upload_id: initMultipartUpload() 成功后response body中的分块上传任务id
             :returns 成功时 statusCode 为 204, body为空
        """
        if not (isinstance(upload_id, str) and upload_id.strip()):
            raise ValueError('upload_id 必须是非空字符串')
        bucket_name = self.bucket.name
        object_key = self.key

        request = {
            'method': 'DELETE',
            'uri': '/' + bucket_name + '/' + object_key + '?uploadId=' + upload_id
        }
        try:
            return self.client.execute(request)
        except Exception as e:
            raise ConnectionError('abort Multi-part upload failed: ' + repr(e))

    def delete(self):
        """删除一个 Object
             @public
             :returns 成功时 statusCode 为 204, 返回的Body为空
        """

        bucket_name = self.bucket.name
        object_key = self.key
        request = {
            'method': 'DELETE',
            'uri': '/' + bucket_name + '/' + object_key
        }
        try:
            return self.client.execute(request)
        except:
            raise ValueError('delete bucket failed!')

    def head(self):
        """获取一个 Object的元数据
             @public
             :returns {dict} 返回Object的元数据
             @example
             jss.bucket('pro-test').object('123.html').head()
        """
        bucket_name = self.bucket.name
        object_key = self.key
        request = {
            'method': 'HEAD',
            'uri': '/' + bucket_name + '/' + object_key
        }
        res = self.client.execute(request)
        res.raise_for_status()
        return res.headers

    def exist(self):
        """判断某个 Object的是否存在
             @public
             :returns 成功时为True, 失败返回false
             @example
             jss.bucket('pro-test').object('123.html').head()
        """
        bucket_name = self.bucket.name
        object_key = self.key
        request = {
            'method': 'HEAD',
            'uri': '/' + bucket_name + '/' + object_key
        }

        r = self.client.execute(request)

        if r.status_code == codes.ok:
            return True
        else:
            return False

from .object import Object
import json

"""
Bucket是存放“文件”（云存储称之为Object）的容器，所有的Object都必须存放到某个Bucket中。
"""


class Bucket:

    def __init__(self, client, name):
        """创建一个 Bucket 实例
             @public
             :param {Client} client Client 实例
             :param {string} name Bucket 名称
        """
        if not (isinstance(name, str) and name.strip()):
            raise ValueError('name cannot be empty')
        self.name = name
        self.client = client

    def create(self):
        """新建一个 Bucket
             @public
             :returns 成功时 statusCode 为 200, 返回的Body为空
        """
        request = {
            'method': 'PUT',
            'uri': '/' + self.name
        }
        try:
            return self.client.execute(request)
        except Exception:
            raise ValueError('cannot create bucket')

    def delete(self):
        """删除一个 Bucket
             @public
             :returns 成功时 statusCode 为 204, 返回的Body为空
        """
        request = {
            'method': 'DELETE',
            'uri': '/' + self.name
        }
        try:
            delete_result = self.client.execute(request)
            return delete_result
        except:
            raise ValueError('cannot delete bucket')

    def object(self, key):
        """创建一个 JssObject
             @public
             :param {string} key Object的名字;
             :returns {JssObject} 新建的 JssObject 对象
             @example
             object=jss.bucket('bucket-name').object('object-name')
        """
        return Object(self.client, self, key)

    def list_object(self, marker=None, maxKeys=None, prefix=None, delimiter=None):
        """列出所有 JssObject （可加筛选条件）
             @public
             :optional param {string} marker 指定的Object的Key的起始标志;
             :optional param {string} maxKeys 指定的Object的数量;
             :optional param {string} prefix 指定的Object Key的前缀;
             :optional param {string} delimiter 指定的Delimiter分组符;
             :returns [{JssObject}] 新建的 JssObject 对象
             @example
             object=jss.bucket('bucket-name').object('object-name')
        """
        name = self.name
        if (not marker and not maxKeys and not prefix and not delimiter):
            request = {
                'method': 'GET',
                'uri': '/' + name,
                'json': True
            }
        else:
            additional_params = {}
            if marker:
                additional_params['marker'] = marker
            if maxKeys:
                additional_params['maxKeys'] = maxKeys
            if prefix:
                additional_params['prefix'] = prefix
            if delimiter:
                additional_params['delimiter'] = delimiter
            request = {
                'method': 'GET',
                'uri': '/' + name,
                'json': True,
                'additional_params': additional_params
            }
        res = self.client.execute(request)
        res.raise_for_status()
        json_text = json.loads(res.text)
        obj_list, hasnext = json_text['Contents'], json_text['HasNext']
        while hasnext:
            request['additional_params']['marker'] = obj_list[-1]['Key']
            res = self.client.execute(request)
            res.raise_for_status()
            json_text = json.loads(res.text)
            obj_list, hasnext = obj_list + json_text['Contents'], json_text['HasNext']
        return obj_list

    # TODO: ACL
    # def acl(self):

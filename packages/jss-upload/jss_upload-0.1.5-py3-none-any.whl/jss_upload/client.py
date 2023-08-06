import base64
import email.utils
import hashlib
import hmac
import logging
import requests

from . import config

log = logging.getLogger(__name__)


class Client:
    def __init__(self, endpoint, access_key, secret_key):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key

    def __auth(self, method, date, headers, access_key, secret_key, uri):
        def getJssHeaders(headers):
            map = []
            for key, value in headers.items():
                if key.startswith(config.JSS_CONFIG['JSS_HEADER_PREFIX']):
                    map.append({key: value})
            return map

        headers_content_md5 = ''
        headers_content_type = headers.get('content-type', '')
        str_to_sign = method + '\n' + headers_content_md5 + '\n' + headers_content_type + '\n' + \
                      headers['date'] + '\n' + uri
        secret_key_encode = secret_key.encode('utf-8')
        h = hmac.new(secret_key_encode, str_to_sign.encode('utf-8'), hashlib.sha1)
        token = base64.b64encode(h.digest())
        return 'jingdong ' + access_key + ':' + token.decode()

    def execute(self, opt):
        date = email.utils.formatdate(usegmt=True)
        request_headers = {'date': date}
        # if additional parameters in headers exist, combine headers information together
        if 'headers' in opt:
            request_headers = {**request_headers, **opt['headers']}

        authorization = self.__auth(opt['method'], date, request_headers, self.access_key, self.secret_key, opt['uri'])
        request_headers['authorization'] = authorization

        log.debug("request header is: ---> {0}".format(request_headers))

        if opt['method'] == "GET":
            url = self.endpoint + opt['uri']
            log.debug("composed url is: " + url)
            if 'json' in opt and 'additional_params' in opt:
                return requests.get(url, params=opt['additional_params'], headers=request_headers)
            else:
                return requests.get(url, headers=request_headers)

        elif opt['method'] == "PUT":
            url = self.endpoint + opt['uri']
            log.debug("composed url is: " + url)
            return requests.put(url, headers=request_headers, data=opt['body'])

        elif opt['method'] == "DELETE":
            url = self.endpoint + opt['uri']
            log.debug("composed url is: " + url)
            return requests.delete(url, headers=request_headers)

        elif opt['method'] == "HEAD":
            url = self.endpoint + opt['uri']
            log.debug("composed url is: " + url)
            return requests.head(url, headers=request_headers)

        elif opt['method'] == "POST":
            url = self.endpoint + opt['uri']
            log.debug("composed url is: " + url)
            if 'body' in opt:
                return requests.post(url, headers=request_headers, data=opt['body'])
            else:
                return requests.post(url, headers=request_headers)
        else:
            raise ValueError("this method: " + opt['method'] + " is not valid")

import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def parse_jss_uri(uri):
    """Return the bucket and object path of the uri.

    Parameters:
        uri : string
            A JSS URI such as `jss://domainname/mybucket/path/to/file`

    Examples:
        >>> parse_jss_uri("jss://domainname/mybucket/path/to/file")
        'mybucket', 'path/to/file'
    """
    if uri.startswith('jss://'):
        uri = uri[6:]
    if '/' not in uri:
        return uri, ""
    elif uri.startswith('/'):
        uri = uri[1:]

    s = uri.split('/', 2)
    return s[1], s[2]

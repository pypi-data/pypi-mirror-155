# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omnio']

package_data = \
{'': ['*']}

modules = \
['README', 'LICENSE']
install_requires = \
['boto3>=1.10,<2.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'omnio',
    'version': '1.2.2',
    'description': 'Python library for opening URIs as streaming file-like objects',
    'long_description': '# omnio\n\n*Python 3 library for opening URIs as streaming file-like objects*\n\nThis library provides the `omnio.open()` function with an interface very\nsimilar to that of the built in Python `open` function.  The difference is\nthat while Python\'s `open` operates only on local filesystem paths, `omnio`\naccepts URIs as well.\n\nIt currently supports `file`, `http`, and `s3` URIs, though it may be\nexpanded to support additional schemes in the future.\n\nIn addition, it supports compression and decompression of streams with gzip\nor bz2.\n\n## Features\n\n* API is a superset of Python 3\'s built-in open() function\n* Based on Python 3 `io` module\n* Gzip and bzip2 support both for reading and writing\n* Local file support using standard library\n* HTTP support using `requests`\n* S3 support using `boto3`\n\n## Examples\n\nRead a local binary file:\n\n    >>> with omnio.open(\'example.bin\', \'r\') as f:\n    >>>     data = f.read()\n\nRead a local text file:\n\n    >>> with omnio.open(\'example.txt\', \'rt\') as f:\n    >>>     text = f.read()\n\nRead a text file from the web:\n\n    >>> with omnio.open(\'https://example.com/example.txt\', \'rt\') as f:\n    >>>     text = f.read()\n\nRead a gzipped text file from the web, uncompressing on the fly:\n\n    >>> with omnio.open(\'https://example.com/example.txt.gz\', \'rtz\') as f:\n    >>>     text = f.read()\n\nRead a text file from s3:\n\n    >>> with omnio.open(\'s3://my-bucket/my-key\', \'rt\') as f:\n    >>>     text = f.read()\n\nWrite a megabyte of random data to s3, compressing with bzip2:\n\n    >>> import os\n    >>> data = os.urandom(1024**2)\n    >>> with omnio.open(\'s3://my-bucket/my-key\', \'wbj\') as f:\n    >>>     f.write(data)\n\nRead a bzip2 compressed csv file into a list of data rows:\n\n    >>> import csv\n    >>> with omnio.open(\'data/example_data.csv.bz2\', \'rtj\') as f:\n    >>>     reader = csv.reader(f)\n    >>>     data = list(reader)\n\n\n## API\n\nThe omnio API consists of a single function intended to be referenced as\n`omnio.open()`. This function API is designed to mimic Python 3\'s built-in\n`open()` as much as possible, and should normally be able to be used as a\ndrop-in replacement.\n\n_Signature:_\n\n`omnio.open(uri, mode=\'rb\', encoding=None, errors=None, newline=None)`\n\n_Returns:_\n\nA file-like object whose type depends on the scheme and the mode.\n\n_Parameters:_\n  * _uri_ -- URI or local path. Supported URI schemes are `file`,\n  `http`, and `s3`. Local paths may be specified by as ordinary path\n  strings.\n\n  * _mode_ -- Optional string that specifies the mode in which the\n  file is opened. It defaults to \'rb\' which means open for reading\n  in binary mode. Supported modes are documented below.\n\n_Modes:_\n\n| Character | Meaning |\n| --------- | ------- |\n| \'r\'       | open for reading (default)                  |\n| \'w\'       | open for writing, truncating the file first |\n| \'b\'       | binary mode (default)                       |\n| \'t\'       | text mode                                   |\n| \'z\'       | use gzip compression                        |\n| \'j\'       | use bzip2 compression                       |\n\nThese characters can be composed into valid modes. Binary mode is\nalways the default, so some mode specifications are equivalent.\nThe complete list of supported modes are as follows:\n\n| Mode        | Meaning |\n| ----------- | ------- |\n| \'r\', \'rb\'   | read bytes                                          |\n| \'rt\'        | read and decode to unicode                          |\n| \'rz\', \'rbz\' | read, decompressing gzip to bytes                   |\n| \'rj\', \'rbj\' | read, decompressing bzip2 to bytes                  |\n| \'rtz\'       | read, decompress gzip to bytes, decode to unicode   |\n| \'rtj\'       | read, decompress bzip2 to bytes, decode to unicode  |\n| \'w\', \'wb\'   | write bytes                                         |\n| \'wt\'        | write unicode, encoding to bytes                    |\n| \'wz\', \'wbz\' | write bytes, compress with gzip                     |\n| \'wj\', \'wbj\' | write bytes, compress with bzip2                    |\n| \'wtz\'       | write unicode, encode to bytes, compress with gzip  |\n| \'wtj\'       | write unicode, encode to bytes, compress with bzip2 |\n\n_Some keyword arguments may be applicable to only certain modes. For\nexample, `encoding` only applies to \'t\' (text) modes._\n\n_Some schemes may not support some modes.  For example, the http\nscheme currently does not support any \'w\' (write) modes._\n\n\n## Configuration\n\nThe `omnio.open` function accepts an optional `config` parameter. This allows\nfor specifying scheme-specific configuration.\n\nThe `default_config()` method returns a config dictionary with all supported\nkeys defined along with their default values.\n\n    >>> import omnio\n    >>> omnio.default_config()\n    {\'file\': {}, \'http\': {\'content_iter_chunk_size\': 512}, \'s3\': {\'upload_part_size\': 5242880, \'boto_client_config_args\': [], \'boto_client_config_kwargs\': {}}}\n\nTo specify alternate values for these parameters, instantiate a default\nconfig, update the dict with the desired values and pass it as a keyword arg\nto the `omnio.open()` function.\n\n    >>> config = omnio.default_config()\n    >>> config["s3"]["boto_client_config_kwargs"] = {"read_timeout": 600}\n    >>> with omnio.open("s3://my-bucket/my-key", "rt", config=config) as fd:\n        fd.read()\n',
    'author': 'Bob Green',
    'author_email': 'rgreen@aquent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scoutexchange/omnio',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

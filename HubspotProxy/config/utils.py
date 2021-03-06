# -*- coding: utf-8 -*-

import os
import sys

import urllib.parse as urlparse


def get_dtb_config(uri):
    dtb = {}
    try:
        url = urlparse.urlparse(uri)

        # Update with environment configuration.
        dtb.update({
            'DB': url.path[1:],
            'USERNAME': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port if url.port else 27017,
        })

    except Exception:
        print('Unexpected error:', sys.exc_info())

    return dtb


def getenv(name, default=None):
    if default is not None:
        return os.environ.get(name, default)
    else:
        return os.environ.get(name)

# -*- coding: utf-8 -*-

import os.path

from .utils import get_dtb_config, getenv


class BaseConfig(object):
    '''
    Base settings for BoostUpTechExam project.
    '''

    DEBUG = False

    TESTING = False

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    SECRET_KEY = getenv('SECRET_KEY')

    MONGODB_SETTINGS = get_dtb_config('mongodb://localhost/hubspot')


class Production(BaseConfig):
    pass


class Development(BaseConfig):
    '''
    Development settings.
    '''
    DEBUG = True


class Testing(BaseConfig):
    '''
    Testing settings.
    '''

    TESTING = True

    MONGODB_SETTINGS = get_dtb_config("mongodb://localhost/HubspotProxy_test")

import os

class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = 'S\xf7\x16\xd2k\xf77\xd8P\xf2\x8b\xc7(\xb8\xf8\xfae\x14o>`\x9b\x14U'


class DevelopmentConfig(BaseConfig):
	DEBUG = True


class ProductionConfig(BaseConfig):
	DEBUG = False
	SECRET_KEY = os.environ.get('SECRET_KEY')
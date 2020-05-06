class Config(object):
    """
    Common configurations
    Pul any configurations here that are common
    """


class DevelopmentConfig(Config):
    """
    Development env configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

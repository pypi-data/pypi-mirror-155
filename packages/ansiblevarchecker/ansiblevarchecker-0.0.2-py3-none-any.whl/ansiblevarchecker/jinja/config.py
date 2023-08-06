class Config(object):
    """Configuration."""

    PACKAGE_NAME = ''
    """Name of the package where you want to load templates from.

    This configuration is for if you are using includes in your jinja templates. This tells jinja
    where to look to be able to load the included template from. If you do not plan on using ``includes``
    this configuration is not needed.
    """

    TEMPLATE_DIR = 'templates'
    """Name of the directory where you want to load templates from. Defaulted to ``templates``

    This configuration is for if you are using includes in your jinja templates. This tells jinja
    which directoy to look to be able to load the included template from. If you do not plan on using ``includes``
    this configuration is not needed.
    """

    CUSTOM_FILTERS = []

    RAISE_ON_NO_FILTER = False

    RAISE_ON_INVALID_FILTER_ARGS = True

    def __init__(self,
                PACKAGE_NAME='',
                TEMPLATE_DIR='templates',
                CUSTOM_FILTERS=[],
                RAISE_ON_NO_FILTER=False,
                RAISE_ON_INVALID_FILTER_ARGS=True):
        self.PACKAGE_NAME = PACKAGE_NAME
        self.TEMPLATE_DIR = TEMPLATE_DIR
        self.CUSTOM_FILTERS = CUSTOM_FILTERS
        self.RAISE_ON_NO_FILTER = RAISE_ON_NO_FILTER
        self.RAISE_ON_INVALID_FILTER_ARGS = RAISE_ON_INVALID_FILTER_ARGS


default_config = Config()

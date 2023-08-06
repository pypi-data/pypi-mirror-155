"""
An API adapter and in-memory cache for the Site Configuration backend configuration.
"""

from django.conf import settings

from dateutil import parser


AMC_V1_STRUCTURE_VERSION = 'amc-v1'


class SiteConfigAdapter:
    """
    Adapter for Open edX translates the values in a format that Open edX can use.
    """

    backend_configs = None

    TYPE_SETTING = 'setting'
    TYPE_SECRET = 'secret'  # nosec
    TYPE_ADMIN = 'admin'
    TYPE_PAGE = 'page'
    TYPE_CSS = 'css'

    def __init__(self, site_uuid, status='live'):
        self.site_uuid = site_uuid
        self.status = status

    def get_backend_configs(self):
        if not self.backend_configs:
            client = settings.SITE_CONFIG_CLIENT
            self.backend_configs = client.get_backend_configs(self.site_uuid, self.status)
        return self.backend_configs

    def delete_backend_configs_cache(self):
        """
        Enforce getting a fresh entry for the current context/request and following ones.
        """
        self.backend_configs = None
        client = settings.SITE_CONFIG_CLIENT
        client.delete_cache_for_site(self.site_uuid, self.status)

    def get_value_of_type(self, config_type, name, default):
        all_configs = self.get_backend_configs()['configuration']
        type_configs = all_configs[config_type]
        return type_configs.get(name, default)

    def get_css_variables_dict(self):
        """
        Get a variable_name:value dictionary of CSS variables.
        """
        config = self.get_backend_configs()['configuration']
        return config[self.TYPE_CSS]

    def get_site_info(self):
        """
        Get the site information from site config.

        Return dict(
          always_active: boolean
          domain_name: string
          environment: dict(name: string)
          subscription_ends: date
          tier: string
          uuid: UUID
        )

        Note, is_active is not returned from the response since it can be outdated.
        """
        site_info = self.get_backend_configs()['site'].copy()  # Get a copy of the object to manipulate it.

        # Remove `is_active` property to avoid caching it
        site_info.pop('is_active', None)

        # Convert the string to useful datetime object
        site_info['subscription_ends'] = parser.parse(site_info['subscription_ends'])

        return site_info

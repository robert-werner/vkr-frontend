from typing import Any

from decouple import config, UndefinedValueError


class Settings(object):  # noqa: WPS230
    """Class with server settings."""

    def __init__(self) -> None:
        """Create class with server settings."""
        self.db_user = self.get_setting("DB_USER", "vkr")
        self.db_password = self.get_setting("DB_PASSWORD", "vkr")
        self.db_name = self.get_setting("DB_NAME", "vkr")
        self.db_host = self.get_setting("DB_HOST", "localhost")
        self.db_port = self.get_setting("DB_PORT", "6432")

    def get_setting(self, name: str, default: Any) -> Any:
        """Get setting.

        :param name: Setting name
        :param default: Default value
        :return: Setting value
        """
        setting = None
        try:
            setting = config(name)
        except UndefinedValueError:
            setting = default

        return setting


settings = Settings()

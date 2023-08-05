from typing import Dict

from airflow.hooks.base import BaseHook

from sifflet.configure.service import SiffletConfig


class SiffletHook(BaseHook):
    """
    Hook for Sifflet interaction.

    This hook requires authentication details:
      - Sifflet tenant - The tenant matches the prefix of your Sifflet url.
      - Sifflet Access Token - The access token must be generated in the Web UI of Sifflet.

    Args:
        sifflet_conn_id (str): The connection ID to use when fetching connection info.
    """

    conn_name_attr = "sifflet_conn_id"
    default_conn_name = "sifflet_default"
    conn_type = "sifflet"
    hook_name = "Sifflet"

    def __init__(self, sifflet_conn_id: str = "sifflet_default") -> None:
        super().__init__()
        self.sifflet_conn_id = sifflet_conn_id

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ["host", "login", "port"],
            "relabeling": {"password": "Sifflet Access Token", "schema": "Sifflet Tenant"},
            "placeholders": {
                "schema": "The tenant matches the prefix of your Sifflet url.",
                "password": "The access token must be generated in the Web UI of Sifflet.",
            },
        }

    def get_conn(self) -> SiffletConfig:
        """Returns the SiffletConfig for the current connection id."""
        conn = self.get_connection(self.sifflet_conn_id)
        conn_params = conn.extra_dejson

        tenant = conn.schema
        token = conn.password
        dev_mode = conn_params.get("dev_mode", False)
        debug = conn_params.get("debug", False)
        return SiffletConfig(tenant=tenant, token=token, dev_mode=dev_mode, debug=debug)

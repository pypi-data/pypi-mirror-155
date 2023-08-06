import base64
import json
from typing import Any, List, Optional

import boto3
from dynaconf import Dynaconf


class LazyConfig:
    def __init__(self, settings: Dynaconf = None):
        self._settings = settings

    def __getattr__(self, item) -> Any:
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    @property
    def settings(self) -> Dynaconf:
        if not self._settings:
            self.load()
        return self._settings

    @property
    def env_name(self) -> Optional[str]:
        return self.get("ENV_FOR_DYNACONF")

    def get(self, key: str, default=None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        if not self._settings:
            raise Exception("Config not loaded")
        self._settings.set(key, value)

    def update(self, **kwargs):
        if not self._settings:
            raise Exception("Config not loaded")
        self._settings.update(**kwargs)

    def load(self, override_files: List[str] = None):
        if not override_files:
            override_files = []
        settings_files = ["settings.toml", "local.toml", "secrets.toml"] + override_files
        self._settings = Dynaconf(environments=True, settings_files=settings_files)
        try:
            self.load_kms_secrets(secret_id=self.get("KMS_SECRET_ID"))
        except Exception as e:
            print(f"Failed loading KMS secrets: {e}")

    def load_kms_secrets(self, secret_id: Optional[str]) -> dict:
        if not secret_id:
            print("No KMS secret name provided")
            return {}
        client = boto3.client(service_name="secretsmanager")
        response = client.get_secret_value(SecretId=secret_id)
        if "SecretString" in response:
            secrets_string = response["SecretString"]
        else:
            secrets_string = base64.b64decode(response["SecretBinary"])
        secrets_dict = json.loads(secrets_string) or {}
        self.update(**secrets_dict)  # type: ignore
        print("KMS secrets loaded successfully")
        return secrets_dict

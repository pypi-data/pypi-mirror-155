from slai.clients.cli import SlaiCliClient, get_cli_client
from slai.modules.parameters import from_config
from importlib import import_module
from functools import lru_cache


def get_model_client(*, model_uri):
    import_path = from_config(
        "MODEL_CLIENT",
        "slai.clients.model.ModelClient",
    )
    class_ = import_path.split(".")[-1]
    path = ".".join(import_path.split(".")[:-1])
    return getattr(import_module(path), class_)(
        model_uri=model_uri,
    )


class ModelClient:
    def __init__(
        self,
        *,
        model_uri: str,
    ):
        self.model_uri = model_uri
        self.cli_client: SlaiCliClient = get_cli_client()
        self.sandbox = self.get_sandbox()

    @lru_cache(maxsize=64)
    def get_sandbox(self):
        sandbox_data = self.cli_client.retrieve_sandbox(
            uri=self.model_uri,
        )
        return sandbox_data

    def get_latest_model_artifact(self):
        model_artifact = self.cli_client.retrieve_model_artifact(
            model_version_id=self.sandbox["model_version_id"],
            model_artifact_id=None,
        )
        return model_artifact

    def list_model_artifacts(self):
        model_artifacts = self.cli_client.retrieve_model_artifact()
        return model_artifacts

import requests
import copy

from functools import lru_cache
from requests.auth import HTTPBasicAuth
from importlib import import_module
from slai.modules.parameters import from_config
from slai.config import get_api_base_urls
from slai.modules.runtime import detect_credentials
from slai.clients.model import ModelClient, get_model_client
from slai.types import ModelTypes, InvalidPayloadException, InvalidTypeException

REQUESTS_TIMEOUT = 180


def get_inference_client(*, model_uri):
    import_path = from_config(
        "MODEL_INFERENCE_CLIENT",
        "slai.clients.inference.ModelInferenceClient",
    )
    class_ = import_path.split(".")[-1]
    path = ".".join(import_path.split(".")[:-1])

    return getattr(import_module(path), class_)(
        model_uri=model_uri,
    )


@lru_cache(maxsize=64)
def _get_model_info(
    base_url,
    client_id,
    client_secret,
    sandbox_id,
):
    body = {"sandbox_id": sandbox_id}

    res = requests.post(
        f"{base_url}/model/info",
        auth=HTTPBasicAuth(client_id, client_secret),
        json=body,
        timeout=REQUESTS_TIMEOUT,
    )
    res.raise_for_status()
    model_info = res.json()

    input_schema = ModelTypes.load_schema(model_info["input_schema"])
    output_schema = ModelTypes.load_schema(model_info["output_schema"])
    inference_url = model_info["inference_url"]

    return input_schema, output_schema, inference_url


class ModelInferenceClient:
    BACKEND_BASE_URL, _ = get_api_base_urls()

    def __init__(self, *, model_uri):
        credentials = detect_credentials()

        self.client_id = credentials["client_id"]
        self.client_secret = credentials["client_secret"]
        self.model_uri = model_uri

        self._load_model()

    def _load_model(self):
        self.model_client: ModelClient = get_model_client(
            model_uri=self.model_uri,
        )
        self.sandbox = self.model_client.get_sandbox()

    def call(self, payload):
        input_schema, output_schema, inference_url = _get_model_info(
            self.BACKEND_BASE_URL,
            self.client_id,
            self.client_secret,
            self.sandbox["short_id"],
        )

        try:
            serialized_payload = ModelTypes.serialize(payload, input_schema)
        except (InvalidTypeException, InvalidPayloadException) as e:
            print(e, e.errors)
            return None

        res = requests.post(
            f"{inference_url}",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            json=serialized_payload,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        response_data = res.json()

        errors = response_data["result"].get("errors", [])
        if errors:
            print("An unhandled exception occurred in your handler:\n ")

            for e in errors:
                print(e)

            return None

        try:
            result = ModelTypes.deserialize(response_data["result"], output_schema)
        except (InvalidTypeException, InvalidPayloadException) as e:
            print(e, e.errors)
            return None

        return result

    def info(self):
        return copy.copy(
            _get_model_info(
                self.BACKEND_BASE_URL,
                self.client_id,
                self.client_secret,
                self.sandbox["short_id"],
            )
        )

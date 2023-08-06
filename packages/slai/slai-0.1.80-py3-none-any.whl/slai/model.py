from slai.clients.inference import get_inference_client


class Model:
    def __init__(self, model_uri):
        self.model_uri = model_uri
        self.inference_client = get_inference_client(
            model_uri=self.model_uri,
        )

    def __call__(self, **inputs):
        return self.inference_client.call(payload=inputs)

    def call(self, **inputs):
        return self.inference_client.call(payload=inputs)

    def info(self):
        return self.inference_client.info()

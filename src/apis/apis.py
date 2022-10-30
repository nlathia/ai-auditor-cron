import os
from src.apis import (gcp)

def get(api_name: str):
    """ Given a name, return an AI API """
    apis = {"gcp": gcp}
    return apis[api_name]

import requests
import os

def save(results: dict):
    results["API_KEY"] = os.environ["API_KEY"] # Very lax
    r = requests.post(
        os.environ["HEROKU_API_URL"],
        json=results,
    )
    if r.status_code != 200:
        raise Exception(f"failed with: {r.status_code}")


from typing import Optional, List
from collections import defaultdict
from datetime import datetime
import os
import random
import logging
# Testing comment
import os
import random

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from dataclasses_json.cfg import config
from flask import Flask, jsonify, request

import evaluate

from src.data import stream, webapp
from src.apis import apis

app = Flask(__name__)
logger = logging.getLogger(__name__)


@dataclass_json
@dataclass
class AuditRequest:

    """ AuditRequest: which API to audit (api_name),
    using which dataset (dataset_name) """

    # Which sentiment API to audit
    api_name: str = "gcp"

    # Which dataset to use in the audit
    dataset_name: str = "rotten_tomatoes"

    # Limit to a given number of requests
    num_samples: Optional[int] = field(default=None, metadata=config(exclude=lambda x: x is None))

    # Number of misclassifications *per class* to return
    num_mistakes: Optional[int] = 1


@dataclass_json
@dataclass
class AuditResponse:

    """ Structure of the response dictionary
    that is sent to the web app """

    # Audit run
    api_name: str
    dataset_name: str
    created: str
    num_samples: int
    num_minutes: float

    # Metrics
    accuracy: float
    f1: float
    precision: float
    recall: float
    mistakes: List[dict]

    @classmethod
    def from_metrics(cls, req, num_samples: int, num_minutes: float, metrics: dict, mistakes: list):
        return AuditResponse(
            api_name=req.api_name,
            dataset_name=req.dataset_name,
            created=datetime.strftime(datetime.utcnow(), "%H:%M %d %B %Y"),
            num_samples=num_samples,
            num_minutes=num_minutes,
            accuracy=metrics.get("accuracy"),
            f1=metrics.get("f1"),
            precision=metrics.get("precision"),
            recall=metrics.get("recall"),
            mistakes=mistakes,
        )


@app.route('/', methods=['POST'])
def main():
    """ Handler which runs the AI API audit """
    req = AuditRequest.from_dict(request.get_json())

    metrics = evaluate.combine(["accuracy", "f1", "precision", "recall"])
    mistakes = defaultdict(list)
    num_examples = 0

    sentiment_api = apis.get(req.api_name)
    client = sentiment_api.get_client()
    start = datetime.utcnow()
    for entry in stream.iter_dataset(req.dataset_name, req.num_samples):
        try:
            y_pred, y_prob = sentiment_api.predict(client, entry['text'])
            y_label = entry['label']

            if y_pred != y_label:
                entry["prediction"] = y_pred
                entry["magnitude"] = y_prob
                mistakes[y_label].append(entry)
            
            metrics.add(references=y_label, predictions=y_pred)
            num_examples += 1
        except Exception as exc:
            logger.exception(exc)
            continue
    end = datetime.utcnow()
    num_minutes = (end - start).seconds / 60
    
    results = metrics.compute()
    mistakes_sample = []
    for examples in mistakes.values():
        mistakes_sample += random.sample(
            examples,
            min(req.num_mistakes, len(examples)),
        )
    
    resp = AuditResponse.from_metrics(
        req,
        num_examples, 
        num_minutes, 
        results, 
        mistakes_sample,
    ).to_dict()
    webapp.save(resp)

    return jsonify(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

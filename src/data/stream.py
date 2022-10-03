from typing import Iterable
from datasets import load_dataset


def iter_dataset(name: str, num_samples: int = None) -> Iterable[dict]:
    """ Stream the `name` dataset from hugging face """
    i = 0
    dataset = load_dataset(name, split="test", streaming=True)
    for entry in dataset:
        if i == num_samples:
            break
        i += 1
        yield entry

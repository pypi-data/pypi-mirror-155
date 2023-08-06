"""
Transformations

This model will merge every `Emission` from the `Transformation` back in the `Cycle`.
"""
from hestia_earth.utils.tools import flatten

REQUIREMENTS = {
    "Cycle": {
        "optional": {
            "transformations": [
                {"@type": "Transformation", "inputs": [{"@type": "Input", "value": ""}]}
            ]
        }
    }
}
RETURNS = {
    "Emission": [{
        "value": ""
    }]
}


def _emissions(transformation: dict):
    emissions = transformation.get('emissions', [])
    inputs = [transformation.get('term')]
    should_run = len(transformation.get('inputs', [])) > 0
    return [{**e, 'inputs': inputs} for e in emissions] if should_run else []


def run(cycle: dict): return flatten(list(map(_emissions, cycle.get('transformations', []))))

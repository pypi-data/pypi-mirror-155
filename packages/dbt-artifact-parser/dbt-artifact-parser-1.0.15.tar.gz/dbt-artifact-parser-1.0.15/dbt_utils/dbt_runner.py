import os
from typing import List


def get_downstream_models(model: str) -> List[str]:
    dbt_model_list = os.popen(f"dbt ls --models {model}+").read()
    return dbt_model_list.splitlines()

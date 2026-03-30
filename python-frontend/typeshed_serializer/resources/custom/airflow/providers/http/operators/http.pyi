from airflow.models.baseoperator import BaseOperator

class HttpOperator(BaseOperator):
    def __init__(self, *args, **kwargs) -> None: ...

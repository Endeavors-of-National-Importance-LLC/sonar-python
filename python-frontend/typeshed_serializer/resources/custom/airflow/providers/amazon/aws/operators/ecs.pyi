from airflow.models.baseoperator import BaseOperator

class EcsRunTaskOperator(BaseOperator):
    def __init__(self, *args, **kwargs) -> None: ...

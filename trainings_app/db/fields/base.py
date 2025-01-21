import abc


class BaseFields(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_fields_list() -> list[str]:
        """Retrieve the list of model fields"""
        ...

    @classmethod
    @abc.abstractmethod
    def get_fields_str(cls) -> str:
        """Retrieve the str containing the model fields"""
        ...

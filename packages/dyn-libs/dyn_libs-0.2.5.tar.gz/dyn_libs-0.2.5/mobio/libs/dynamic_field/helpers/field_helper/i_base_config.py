import inspect


class IBaseConfig:

    def __init__(self):
        self.result = {}

    @classmethod
    def get_all_attribute(cls):
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        values = [
            a[1]
            for a in attributes
            if not (a[0].startswith("__") and a[0].endswith("__"))
        ]
        return values

    def to_json(self):
        return {x: self.result.get(x) for x in self.get_all_attribute()}

    def set_all_data(self, **kwargs):
        for key in self.get_all_attribute():
            if key in kwargs:
                self.result[key] = kwargs.get(key)

    @staticmethod
    def check_field_value_type(field_key, field_value, field_type):
        if type(field_value) != field_type:
            raise Exception(
                "{}: {} is not valid".format(
                    field_key,field_value,
                )
            )

import inspect
from enum import Enum


class IBaseConstant:
    @classmethod
    def get_all_constant(cls):
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        values = [
            a[1]
            for a in attributes
            if not (a[0].startswith("__") and a[0].endswith("__"))
        ]
        return values


class MerchantConfigCommon:
    PREFIX_DYNAMIC_FIELD = "_dyn"
    PREFIX_CRITERIA = 'cri'


class DynamicFieldProperty(IBaseConstant):
    INTEGER = 1
    FLOAT = 4
    STRING = 2
    DATETIME = 3
    DICT = 5
    EMAIL = 6
    PHONE_NUMBER = 7
    UDT = 14


class DisplayType(Enum):
    SINGLE_LINE = "single_line"
    MULTI_LINE = "multi_line"
    DROPDOWN_SINGLE_LINE = "dropdown_single_line"
    DROPDOWN_MULTI_LINE = "dropdown_multi_line"
    RADIO_SELECT = "radio"
    CHECKBOX = "checkbox"
    DATE_PICKER = "date_picker"
    TAGS = "tags"


class DynamicFieldGroup:
    INFORMATION = "information"
    DEMOGRAPHIC = "demographic"
    ACTIVITY = "activity"
    LOYALTY = "loyalty"
    OTHER = "other"
    DYNAMIC = "dynamic"


class DynamicFieldStatus(IBaseConstant):
    ENABLE = 1
    DISABLE = 0
    DELETED = -1


class DataSelectedStatus(IBaseConstant):
    ENABLE = 1
    DISABLE = 0


DATE_PICKER_FORMAT = [
    {"key": "dd/mm", "format": "%d/%m", "alternate_format": "%d-%m", "year": 2099},
    {
        "key": "dd/mm/yyyy",
        "format": "%d/%m/%Y",
        "alternate_format": "%d-%m-%Y",
        "year": None,
    },
    {
        "key": "dd/mm/yyyy hh:mm",
        "format": "%d/%m/%Y %H:%M",
        "alternate_format": "%d-%m-%Y %H:%M",
        "year": None,
    },
]

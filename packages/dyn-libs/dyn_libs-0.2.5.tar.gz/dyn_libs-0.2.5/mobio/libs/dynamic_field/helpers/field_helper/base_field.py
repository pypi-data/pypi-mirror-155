from datetime import datetime
from random import randint
from time import time
import re

from unidecode import unidecode
from mobio.libs.dynamic_field.helpers import (
    DynamicFieldProperty,
    DisplayType,
    DATE_PICKER_FORMAT,
    MerchantConfigCommon,
    DynamicFieldStatus,
    DynamicFieldGroup,
    DataSelectedStatus,
)
from mobio.libs.dynamic_field.helpers.field_helper.i_base_config import IBaseConfig


class BaseDataSelected(IBaseConfig):

    ID = "id"
    VALUE = "value"
    COLOR = "color"
    ENABLE = "enable"

    def set_id(self, data_id: int):
        self.result[self.ID] = data_id

    def get_id(self):
        return self.result.get(self.ID)

    def set_value(self, value):
        self.result[self.VALUE] = value

    def get_value(self):
        return self.result.get(self.VALUE)

    def set_color(self, color):
        self.result[self.COLOR] = color

    def get_color(self):
        return self.result.get(self.COLOR)

    def set_enable(self, enable):
        self.result[self.ENABLE] = enable

    def get_enable(self):
        return (
            self.result.get(self.ENABLE)
            if self.result.get(self.ENABLE)
            else DataSelectedStatus.ENABLE
        )


class BaseHistory(IBaseConfig):
    STAFF_ID = "staff_id"
    FULLNAME = "fullname"
    USERNAME = "username"
    CREATED_TIME = "created_time"

    def set_staff_id(self, staff_id):
        self.result[self.STAFF_ID] = staff_id

    def get_staff_id(self):
        return self.result.get(self.STAFF_ID)

    def set_fullname(self, fullname):
        self.result[self.FULLNAME] = fullname

    def get_fullname(self):
        return self.result.get(self.FULLNAME)

    def set_username(self, username):
        self.result[self.USERNAME] = username

    def get_username(self):
        return self.result.get(self.USERNAME)

    def set_created_time(self, created_time):
        self.result[self.CREATED_TIME] = created_time

    def get_created_time(self):
        return (
            self.result.get(self.CREATED_TIME)
            if self.result.get(self.CREATED_TIME)
            else datetime.utcnow()
        )


class BaseField(IBaseConfig):
    # DISPLAY
    DISPLAY_DETAIL = "display_detail"
    DISPLAY_IN_FORM_ADD = "display_in_form_add"
    DISPLAY_IN_FORM_ADD_SELECTED = "display_in_form_add_selected"
    ORDER_FORM_ADD = "order_form_add"
    REQUIRED_FORM_ADD = "required_form_add"
    DISPLAY_IN_FORM_UPDATE = "display_in_form_update"
    DISPLAY_IN_FORM_UPDATE_SELECTED = "display_in_form_update_selected"
    ORDER_FORM_UPDATE = "order_form_update"
    REQUIRED_FORM_UPDATE = "required_form_update"
    DISPLAY_IN_IMPORT_FILE = "display_in_import_file"
    DISPLAY_IN_LIST_FIELD = "display_in_list_field"
    DISPLAY_IN_LIST_FIELD_SELECTED = "display_in_list_field_selected"
    ORDER_LIST_FIELD = "order_list_field"
    DISPLAY_IN_FILTER = "display_in_filter"
    DISABLE_REMOVE_FORM_INPUT = "disable_remove_form_input"
    DISABLE_REMOVE_LIST = "disable_remove_list"
    DISABLE_REQUIRED_FORM_INPUT = "disable_required_form_input"
    ENABLE_DATA_COLOR = "enable_data_color"

    # CONFIG
    FIELD_NAME = "field_name"
    FIELD_KEY = "field_key"
    FIELD_PROPERTY = "field_property"
    DISPLAY_TYPE = "display_type"
    DATA_SELECTED = "data_selected"
    FORMAT = "format"
    GROUP = "group"
    IS_BASE = "is_base"
    STATUS = "status"
    TRANSLATE_KEY = "translate_key"
    SUPPORT_SORT = "support_sort"
    DESCRIPTION = "description"
    CREATED_TIME = "created_time"
    UPDATED_TIME = "updated_time"
    HISTORY = "history"
    LAST_UPDATE_BY = "last_update_by"
    IS_ENCRYPT = "is_encrypt"
    FIELD_ORDER = "order"

    def __init__(self):
        super().__init__()
        self.result = {
            self.CREATED_TIME: datetime.utcnow(),
            self.UPDATED_TIME: datetime.utcnow(),
            self.STATUS: DynamicFieldStatus.ENABLE,
            self.IS_BASE: False,
            self.DISPLAY_DETAIL: True,
            self.DISPLAY_IN_FORM_ADD: True,
            self.DISPLAY_IN_FORM_ADD_SELECTED: True,
            self.ORDER_FORM_ADD: randint(1, 300),
            self.REQUIRED_FORM_ADD: False,
            self.DISPLAY_IN_FORM_UPDATE: True,
            self.DISPLAY_IN_FORM_UPDATE_SELECTED: True,
            self.ORDER_FORM_UPDATE: randint(1, 300),
            self.REQUIRED_FORM_UPDATE: False,
            self.DISPLAY_IN_IMPORT_FILE: True,
            self.DISPLAY_IN_LIST_FIELD: True,
            self.DISPLAY_IN_LIST_FIELD_SELECTED: True,
            self.ORDER_LIST_FIELD: randint(1, 300),
            self.DISPLAY_IN_FILTER: True,
            self.DISABLE_REMOVE_FORM_INPUT: False,
            self.DISABLE_REMOVE_LIST: False,
            self.DISABLE_REQUIRED_FORM_INPUT: False,
            self.ENABLE_DATA_COLOR: False,
            self.FIELD_ORDER: randint(1, 300),
        }

    @staticmethod
    def __convert_field_name_2_field_key__(field_name):
        time_stamp = int(round(time() * 1000))
        return "{}_{}_{}".format(
            MerchantConfigCommon.PREFIX_DYNAMIC_FIELD,
            re.sub("[^a-zA-Z0-9]|\\s+", "_", unidecode(field_name)),
            time_stamp,
        ).lower()

    def set_display_detail(self, display_detail: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_DETAIL,
            field_value=display_detail,
            field_type=str,
        )
        self.result[self.DISPLAY_DETAIL] = display_detail

    def get_display_detail(self):
        return self.result.get(self.DISPLAY_DETAIL)

    def set_display_in_form_add(self, display_in_form_add: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_IN_FORM_ADD,
            field_value=display_in_form_add,
            field_type=bool,
        )
        self.result[self.DISPLAY_IN_FORM_ADD] = display_in_form_add

    def get_display_in_form_add(self):
        return self.result.get(self.DISPLAY_IN_FORM_ADD)

    def set_display_in_form_add_selected(self, display_in_form_add_selected: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_IN_FORM_ADD_SELECTED,
            field_value=display_in_form_add_selected,
            field_type=bool,
        )
        self.result[self.DISPLAY_IN_FORM_ADD_SELECTED] = display_in_form_add_selected

    def get_display_in_form_add_selected(self):
        return self.result.get(self.DISPLAY_IN_FORM_ADD_SELECTED)

    def set_order_form_add(self, order_form_add):
        self.result[self.ORDER_FORM_ADD] = order_form_add

    def get_order_form_add(self):
        return self.result.get(self.ORDER_FORM_ADD)

    def set_required_form_add(self, required_form_add: bool):
        self.check_field_value_type(
            field_key=self.REQUIRED_FORM_ADD,
            field_value=required_form_add,
            field_type=bool,
        )
        self.result[self.REQUIRED_FORM_ADD] = required_form_add

    def get_required_form_add(self):
        return self.result.get(self.REQUIRED_FORM_ADD)

    def set_display_in_form_update(self, display_in_form_update: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_IN_FORM_UPDATE,
            field_value=display_in_form_update,
            field_type=bool,
        )
        self.result[self.DISPLAY_IN_FORM_UPDATE] = display_in_form_update

    def get_display_in_form_update(self):
        return self.result.get(self.DISPLAY_IN_FORM_UPDATE)

    def set_display_in_form_update_selected(self, display_in_form_update_selected: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_IN_FORM_UPDATE_SELECTED,
            field_value=display_in_form_update_selected,
            field_type=bool,
        )
        self.result[
            self.DISPLAY_IN_FORM_UPDATE_SELECTED
        ] = display_in_form_update_selected

    def get_display_in_form_update_selected(self):
        return self.result.get(self.DISPLAY_IN_FORM_UPDATE_SELECTED)

    def set_order_form_update(self, order_form_update):
        self.result[self.ORDER_FORM_UPDATE] = order_form_update

    def get_order_form_update(self):
        return self.result.get(self.ORDER_FORM_UPDATE)

    def set_required_form_update(self, required_form_update: bool):
        self.check_field_value_type(
            field_key=self.REQUIRED_FORM_UPDATE,
            field_value=required_form_update,
            field_type=bool,
        )
        self.result[self.REQUIRED_FORM_UPDATE] = required_form_update

    def get_required_form_update(self):
        return self.result.get(self.REQUIRED_FORM_UPDATE)

    def set_display_in_import_file(self, display_in_import_file: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_IN_IMPORT_FILE,
            field_value=display_in_import_file,
            field_type=bool,
        )
        self.result[self.DISPLAY_IN_IMPORT_FILE] = display_in_import_file

    def get_display_in_import_file(self):
        return self.result.get(self.DISPLAY_IN_IMPORT_FILE)

    def set_display_in_list_field(self, display_in_list_field: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_IN_LIST_FIELD,
            field_value=display_in_list_field,
            field_type=bool,
        )
        self.result[self.DISPLAY_IN_LIST_FIELD] = display_in_list_field

    def get_display_in_list_field(self):
        return self.result.get(self.DISPLAY_IN_LIST_FIELD)

    def set_display_in_list_field_selected(self, display_in_list_field_selected: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_IN_LIST_FIELD_SELECTED,
            field_value=display_in_list_field_selected,
            field_type=bool,
        )
        self.result[
            self.DISPLAY_IN_LIST_FIELD_SELECTED
        ] = display_in_list_field_selected

    def get_display_in_list_field_selected(self):
        return self.result.get(self.DISPLAY_IN_LIST_FIELD_SELECTED)

    def set_order_list_field(self, order_list_field):
        self.result[self.ORDER_LIST_FIELD] = order_list_field

    def get_order_list_field(self):
        return self.result.get(self.ORDER_LIST_FIELD)

    def set_display_in_filter(self, display_in_filter: bool):
        self.check_field_value_type(
            field_key=self.DISPLAY_IN_FILTER,
            field_value=display_in_filter,
            field_type=bool,
        )
        self.result[self.DISPLAY_IN_FILTER] = display_in_filter

    def get_display_in_filter(self):
        return self.result.get(self.DISPLAY_IN_FILTER)

    def set_disable_remove_form_input(self, disable_remove_form_input: bool):
        self.check_field_value_type(
            field_key=self.DISABLE_REMOVE_FORM_INPUT,
            field_value=disable_remove_form_input,
            field_type=bool,
        )
        self.result[self.DISABLE_REMOVE_FORM_INPUT] = disable_remove_form_input

    def get_disable_remove_form_input(self):
        return self.result.get(self.DISABLE_REMOVE_FORM_INPUT)

    def set_disable_remove_list(self, disable_remove_list: bool):
        self.check_field_value_type(
            field_key=self.DISABLE_REMOVE_LIST,
            field_value=disable_remove_list,
            field_type=bool,
        )
        self.result[self.DISABLE_REMOVE_LIST] = disable_remove_list

    def get_disable_remove_list(self):
        return self.result.get(self.DISABLE_REMOVE_LIST)

    def set_disable_required_form_input(self, disable_required_form_input: bool):
        self.check_field_value_type(
            field_key=self.DISABLE_REQUIRED_FORM_INPUT,
            field_value=disable_required_form_input,
            field_type=bool,
        )
        self.result[self.DISABLE_REQUIRED_FORM_INPUT] = disable_required_form_input

    def get_disable_required_form_input(self):
        return self.result.get(self.DISABLE_REQUIRED_FORM_INPUT)

    def set_enable_data_color(self, enable_data_color: bool):
        self.check_field_value_type(
            field_key=self.ENABLE_DATA_COLOR,
            field_value=enable_data_color,
            field_type=bool,
        )
        self.result[self.ENABLE_DATA_COLOR] = enable_data_color

    def get_enable_data_color(self):
        return (
            self.result.get(self.ENABLE_DATA_COLOR)
            if self.result.get(self.ENABLE_DATA_COLOR)
            else False
        )

    def set_field_name(self, field_name: str):
        if not field_name or (3 > len(field_name) or len(field_name) > 50):
            raise Exception(
                "{}: must be between 3 and 50 in length".format(self.FIELD_NAME)
            )
        self.result[self.FIELD_NAME] = field_name.strip()
        # self.result[self.FIELD_KEY] = self.__convert_field_name_2_field_key__(
        #     self.result[self.FIELD_NAME]
        # )

    def get_field_name(self):
        return self.result.get(self.FIELD_NAME)

    def set_field_key(self, field_key: str):
        if not field_key.startswith(MerchantConfigCommon.PREFIX_DYNAMIC_FIELD):
            self.check_field_value_type(
                field_key=self.FIELD_KEY,
                field_value=field_key,
                field_type=str,
            )
        self.result[self.FIELD_KEY] = field_key

    def get_field_key(self):
        return self.result.get(self.FIELD_KEY)

    def set_field_property(self, field_property):
        if field_property not in DynamicFieldProperty.get_all_constant():
            raise Exception(
                "{}: {} is not valid".format(self.FIELD_PROPERTY, field_property)
            )
        self.result[self.FIELD_PROPERTY] = field_property

    def get_field_property(self):
        return self.result.get(self.FIELD_PROPERTY)

    def set_display_type(self, display_type):
        if display_type not in [x.value for x in DisplayType]:
            raise Exception(
                "{}: {} is not valid".format(self.DISPLAY_TYPE, display_type)
            )
        self.result[self.DISPLAY_TYPE] = display_type

    def get_display_type(self):
        return self.result.get(self.DISPLAY_TYPE)

    def set_data_selected(self, data_selected: list):
        for x in data_selected:
            if not isinstance(x, BaseDataSelected):
                raise Exception(
                    "{}: {} is not valid".format(self.DATA_SELECTED, data_selected)
                )

        self.result[self.DATA_SELECTED] = [x.to_json() for x in data_selected]

    def get_data_selected(self):
        return self.result.get(self.DATA_SELECTED)

    def set_format(self, date_format):
        if date_format not in [x.get("key") for x in DATE_PICKER_FORMAT]:
            raise Exception("{}: {} is not valid".format(self.FORMAT, date_format))
        self.result[self.FORMAT] = date_format

    def get_format(self):
        return self.result.get(self.FORMAT)

    def set_group(self, group):
        self.result[self.GROUP] = group

    def get_group(self):
        return (
            self.result.get(self.GROUP)
            if self.result.get(self.GROUP)
            else DynamicFieldGroup.DYNAMIC
        )

    def set_is_base(self, is_base: bool):
        self.result[self.IS_BASE] = is_base

    def get_is_base(self):
        return self.result.get(self.IS_BASE) if self.result.get(self.IS_BASE) else False

    def set_status(self, status):
        if status not in DynamicFieldStatus.get_all_constant():
            raise Exception("{}: {} is not valid".format(self.STATUS, status))
        self.result[self.STATUS] = status

    def get_status(self):
        return (
            self.result.get(self.STATUS)
            if self.result.get(self.STATUS)
            else DynamicFieldStatus.ENABLE
        )

    def set_translate_key(self, translate_key):
        self.result[self.TRANSLATE_KEY] = translate_key

    def get_translate_key(self):
        return self.result.get(self.TRANSLATE_KEY)

    def set_support_sort(self, support_sort: bool):
        self.check_field_value_type(
            field_key=self.SUPPORT_SORT,
            field_value=support_sort,
            field_type=bool,
        )
        self.result[self.SUPPORT_SORT] = support_sort

    def get_support_sort(self):
        return (
            self.result.get(self.SUPPORT_SORT)
            if self.result.get(self.SUPPORT_SORT)
            else False
        )

    def set_description(self, description):
        self.result[self.DESCRIPTION] = description

    def get_description(self):
        return self.result.get(self.DESCRIPTION)

    def set_created_time(self, created_time):
        self.result[self.CREATED_TIME] = created_time

    def get_created_time(self):
        return (
            self.result.get(self.CREATED_TIME)
            if self.result.get(self.CREATED_TIME)
            else datetime.utcnow()
        )

    def set_updated_time(self, updated_time):
        self.result[self.UPDATED_TIME] = updated_time

    def get_updated_time(self):
        return (
            self.result.get(self.UPDATED_TIME)
            if self.result.get(self.UPDATED_TIME)
            else datetime.utcnow()
        )

    def set_last_update_by(self, last_update_by):
        if not isinstance(last_update_by, BaseHistory):
            raise Exception(
                "{}: {} is not valid".format(self.LAST_UPDATE_BY, last_update_by)
            )
        self.result[self.LAST_UPDATE_BY] = last_update_by.to_json()
        if not self.result.get(self.HISTORY):
            self.result[self.HISTORY] = []
        if len(self.result.get(self.HISTORY)) > 5:
            self.result[self.HISTORY].pop(0)
        self.result[self.HISTORY].append(self.result[self.LAST_UPDATE_BY])

    def get_last_update_by(self):
        return self.result.get(self.LAST_UPDATE_BY)

    def set_is_encrypt(self, is_encrypt: bool):
        self.check_field_value_type(
            field_key=self.IS_ENCRYPT,
            field_value=is_encrypt,
            field_type=bool,
        )
        self.result[self.IS_ENCRYPT] = is_encrypt

    def get_is_encrypt(self):
        return self.result.get(self.IS_ENCRYPT)

    def set_field_order(self, order: int):
        self.check_field_value_type(
            field_key=self.FIELD_ORDER,
            field_value=order,
            field_type=int,
        )
        self.result[self.FIELD_ORDER] = order

    def get_field_order(self):
        return self.result.get(self.FIELD_ORDER) or randint(80, 300)

    def create_elastic_mapping(self):
        if self.result.get(self.FIELD_PROPERTY) is None:
            print(
                "{}::create_elastic_mapping: field property is None".format(
                    self.__class__.__name__
                )
            )
            return None

        if self.result.get(self.FIELD_PROPERTY) == DynamicFieldProperty.INTEGER:
            return {self.result.get(self.FIELD_KEY): {"type": "long"}}
        elif self.result.get(self.FIELD_PROPERTY) == DynamicFieldProperty.FLOAT:
            return {self.result.get(self.FIELD_KEY): {"type": "double"}}
        if self.result.get(self.FIELD_PROPERTY) == DynamicFieldProperty.STRING:
            return {
                self.result.get(self.FIELD_KEY): {
                    "type": "keyword",
                    "normalizer": "lowerasciinormalizer",
                }
            }
        if self.result.get(self.FIELD_PROPERTY) == DynamicFieldProperty.DATETIME:
            return {self.result.get(self.FIELD_KEY): {"type": "date"}}
        if self.result.get(self.FIELD_PROPERTY) == DynamicFieldProperty.UDT:
            return {
                self.result.get(self.FIELD_KEY): {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {
                            "type": "keyword",
                            "normalizer": "lowerasciinormalizer",
                        },
                    },
                }
            }
        raise Exception(self.result.get(self.FIELD_KEY))

    def to_json(self):
        # set default data to config if not has data
        lst_key_required = [
            self.FIELD_NAME,
            self.FIELD_PROPERTY,
            self.DISPLAY_TYPE,
        ]
        lst_key_missing = []
        for key in lst_key_required:
            if not self.result.get(key):
                lst_key_missing.append(key)
        if lst_key_missing:
            raise Exception("{}: is null or empty".format(",".join(lst_key_missing)))

        # Required FORMAT if DISPLAY_TYPE is datetime
        if self.result.get(
            self.DISPLAY_TYPE
        ) == DisplayType.DATE_PICKER.value and not self.result.get(self.FORMAT):
            raise Exception(
                "{}: is required with {}: {}".format(
                    self.FORMAT, self.DISPLAY_TYPE, self.result.get(self.DISPLAY_TYPE)
                )
            )

        if not self.result.get(self.FIELD_KEY):
            self.result[self.FIELD_KEY] = self.__convert_field_name_2_field_key__(
                self.result[self.FIELD_NAME]
            )
        if not self.result.get(self.GROUP):
            self.result[self.GROUP] = self.get_group()
        if not self.result.get(self.IS_BASE):
            self.result[self.IS_BASE] = self.get_is_base()
        if not self.result.get(self.STATUS):
            self.result[self.STATUS] = self.get_status()
        if not self.result.get(self.SUPPORT_SORT):
            self.result[self.SUPPORT_SORT] = self.get_support_sort()
        if not self.result.get(self.CREATED_TIME):
            self.result[self.CREATED_TIME] = self.get_created_time()
        if not self.result.get(self.UPDATED_TIME):
            self.result[self.UPDATED_TIME] = self.get_updated_time()
        if not self.result.get(self.HISTORY):
            last_update_by = BaseHistory()
            last_update_by.set_all_data(
                staff_id="mobio",
                fullname="MOBIO",
                username="MOBIO",
                created_time=self.get_created_time(),
            )
            self.set_last_update_by(last_update_by)
        if not self.result.get(self.FIELD_ORDER):
            self.result[self.FIELD_ORDER] = self.get_field_order()
        if not self.result.get(self.ENABLE_DATA_COLOR):
            self.result[self.ENABLE_DATA_COLOR] = self.get_enable_data_color()
        return {x: self.result.get(x) for x in self.get_all_attribute()}

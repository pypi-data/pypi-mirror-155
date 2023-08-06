from datetime import datetime
from mobio.libs.dynamic_field.helpers import MerchantConfigCommon
from mobio.libs.dynamic_field.helpers.field_helper.base_field import (
    BaseField,
    BaseHistory,
)
from mobio.libs.dynamic_field.models.elastic.base_model import ElasticSearchBaseModel
from mobio.libs.dynamic_field.models.mongo.field_history_model import FieldHistoryModel
from mobio.libs.dynamic_field.models.mongo.merchant_config import MerchantConfig


class IBaseDynController:
    def __init__(self, mongo_url_connection):
        self.url_connection = mongo_url_connection

    def remove_field(self, merchant_id, field_key, updated_by):
        if not field_key.startswith(MerchantConfigCommon.PREFIX_DYNAMIC_FIELD):
            raise Exception("field: {} cannot be changed".format(field_key))
        merchant_config = MerchantConfig(
            url_connection=self.url_connection
        ).get_merchant_config(merchant_id=merchant_id)
        merchant_fields = merchant_config.get(MerchantConfig.DYNAMIC_FIELDS)
        old_dyn_fields = [
            x
            for x in merchant_fields
            if x.get(BaseField.FIELD_KEY).startswith(
                MerchantConfigCommon.PREFIX_DYNAMIC_FIELD
            )
        ]
        exists_field = next(
            (x for x in old_dyn_fields if x.get(BaseField.FIELD_KEY) == field_key),
            None,
        )
        if not exists_field:
            print("field: {} not exists".format(field_key))
            return False

        new_dyn_fields = [
            x for x in old_dyn_fields if x.get(BaseField.FIELD_KEY) != field_key
        ]
        merchant_config[MerchantConfig.DYNAMIC_FIELDS] = new_dyn_fields
        merchant_config[MerchantConfig.UPDATED_TIME] = datetime.utcnow()
        result_update = MerchantConfig(self.url_connection).update_merchant(
            merchant_config=merchant_config
        )
        if result_update:
            result_logging = self.logging_field_change(
                merchant_id=merchant_id,
                old_fields=old_dyn_fields,
                new_fields=new_dyn_fields,
                staff_id=updated_by.to_json().get(BaseHistory.STAFF_ID),
            )
            print(
                "result_update: {}, result_logging: {}".format(
                    result_update, result_logging
                )
            )
            return True
        return False

    def save_field(
        self,
        merchant_id,
        field_class,
        updated_by,
        els_index,
    ):
        field_key = field_class.get_field_key()

        if not field_key.startswith(MerchantConfigCommon.PREFIX_DYNAMIC_FIELD):
            raise Exception("field: {} cannot be changed".format(field_key))

        merchant_config = MerchantConfig(
            url_connection=self.url_connection
        ).get_merchant_config(merchant_id=merchant_id)
        merchant_fields = merchant_config.get(MerchantConfig.DYNAMIC_FIELDS)
        old_dyn_fields = [
            x
            for x in merchant_fields
            if x.get(BaseField.FIELD_KEY).startswith(
                MerchantConfigCommon.PREFIX_DYNAMIC_FIELD
            )
        ]
        exists_field = next(
            (x for x in old_dyn_fields if x.get(BaseField.FIELD_KEY) == field_key),
            None,
        )
        result_els = True
        if not exists_field:
            result_els = self.put_elastic_mapping(
                els_mapping=field_class.create_elastic_mapping(),
                index=els_index
            )
        else:
            field_class.set_all_data(history=list(exists_field.get("history", [])))
        if not result_els:
            raise Exception("put mapping for key: {} error".format(field_key))

        json_field = self.generate_field(
            field_class=field_class,
            updated_by=updated_by,
        )
        new_dyn_fields = [
            x for x in old_dyn_fields if x.get(BaseField.FIELD_KEY) != field_key
        ]
        new_dyn_fields.append(json_field)
        merchant_config[MerchantConfig.DYNAMIC_FIELDS] = new_dyn_fields
        merchant_config[MerchantConfig.UPDATED_TIME] = datetime.utcnow()
        result_update = MerchantConfig(self.url_connection).update_merchant(
            merchant_config=merchant_config
        )
        if result_update:
            result_logging = self.logging_field_change(
                merchant_id=merchant_id,
                old_fields=old_dyn_fields,
                new_fields=new_dyn_fields,
                staff_id=updated_by.to_json().get(BaseHistory.STAFF_ID),
            )
            print(
                "result_update: {}, result_logging: {}".format(
                    result_update, result_logging
                )
            )
            return True
        return False

    @staticmethod
    def generate_field(field_class, updated_by):
        field_class.set_last_update_by(last_update_by=updated_by)
        dynamic_field_insert = field_class.to_json()
        return dynamic_field_insert

    def logging_field_change(
        self, merchant_id, old_fields: list, new_fields: list, staff_id="mobio"
    ):
        lst_add = []
        lst_change = {}
        lst_remove = []
        lst_keys = set()
        for old_field in old_fields:
            exists_in_new = next(
                (
                    x
                    for x in new_fields
                    if x.get(BaseField.FIELD_KEY) == old_field.get(BaseField.FIELD_KEY)
                ),
                None,
            )
            if not exists_in_new:
                lst_remove.append(old_field)
                lst_keys.add(old_field.get(BaseField.FIELD_KEY))
            else:
                for key, value in old_field.items():
                    if key not in exists_in_new or exists_in_new.get(key) != value:
                        lst_change[exists_in_new.get(BaseField.FIELD_KEY)] = {
                            "old": old_field,
                            "new": exists_in_new,
                        }
                        lst_keys.add(exists_in_new.get(BaseField.FIELD_KEY))
                        break
        for new_field in new_fields:
            exists_in_old = next(
                (
                    x
                    for x in old_fields
                    if x.get(BaseField.FIELD_KEY) == new_field.get(BaseField.FIELD_KEY)
                ),
                None,
            )
            if not exists_in_old:
                lst_add.append(new_field)
                lst_keys.add(new_field.get(BaseField.FIELD_KEY))
            else:
                for key, value in new_field.items():
                    if key not in exists_in_old or value != exists_in_old.get(key):
                        lst_change[exists_in_old.get(BaseField.FIELD_KEY)] = {
                            "old": exists_in_old,
                            "new": new_field,
                        }
                        lst_keys.add(exists_in_old.get(BaseField.FIELD_KEY))
                        break
        return FieldHistoryModel(self.url_connection).logging_change(
            merchant_id=merchant_id,
            staff_id=staff_id,
            lst_add=lst_add,
            lst_remove=lst_remove,
            lst_change=lst_change,
            lst_keys=list(lst_keys),
        )

    # @staticmethod
    # def __validate_create_mapping__(data):
    #     rules = {
    #         "fields": [
    #             Required,
    #             InstanceOf(list),
    #             Each(
    #                 {
    #                     "field_property": [
    #                         Required,
    #                         In(DynamicFieldProperty.get_all_property()),
    #                     ]
    #                 }
    #             ),
    #         ]
    #     }
    #     valid = HttpValidator(rules)
    #     val_result = valid.validate_object(data)
    #     if not val_result[VALIDATION_RESULT.VALID]:
    #         errors = val_result[VALIDATION_RESULT.ERRORS]
    #         raise ParamInvalidError(LANG.VALIDATE_ERROR, errors)

    def put_elastic_mapping(self, els_mapping, index):
        """
        Create elasticsearch mapping json base on field property for dynamic field.
        :param els_mapping: dict dynamic fields
        :param index: elastic search index name
        :return: elastic search mapping string
        """
        try:
            es_model = ElasticSearchBaseModel()
            es = es_model.get_elasticsearch()
            if es.indices.exists(index=index):
                result = es.indices.put_mapping(
                    index=index,
                    body={"properties": els_mapping}
                )
                return result
            else:
                print(
                    "{}::create_elastic_mapping: index {} in elasticsearch not exists".format(
                        self.__class__.__name__, index
                    )
                )
                return None
        except Exception as e:
            print(
                "{}::create_elastic_mapping: exception: %s".format(
                    self.__class__.__name__, e
                )
            )
            raise e

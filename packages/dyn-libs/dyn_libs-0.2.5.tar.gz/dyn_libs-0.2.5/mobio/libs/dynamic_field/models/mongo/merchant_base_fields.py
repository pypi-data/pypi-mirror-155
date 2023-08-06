from datetime import datetime

from mobio.libs.dynamic_field.helpers.field_helper.base_field import (
    BaseField,
    BaseHistory,
)
from mobio.libs.dynamic_field.models.mongo.base_model import BaseModel


class FieldTemplate:
    MOBIO_TEMPLATE = 1


class MerchantBaseFields(BaseModel):
    def __init__(self, url_connection):
        super().__init__(url_connection=url_connection)
        self.collection = "merchant_base_fields"

    FIELDS = "fields"
    TEMPLATE = "template"
    CREATED_TIME = "created_time"
    UPDATED_TIME = "updated_time"

    @staticmethod
    def create_base_fields():
        return []

    def get_fields_by_template(self, template: int):
        result = self.get_db().find_one({"template": template})
        if not result:
            result = {
                self.FIELDS: self.create_base_fields(),
                self.TEMPLATE: template,
                self.CREATED_TIME: datetime.utcnow(),
                self.UPDATED_TIME: datetime.utcnow(),
            }
            inserted_id = self.get_db().insert_one(result)
            print("create template id: {}, inserted: {}".format(template, inserted_id))
        for i in range(len(result.get("fields"))):
            field = result.get("fields")[i]
            if not field.get(BaseField.HISTORY):
                history = BaseHistory()
                history.set_all_data(
                    staff_id="mobio",
                    fullname="MOBIO",
                    username="MOBIO",
                    created_time=datetime.utcnow(),
                )
                if not field.get("history"):
                    field["history"] = []
                field["history"].append(history.to_json())
                result.get("fields")[i] = field
        return result

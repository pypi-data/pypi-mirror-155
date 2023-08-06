import uuid
from datetime import datetime
from mobio.libs.dynamic_field.models.mongo.base_model import BaseModel
from mobio.libs.dynamic_field.models.mongo.merchant_base_fields import (
    MerchantBaseFields,
)


class MerchantConfig(BaseModel):
    CREATED_TIME = "created_time"
    UPDATED_TIME = "updated_time"
    MERCHANT_ID = "merchant_id"
    DYNAMIC_FIELDS = "dynamic_fields"
    PARENTS = "parents"
    TIMEZONE = "timezone"
    VERSION = "version"
    FIELD_TEMPLATE = "field_template"

    def __init__(self, url_connection):
        super().__init__(url_connection=url_connection)
        self.collection = "merchant_config"

    def generate_merchant_config(self, merchant_id):
        merchant_id = self.normalize_uuid(merchant_id)
        data = {
            self.MERCHANT_ID: merchant_id,
            self.CREATED_TIME: datetime.utcnow(),
            self.DYNAMIC_FIELDS: [],
            self.PARENTS: [],
            self.FIELD_TEMPLATE: 1,
            self.TIMEZONE: "Asia/Ho_Chi_Minh",
            self.VERSION: 0.1,
        }
        return data

    def get_merchant_config(self, merchant_id):
        merchant_id = self.normalize_uuid(merchant_id)
        result = self.get_db().find_one({self.MERCHANT_ID: merchant_id})
        if result is None:
            data = self.generate_merchant_config(merchant_id)
            result_insert = self.get_db().insert_one(data)
            result = data
            result["_id"] = result_insert.inserted_id
        base_fields = MerchantBaseFields(
            url_connection=self.url_connection
        ).get_fields_by_template(result.get(self.FIELD_TEMPLATE) or 1)
        merchant_fields = result.get(self.DYNAMIC_FIELDS) or []
        merchant_fields.extend(base_fields.get(MerchantBaseFields.FIELDS))
        result[self.DYNAMIC_FIELDS] = merchant_fields
        return result

    def update_merchant(self, merchant_config):
        if "_id" in merchant_config:
            result_update = self.get_db().update_one(
                {"_id": merchant_config.get("_id")},
                {
                    "$set": {
                        i: merchant_config[i] for i in merchant_config if i != "_id"
                    }
                },
                upsert=True,
            )
        else:
            result_update = self.get_db().update_one(
                {"merchant_id": merchant_config.get("merchant_id")},
                {
                    "$set": {
                        i: merchant_config[i] for i in merchant_config if i != "_id"
                    }
                },
                upsert=True,
            )
        return result_update.matched_count

    def check_merchant_exists(self, merchant_id):
        merchant_id = (
            uuid.UUID(merchant_id) if type(merchant_id) == str else merchant_id
        )
        result = self.get_db().find_one({"merchant_id": merchant_id})
        return result

from mobio.libs.dynamic_field.models.mongo.base_model import BaseModel


class FieldHistoryModel(BaseModel):
    MERCHANT_ID = "merchant_id"
    STAFF_ID = "staff_id"
    FIELD_LOGGING = "field_logging"
    LST_KEYS = "lst_keys"

    def __init__(self, url_connection):
        super().__init__(url_connection=url_connection)
        self.collection = "field_history"

    def logging_change(
        self, merchant_id, staff_id, lst_add, lst_remove, lst_change, lst_keys
    ):
        return (
            self.get_db()
            .insert_one(
                {
                    self.MERCHANT_ID: self.normalize_uuid(merchant_id),
                    self.STAFF_ID: staff_id,
                    self.FIELD_LOGGING: {
                        "add": lst_add,
                        "change": lst_change,
                        "remove": lst_remove,
                    },
                    self.LST_KEYS: lst_keys,
                }
            )
            .inserted_id
        )

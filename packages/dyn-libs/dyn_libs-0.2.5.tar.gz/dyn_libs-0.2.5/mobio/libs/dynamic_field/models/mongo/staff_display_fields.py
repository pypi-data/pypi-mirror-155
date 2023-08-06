from datetime import datetime
from mobio.libs.dynamic_field.models.mongo.base_model import BaseModel


class StaffDisplayFields(BaseModel):
    def __init__(self, url_connection):
        super().__init__(url_connection=url_connection)
        self.collection = 'staff_display_fields'

    def get_fields_by_staff(self, staff_id: str):
        result = self.get_db().find_one({"staff_id": staff_id})
        if not result:
            result = {
                "input": [],
                "dashboard": [],
                "staff_id": staff_id,
                "created_time": datetime.utcnow(),
                "updated_time": datetime.utcnow()
            }
            inserted_id = self.get_db().insert_one(result)
            result["_id"] = inserted_id
        return result

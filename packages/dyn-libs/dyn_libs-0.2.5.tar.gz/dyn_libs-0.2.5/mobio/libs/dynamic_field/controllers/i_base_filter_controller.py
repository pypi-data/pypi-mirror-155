import configparser
import json
import math
from datetime import datetime
from mobio.libs.dynamic_field.common import (
    Elastic,
    OPERATOR_KEY,
    AUDIENCE_STRUCTURE,
    COMMON,
)
from mobio.libs.dynamic_field.common.es_paginate import ESPaginate
from mobio.libs.dynamic_field.common.utils import GMT_7
from mobio.libs.dynamic_field.helpers import MerchantConfigCommon
from mobio.libs.dynamic_field.helpers.field_helper.base_field import BaseField
from mobio.libs.dynamic_field.models.elastic.base_model import ElasticSearchBaseModel
from mobio.libs.dynamic_field.models.mongo.merchant_config import MerchantConfig


class IBaseFilterController:
    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_name, "utf-8")
        if self.config.has_section(Elastic.__name__):
            if self.config.get(Elastic.__name__, Elastic.INDEX):
                self.index = self.config.get(Elastic.__name__, Elastic.INDEX)
            if self.config.get(Elastic.__name__, Elastic.DOC_TYPE):
                self.doc_type = self.config.get(Elastic.__name__, Elastic.DOC_TYPE)

    def add_els_config(self, index, doc_type):
        self.index = index
        self.doc_type = doc_type

    def __building_query__(self, merchant_id, es_filter, merchant_config):

        """
        :param merchant_id:
        :param es_filter:
        :param merchant_config:
        :return:

        Xử lý merge các field của mkt_user_event thành 1 để query.
        """
        must = [{"terms": {"merchant_id": merchant_id}}]

        m, must_not, should = self.build_query_from_es_filter(
            es_filter, merchant_config
        )
        must.extend(m)
        return must, must_not, should

    def mapping_operator(self, operator_key):
        operator = ""
        if operator_key == OPERATOR_KEY.OP_IS_GREATER:
            operator = "gt"
        if operator_key == OPERATOR_KEY.OP_IS_GREATER_EQUAL:
            operator = "gte"
        if operator_key == OPERATOR_KEY.OP_IS_LESS:
            operator = "lt"
        if operator_key == OPERATOR_KEY.OP_IS_LESS_EQUAL:
            operator = "lte"
        return operator

    def processing_nested_object(self, obj_field, must, must_not, operator_key, values):
        path = obj_field.get("path")
        field_map = obj_field.get("field")
        obj_nested = {"path": path}
        field = path + "." + field_map

        if operator_key == OPERATOR_KEY.OP_IS_EQUAL:
            obj_nested["query"] = {"match": {field: values[0]}}

        elif (
            operator_key == OPERATOR_KEY.OP_IS_BETWEEN
            or operator_key == OPERATOR_KEY.OP_IS_GREATER
            or operator_key == OPERATOR_KEY.OP_IS_GREATER_EQUAL
            or operator_key == OPERATOR_KEY.OP_IS_LESS
            or operator_key == OPERATOR_KEY.OP_IS_LESS_EQUAL
        ):
            obj_operator = {}

            if operator_key == OPERATOR_KEY.OP_IS_BETWEEN:
                obj_operator["gte"] = values[0]
                obj_operator["lte"] = values[1]
            else:
                operator = self.mapping_operator(operator_key)
                obj_operator[operator] = values[0]
            obj_nested["query"] = {"range": {field: obj_operator}}
        elif operator_key in [OPERATOR_KEY.OP_IS_IN, OPERATOR_KEY.OP_IS_NOT_IN]:
            obj_nested["query"] = {"terms": {field: values}}
        elif operator_key in [OPERATOR_KEY.OP_IS_HAS, OPERATOR_KEY.OP_IS_HAS_NOT]:
            obj_nested["query"] = {"wildcard": {field: "*" + values[0] + "*"}}
        elif operator_key in [OPERATOR_KEY.OP_IS_EMPTY, OPERATOR_KEY.OP_IS_NOT_EMPTY]:
            obj_nested["query"] = {"bool": {"filter": {"exists": {"field": path}}}}
        if operator_key in [
            OPERATOR_KEY.OP_IS_HAS_NOT,
            OPERATOR_KEY.OP_IS_EMPTY,
            OPERATOR_KEY.OP_IS_NOT_IN,
        ]:
            must_not.append({"nested": obj_nested})
        else:
            must.append({"nested": obj_nested})

    def build_query_from_es_filter(self, es_filter, merchant_config):
        must = []
        must_not = []
        should = []

        lst_field_map = self.config.get("criteria_mapping", "criteria_mapping")
        json_field_map = {}
        try:
            if lst_field_map:
                json_field_map = json.loads(lst_field_map)
                if merchant_config:
                    for df in merchant_config.get(MerchantConfig.DYNAMIC_FIELDS):
                        if df.get(BaseField.FIELD_KEY).startswith(
                            MerchantConfigCommon.PREFIX_DYNAMIC_FIELD
                        ):
                            df_cri_key = MerchantConfigCommon.PREFIX_CRITERIA + df.get(
                                BaseField.FIELD_KEY
                            )
                            json_field_map[df_cri_key] = {
                                "field": df.get(BaseField.FIELD_KEY)
                            }
        except Exception as e:
            print("FilterController::building_query()- exception: %r", e)

        for audience in es_filter:
            if (
                AUDIENCE_STRUCTURE.CRITERIA_KEY in audience
                and AUDIENCE_STRUCTURE.OPERATOR_KEY in audience
                and AUDIENCE_STRUCTURE.VALUES in audience
            ):
                criteria_key = audience.get("criteria_key")
                operator_key = audience.get("operator_key")
                values = audience.get("values")

                obj_field = json_field_map.get(criteria_key)

                if obj_field:
                    field = obj_field.get("field")

                    if "path" in obj_field:
                        self.processing_nested_object(
                            obj_field=obj_field,
                            must=must,
                            must_not=must_not,
                            operator_key=operator_key,
                            values=values,
                        )
                    elif operator_key == OPERATOR_KEY.OP_IS_EQUAL:
                        must.append({"match": {field: values[0]}})
                    elif operator_key == OPERATOR_KEY.OP_IS_NOT_EQUAL:
                        must_not.append({"match": {field: values[0]}})
                    elif operator_key == OPERATOR_KEY.OP_IS_HAS:
                        should.append({"wildcard": {field: "*" + values[0] + "*"}})
                    elif operator_key == OPERATOR_KEY.OP_IS_HAS_NOT:
                        must_not.append({"wildcard": {field: "*" + values[0] + "*"}})
                    elif operator_key == OPERATOR_KEY.OP_IS_REGEX:
                        if len(values) == 1:
                            must.append({"regexp": {field: values[0]}})
                        elif len(values) > 1:
                            sh = [{"regexp": {field: x}} for x in values]
                            should.extend(sh)

                    elif (
                        operator_key == OPERATOR_KEY.OP_IS_BETWEEN
                        or operator_key == OPERATOR_KEY.OP_IS_GREATER
                        or operator_key == OPERATOR_KEY.OP_IS_GREATER_EQUAL
                        or operator_key == OPERATOR_KEY.OP_IS_LESS
                        or operator_key == OPERATOR_KEY.OP_IS_LESS_EQUAL
                    ):
                        obj_operator = {}
                        if (
                            operator_key == OPERATOR_KEY.OP_IS_BETWEEN
                            and values is not None
                            and len(values) == 2
                        ):
                            obj_operator = {
                                "gte": str(values[0]),
                                "lte": str(values[1]),
                            }
                        else:
                            if values is not None and len(values) == 1:
                                # operator = self.mapping_operator(values)
                                # obj_operator[operator] = str(values[0])
                                operator = self.mapping_operator(operator_key)
                                obj_operator[operator] = str(values[0])
                        if len(obj_operator) > 0:
                            must.append({"range": {field: obj_operator}})

                        must.append({"range": {field: obj_operator}})

                    elif operator_key == OPERATOR_KEY.OP_IS_IN:
                        must.append({"terms": {field: values}})
                    elif operator_key == OPERATOR_KEY.OP_IS_NOT_IN:
                        must_not.append({"terms": {field: values}})
                    elif operator_key == OPERATOR_KEY.OP_IS_EMPTY:
                        must_not.append({"exists": {"field": field}})
                    elif operator_key == OPERATOR_KEY.OP_IS_NOT_EMPTY:
                        must.append({"exists": {"field": field}})
            else:
                raise Exception("input not found")
        return must, must_not, should

    def es_filter(self, merchant_config, request_data, request_args):
        merchant_id = [merchant_config.get("merchant_id")]

        es_filter = []

        must, must_not, should = self.__building_query__(
            merchant_id, es_filter, merchant_config
        )

        fields = request_data.get("fields") or [
            x.get(BaseField.FIELD_KEY)
            for x in merchant_config.get(MerchantConfig.DYNAMIC_FIELDS)
        ]
        after_token = request_args.get("after_token")
        sort_field = ""
        order = "desc"
        page = 1
        per_page = 10
        if "page" in request_args:
            page = int(request_args["page"])
        if "per_page" in request_args:
            per_page = int(request_args["per_page"])
        if "sort" in request_args and request_args.get("sort"):
            sort_field = request_args.get("sort")
        # lst_obj_sort = []
        lst_sort_field = []
        if sort_field:
            arr_sort_field = sort_field.split(",")
            for sort in arr_sort_field:
                lst_sort_field.append(sort)

        if "updated_time" not in lst_sort_field and len(lst_sort_field) == 0:
            lst_sort_field.append("updated_time")

        if "order" in request_args and request_args.get("order"):
            order = request_args.get("order")

        if "from" in request_args and "to" in request_args:
            from_time = self.__get_time_from_args("from", request_args)
            to_time = self.__get_time_from_args("to", request_args)

            must.append(
                {
                    "range": {
                        "updated_time": {
                            "gte": from_time.strftime(COMMON.DATE_TIME_FORMAT),
                            "lte": to_time.strftime(COMMON.DATE_TIME_FORMAT),
                        }
                    }
                }
            )

        must.append({"bool": {"should": should}})

        must.append({"bool": {"should": should}})
        query = {"bool": {"must": must, "must_not": must_not}}
        es_data = self.get_data_in_es(
            query, ",".join(lst_sort_field), after_token, fields, order, per_page
        )
        result = es_data[0]
        return {
            "data": result,
            "paging": {
                "cursors": {"after": es_data[1], "before": ""},
                "total_count": es_data[2],
                "page": page,
                "per_page": per_page,
                "page_count": math.ceil(es_data[2] / per_page),
            },
        }

    def __get_time_from_args(self, key, args):
        time = None
        if key in args:
            try:
                # convert to local time (GMT+7)
                time = datetime.fromtimestamp(float(args[key]), GMT_7)
            except Exception as ex:
                print(
                    "UserController::__get_time_from_agrs():time(%s): %s"
                    % (args[key], ex)
                )
        if not time:
            time = datetime.now(GMT_7)
        return time

    def __check_sort_field(self, item_field, order):
        obj = {item_field: {"order": order}}
        return obj

    def get_data_in_es(self, query, sort, after_token, fields, order, per_page):
        try:
            per_page = int(per_page)
        except Exception as ex:
            print("get_data_in_es()- ERROR: {}".format(ex))
            per_page = 10

        es = ElasticSearchBaseModel().get_elasticsearch()

        results = []
        last_item = ""

        lst_sort_field = []
        if sort:
            lst_sort_field = sort.split(",")

        lst_obj_sort = []
        for item_field in lst_sort_field:
            if item_field:
                lst_obj_sort.append(self.__check_sort_field(item_field, order))

        fields = list(set(fields))
        body = {
            "query": query,
            "_source": fields,
            "sort": lst_obj_sort,
            "size": per_page,
        }
        if after_token:
            body["search_after"] = ESPaginate.parse_token(after_token)

        page = es.search(
            index=self.index,
            doc_type=self.doc_type,
            body=body,
        )

        scroll_size = page["hits"]["total"]

        data = page["hits"]["hits"]

        for item in data:
            source = item["_source"]
            results.append(source)
            last_item = item

        if last_item and len(results) == per_page:
            after_token = ESPaginate.generate_after_token(last_item)
        else:
            after_token = ""
        return results, after_token, scroll_size

# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import Dict, List


class CancelTaskRequest(TeaModel):
    def __init__(
        self,
        task_uid: str = None,
    ):
        self.task_uid = task_uid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_uid is not None:
            result['TaskUid'] = self.task_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskUid') is not None:
            self.task_uid = m.get('TaskUid')
        return self


class CancelTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CancelTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CancelTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CancelTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateTaskRequest(TeaModel):
    def __init__(
        self,
        level: int = None,
        mq_config_name: str = None,
        oss_bucket_name: str = None,
        oss_config_name: str = None,
        oss_endpoint: str = None,
        oss_input_path: str = None,
        oss_output_path: str = None,
        priority: int = None,
        task_description: str = None,
        task_name: str = None,
    ):
        self.level = level
        self.mq_config_name = mq_config_name
        self.oss_bucket_name = oss_bucket_name
        self.oss_config_name = oss_config_name
        self.oss_endpoint = oss_endpoint
        self.oss_input_path = oss_input_path
        self.oss_output_path = oss_output_path
        self.priority = priority
        self.task_description = task_description
        self.task_name = task_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.level is not None:
            result['Level'] = self.level
        if self.mq_config_name is not None:
            result['MqConfigName'] = self.mq_config_name
        if self.oss_bucket_name is not None:
            result['OssBucketName'] = self.oss_bucket_name
        if self.oss_config_name is not None:
            result['OssConfigName'] = self.oss_config_name
        if self.oss_endpoint is not None:
            result['OssEndpoint'] = self.oss_endpoint
        if self.oss_input_path is not None:
            result['OssInputPath'] = self.oss_input_path
        if self.oss_output_path is not None:
            result['OssOutputPath'] = self.oss_output_path
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.task_description is not None:
            result['TaskDescription'] = self.task_description
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('MqConfigName') is not None:
            self.mq_config_name = m.get('MqConfigName')
        if m.get('OssBucketName') is not None:
            self.oss_bucket_name = m.get('OssBucketName')
        if m.get('OssConfigName') is not None:
            self.oss_config_name = m.get('OssConfigName')
        if m.get('OssEndpoint') is not None:
            self.oss_endpoint = m.get('OssEndpoint')
        if m.get('OssInputPath') is not None:
            self.oss_input_path = m.get('OssInputPath')
        if m.get('OssOutputPath') is not None:
            self.oss_output_path = m.get('OssOutputPath')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('TaskDescription') is not None:
            self.task_description = m.get('TaskDescription')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        return self


class CreateTaskResponseBodyResponse(TeaModel):
    def __init__(
        self,
        task_uid: str = None,
    ):
        self.task_uid = task_uid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_uid is not None:
            result['TaskUid'] = self.task_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskUid') is not None:
            self.task_uid = m.get('TaskUid')
        return self


class CreateTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        response: CreateTaskResponseBodyResponse = None,
        success: str = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.response = response
        self.success = success

    def validate(self):
        if self.response:
            self.response.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.response is not None:
            result['Response'] = self.response.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Response') is not None:
            temp_model = CreateTaskResponseBodyResponse()
            self.response = temp_model.from_map(m['Response'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateTaskResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CreateTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteMqConfigRequest(TeaModel):
    def __init__(
        self,
        config_name: str = None,
    ):
        self.config_name = config_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_name is not None:
            result['ConfigName'] = self.config_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigName') is not None:
            self.config_name = m.get('ConfigName')
        return self


class DeleteMqConfigResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        success: str = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteMqConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteMqConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteMqConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteOssConfigRequest(TeaModel):
    def __init__(
        self,
        config_name: str = None,
    ):
        self.config_name = config_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_name is not None:
            result['ConfigName'] = self.config_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigName') is not None:
            self.config_name = m.get('ConfigName')
        return self


class DeleteOssConfigResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteOssConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DeleteOssConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DeleteOssConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectImageRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        return self


class DetectImageResponseBodyResponseDataInfo(TeaModel):
    def __init__(
        self,
        category: str = None,
        conf: float = None,
        direction: str = None,
        well: str = None,
    ):
        self.category = category
        self.conf = conf
        self.direction = direction
        self.well = well

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.category is not None:
            result['Category'] = self.category
        if self.conf is not None:
            result['Conf'] = self.conf
        if self.direction is not None:
            result['Direction'] = self.direction
        if self.well is not None:
            result['Well'] = self.well
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('Conf') is not None:
            self.conf = m.get('Conf')
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')
        if m.get('Well') is not None:
            self.well = m.get('Well')
        return self


class DetectImageResponseBodyResponseDataResults(TeaModel):
    def __init__(
        self,
        category_list: List[str] = None,
        conf_list: List[float] = None,
        direction: str = None,
        rect: List[float] = None,
        task_type: str = None,
    ):
        self.category_list = category_list
        self.conf_list = conf_list
        self.direction = direction
        self.rect = rect
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.category_list is not None:
            result['CategoryList'] = self.category_list
        if self.conf_list is not None:
            result['ConfList'] = self.conf_list
        if self.direction is not None:
            result['Direction'] = self.direction
        if self.rect is not None:
            result['Rect'] = self.rect
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CategoryList') is not None:
            self.category_list = m.get('CategoryList')
        if m.get('ConfList') is not None:
            self.conf_list = m.get('ConfList')
        if m.get('Direction') is not None:
            self.direction = m.get('Direction')
        if m.get('Rect') is not None:
            self.rect = m.get('Rect')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        return self


class DetectImageResponseBodyResponseData(TeaModel):
    def __init__(
        self,
        info: DetectImageResponseBodyResponseDataInfo = None,
        results: List[DetectImageResponseBodyResponseDataResults] = None,
    ):
        self.info = info
        self.results = results

    def validate(self):
        if self.info:
            self.info.validate()
        if self.results:
            for k in self.results:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.info is not None:
            result['Info'] = self.info.to_map()
        result['Results'] = []
        if self.results is not None:
            for k in self.results:
                result['Results'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Info') is not None:
            temp_model = DetectImageResponseBodyResponseDataInfo()
            self.info = temp_model.from_map(m['Info'])
        self.results = []
        if m.get('Results') is not None:
            for k in m.get('Results'):
                temp_model = DetectImageResponseBodyResponseDataResults()
                self.results.append(temp_model.from_map(k))
        return self


class DetectImageResponseBodyResponse(TeaModel):
    def __init__(
        self,
        data: DetectImageResponseBodyResponseData = None,
        error_code: int = None,
        error_message: str = None,
        flag: bool = None,
    ):
        self.data = data
        self.error_code = error_code
        self.error_message = error_message
        self.flag = flag

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.error_code is not None:
            result['ErrorCode'] = self.error_code
        if self.error_message is not None:
            result['ErrorMessage'] = self.error_message
        if self.flag is not None:
            result['Flag'] = self.flag
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DetectImageResponseBodyResponseData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('ErrorCode') is not None:
            self.error_code = m.get('ErrorCode')
        if m.get('ErrorMessage') is not None:
            self.error_message = m.get('ErrorMessage')
        if m.get('Flag') is not None:
            self.flag = m.get('Flag')
        return self


class DetectImageResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        response: DetectImageResponseBodyResponse = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.response = response
        self.success = success

    def validate(self):
        if self.response:
            self.response.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.response is not None:
            result['Response'] = self.response.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Response') is not None:
            temp_model = DetectImageResponseBodyResponse()
            self.response = temp_model.from_map(m['Response'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DetectImageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DetectImageResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DetectImageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetMqConfigListRequest(TeaModel):
    def __init__(
        self,
        page_index: int = None,
        page_size: int = None,
    ):
        self.page_index = page_index
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_index is not None:
            result['PageIndex'] = self.page_index
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageIndex') is not None:
            self.page_index = m.get('PageIndex')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class GetMqConfigListResponseBodyResponseList(TeaModel):
    def __init__(
        self,
        config_name: str = None,
        gmt_create: str = None,
        mq_access_key: str = None,
        mq_endpoint: str = None,
        mq_group_id: str = None,
        mq_topic: str = None,
    ):
        self.config_name = config_name
        self.gmt_create = gmt_create
        self.mq_access_key = mq_access_key
        self.mq_endpoint = mq_endpoint
        self.mq_group_id = mq_group_id
        self.mq_topic = mq_topic

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_name is not None:
            result['ConfigName'] = self.config_name
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.mq_access_key is not None:
            result['MqAccessKey'] = self.mq_access_key
        if self.mq_endpoint is not None:
            result['MqEndpoint'] = self.mq_endpoint
        if self.mq_group_id is not None:
            result['MqGroupId'] = self.mq_group_id
        if self.mq_topic is not None:
            result['MqTopic'] = self.mq_topic
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigName') is not None:
            self.config_name = m.get('ConfigName')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('MqAccessKey') is not None:
            self.mq_access_key = m.get('MqAccessKey')
        if m.get('MqEndpoint') is not None:
            self.mq_endpoint = m.get('MqEndpoint')
        if m.get('MqGroupId') is not None:
            self.mq_group_id = m.get('MqGroupId')
        if m.get('MqTopic') is not None:
            self.mq_topic = m.get('MqTopic')
        return self


class GetMqConfigListResponseBodyResponse(TeaModel):
    def __init__(
        self,
        list: List[GetMqConfigListResponseBodyResponseList] = None,
        page_index: int = None,
        page_size: int = None,
        total: int = None,
    ):
        self.list = list
        self.page_index = page_index
        self.page_size = page_size
        self.total = total

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        if self.page_index is not None:
            result['PageIndex'] = self.page_index
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = GetMqConfigListResponseBodyResponseList()
                self.list.append(temp_model.from_map(k))
        if m.get('PageIndex') is not None:
            self.page_index = m.get('PageIndex')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class GetMqConfigListResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        response: GetMqConfigListResponseBodyResponse = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.response = response
        self.success = success

    def validate(self):
        if self.response:
            self.response.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.response is not None:
            result['Response'] = self.response.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Response') is not None:
            temp_model = GetMqConfigListResponseBodyResponse()
            self.response = temp_model.from_map(m['Response'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetMqConfigListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetMqConfigListResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetMqConfigListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetOssConfigListRequest(TeaModel):
    def __init__(
        self,
        config_name: str = None,
        page_index: int = None,
        page_size: int = None,
    ):
        self.config_name = config_name
        self.page_index = page_index
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_name is not None:
            result['ConfigName'] = self.config_name
        if self.page_index is not None:
            result['PageIndex'] = self.page_index
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigName') is not None:
            self.config_name = m.get('ConfigName')
        if m.get('PageIndex') is not None:
            self.page_index = m.get('PageIndex')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class GetOssConfigListResponseBodyResponseList(TeaModel):
    def __init__(
        self,
        access_key_id: str = None,
        config_name: str = None,
        gmt_create: str = None,
        oss_bucket_name: str = None,
        oss_endpoint: str = None,
        uid: str = None,
    ):
        self.access_key_id = access_key_id
        self.config_name = config_name
        self.gmt_create = gmt_create
        self.oss_bucket_name = oss_bucket_name
        self.oss_endpoint = oss_endpoint
        self.uid = uid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.access_key_id is not None:
            result['AccessKeyId'] = self.access_key_id
        if self.config_name is not None:
            result['ConfigName'] = self.config_name
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.oss_bucket_name is not None:
            result['OssBucketName'] = self.oss_bucket_name
        if self.oss_endpoint is not None:
            result['OssEndpoint'] = self.oss_endpoint
        if self.uid is not None:
            result['Uid'] = self.uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccessKeyId') is not None:
            self.access_key_id = m.get('AccessKeyId')
        if m.get('ConfigName') is not None:
            self.config_name = m.get('ConfigName')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('OssBucketName') is not None:
            self.oss_bucket_name = m.get('OssBucketName')
        if m.get('OssEndpoint') is not None:
            self.oss_endpoint = m.get('OssEndpoint')
        if m.get('Uid') is not None:
            self.uid = m.get('Uid')
        return self


class GetOssConfigListResponseBodyResponse(TeaModel):
    def __init__(
        self,
        list: List[GetOssConfigListResponseBodyResponseList] = None,
        page_index: int = None,
        page_size: int = None,
        total: int = None,
    ):
        self.list = list
        self.page_index = page_index
        self.page_size = page_size
        self.total = total

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        if self.page_index is not None:
            result['PageIndex'] = self.page_index
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = GetOssConfigListResponseBodyResponseList()
                self.list.append(temp_model.from_map(k))
        if m.get('PageIndex') is not None:
            self.page_index = m.get('PageIndex')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class GetOssConfigListResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        response: GetOssConfigListResponseBodyResponse = None,
        success: str = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.response = response
        self.success = success

    def validate(self):
        if self.response:
            self.response.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.response is not None:
            result['Response'] = self.response.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Response') is not None:
            temp_model = GetOssConfigListResponseBodyResponse()
            self.response = temp_model.from_map(m['Response'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetOssConfigListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetOssConfigListResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetOssConfigListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTaskDetailRequest(TeaModel):
    def __init__(
        self,
        task_uid: str = None,
    ):
        self.task_uid = task_uid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_uid is not None:
            result['TaskUid'] = self.task_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskUid') is not None:
            self.task_uid = m.get('TaskUid')
        return self


class GetTaskDetailResponseBodyResponseDeduplicateProcessInfos(TeaModel):
    def __init__(
        self,
        flag: bool = None,
        json_num: int = None,
        result_num: int = None,
        video_name: str = None,
    ):
        self.flag = flag
        self.json_num = json_num
        self.result_num = result_num
        self.video_name = video_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.flag is not None:
            result['Flag'] = self.flag
        if self.json_num is not None:
            result['JsonNum'] = self.json_num
        if self.result_num is not None:
            result['ResultNum'] = self.result_num
        if self.video_name is not None:
            result['VideoName'] = self.video_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Flag') is not None:
            self.flag = m.get('Flag')
        if m.get('JsonNum') is not None:
            self.json_num = m.get('JsonNum')
        if m.get('ResultNum') is not None:
            self.result_num = m.get('ResultNum')
        if m.get('VideoName') is not None:
            self.video_name = m.get('VideoName')
        return self


class GetTaskDetailResponseBodyResponse(TeaModel):
    def __init__(
        self,
        deduplicate_process_infos: List[GetTaskDetailResponseBodyResponseDeduplicateProcessInfos] = None,
        deduplicate_result_oss_path: str = None,
        error_code: int = None,
        exception_message: str = None,
        gmt_create: str = None,
        gmt_modified: str = None,
        image_completed_total: int = None,
        image_total: int = None,
        level: int = None,
        mid_result_oss_path: str = None,
        mq_access_key: str = None,
        mq_config_name: str = None,
        mq_endpoint: str = None,
        mq_group_id: str = None,
        mq_topic: str = None,
        oss_access_key_id: str = None,
        oss_bucket_name: str = None,
        oss_config_name: str = None,
        oss_endpoint: str = None,
        oss_input_path: str = None,
        oss_output_path: str = None,
        priority: int = None,
        task_description: str = None,
        task_name: str = None,
        task_status: str = None,
        task_uid: str = None,
    ):
        self.deduplicate_process_infos = deduplicate_process_infos
        self.deduplicate_result_oss_path = deduplicate_result_oss_path
        self.error_code = error_code
        self.exception_message = exception_message
        self.gmt_create = gmt_create
        self.gmt_modified = gmt_modified
        self.image_completed_total = image_completed_total
        self.image_total = image_total
        self.level = level
        self.mid_result_oss_path = mid_result_oss_path
        self.mq_access_key = mq_access_key
        self.mq_config_name = mq_config_name
        self.mq_endpoint = mq_endpoint
        self.mq_group_id = mq_group_id
        self.mq_topic = mq_topic
        self.oss_access_key_id = oss_access_key_id
        self.oss_bucket_name = oss_bucket_name
        self.oss_config_name = oss_config_name
        self.oss_endpoint = oss_endpoint
        self.oss_input_path = oss_input_path
        self.oss_output_path = oss_output_path
        self.priority = priority
        self.task_description = task_description
        self.task_name = task_name
        self.task_status = task_status
        self.task_uid = task_uid

    def validate(self):
        if self.deduplicate_process_infos:
            for k in self.deduplicate_process_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DeduplicateProcessInfos'] = []
        if self.deduplicate_process_infos is not None:
            for k in self.deduplicate_process_infos:
                result['DeduplicateProcessInfos'].append(k.to_map() if k else None)
        if self.deduplicate_result_oss_path is not None:
            result['DeduplicateResultOssPath'] = self.deduplicate_result_oss_path
        if self.error_code is not None:
            result['ErrorCode'] = self.error_code
        if self.exception_message is not None:
            result['ExceptionMessage'] = self.exception_message
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.gmt_modified is not None:
            result['GmtModified'] = self.gmt_modified
        if self.image_completed_total is not None:
            result['ImageCompletedTotal'] = self.image_completed_total
        if self.image_total is not None:
            result['ImageTotal'] = self.image_total
        if self.level is not None:
            result['Level'] = self.level
        if self.mid_result_oss_path is not None:
            result['MidResultOssPath'] = self.mid_result_oss_path
        if self.mq_access_key is not None:
            result['MqAccessKey'] = self.mq_access_key
        if self.mq_config_name is not None:
            result['MqConfigName'] = self.mq_config_name
        if self.mq_endpoint is not None:
            result['MqEndpoint'] = self.mq_endpoint
        if self.mq_group_id is not None:
            result['MqGroupId'] = self.mq_group_id
        if self.mq_topic is not None:
            result['MqTopic'] = self.mq_topic
        if self.oss_access_key_id is not None:
            result['OssAccessKeyId'] = self.oss_access_key_id
        if self.oss_bucket_name is not None:
            result['OssBucketName'] = self.oss_bucket_name
        if self.oss_config_name is not None:
            result['OssConfigName'] = self.oss_config_name
        if self.oss_endpoint is not None:
            result['OssEndpoint'] = self.oss_endpoint
        if self.oss_input_path is not None:
            result['OssInputPath'] = self.oss_input_path
        if self.oss_output_path is not None:
            result['OssOutputPath'] = self.oss_output_path
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.task_description is not None:
            result['TaskDescription'] = self.task_description
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_status is not None:
            result['TaskStatus'] = self.task_status
        if self.task_uid is not None:
            result['TaskUid'] = self.task_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.deduplicate_process_infos = []
        if m.get('DeduplicateProcessInfos') is not None:
            for k in m.get('DeduplicateProcessInfos'):
                temp_model = GetTaskDetailResponseBodyResponseDeduplicateProcessInfos()
                self.deduplicate_process_infos.append(temp_model.from_map(k))
        if m.get('DeduplicateResultOssPath') is not None:
            self.deduplicate_result_oss_path = m.get('DeduplicateResultOssPath')
        if m.get('ErrorCode') is not None:
            self.error_code = m.get('ErrorCode')
        if m.get('ExceptionMessage') is not None:
            self.exception_message = m.get('ExceptionMessage')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('GmtModified') is not None:
            self.gmt_modified = m.get('GmtModified')
        if m.get('ImageCompletedTotal') is not None:
            self.image_completed_total = m.get('ImageCompletedTotal')
        if m.get('ImageTotal') is not None:
            self.image_total = m.get('ImageTotal')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('MidResultOssPath') is not None:
            self.mid_result_oss_path = m.get('MidResultOssPath')
        if m.get('MqAccessKey') is not None:
            self.mq_access_key = m.get('MqAccessKey')
        if m.get('MqConfigName') is not None:
            self.mq_config_name = m.get('MqConfigName')
        if m.get('MqEndpoint') is not None:
            self.mq_endpoint = m.get('MqEndpoint')
        if m.get('MqGroupId') is not None:
            self.mq_group_id = m.get('MqGroupId')
        if m.get('MqTopic') is not None:
            self.mq_topic = m.get('MqTopic')
        if m.get('OssAccessKeyId') is not None:
            self.oss_access_key_id = m.get('OssAccessKeyId')
        if m.get('OssBucketName') is not None:
            self.oss_bucket_name = m.get('OssBucketName')
        if m.get('OssConfigName') is not None:
            self.oss_config_name = m.get('OssConfigName')
        if m.get('OssEndpoint') is not None:
            self.oss_endpoint = m.get('OssEndpoint')
        if m.get('OssInputPath') is not None:
            self.oss_input_path = m.get('OssInputPath')
        if m.get('OssOutputPath') is not None:
            self.oss_output_path = m.get('OssOutputPath')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('TaskDescription') is not None:
            self.task_description = m.get('TaskDescription')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskStatus') is not None:
            self.task_status = m.get('TaskStatus')
        if m.get('TaskUid') is not None:
            self.task_uid = m.get('TaskUid')
        return self


class GetTaskDetailResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        response: GetTaskDetailResponseBodyResponse = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.response = response
        self.success = success

    def validate(self):
        if self.response:
            self.response.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.response is not None:
            result['Response'] = self.response.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Response') is not None:
            temp_model = GetTaskDetailResponseBodyResponse()
            self.response = temp_model.from_map(m['Response'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetTaskDetailResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTaskDetailResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetTaskDetailResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTaskListRequest(TeaModel):
    def __init__(
        self,
        page_index: int = None,
        page_size: int = None,
        task_status: str = None,
    ):
        self.page_index = page_index
        self.page_size = page_size
        self.task_status = task_status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_index is not None:
            result['PageIndex'] = self.page_index
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.task_status is not None:
            result['TaskStatus'] = self.task_status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageIndex') is not None:
            self.page_index = m.get('PageIndex')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TaskStatus') is not None:
            self.task_status = m.get('TaskStatus')
        return self


class GetTaskListResponseBodyResponseTaskList(TeaModel):
    def __init__(
        self,
        gmt_create: str = None,
        gmt_modified: str = None,
        level: int = None,
        priority: str = None,
        task_description: str = None,
        task_name: str = None,
        task_status: str = None,
        task_uid: str = None,
    ):
        self.gmt_create = gmt_create
        self.gmt_modified = gmt_modified
        self.level = level
        self.priority = priority
        self.task_description = task_description
        self.task_name = task_name
        self.task_status = task_status
        self.task_uid = task_uid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.gmt_modified is not None:
            result['GmtModified'] = self.gmt_modified
        if self.level is not None:
            result['Level'] = self.level
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.task_description is not None:
            result['TaskDescription'] = self.task_description
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_status is not None:
            result['TaskStatus'] = self.task_status
        if self.task_uid is not None:
            result['TaskUid'] = self.task_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('GmtModified') is not None:
            self.gmt_modified = m.get('GmtModified')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('TaskDescription') is not None:
            self.task_description = m.get('TaskDescription')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskStatus') is not None:
            self.task_status = m.get('TaskStatus')
        if m.get('TaskUid') is not None:
            self.task_uid = m.get('TaskUid')
        return self


class GetTaskListResponseBodyResponse(TeaModel):
    def __init__(
        self,
        page_index: int = None,
        page_size: int = None,
        task_list: List[GetTaskListResponseBodyResponseTaskList] = None,
        total: int = None,
    ):
        self.page_index = page_index
        self.page_size = page_size
        self.task_list = task_list
        self.total = total

    def validate(self):
        if self.task_list:
            for k in self.task_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_index is not None:
            result['PageIndex'] = self.page_index
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        result['TaskList'] = []
        if self.task_list is not None:
            for k in self.task_list:
                result['TaskList'].append(k.to_map() if k else None)
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageIndex') is not None:
            self.page_index = m.get('PageIndex')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        self.task_list = []
        if m.get('TaskList') is not None:
            for k in m.get('TaskList'):
                temp_model = GetTaskListResponseBodyResponseTaskList()
                self.task_list.append(temp_model.from_map(k))
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class GetTaskListResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        response: GetTaskListResponseBodyResponse = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.response = response
        self.success = success

    def validate(self):
        if self.response:
            self.response.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.response is not None:
            result['Response'] = self.response.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Response') is not None:
            temp_model = GetTaskListResponseBodyResponse()
            self.response = temp_model.from_map(m['Response'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetTaskListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTaskListResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetTaskListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SaveMqConfigRequest(TeaModel):
    def __init__(
        self,
        config_name: str = None,
        mq_access_key: str = None,
        mq_access_secret: str = None,
        mq_endpoint: str = None,
        mq_group_id: str = None,
        mq_topic: str = None,
    ):
        self.config_name = config_name
        self.mq_access_key = mq_access_key
        self.mq_access_secret = mq_access_secret
        self.mq_endpoint = mq_endpoint
        self.mq_group_id = mq_group_id
        self.mq_topic = mq_topic

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_name is not None:
            result['ConfigName'] = self.config_name
        if self.mq_access_key is not None:
            result['MqAccessKey'] = self.mq_access_key
        if self.mq_access_secret is not None:
            result['MqAccessSecret'] = self.mq_access_secret
        if self.mq_endpoint is not None:
            result['MqEndpoint'] = self.mq_endpoint
        if self.mq_group_id is not None:
            result['MqGroupId'] = self.mq_group_id
        if self.mq_topic is not None:
            result['MqTopic'] = self.mq_topic
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigName') is not None:
            self.config_name = m.get('ConfigName')
        if m.get('MqAccessKey') is not None:
            self.mq_access_key = m.get('MqAccessKey')
        if m.get('MqAccessSecret') is not None:
            self.mq_access_secret = m.get('MqAccessSecret')
        if m.get('MqEndpoint') is not None:
            self.mq_endpoint = m.get('MqEndpoint')
        if m.get('MqGroupId') is not None:
            self.mq_group_id = m.get('MqGroupId')
        if m.get('MqTopic') is not None:
            self.mq_topic = m.get('MqTopic')
        return self


class SaveMqConfigResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SaveMqConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: SaveMqConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = SaveMqConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SaveOssConfigRequest(TeaModel):
    def __init__(
        self,
        config_name: str = None,
        oss_access_key_id: str = None,
        oss_access_key_secret: str = None,
        oss_bucket_name: str = None,
        oss_endpoint: str = None,
    ):
        self.config_name = config_name
        self.oss_access_key_id = oss_access_key_id
        self.oss_access_key_secret = oss_access_key_secret
        self.oss_bucket_name = oss_bucket_name
        self.oss_endpoint = oss_endpoint

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.config_name is not None:
            result['ConfigName'] = self.config_name
        if self.oss_access_key_id is not None:
            result['OssAccessKeyId'] = self.oss_access_key_id
        if self.oss_access_key_secret is not None:
            result['OssAccessKeySecret'] = self.oss_access_key_secret
        if self.oss_bucket_name is not None:
            result['OssBucketName'] = self.oss_bucket_name
        if self.oss_endpoint is not None:
            result['OssEndpoint'] = self.oss_endpoint
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConfigName') is not None:
            self.config_name = m.get('ConfigName')
        if m.get('OssAccessKeyId') is not None:
            self.oss_access_key_id = m.get('OssAccessKeyId')
        if m.get('OssAccessKeySecret') is not None:
            self.oss_access_key_secret = m.get('OssAccessKeySecret')
        if m.get('OssBucketName') is not None:
            self.oss_bucket_name = m.get('OssBucketName')
        if m.get('OssEndpoint') is not None:
            self.oss_endpoint = m.get('OssEndpoint')
        return self


class SaveOssConfigResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SaveOssConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: SaveOssConfigResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = SaveOssConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateTaskPriorityRequest(TeaModel):
    def __init__(
        self,
        priority: int = None,
        task_uid: str = None,
    ):
        self.priority = priority
        self.task_uid = task_uid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.task_uid is not None:
            result['TaskUid'] = self.task_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('TaskUid') is not None:
            self.task_uid = m.get('TaskUid')
        return self


class UpdateTaskPriorityResponseBody(TeaModel):
    def __init__(
        self,
        code: str = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UpdateTaskPriorityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: UpdateTaskPriorityResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = UpdateTaskPriorityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self



# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import BinaryIO, Dict, List


class AePredictCategoryRequest(TeaModel):
    def __init__(
        self,
        pic_url: str = None,
    ):
        self.pic_url = pic_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        return self


class AePredictCategoryAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
    ):
        self.pic_url_object = pic_url_object

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        return self


class AePredictCategoryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class AePropRecRequest(TeaModel):
    def __init__(
        self,
        pic_url: str = None,
    ):
        self.pic_url = pic_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        return self


class AePropRecAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
    ):
        self.pic_url_object = pic_url_object

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        return self


class AePropRecResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class AlivisionImgdupRequest(TeaModel):
    def __init__(
        self,
        image_height: int = None,
        image_width: int = None,
        output_image_num: int = None,
        pic_num_list: str = None,
        pic_url_list: str = None,
    ):
        self.image_height = image_height
        self.image_width = image_width
        self.output_image_num = output_image_num
        self.pic_num_list = pic_num_list
        self.pic_url_list = pic_url_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.image_height is not None:
            result['ImageHeight'] = self.image_height
        if self.image_width is not None:
            result['ImageWidth'] = self.image_width
        if self.output_image_num is not None:
            result['OutputImageNum'] = self.output_image_num
        if self.pic_num_list is not None:
            result['PicNumList'] = self.pic_num_list
        if self.pic_url_list is not None:
            result['PicUrlList'] = self.pic_url_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageHeight') is not None:
            self.image_height = m.get('ImageHeight')
        if m.get('ImageWidth') is not None:
            self.image_width = m.get('ImageWidth')
        if m.get('OutputImageNum') is not None:
            self.output_image_num = m.get('OutputImageNum')
        if m.get('PicNumList') is not None:
            self.pic_num_list = m.get('PicNumList')
        if m.get('PicUrlList') is not None:
            self.pic_url_list = m.get('PicUrlList')
        return self


class AlivisionImgdupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class CreateImageAmazonTaskRequest(TeaModel):
    def __init__(
        self,
        gif: bool = None,
        img_url_list: List[str] = None,
        template_mode: str = None,
        text_list: List[str] = None,
    ):
        self.gif = gif
        self.img_url_list = img_url_list
        self.template_mode = template_mode
        self.text_list = text_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gif is not None:
            result['Gif'] = self.gif
        if self.img_url_list is not None:
            result['ImgUrlList'] = self.img_url_list
        if self.template_mode is not None:
            result['TemplateMode'] = self.template_mode
        if self.text_list is not None:
            result['TextList'] = self.text_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Gif') is not None:
            self.gif = m.get('Gif')
        if m.get('ImgUrlList') is not None:
            self.img_url_list = m.get('ImgUrlList')
        if m.get('TemplateMode') is not None:
            self.template_mode = m.get('TemplateMode')
        if m.get('TextList') is not None:
            self.text_list = m.get('TextList')
        return self


class CreateImageAmazonTaskShrinkRequest(TeaModel):
    def __init__(
        self,
        gif: bool = None,
        img_url_list_shrink: str = None,
        template_mode: str = None,
        text_list_shrink: str = None,
    ):
        self.gif = gif
        self.img_url_list_shrink = img_url_list_shrink
        self.template_mode = template_mode
        self.text_list_shrink = text_list_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gif is not None:
            result['Gif'] = self.gif
        if self.img_url_list_shrink is not None:
            result['ImgUrlList'] = self.img_url_list_shrink
        if self.template_mode is not None:
            result['TemplateMode'] = self.template_mode
        if self.text_list_shrink is not None:
            result['TextList'] = self.text_list_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Gif') is not None:
            self.gif = m.get('Gif')
        if m.get('ImgUrlList') is not None:
            self.img_url_list_shrink = m.get('ImgUrlList')
        if m.get('TemplateMode') is not None:
            self.template_mode = m.get('TemplateMode')
        if m.get('TextList') is not None:
            self.text_list_shrink = m.get('TextList')
        return self


class CreateImageAmazonTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: int = None,
        data: int = None,
        message: str = None,
        request_id: str = None,
        success_response: bool = None,
    ):
        self.code = code
        self.data = data
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success_response = success_response

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success_response is not None:
            result['SuccessResponse'] = self.success_response
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SuccessResponse') is not None:
            self.success_response = m.get('SuccessResponse')
        return self


class CreateImageAmazonTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateImageAmazonTaskResponseBody = None,
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
            temp_model = CreateImageAmazonTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateRemoveWorkTaskRequest(TeaModel):
    def __init__(
        self,
        item_identity: str = None,
        pic_url: str = None,
    ):
        self.item_identity = item_identity
        self.pic_url = pic_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.item_identity is not None:
            result['ItemIdentity'] = self.item_identity
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ItemIdentity') is not None:
            self.item_identity = m.get('ItemIdentity')
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        return self


class CreateRemoveWorkTaskAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
        item_identity: str = None,
    ):
        self.pic_url_object = pic_url_object
        self.item_identity = item_identity

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        if self.item_identity is not None:
            result['ItemIdentity'] = self.item_identity
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        if m.get('ItemIdentity') is not None:
            self.item_identity = m.get('ItemIdentity')
        return self


class CreateRemoveWorkTaskResponseBody(TeaModel):
    def __init__(
        self,
        code: int = None,
        data: int = None,
        message: str = None,
        request_id: str = None,
        success_response: bool = None,
    ):
        self.code = code
        self.data = data
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success_response = success_response

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success_response is not None:
            result['SuccessResponse'] = self.success_response
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SuccessResponse') is not None:
            self.success_response = m.get('SuccessResponse')
        return self


class CreateRemoveWorkTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CreateRemoveWorkTaskResponseBody = None,
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
            temp_model = CreateRemoveWorkTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class FaceshifterTRequest(TeaModel):
    def __init__(
        self,
        age: int = None,
        gender: int = None,
        pic_url: str = None,
        race: int = None,
    ):
        self.age = age
        self.gender = gender
        self.pic_url = pic_url
        self.race = race

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.age is not None:
            result['Age'] = self.age
        if self.gender is not None:
            result['Gender'] = self.gender
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        if self.race is not None:
            result['Race'] = self.race
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Age') is not None:
            self.age = m.get('Age')
        if m.get('Gender') is not None:
            self.gender = m.get('Gender')
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        if m.get('Race') is not None:
            self.race = m.get('Race')
        return self


class FaceshifterTAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
        age: int = None,
        gender: int = None,
        race: int = None,
    ):
        self.pic_url_object = pic_url_object
        self.age = age
        self.gender = gender
        self.race = race

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        if self.age is not None:
            result['Age'] = self.age
        if self.gender is not None:
            result['Gender'] = self.gender
        if self.race is not None:
            result['Race'] = self.race
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        if m.get('Age') is not None:
            self.age = m.get('Age')
        if m.get('Gender') is not None:
            self.gender = m.get('Gender')
        if m.get('Race') is not None:
            self.race = m.get('Race')
        return self


class FaceshifterTResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class GetTaskResultRequest(TeaModel):
    def __init__(
        self,
        task_id: int = None,
    ):
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class GetTaskResultResponseBodyData(TeaModel):
    def __init__(
        self,
        result: str = None,
        status: int = None,
        status_name: str = None,
        task_id: int = None,
    ):
        self.result = result
        self.status = status
        self.status_name = status_name
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.result is not None:
            result['Result'] = self.result
        if self.status is not None:
            result['Status'] = self.status
        if self.status_name is not None:
            result['StatusName'] = self.status_name
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('StatusName') is not None:
            self.status_name = m.get('StatusName')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class GetTaskResultResponseBody(TeaModel):
    def __init__(
        self,
        code: int = None,
        data: GetTaskResultResponseBodyData = None,
        message: str = None,
        request_id: str = None,
        success_response: bool = None,
    ):
        self.code = code
        self.data = data
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success_response = success_response

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success_response is not None:
            result['SuccessResponse'] = self.success_response
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            temp_model = GetTaskResultResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SuccessResponse') is not None:
            self.success_response = m.get('SuccessResponse')
        return self


class GetTaskResultResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTaskResultResponseBody = None,
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
            temp_model = GetTaskResultResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTaskStatusRequest(TeaModel):
    def __init__(
        self,
        task_id: int = None,
    ):
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class GetTaskStatusResponseBodyData(TeaModel):
    def __init__(
        self,
        status: int = None,
        status_name: str = None,
        task_id: int = None,
    ):
        self.status = status
        self.status_name = status_name
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.status_name is not None:
            result['StatusName'] = self.status_name
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('StatusName') is not None:
            self.status_name = m.get('StatusName')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class GetTaskStatusResponseBody(TeaModel):
    def __init__(
        self,
        code: int = None,
        data: GetTaskStatusResponseBodyData = None,
        message: str = None,
        request_id: str = None,
        success_response: bool = None,
    ):
        self.code = code
        self.data = data
        self.message = message
        # Id of the request
        self.request_id = request_id
        self.success_response = success_response

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success_response is not None:
            result['SuccessResponse'] = self.success_response
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            temp_model = GetTaskStatusResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SuccessResponse') is not None:
            self.success_response = m.get('SuccessResponse')
        return self


class GetTaskStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetTaskStatusResponseBody = None,
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
            temp_model = GetTaskStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class KuajingSegRequest(TeaModel):
    def __init__(
        self,
        pic_url: str = None,
        return_pic_format: str = None,
        return_pic_type: str = None,
    ):
        self.pic_url = pic_url
        self.return_pic_format = return_pic_format
        self.return_pic_type = return_pic_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        if self.return_pic_format is not None:
            result['ReturnPicFormat'] = self.return_pic_format
        if self.return_pic_type is not None:
            result['ReturnPicType'] = self.return_pic_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        if m.get('ReturnPicFormat') is not None:
            self.return_pic_format = m.get('ReturnPicFormat')
        if m.get('ReturnPicType') is not None:
            self.return_pic_type = m.get('ReturnPicType')
        return self


class KuajingSegAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
        return_pic_format: str = None,
        return_pic_type: str = None,
    ):
        self.pic_url_object = pic_url_object
        self.return_pic_format = return_pic_format
        self.return_pic_type = return_pic_type

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        if self.return_pic_format is not None:
            result['ReturnPicFormat'] = self.return_pic_format
        if self.return_pic_type is not None:
            result['ReturnPicType'] = self.return_pic_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        if m.get('ReturnPicFormat') is not None:
            self.return_pic_format = m.get('ReturnPicFormat')
        if m.get('ReturnPicType') is not None:
            self.return_pic_type = m.get('ReturnPicType')
        return self


class KuajingSegResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class RemoveWordsRequest(TeaModel):
    def __init__(
        self,
        pic_url: str = None,
    ):
        self.pic_url = pic_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        return self


class RemoveWordsAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
    ):
        self.pic_url_object = pic_url_object

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        return self


class RemoveWordsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class ReplaceBackgroundRequest(TeaModel):
    def __init__(
        self,
        background_id: str = None,
        num: int = None,
        pic_background_url: str = None,
        pic_url: str = None,
    ):
        # 返回的图片背景图片ID
        self.background_id = background_id
        self.num = num
        self.pic_background_url = pic_background_url
        # 图片地址
        self.pic_url = pic_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.background_id is not None:
            result['BackgroundId'] = self.background_id
        if self.num is not None:
            result['Num'] = self.num
        if self.pic_background_url is not None:
            result['PicBackgroundUrl'] = self.pic_background_url
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackgroundId') is not None:
            self.background_id = m.get('BackgroundId')
        if m.get('Num') is not None:
            self.num = m.get('Num')
        if m.get('PicBackgroundUrl') is not None:
            self.pic_background_url = m.get('PicBackgroundUrl')
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        return self


class ReplaceBackgroundAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
        background_id: str = None,
        num: int = None,
        pic_background_url: str = None,
    ):
        self.pic_url_object = pic_url_object
        # 返回的图片背景图片ID
        self.background_id = background_id
        self.num = num
        self.pic_background_url = pic_background_url

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        if self.background_id is not None:
            result['BackgroundId'] = self.background_id
        if self.num is not None:
            result['Num'] = self.num
        if self.pic_background_url is not None:
            result['PicBackgroundUrl'] = self.pic_background_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        if m.get('BackgroundId') is not None:
            self.background_id = m.get('BackgroundId')
        if m.get('Num') is not None:
            self.num = m.get('Num')
        if m.get('PicBackgroundUrl') is not None:
            self.pic_background_url = m.get('PicBackgroundUrl')
        return self


class ReplaceBackgroundResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class SeleteCommodityRequest(TeaModel):
    def __init__(
        self,
        num: int = None,
        pid: str = None,
        query: str = None,
        start: int = None,
    ):
        self.num = num
        self.pid = pid
        self.query = query
        self.start = start

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.num is not None:
            result['Num'] = self.num
        if self.pid is not None:
            result['Pid'] = self.pid
        if self.query is not None:
            result['Query'] = self.query
        if self.start is not None:
            result['Start'] = self.start
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Num') is not None:
            self.num = m.get('Num')
        if m.get('Pid') is not None:
            self.pid = m.get('Pid')
        if m.get('Query') is not None:
            self.query = m.get('Query')
        if m.get('Start') is not None:
            self.start = m.get('Start')
        return self


class SeleteCommodityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class SeleteCommodityByBToBRequest(TeaModel):
    def __init__(
        self,
        num: int = None,
        pid: str = None,
        query: str = None,
        start: int = None,
    ):
        self.num = num
        self.pid = pid
        self.query = query
        self.start = start

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.num is not None:
            result['Num'] = self.num
        if self.pid is not None:
            result['Pid'] = self.pid
        if self.query is not None:
            result['Query'] = self.query
        if self.start is not None:
            result['Start'] = self.start
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Num') is not None:
            self.num = m.get('Num')
        if m.get('Pid') is not None:
            self.pid = m.get('Pid')
        if m.get('Query') is not None:
            self.query = m.get('Query')
        if m.get('Start') is not None:
            self.start = m.get('Start')
        return self


class SeleteCommodityByBToBResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class TbPredictCategoryRequest(TeaModel):
    def __init__(
        self,
        pic_url: str = None,
    ):
        self.pic_url = pic_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        return self


class TbPredictCategoryAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
    ):
        self.pic_url_object = pic_url_object

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        return self


class TbPredictCategoryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class TbPropRecRequest(TeaModel):
    def __init__(
        self,
        pic_url: str = None,
    ):
        self.pic_url = pic_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url is not None:
            result['PicUrl'] = self.pic_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrl') is not None:
            self.pic_url = m.get('PicUrl')
        return self


class TbPropRecAdvanceRequest(TeaModel):
    def __init__(
        self,
        pic_url_object: BinaryIO = None,
    ):
        self.pic_url_object = pic_url_object

    def validate(self):
        self.validate_required(self.pic_url_object, 'pic_url_object')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pic_url_object is not None:
            result['PicUrlObject'] = self.pic_url_object
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PicUrlObject') is not None:
            self.pic_url_object = m.get('PicUrlObject')
        return self


class TbPropRecResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self


class TransferUrlByBtoBRequest(TeaModel):
    def __init__(
        self,
        offer_id: int = None,
        pid: str = None,
    ):
        self.offer_id = offer_id
        self.pid = pid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.offer_id is not None:
            result['OfferId'] = self.offer_id
        if self.pid is not None:
            result['Pid'] = self.pid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OfferId') is not None:
            self.offer_id = m.get('OfferId')
        if m.get('Pid') is not None:
            self.pid = m.get('Pid')
        return self


class TransferUrlByBtoBResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: dict = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.status_code, 'status_code')
        self.validate_required(self.body, 'body')

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
            result['body'] = self.body
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            self.body = m.get('body')
        return self



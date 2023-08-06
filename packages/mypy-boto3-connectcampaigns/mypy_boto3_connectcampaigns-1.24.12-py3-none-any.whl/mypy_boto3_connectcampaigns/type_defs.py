"""
Type annotations for connectcampaigns service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/type_defs/)

Usage::

    ```python
    from mypy_boto3_connectcampaigns.type_defs import AnswerMachineDetectionConfigTypeDef

    data: AnswerMachineDetectionConfigTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    CampaignStateType,
    FailureCodeType,
    GetCampaignStateBatchFailureCodeType,
    InstanceOnboardingJobFailureCodeType,
    InstanceOnboardingJobStatusCodeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AnswerMachineDetectionConfigTypeDef",
    "InstanceIdFilterTypeDef",
    "CampaignSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteCampaignRequestRequestTypeDef",
    "DeleteConnectInstanceConfigRequestRequestTypeDef",
    "DeleteInstanceOnboardingJobRequestRequestTypeDef",
    "DescribeCampaignRequestRequestTypeDef",
    "DialRequestTypeDef",
    "PredictiveDialerConfigTypeDef",
    "ProgressiveDialerConfigTypeDef",
    "EncryptionConfigTypeDef",
    "FailedCampaignStateResponseTypeDef",
    "FailedRequestTypeDef",
    "GetCampaignStateBatchRequestRequestTypeDef",
    "SuccessfulCampaignStateResponseTypeDef",
    "GetCampaignStateRequestRequestTypeDef",
    "GetConnectInstanceConfigRequestRequestTypeDef",
    "GetInstanceOnboardingJobStatusRequestRequestTypeDef",
    "InstanceOnboardingJobStatusTypeDef",
    "PaginatorConfigTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PauseCampaignRequestRequestTypeDef",
    "SuccessfulRequestTypeDef",
    "ResumeCampaignRequestRequestTypeDef",
    "StartCampaignRequestRequestTypeDef",
    "StopCampaignRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCampaignNameRequestRequestTypeDef",
    "OutboundCallConfigTypeDef",
    "UpdateCampaignOutboundCallConfigRequestRequestTypeDef",
    "CampaignFiltersTypeDef",
    "CreateCampaignResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCampaignStateResponseTypeDef",
    "ListCampaignsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutDialRequestBatchRequestRequestTypeDef",
    "DialerConfigTypeDef",
    "InstanceConfigTypeDef",
    "StartInstanceOnboardingJobRequestRequestTypeDef",
    "GetCampaignStateBatchResponseTypeDef",
    "GetInstanceOnboardingJobStatusResponseTypeDef",
    "StartInstanceOnboardingJobResponseTypeDef",
    "PutDialRequestBatchResponseTypeDef",
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    "ListCampaignsRequestRequestTypeDef",
    "CampaignTypeDef",
    "CreateCampaignRequestRequestTypeDef",
    "UpdateCampaignDialerConfigRequestRequestTypeDef",
    "GetConnectInstanceConfigResponseTypeDef",
    "DescribeCampaignResponseTypeDef",
)

AnswerMachineDetectionConfigTypeDef = TypedDict(
    "AnswerMachineDetectionConfigTypeDef",
    {
        "enableAnswerMachineDetection": bool,
    },
)

InstanceIdFilterTypeDef = TypedDict(
    "InstanceIdFilterTypeDef",
    {
        "operator": Literal["Eq"],
        "value": str,
    },
)

CampaignSummaryTypeDef = TypedDict(
    "CampaignSummaryTypeDef",
    {
        "arn": str,
        "connectInstanceId": str,
        "id": str,
        "name": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

DeleteCampaignRequestRequestTypeDef = TypedDict(
    "DeleteCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteConnectInstanceConfigRequestRequestTypeDef = TypedDict(
    "DeleteConnectInstanceConfigRequestRequestTypeDef",
    {
        "connectInstanceId": str,
    },
)

DeleteInstanceOnboardingJobRequestRequestTypeDef = TypedDict(
    "DeleteInstanceOnboardingJobRequestRequestTypeDef",
    {
        "connectInstanceId": str,
    },
)

DescribeCampaignRequestRequestTypeDef = TypedDict(
    "DescribeCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

DialRequestTypeDef = TypedDict(
    "DialRequestTypeDef",
    {
        "attributes": Mapping[str, str],
        "clientToken": str,
        "expirationTime": Union[datetime, str],
        "phoneNumber": str,
    },
)

PredictiveDialerConfigTypeDef = TypedDict(
    "PredictiveDialerConfigTypeDef",
    {
        "bandwidthAllocation": float,
    },
)

ProgressiveDialerConfigTypeDef = TypedDict(
    "ProgressiveDialerConfigTypeDef",
    {
        "bandwidthAllocation": float,
    },
)

_RequiredEncryptionConfigTypeDef = TypedDict(
    "_RequiredEncryptionConfigTypeDef",
    {
        "enabled": bool,
    },
)
_OptionalEncryptionConfigTypeDef = TypedDict(
    "_OptionalEncryptionConfigTypeDef",
    {
        "encryptionType": Literal["KMS"],
        "keyArn": str,
    },
    total=False,
)


class EncryptionConfigTypeDef(_RequiredEncryptionConfigTypeDef, _OptionalEncryptionConfigTypeDef):
    pass


FailedCampaignStateResponseTypeDef = TypedDict(
    "FailedCampaignStateResponseTypeDef",
    {
        "campaignId": str,
        "failureCode": GetCampaignStateBatchFailureCodeType,
    },
    total=False,
)

FailedRequestTypeDef = TypedDict(
    "FailedRequestTypeDef",
    {
        "clientToken": str,
        "failureCode": FailureCodeType,
        "id": str,
    },
    total=False,
)

GetCampaignStateBatchRequestRequestTypeDef = TypedDict(
    "GetCampaignStateBatchRequestRequestTypeDef",
    {
        "campaignIds": Sequence[str],
    },
)

SuccessfulCampaignStateResponseTypeDef = TypedDict(
    "SuccessfulCampaignStateResponseTypeDef",
    {
        "campaignId": str,
        "state": CampaignStateType,
    },
    total=False,
)

GetCampaignStateRequestRequestTypeDef = TypedDict(
    "GetCampaignStateRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetConnectInstanceConfigRequestRequestTypeDef = TypedDict(
    "GetConnectInstanceConfigRequestRequestTypeDef",
    {
        "connectInstanceId": str,
    },
)

GetInstanceOnboardingJobStatusRequestRequestTypeDef = TypedDict(
    "GetInstanceOnboardingJobStatusRequestRequestTypeDef",
    {
        "connectInstanceId": str,
    },
)

_RequiredInstanceOnboardingJobStatusTypeDef = TypedDict(
    "_RequiredInstanceOnboardingJobStatusTypeDef",
    {
        "connectInstanceId": str,
        "status": InstanceOnboardingJobStatusCodeType,
    },
)
_OptionalInstanceOnboardingJobStatusTypeDef = TypedDict(
    "_OptionalInstanceOnboardingJobStatusTypeDef",
    {
        "failureCode": InstanceOnboardingJobFailureCodeType,
    },
    total=False,
)


class InstanceOnboardingJobStatusTypeDef(
    _RequiredInstanceOnboardingJobStatusTypeDef, _OptionalInstanceOnboardingJobStatusTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "arn": str,
    },
)

PauseCampaignRequestRequestTypeDef = TypedDict(
    "PauseCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

SuccessfulRequestTypeDef = TypedDict(
    "SuccessfulRequestTypeDef",
    {
        "clientToken": str,
        "id": str,
    },
    total=False,
)

ResumeCampaignRequestRequestTypeDef = TypedDict(
    "ResumeCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

StartCampaignRequestRequestTypeDef = TypedDict(
    "StartCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

StopCampaignRequestRequestTypeDef = TypedDict(
    "StopCampaignRequestRequestTypeDef",
    {
        "id": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "arn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "arn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateCampaignNameRequestRequestTypeDef = TypedDict(
    "UpdateCampaignNameRequestRequestTypeDef",
    {
        "id": str,
        "name": str,
    },
)

_RequiredOutboundCallConfigTypeDef = TypedDict(
    "_RequiredOutboundCallConfigTypeDef",
    {
        "connectContactFlowId": str,
        "connectQueueId": str,
    },
)
_OptionalOutboundCallConfigTypeDef = TypedDict(
    "_OptionalOutboundCallConfigTypeDef",
    {
        "answerMachineDetectionConfig": AnswerMachineDetectionConfigTypeDef,
        "connectSourcePhoneNumber": str,
    },
    total=False,
)


class OutboundCallConfigTypeDef(
    _RequiredOutboundCallConfigTypeDef, _OptionalOutboundCallConfigTypeDef
):
    pass


_RequiredUpdateCampaignOutboundCallConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCampaignOutboundCallConfigRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateCampaignOutboundCallConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCampaignOutboundCallConfigRequestRequestTypeDef",
    {
        "answerMachineDetectionConfig": AnswerMachineDetectionConfigTypeDef,
        "connectContactFlowId": str,
        "connectSourcePhoneNumber": str,
    },
    total=False,
)


class UpdateCampaignOutboundCallConfigRequestRequestTypeDef(
    _RequiredUpdateCampaignOutboundCallConfigRequestRequestTypeDef,
    _OptionalUpdateCampaignOutboundCallConfigRequestRequestTypeDef,
):
    pass


CampaignFiltersTypeDef = TypedDict(
    "CampaignFiltersTypeDef",
    {
        "instanceIdFilter": InstanceIdFilterTypeDef,
    },
    total=False,
)

CreateCampaignResponseTypeDef = TypedDict(
    "CreateCampaignResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCampaignStateResponseTypeDef = TypedDict(
    "GetCampaignStateResponseTypeDef",
    {
        "state": CampaignStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCampaignsResponseTypeDef = TypedDict(
    "ListCampaignsResponseTypeDef",
    {
        "campaignSummaryList": List[CampaignSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDialRequestBatchRequestRequestTypeDef = TypedDict(
    "PutDialRequestBatchRequestRequestTypeDef",
    {
        "dialRequests": Sequence[DialRequestTypeDef],
        "id": str,
    },
)

DialerConfigTypeDef = TypedDict(
    "DialerConfigTypeDef",
    {
        "predictiveDialerConfig": PredictiveDialerConfigTypeDef,
        "progressiveDialerConfig": ProgressiveDialerConfigTypeDef,
    },
    total=False,
)

InstanceConfigTypeDef = TypedDict(
    "InstanceConfigTypeDef",
    {
        "connectInstanceId": str,
        "encryptionConfig": EncryptionConfigTypeDef,
        "serviceLinkedRoleArn": str,
    },
)

StartInstanceOnboardingJobRequestRequestTypeDef = TypedDict(
    "StartInstanceOnboardingJobRequestRequestTypeDef",
    {
        "connectInstanceId": str,
        "encryptionConfig": EncryptionConfigTypeDef,
    },
)

GetCampaignStateBatchResponseTypeDef = TypedDict(
    "GetCampaignStateBatchResponseTypeDef",
    {
        "failedRequests": List[FailedCampaignStateResponseTypeDef],
        "successfulRequests": List[SuccessfulCampaignStateResponseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInstanceOnboardingJobStatusResponseTypeDef = TypedDict(
    "GetInstanceOnboardingJobStatusResponseTypeDef",
    {
        "connectInstanceOnboardingJobStatus": InstanceOnboardingJobStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartInstanceOnboardingJobResponseTypeDef = TypedDict(
    "StartInstanceOnboardingJobResponseTypeDef",
    {
        "connectInstanceOnboardingJobStatus": InstanceOnboardingJobStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDialRequestBatchResponseTypeDef = TypedDict(
    "PutDialRequestBatchResponseTypeDef",
    {
        "failedRequests": List[FailedRequestTypeDef],
        "successfulRequests": List[SuccessfulRequestTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCampaignsRequestListCampaignsPaginateTypeDef = TypedDict(
    "ListCampaignsRequestListCampaignsPaginateTypeDef",
    {
        "filters": CampaignFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCampaignsRequestRequestTypeDef = TypedDict(
    "ListCampaignsRequestRequestTypeDef",
    {
        "filters": CampaignFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredCampaignTypeDef = TypedDict(
    "_RequiredCampaignTypeDef",
    {
        "arn": str,
        "connectInstanceId": str,
        "dialerConfig": DialerConfigTypeDef,
        "id": str,
        "name": str,
        "outboundCallConfig": OutboundCallConfigTypeDef,
    },
)
_OptionalCampaignTypeDef = TypedDict(
    "_OptionalCampaignTypeDef",
    {
        "tags": Dict[str, str],
    },
    total=False,
)


class CampaignTypeDef(_RequiredCampaignTypeDef, _OptionalCampaignTypeDef):
    pass


_RequiredCreateCampaignRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCampaignRequestRequestTypeDef",
    {
        "connectInstanceId": str,
        "dialerConfig": DialerConfigTypeDef,
        "name": str,
        "outboundCallConfig": OutboundCallConfigTypeDef,
    },
)
_OptionalCreateCampaignRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCampaignRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateCampaignRequestRequestTypeDef(
    _RequiredCreateCampaignRequestRequestTypeDef, _OptionalCreateCampaignRequestRequestTypeDef
):
    pass


UpdateCampaignDialerConfigRequestRequestTypeDef = TypedDict(
    "UpdateCampaignDialerConfigRequestRequestTypeDef",
    {
        "dialerConfig": DialerConfigTypeDef,
        "id": str,
    },
)

GetConnectInstanceConfigResponseTypeDef = TypedDict(
    "GetConnectInstanceConfigResponseTypeDef",
    {
        "connectInstanceConfig": InstanceConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCampaignResponseTypeDef = TypedDict(
    "DescribeCampaignResponseTypeDef",
    {
        "campaign": CampaignTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

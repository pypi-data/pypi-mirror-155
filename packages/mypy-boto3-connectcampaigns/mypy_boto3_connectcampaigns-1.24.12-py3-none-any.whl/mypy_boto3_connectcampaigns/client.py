"""
Type annotations for connectcampaigns service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_connectcampaigns.client import ConnectCampaignServiceClient

    session = Session()
    client: ConnectCampaignServiceClient = session.client("connectcampaigns")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListCampaignsPaginator
from .type_defs import (
    AnswerMachineDetectionConfigTypeDef,
    CampaignFiltersTypeDef,
    CreateCampaignResponseTypeDef,
    DescribeCampaignResponseTypeDef,
    DialerConfigTypeDef,
    DialRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EncryptionConfigTypeDef,
    GetCampaignStateBatchResponseTypeDef,
    GetCampaignStateResponseTypeDef,
    GetConnectInstanceConfigResponseTypeDef,
    GetInstanceOnboardingJobStatusResponseTypeDef,
    ListCampaignsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OutboundCallConfigTypeDef,
    PutDialRequestBatchResponseTypeDef,
    StartInstanceOnboardingJobResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ConnectCampaignServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidCampaignStateException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ConnectCampaignServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectCampaignServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#close)
        """

    def create_campaign(
        self,
        *,
        connectInstanceId: str,
        dialerConfig: DialerConfigTypeDef,
        name: str,
        outboundCallConfig: OutboundCallConfigTypeDef,
        tags: Mapping[str, str] = ...
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.create_campaign)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#create_campaign)
        """

    def delete_campaign(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a campaign from the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.delete_campaign)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#delete_campaign)
        """

    def delete_connect_instance_config(
        self, *, connectInstanceId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a connect instance config from the specified AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.delete_connect_instance_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#delete_connect_instance_config)
        """

    def delete_instance_onboarding_job(
        self, *, connectInstanceId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the Connect Campaigns onboarding job for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.delete_instance_onboarding_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#delete_instance_onboarding_job)
        """

    def describe_campaign(self, *, id: str) -> DescribeCampaignResponseTypeDef:
        """
        Describes the specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.describe_campaign)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#describe_campaign)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#generate_presigned_url)
        """

    def get_campaign_state(self, *, id: str) -> GetCampaignStateResponseTypeDef:
        """
        Get state of a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.get_campaign_state)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#get_campaign_state)
        """

    def get_campaign_state_batch(
        self, *, campaignIds: Sequence[str]
    ) -> GetCampaignStateBatchResponseTypeDef:
        """
        Get state of campaigns for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.get_campaign_state_batch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#get_campaign_state_batch)
        """

    def get_connect_instance_config(
        self, *, connectInstanceId: str
    ) -> GetConnectInstanceConfigResponseTypeDef:
        """
        Get the specific Connect instance config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.get_connect_instance_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#get_connect_instance_config)
        """

    def get_instance_onboarding_job_status(
        self, *, connectInstanceId: str
    ) -> GetInstanceOnboardingJobStatusResponseTypeDef:
        """
        Get the specific instance onboarding job status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.get_instance_onboarding_job_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#get_instance_onboarding_job_status)
        """

    def list_campaigns(
        self, *, filters: CampaignFiltersTypeDef = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListCampaignsResponseTypeDef:
        """
        Provides summary information about the campaigns under the specified Amazon
        Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.list_campaigns)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#list_campaigns)
        """

    def list_tags_for_resource(self, *, arn: str) -> ListTagsForResourceResponseTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#list_tags_for_resource)
        """

    def pause_campaign(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Pauses a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.pause_campaign)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#pause_campaign)
        """

    def put_dial_request_batch(
        self, *, dialRequests: Sequence[DialRequestTypeDef], id: str
    ) -> PutDialRequestBatchResponseTypeDef:
        """
        Creates dials requests for the specified campaign Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.put_dial_request_batch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#put_dial_request_batch)
        """

    def resume_campaign(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.resume_campaign)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#resume_campaign)
        """

    def start_campaign(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Starts a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.start_campaign)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#start_campaign)
        """

    def start_instance_onboarding_job(
        self, *, connectInstanceId: str, encryptionConfig: EncryptionConfigTypeDef
    ) -> StartInstanceOnboardingJobResponseTypeDef:
        """
        Onboard the specific Amazon Connect instance to Connect Campaigns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.start_instance_onboarding_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#start_instance_onboarding_job)
        """

    def stop_campaign(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.stop_campaign)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#stop_campaign)
        """

    def tag_resource(self, *, arn: str, tags: Mapping[str, str]) -> EmptyResponseMetadataTypeDef:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#tag_resource)
        """

    def untag_resource(self, *, arn: str, tagKeys: Sequence[str]) -> EmptyResponseMetadataTypeDef:
        """
        Untag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#untag_resource)
        """

    def update_campaign_dialer_config(
        self, *, dialerConfig: DialerConfigTypeDef, id: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the dialer config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.update_campaign_dialer_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#update_campaign_dialer_config)
        """

    def update_campaign_name(self, *, id: str, name: str) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.update_campaign_name)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#update_campaign_name)
        """

    def update_campaign_outbound_call_config(
        self,
        *,
        id: str,
        answerMachineDetectionConfig: AnswerMachineDetectionConfigTypeDef = ...,
        connectContactFlowId: str = ...,
        connectSourcePhoneNumber: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the outbound call config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.update_campaign_outbound_call_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#update_campaign_outbound_call_config)
        """

    def get_paginator(self, operation_name: Literal["list_campaigns"]) -> ListCampaignsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcampaigns/client/#get_paginator)
        """

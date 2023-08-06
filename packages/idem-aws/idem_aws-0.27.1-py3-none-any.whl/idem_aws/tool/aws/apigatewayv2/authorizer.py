from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions for AWS API Gateway v2 Authorizer resources.
"""


def convert_raw_authorizer_to_present(
    hub, api_id: str, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    r"""
    Convert AWS API Gateway v2 Authorizer resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        api_id(string): The API resource identifier in Amazon Web Services.
        raw_resource(Dict[str, Any]): The AWS response to convert.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_parameters = OrderedDict(
        {
            "AuthorizerCredentialsArn": "authorizer_credentials_arn",
            "AuthorizerPayloadFormatVersion": "authorizer_payload_format_version",
            "AuthorizerResultTtlInSeconds": "authorizer_result_ttl_in_seconds",
            "AuthorizerType": "authorizer_type",
            "AuthorizerUri": "authorizer_uri",
            "EnableSimpleResponses": "enable_simple_responses",
            "IdentitySource": "identity_source",
            "JwtConfiguration": "jwt_configuration",
        }
    )
    resource_translated = {
        "name": raw_resource.get("Name"),
        "resource_id": raw_resource.get("AuthorizerId"),
        "api_id": api_id,
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated

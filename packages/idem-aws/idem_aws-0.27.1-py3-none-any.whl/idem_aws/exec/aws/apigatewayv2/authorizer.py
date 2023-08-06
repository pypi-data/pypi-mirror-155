from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Exec functions for AWS API Gateway v2 Authorizer resources.
"""


async def update(
    hub,
    ctx,
    api_id: str,
    resource_id: str,
    raw_resource: Dict[str, Any],
    resource_parameters: Dict[str, None],
) -> Dict[str, Any]:
    r"""
    Updates an AWS API Gateway v2 Authorizer resource.

    Args:
        hub: required for functions in hub.
        ctx: context.
        api_id(string): The API resource identifier in Amazon Web Services.
        resource_id(string): The Authorizer resource identifier in Amazon Web Services.
        raw_resource(Dict): Existing resource parameters in Amazon Web Services.
        resource_parameters(Dict): Parameters from SLS file.

    Returns:
        Dict[str, Any]
    """

    result = dict(comment=(), result=True, ret=None)

    parameters = OrderedDict(
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

    parameters_to_update = {}

    identity_source = resource_parameters.get("IdentitySource")
    if identity_source:
        if not hub.tool.aws.state_comparison_utils.are_lists_identical(
            identity_source,
            raw_resource.get("IdentitySource"),
        ):
            parameters_to_update["IdentitySource"] = identity_source

        resource_parameters.pop("IdentitySource")

    jwt_configuration = resource_parameters.get("JwtConfiguration")
    if jwt_configuration is not None:
        update_jwt_configuration = False
        old_jwt_configuration = raw_resource.get("JwtConfiguration")

        if not hub.tool.aws.state_comparison_utils.are_lists_identical(
            jwt_configuration.get("Audience"),
            old_jwt_configuration.get("Audience"),
        ):
            update_jwt_configuration = True
        elif jwt_configuration.get("Issuer") is not None and jwt_configuration.get(
            "Issuer"
        ) != old_jwt_configuration.get("Issuer"):
            update_jwt_configuration = True

        if update_jwt_configuration:
            parameters_to_update["JwtConfiguration"] = jwt_configuration

        resource_parameters.pop("JwtConfiguration")

    for key, value in resource_parameters.items():
        if value is not None and value != raw_resource.get(key):
            parameters_to_update[key] = resource_parameters[key]

    if parameters_to_update:
        result["ret"] = {}
        for parameter_raw, parameter_present in parameters.items():
            if parameter_raw in parameters_to_update:
                result["ret"][parameter_present] = parameters_to_update[parameter_raw]

        if ctx.get("test", False):
            result["comment"] = (
                f"Would update parameters: " + ",".join(result["ret"].keys()),
            )
        else:
            update_ret = await hub.exec.boto3.client.apigatewayv2.update_authorizer(
                ctx,
                ApiId=api_id,
                AuthorizerId=resource_id,
                **parameters_to_update,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result

            result["comment"] = (
                f"Updated parameters: " + ",".join(result["ret"].keys()),
            )

    return result

from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Exec functions for AWS API Gateway v2 Domain Name resources.
"""


async def update(
    hub,
    ctx,
    resource_id: str,
    raw_resource: Dict[str, Any],
    resource_parameters: Dict[str, None],
) -> Dict[str, Any]:
    r"""
    Updates an AWS API Gateway v2 Domain Name resource.

    Args:
        hub: required for functions in hub.
        ctx: context.
        resource_id(string): The Domain Name resource identifier in Amazon Web Services.
        raw_resource(Dict): Existing resource parameters in Amazon Web Services.
        resource_parameters(Dict): Parameters from SLS file.

    Returns:
        Dict[str, Any]
    """

    result = dict(comment=(), result=True, ret=None)

    parameters = OrderedDict(
        {
            "DomainNameConfigurations": "domain_name_configurations",
            "MutualTlsAuthentication": "mutual_tls_authentication",
        }
    )

    parameters_to_update = {}

    domain_name_configurations = resource_parameters.get("DomainNameConfigurations")
    if domain_name_configurations is not None:
        if not hub.tool.aws.apigatewayv2.domain_name.are_domain_name_configurations_identical(
            domain_name_configurations,
            raw_resource.get("DomainNameConfigurations"),
        ):
            parameters_to_update[
                "DomainNameConfigurations"
            ] = domain_name_configurations

        resource_parameters.pop("DomainNameConfigurations")

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
            update_ret = await hub.exec.boto3.client.apigatewayv2.update_domain_name(
                ctx,
                DomainName=resource_id,
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

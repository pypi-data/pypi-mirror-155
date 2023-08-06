from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

"""
Util functions for AWS API Gateway v2 Domain Name resources.
"""


def convert_raw_domain_name_to_present(
    hub, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    r"""
    Convert AWS API Gateway v2 Domain Name resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        raw_resource(Dict[str, Any]): The AWS response to convert.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_parameters = OrderedDict(
        {
            "ApiMappingSelectionExpression": "api_mapping_selection_expression",
            "DomainNameConfigurations": "domain_name_configurations",
            "MutualTlsAuthentication": "mutual_tls_authentication",
            "Tags": "tags",
        }
    )
    resource_translated = {
        "resource_id": raw_resource.get("DomainName"),
        "name": raw_resource.get("DomainName"),
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


def are_domain_name_configurations_identical(
    hub,
    new_configuration: List,
    old_configuration: List,
) -> bool:
    r"""
    Compares the new and old domain name configurations.

    Args:
        hub: required for functions in hub.
        new_configuration(List): The new domain name configuration parameters.
        old_configuration(List): The old domain name configuration parameters.

    Returns:
        bool: true if there are no differences between the new and old domain name configurations.
    """

    if (new_configuration is None or len(new_configuration) == 0) and (
        old_configuration is None or len(old_configuration) == 0
    ):
        return True
    if (
        new_configuration is None
        or len(new_configuration) == 0
        or old_configuration is None
        or len(old_configuration) == 0
    ):
        return False

    diff = [
        i
        for i in new_configuration + old_configuration
        if i not in new_configuration or i not in old_configuration
    ]

    return len(diff) == 0

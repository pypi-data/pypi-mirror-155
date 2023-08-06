import copy
from typing import Any
from typing import Dict
from typing import List


async def update_tags(
    hub,
    ctx,
    resource_id: str,
    old_tags: List[Dict[str, Any]],
    new_tags: List[Dict[str, Any]],
):
    """
    Update tags of AWS CloudWatchEvents resources

    Args:
        hub:
        ctx:
        resource_id: aws events rule arn
        old_tags: List of existing tags
        new_tags: List of new tags

    Returns:
        {"result": True|False, "comment": ("A message",), "ret": None}

    """

    tags_to_add = []
    tags_to_remove = []
    old_tags_map = {tag.get("Key"): tag for tag in old_tags or []}
    tags_result = copy.deepcopy(old_tags_map)
    if new_tags is not None:
        for tag in new_tags:
            if tag.get("Key") in old_tags_map:
                if tag.get("Value") == old_tags_map.get(tag.get("Key")).get("Value"):
                    del old_tags_map[tag.get("Key")]
                else:
                    tags_to_add.append(tag)
            else:
                tags_to_add.append(tag)
        tags_to_remove = list(old_tags_map.keys())

    result = dict(comment=(), result=True, ret=None)
    if (not tags_to_remove) and (not tags_to_add):
        return result

    if tags_to_remove:
        if not ctx.get("test", False):
            delete_tag_resp = await hub.exec.boto3.client.events.untag_resource(
                ctx, ResourceARN=resource_id, TagKeys=tags_to_remove
            )
            if not delete_tag_resp:
                failure_message = (
                    f"Could not delete tags {tags_to_remove} for aws.events.rule with ARN {resource_id}. "
                    f"Failed with error: {delete_tag_resp['comment']}",
                )
                hub.log.debug(failure_message)
                result["comment"] = failure_message
                result["result"] = False
                return result
        [tags_result.pop(key) for key in tags_to_remove]

    if tags_to_add:
        if not ctx.get("test", False):
            create_tag_resp = await hub.exec.boto3.client.events.tag_resource(
                ctx, ResourceARN=resource_id, Tags=tags_to_add
            )
            if not create_tag_resp:
                failure_message = (
                    f"Could not create tags {tags_to_add} for aws.events.rule with ARN {resource_id}."
                    f" Failed with error: " + create_tag_resp["comment"],
                )
                hub.log.debug(failure_message)
                result["comment"] = result["comment"] + failure_message
                result["result"] = False
                return result

    result["ret"] = {"tags": list(tags_result.values()) + list(tags_to_add)}
    result["comment"] = result["comment"] + (
        f"Update tags: Add [{tags_to_add}] Remove [{tags_to_remove}]",
    )
    return result

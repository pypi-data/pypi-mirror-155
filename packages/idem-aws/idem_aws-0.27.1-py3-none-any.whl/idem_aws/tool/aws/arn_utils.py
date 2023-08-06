def build_arn(
    hub,
    partition: str,
    service: str,
    region: str = None,
    account_id: str = None,
    resource: str = None,
) -> str:
    """
    Creates an ARN from parameters.

    Args:
        hub: The redistributed pop central hub.
        partition(str): The partition that the resource is in. For standard AWS regions, the partition is "aws". If you have resources in
            other partitions, the partition is "aws-partitionname". For example, the partition for resources in the China
                (Beijing) region is "aws-cn".
        service(str): The service namespace that identifies the AWS product (for example, Amazon S3, IAM, or Amazon RDS). For a list of
                namespaces, see http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces.
        region(str, optional): The region the resource resides in. Note that the ARNs for some resources do not require a region, so this
                component might be omitted.
        account_id(str, optional): The ID of the AWS account that owns the resource, without the hyphens. For example, 123456789012. Note that the
                ARNs for some resources don't require an account number, so this component might be omitted.
        resource(str, optional): The content of this part of the ARN varies by service. It often includes an indicator of the type of resource —
                for example, an IAM user or Amazon RDS database - followed by a slash (/) or a colon (:), followed by the
                resource name itself. Some services allows paths for resource names, as described in
                http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#arns-paths.

    Returns:
        The ARN (str)
    """
    ARN_PREFIX = "arn"
    ARN_DELIMITER = ":"
    return (
        ARN_PREFIX
        + ARN_DELIMITER
        + partition
        + ARN_DELIMITER
        + service
        + ARN_DELIMITER
        + str(region or "")
        + ARN_DELIMITER
        + str(account_id or "")
        + ARN_DELIMITER
        + str(resource or "")
    )

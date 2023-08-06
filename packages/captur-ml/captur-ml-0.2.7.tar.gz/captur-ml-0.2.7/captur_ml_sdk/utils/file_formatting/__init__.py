def get_bucket_from_gs_uri(gs_uri: str) -> str:
    """Extracts the bucket name from a Google Storage URI.

    Args:
        gs_uri (str): Google Storage URI.

    Returns:
        str: Bucket name.
    """
    return gs_uri.split("/")[2]


def get_filepath_from_gs_uri(gs_uri: str) -> str:
    """Extracts the filepath from a Google Storage URI.

    Args:
        gs_uri (str): Google Storage URI.

    Returns:
        str: Filepath.
    """
    return "/".join(gs_uri.split("/")[3:])

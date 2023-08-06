import os
from google.cloud import error_reporting

from captur_ml_sdk.dtypes.exceptions import SentryDSNNotProvidedError

def get_google_cloud_error_reporting_client() -> error_reporting.Client:
    """Returns a Google Cloud error reporting client

    Returns:
        error_reporting.Client: A Google Cloud error reporting client
    """
    return error_reporting.Client()

def initialise_sentry():
    """Initialises the Sentry client according to the SENTRY_DSN environment variable

    Raises:
        SentryDSNNotProvidedError: If the SENTRY_DSN environment variable is not set
    """
    import sentry_sdk

    if not os.getenv("SENTRY_DSN"):
        raise SentryDSNNotProvidedError("SENTRY_DSN environment variable must be set to use Sentry for error reporting.")

    sentry_sdk.init(traces_sample_rate=1.0)

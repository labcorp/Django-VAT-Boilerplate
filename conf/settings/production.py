# pylint: disable=W0614, W0401
from conf.settings.base import *
from conf.settings.project import *


DEBUG = ENV.bool("DEBUG", False)
PTVSD_SERVER = ENV.bool("PTVSD_SERVER", False)

ALLOWED_HOSTS = ['*', ]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + PROJECT_APPS

USE_SPACES = ENV.bool("USE_SPACES", False)

if USE_SPACES:
    SPACES_ENDPOINT = ENV("SPACES_ENDPOINT")
    SPACES_REGION = ENV("SPACES_REGION")
    SPACES_BUCKET = ENV("SPACES_BUCKET")

    AWS_ACCESS_KEY_ID = ENV("SPACES_KEY")
    AWS_SECRET_ACCESS_KEY = ENV("SPACES_SECRET")
    AWS_S3_ENDPOINT_URL = SPACES_ENDPOINT
    AWS_STORAGE_BUCKET_NAME = SPACES_BUCKET
    AWS_S3_REGION_NAME = SPACES_REGION
    AWS_S3_ADDRESSING_STYLE = "virtual"
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400, s-maxage=86400",
    }

    static_path = ENV("SPACES_STATIC_PATH", default="static").strip("/")
    media_path = ENV("SPACES_MEDIA_PATH", default="media").strip("/")
    static_custom_domain = ENV("SPACES_STATIC_DOMAIN", default="").strip()
    media_custom_domain = ENV("SPACES_MEDIA_DOMAIN", default=static_custom_domain).strip()

    def _domain_to_urls(value: str) -> tuple[str, str]:
        if not value:
            return "", ""
        cleaned = value.rstrip("/")
        if cleaned.startswith("http://") or cleaned.startswith("https://"):
            protocol, domain = cleaned.split("://", 1)
            return f"{protocol}://{domain}", domain
        return f"https://{cleaned}", cleaned

    bucket_base = f"{SPACES_ENDPOINT.rstrip('/')}/{SPACES_BUCKET}"
    static_base_url, static_domain_value = _domain_to_urls(static_custom_domain)
    media_base_url, media_domain_value = _domain_to_urls(media_custom_domain)

    static_base = static_base_url or bucket_base
    media_base = media_base_url or bucket_base

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": media_path,
                "file_overwrite": False,
                "custom_domain": media_domain_value or None,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": static_path,
                "custom_domain": static_domain_value or None,
            },
        },
    }

    STATIC_URL = f"{static_base}/{static_path}/"
    MEDIA_URL = f"{media_base}/{media_path}/"

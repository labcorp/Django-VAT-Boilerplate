from conf.settings.base import ENV


# Feature flags
USE_SPACES = ENV.bool('USE_SPACES', False)
USE_S3 = ENV.bool('USE_S3', False)
# Optional: enable serving staticfiles from remote storage (S3/Spaces)
USE_REMOTE_STATIC = ENV.bool('USE_REMOTE_STATIC', False)
# Optional explicit override: 'spaces' or 's3' (case-insensitive)
STORAGE_PROVIDER = (ENV('STORAGE_PROVIDER', default='') or '').lower()
# Control whether uploaded objects should be made public ('public-read')
STORAGE_PUBLIC = ENV.bool('STORAGE_PUBLIC', False)


def _domain_to_urls(value: str) -> tuple[str, str]:
    """Return (url_with_protocol, domain) or ('','') when empty.

    Accepts values with or without protocol.
    """
    if not value:
        return '', ''
    cleaned = value.rstrip('/')
    if cleaned.startswith('http://') or cleaned.startswith('https://'):
        protocol, domain = cleaned.split('://', 1)
        return f'{protocol}://{domain}', domain
    return f'https://{cleaned}', cleaned


# Decide provider: explicit override > feature flags. If both flags set and no override,
# prefer 'spaces' to preserve previous behavior where Spaces was commonly expected.
provider = None
if STORAGE_PROVIDER in ('spaces', 's3'):
    provider = STORAGE_PROVIDER
elif USE_SPACES and not USE_S3:
    provider = 'spaces'
elif USE_S3 and not USE_SPACES:
    provider = 's3'
elif USE_SPACES and USE_S3:
    provider = 'spaces'


if provider:
    # Common safe defaults
    # Default ACL: None (do not explicitly set ACL). You can enable public ACLs
    # via the STORAGE_PUBLIC flag (documented in env.example.storage).
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400, s-maxage=86400',
    }

    # Read path/domain envs with fallbacks so same names can work for both providers
    static_path = (
        (ENV('SPACES_STATIC_PATH', default=ENV('STATIC_PATH', default='static')) or 'static').strip('/')
    )  # type: ignore
    media_path = (
        (ENV('SPACES_MEDIA_PATH', default=ENV('MEDIA_PATH', default='media')) or 'media').strip("/")
    )  # type: ignore

    # Provider-specific settings
    if provider == 'spaces':
        # DigitalOcean Spaces
        SPACES_ENDPOINT = ENV('SPACES_ENDPOINT')
        SPACES_REGION = ENV('SPACES_REGION', default='')
        SPACES_BUCKET = ENV('SPACES_BUCKET')

        AWS_ACCESS_KEY_ID = ENV('SPACES_KEY')
        AWS_SECRET_ACCESS_KEY = ENV('SPACES_SECRET')
        AWS_S3_ENDPOINT_URL = SPACES_ENDPOINT
        AWS_STORAGE_BUCKET_NAME = SPACES_BUCKET
        AWS_S3_REGION_NAME = SPACES_REGION or None
        AWS_S3_ADDRESSING_STYLE = 'virtual'
        AWS_S3_SIGNATURE_VERSION = 's3v4'

        static_custom_domain = (ENV('SPACES_STATIC_DOMAIN', default='') or '').strip()
        media_custom_domain = (ENV('SPACES_MEDIA_DOMAIN', default='') or static_custom_domain).strip()

        bucket_base = f'{SPACES_ENDPOINT.rstrip("/")}/{SPACES_BUCKET}'  # type: ignore

    else:
        # AWS S3
        AWS_ACCESS_KEY_ID = ENV('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = ENV('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = ENV('AWS_STORAGE_BUCKET')
        AWS_S3_REGION_NAME = ENV('AWS_S3_REGION', default=None)

        # Optional: allow custom endpoint or custom domain for S3-compatible services
        AWS_S3_ENDPOINT_URL = ENV('AWS_S3_ENDPOINT_URL', default='') or None

        static_custom_domain = (ENV('AWS_STATIC_DOMAIN', default=ENV('STATIC_DOMAIN', default='')) or '').strip()
        media_custom_domain = (ENV('AWS_MEDIA_DOMAIN', default=ENV('MEDIA_DOMAIN', default='')) or static_custom_domain).strip()

        # Determine a sensible bucket base for AWS: prefer explicit endpoint, then virtual-hosted
        if AWS_S3_ENDPOINT_URL:
            bucket_base = f'{AWS_S3_ENDPOINT_URL.rstrip("/")}/{AWS_STORAGE_BUCKET_NAME}'
        else:
            # virtual-hosted style (common): https://{bucket}.s3.amazonaws.com
            bucket_base = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Turn custom domains into (url, domain) pairs for media
    media_base_url, media_domain_value = _domain_to_urls(media_custom_domain)
    media_base = media_base_url or bucket_base

    # Configure remote storage for media (default)
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'location': media_path,
                'file_overwrite': False,
                'custom_domain': media_domain_value or None,
            },
        },
    }

    # If STORAGE_PUBLIC is enabled, set ACL to public-read so uploaded objects
    # are readable by everyone. Prefer using a bucket policy for production, but
    # this flag helps in simpler setups (e.g., test Spaces bucket set to public).
    if STORAGE_PUBLIC:
        AWS_DEFAULT_ACL = 'public-read'
        # Also include ACL in object parameters for backends that use it
        AWS_S3_OBJECT_PARAMETERS['ACL'] = 'public-read'

    # Ensure there's always a config for 'staticfiles'. By default static files
    # are served locally using Django's StaticFilesStorage. If USE_REMOTE_STATIC
    # is enabled, override to use the remote S3/Spaces backend.
    STORAGES['staticfiles'] = {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    }

    # Optionally configure staticfiles to use remote storage too
    if USE_REMOTE_STATIC:
        static_base_url, static_domain_value = _domain_to_urls(static_custom_domain)
        static_base = static_base_url or bucket_base
        STORAGES['staticfiles'] = {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
            'OPTIONS': {
                'location': static_path,
                'custom_domain': static_domain_value or None,
            },
        }
        # Override STATIC_URL only when remote static is enabled
        STATIC_URL = f'{static_base}/{static_path}/'

    # MEDIA_URL always points to remote media when provider is enabled
    MEDIA_URL = f'{media_base}/{media_path}/'

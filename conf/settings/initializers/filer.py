THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'storages.backends.s3boto3.S3Boto3Storage',
        },
        'thumbnails': {
            'ENGINE': 'storages.backends.s3boto3.S3Boto3Storage',
        },
    }
}

FILER_CANONICAL_URL = 'public/'

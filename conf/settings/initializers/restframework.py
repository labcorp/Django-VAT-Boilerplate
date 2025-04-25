from datetime import timedelta


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Project\'s API',
    'DESCRIPTION': 'Your awesome project description.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },

    # Available SwaggerUI versions: https://github.com/swagger-api/swagger-ui/releases
    'SWAGGER_UI_DIST': '//unpkg.com/swagger-ui-dist@5.21.0', # default
}

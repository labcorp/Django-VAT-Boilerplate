from django.conf import settings

#TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/lw4ox3emvek1sk7lme65bh160x9wruop4rbky567hnli8wih/tinymce/5/tinymce.min.js'
TINYMCE_FILEBROWSER = False
TINYMCE_DEFAULT_CONFIG = {
    "menubar": False,
    "block_formats": "Paragraph=p; Heading 1=h1; Heading 2=h2; Heading 3=h3; Heading 4=h4; Heading 5=h5; Heading 6=h6;",
    "relative_urls": False,
    "remove_script_host": False,
    "convert_urls": True,
    "width": 900,
    "height": 480,
    "min_height": 480,
    "plugin_preview_width": 700,
    "promotion": False,
    "keep_styles": False,
    "autoresize_bottom_margin": 0,
    "visualblocks_default_state": False,
    "image_advtab": True,
    "image_caption": True,
    "plugins": "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code "
        "fullscreen insertdatetime media table code help wordcount emoticons", # autoresize
    "external_plugins": {
        "POeye": "/static/admin/js/tinymce-content_plugin.js",
    },
    "image_dimensions": False,
    "toolbar": [
        "undo redo | blocks | bold italic underline strikethrough | forecolor backcolor | fontsizeselect formatselect | removeformat visualblocks",
        "alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist checklist | pagebreak | charmap emoticons | "
        "fullscreen  preview code | table image media link anchor | POeye"
    ],
    "link_class_list": [
        {
            "title": 'Default',
            "value": ''
        }, {
            "title": 'Button (primary)',
            "value": 'btn btn-primary'
        }, {
            "title": 'Button (success)',
            "value": 'btn btn-success'
        }, {
            "title": 'Button (info)',
            "value": 'btn btn-info'
        }
    ],
    "content_style": ".eye { float: left; margin-right: 20px; max-width: 250px; background-color: #f5f5f5; border-radius: 4px; padding: 10px; } figure.eye { margin: 0 } .eye span { display: block; } .eye-content { } .eye-caption { font-weight: bold; text-align: left; color: inherit;  }",
    "image_class_list": [
        {
            "title": 'None',
            "value": ''
        },
        {
            "title": 'Olho',
            "value": 'eye-image'
        },
    ],
    "toolbar_mode": "sliding",
    "toolbar_sticky": True,
    "custom_undo_redo_levels": 10,
    "language": "pt_BR",  # To force a specific language instead of the Django current language.
    "images_upload_url": "/tinymce/upload",
    "images_upload_handler": "tinymce_image_upload_handler"
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = settings.DEBUG
TINYMCE_EXTRA_MEDIA = {
    'css': {
        'all': [

        ],
    },
    'js': [
        "https://cdn.jsdelivr.net/npm/js-cookie",
        "admin/js/tinymce-upload.js",
    ],
}

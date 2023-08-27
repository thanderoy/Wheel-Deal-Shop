from .settings import * # noqa

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",    # noqa
    },
}

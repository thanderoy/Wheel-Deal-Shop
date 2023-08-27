import uuid

from django.db import models


class BaseModel(models.Model):
    """Base class for all models."""

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True, editable=False)
    updated = models.DateTimeField(
        auto_now=True, db_index=True, editable=False)

    class Meta:
        """Define a default least recently used ordering."""

        abstract = True
        ordering = ("-updated", "-created")
        indexes = [
            models.Index(fields=['-created']),
        ]

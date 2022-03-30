import uuid


from django.db import models 


class AbstractBaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True



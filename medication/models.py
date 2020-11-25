import os
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
from django_resized import ResizedImageField
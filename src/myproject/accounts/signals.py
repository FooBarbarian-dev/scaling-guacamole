"""Account signals — auto-create related objects on user creation."""
import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, instance, created, **kwargs):
    """Handle post-save for user model."""
    if created:
        logger.info(f"New user created: {instance.username}")

"""Rate limiting configuration."""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonBurstThrottle(AnonRateThrottle):
    rate = "10/min"


class UserBurstThrottle(UserRateThrottle):
    rate = "60/min"


class BurstThrottle(UserRateThrottle):
    scope = "burst"
    rate = "120/min"

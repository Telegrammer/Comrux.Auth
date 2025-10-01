__all__ = ["AccessKeyValidityPolicy"]

from datetime import timedelta
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AccessKeyValidityPolicy:
    ttl: timedelta
    min_freshness_precentage: float


@dataclass(frozen=True, slots=True)
class EmailVerificationPolicy:
    token_ttl: timedelta
    min_freshness_precentage: float

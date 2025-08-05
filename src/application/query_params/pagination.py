from dataclasses import dataclass


__all__ = ["Pagination"]


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination:

    limit: int
    offset: int

    def __post_init__(self):
        if self.limit < 0:
            raise ValueError(
                f"Limit param must be non-negative value, got {self.limit}"
            )
        if self.offset < 0:
            raise ValueError(
                f"Offset param must be non-negative value, got {self.offset}"
            )

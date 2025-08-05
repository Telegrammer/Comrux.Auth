from .sorting import SortingOrder
from .pagination import Pagination
from dataclasses import dataclass

__all__ = ["UserListSorting", "UserListParams"]

@dataclass(frozen=True, slots=True, kw_only=True)
class UserListSorting:
    field_name: str
    sorting_order: SortingOrder


@dataclass(frozen=True, slots=True)
class UserListParams:
    pagination: Pagination
    sorting: UserListSorting

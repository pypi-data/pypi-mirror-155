"""Utility functions."""

from pathlib import Path
from typing import Callable, Iterable, Iterator, TypeVar

__all__ = ["find_index", "iter_child_directories", "without_none_values"]

T = TypeVar("T")


def find_index(predicate: Callable[[T], bool], items: Iterable[T], default=None) -> int:
    """Find the index of the first item satisfying the predicate."""
    return next((i for i, item in enumerate(items) if predicate(item)), default)


def iter_child_directories(directory: Path) -> Iterator[Path]:
    """Iterate over child directories of a directory."""
    for child in directory.iterdir():
        if child.is_dir():
            yield child


def without_none_values(d: dict) -> dict:
    """Return a copy of d without None values."""
    return {k: v for k, v in d.items() if v is not None}

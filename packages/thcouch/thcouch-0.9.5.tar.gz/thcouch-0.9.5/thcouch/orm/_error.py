__all__ = ['CouchError']

from typing import Any
from dataclasses import dataclass


@dataclass
class CouchError:
    error: Any

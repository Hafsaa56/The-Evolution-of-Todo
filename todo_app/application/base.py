"""Base use case interface."""

from abc import ABC
from typing import TypeVar, Generic

Input = TypeVar('Input')
Output = TypeVar('Output')


class UseCase(ABC, Generic[Input, Output]):
    """Base use case interface."""

    async def execute(self, input_data: Input) -> Output:
        """Execute the use case."""
        raise NotImplementedError
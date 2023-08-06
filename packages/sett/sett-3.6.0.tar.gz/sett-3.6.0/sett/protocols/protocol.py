from typing import Sequence, Optional, Callable, Any
from abc import ABC, abstractmethod
from ..utils.progress import ProgressInterface


class Protocol(ABC):
    @abstractmethod
    def upload(
        self,
        files: Sequence[str],
        two_factor_callback: Callable[[], str],
        progress: Optional[ProgressInterface] = None,
    ) -> Any:
        ...

    def required_password_args(self) -> Sequence[str]:
        return ()

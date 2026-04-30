from abc import ABC, abstractmethod

from cv2.typing import MatLike


class BaseClassifier(ABC):
    @abstractmethod
    def pred(self, image: MatLike) -> tuple[str, float]:
        """All subclasses must implement this method."""
        pass

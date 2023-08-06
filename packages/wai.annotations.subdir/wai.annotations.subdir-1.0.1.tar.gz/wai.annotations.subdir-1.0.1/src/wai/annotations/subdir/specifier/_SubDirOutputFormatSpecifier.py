from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class SubDirOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing image classification instances where
    each image is stored in a sub-directory named after the class label.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes images to sub-directories named after their class labels."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import SubDirWriter
        return SubDirWriter,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier

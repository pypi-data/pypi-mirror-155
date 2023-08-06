from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class SubDirInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading image classification instances where
    each image is stored in a sub-directory named after the class label.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads images from sub-directories named after their class labels."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.core.component.util import LocalFilenameSource
        from ..component import SubDirReader
        return LocalFilenameSource, SubDirReader

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier

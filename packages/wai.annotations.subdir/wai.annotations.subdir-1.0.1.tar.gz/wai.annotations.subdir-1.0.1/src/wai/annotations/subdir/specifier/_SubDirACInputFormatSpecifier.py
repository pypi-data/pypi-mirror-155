from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class SubDirACInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading audio classification instances where
    each audio file is stored in a sub-directory named after the class label.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads audio files from sub-directories named after their class labels."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.core.component.util import LocalFilenameSource
        from ..component import SubDirACReader
        return LocalFilenameSource, SubDirACReader

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier
        return AudioClassificationDomainSpecifier

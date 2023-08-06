import os

from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.classification import Classification
from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.classification import AudioClassificationInstance


class SubDirACReader(AnnotationFileProcessor[AudioClassificationInstance]):
    """
    Reader of audio-classification datasets which store images in
    folders named after the classification label.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[AudioClassificationInstance]):
        # The label is the last directory folder of the filename
        label = os.path.basename(os.path.dirname(filename))

        then(
            AudioClassificationInstance(
                Audio.from_file(filename),
                Classification(label)
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[AudioClassificationInstance]):
        then(
            AudioClassificationInstance(
                Audio.from_file(filename),
                None
            )
        )

import os
from wai.annotations.core.component import SourceComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from wai.common.cli.options import TypedOption


class TestIS(SourceComponent[ImageSegmentationInstance]):

    input_dir: str = TypedOption(
        "--dir",
        type=str,
        default=".",
        help="the directory with the jpg files"
    )

    labels: str = TypedOption(
        "--labels",
        type=str,
        default=None,
        nargs="+",
        help="the labels to use"
    )

    def produce(
            self,
            then: ThenFunction[ImageSegmentationInstance],
            done: DoneFunction
    ):
        """
        Produces elements and inserts them into the stream. Should call 'then'
        for each element produced, and then call 'done' when finished.

        :param then:    A function which forwards elements into the stream.
        :param done:    A function which closes the stream when called.
        """
        for f in os.listdir(self.input_dir):
            if not f.lower().endswith(".jpg"):
                continue
            full = os.path.join(self.input_dir, f)
            data = Image.from_file(full)
            then(ImageSegmentationInstance(data, ImageSegmentationAnnotation(list(self.labels), (data.width, data.height))))
        done()

import os
from wai.annotations.core.component import SourceComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.common.cli.options import TypedOption
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject


class TestOD(SourceComponent[ImageObjectDetectionInstance]):

    input_dir: str = TypedOption(
        "--dir",
        type=str,
        default=".",
        help="the directory with the jpg files"
    )

    def produce(
            self,
            then: ThenFunction[ImageObjectDetectionInstance],
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
            label = os.path.splitext(f)[0]
            lobj = LocatedObject(0, 0, data.width - 1, data.height - 1)
            lobj.metadata["type"] = label
            lobjs = LocatedObjects([lobj])
            then(ImageObjectDetectionInstance(data, lobjs))
        done()

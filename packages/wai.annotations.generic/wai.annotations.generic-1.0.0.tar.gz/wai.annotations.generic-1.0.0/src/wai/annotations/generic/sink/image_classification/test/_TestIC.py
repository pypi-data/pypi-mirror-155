from wai.common.cli.options import TypedOption
from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.image.classification import ImageClassificationInstance

OUTPUT_FILENAME = "filename"
OUTPUT_DIMENSIONS = "dimensions"
OUTPUT_LABEL = "label"
OUTPUTS = [
    OUTPUT_FILENAME,
    OUTPUT_DIMENSIONS,
    OUTPUT_LABEL,
]


class TestIC(SinkComponent[ImageClassificationInstance]):

    output: str = TypedOption(
        "--output",
        type=str,
        default=OUTPUT_FILENAME,
        help="the information to output: %s" % "|".join(OUTPUTS)
    )

    def consume_element(self, element: ImageClassificationInstance):
        """
        Consumes instances.
        """
        if self.output == OUTPUT_FILENAME:
            self.logger.info(element.data.filename)
        elif self.output == OUTPUT_DIMENSIONS:
            self.logger.info("%d,%d" % (element.data.width, element.data.height))
        elif self.output == OUTPUT_LABEL:
            self.logger.info(element.annotations.label)
        else:
            raise Exception("Unknown output type (%s): %s" % ("|".join(OUTPUTS), self.output))

    def finish(self):
        self.logger.info("finished")

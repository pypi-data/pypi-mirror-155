from wai.common.cli.options import TypedOption
from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.audio.speech import SpeechInstance

OUTPUT_FILENAME = "filename"
OUTPUT_TRANSCRIPT = "transcript"
OUTPUTS = [
    OUTPUT_FILENAME,
    OUTPUT_TRANSCRIPT,
]


class TestSP(SinkComponent[SpeechInstance]):

    output: str = TypedOption(
        "--output",
        type=str,
        default=OUTPUT_FILENAME,
        help="the information to output: %s" % "|".join(OUTPUTS)
    )

    def consume_element(self, element: SpeechInstance):
        """
        Consumes instances.
        """
        if self.output == OUTPUT_FILENAME:
            self.logger.info(element.data.filename)
        elif self.output == OUTPUT_TRANSCRIPT:
            self.logger.info(element.annotations.text)
        else:
            raise Exception("Unknown output type (%s): %s" % ("|".join(OUTPUTS), self.output))

    def finish(self):
        self.logger.info("finished")

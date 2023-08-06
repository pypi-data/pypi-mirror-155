from wai.common.cli.options import TypedOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.audio.classification import AudioClassificationInstance

OUTPUT_FILENAME = "filename"
OUTPUT_LABEL = "label"
OUTPUTS = [
    OUTPUT_FILENAME,
    OUTPUT_LABEL,
]


class TestAC(
    RequiresNoFinalisation,
    ProcessorComponent[AudioClassificationInstance, AudioClassificationInstance]
):

    output: str = TypedOption(
        "--output",
        type=str,
        default=OUTPUT_FILENAME,
        help="the information to output: %s" % "|".join(OUTPUTS)
    )

    def process_element(
            self,
            element: AudioClassificationInstance,
            then: ThenFunction[AudioClassificationInstance],
            done: DoneFunction
    ):
        if self.output == OUTPUT_FILENAME:
            self.logger.info(element.data.filename)
        elif self.output == OUTPUT_LABEL:
            self.logger.info(element.annotations.label)
        else:
            raise Exception("Unknown output type (%s): %s" % ("|".join(OUTPUTS), self.output))
        then(element)

import os
from wai.annotations.core.component import SourceComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.speech import SpeechInstance, Transcription
from wai.common.cli.options import TypedOption


class TestSP(SourceComponent[SpeechInstance]):

    input_dir: str = TypedOption(
        "--dir",
        type=str,
        default=".",
        help="the directory with the wav files"
    )

    def produce(
            self,
            then: ThenFunction[SpeechInstance],
            done: DoneFunction
    ):
        """
        Produces elements and inserts them into the stream. Should call 'then'
        for each element produced, and then call 'done' when finished.

        :param then:    A function which forwards elements into the stream.
        :param done:    A function which closes the stream when called.
        """
        for f in os.listdir(self.input_dir):
            if not f.lower().endswith(".wav"):
                continue
            transcript = os.path.splitext(f)[0]
            full = os.path.join(self.input_dir, f)
            data = Audio.from_file(full)
            then(SpeechInstance(data, Transcription(transcript)))
        done()

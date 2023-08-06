import os
import csv
from wai.annotations.core.component import SourceComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.classification import AudioClassificationInstance
from wai.annotations.domain.classification import Classification
from wai.common.cli.options import TypedOption


class Urban8k(SourceComponent[AudioClassificationInstance]):

    metadata_csv: str = TypedOption(
        "--metadata-csv",
        type=str,
        help="the CSV file with the meta-data information"
    )

    folds_dir: str = TypedOption(
        "--fold-dir",
        type=str,
        help="the directory with the folds"
    )

    def produce(
            self,
            then: ThenFunction[AudioClassificationInstance],
            done: DoneFunction
    ):
        """
        Produces elements and inserts them into the stream. Should call 'then'
        for each element produced, and then call 'done' when finished.

        :param then:    A function which forwards elements into the stream.
        :param done:    A function which closes the stream when called.
        """
        with open(self.metadata_csv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                full = os.path.join(self.folds_dir, "fold" + row["fold"], row["slice_file_name"])
                if os.path.exists(full):
                    label = row["class"]
                    data = Audio.from_file(full)
                    then(AudioClassificationInstance(data, Classification(label)))
                else:
                    self.logger.error("Failed to located WAV file: %s" % full)
        done()

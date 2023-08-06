import csv
import json

import sys
from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.audio import AudioInstance
from wai.annotations.domain.audio.classification import AudioClassificationInstance
from wai.annotations.domain.audio.speech import SpeechInstance
from wai.common.cli.options import TypedOption

OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_CSV = "csv"
OUTPUT_FORMAT_JSON = "json"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_JSON,
]


class AudioInfo(SinkComponent[AudioInstance]):

    output_format: str = TypedOption(
        "-f", "--format",
        type=str,
        default=OUTPUT_FORMAT_TEXT,
        help="the format to use for the output, available modes: %s" % ", ".join(OUTPUT_FORMATS)
    )

    output_file: str = TypedOption(
        "-o", "--output",
        type=str,
        default="",
        help="the file to write the information to; uses stdout if omitted"
    )

    def init_info(self):
        """
        Initializes the information.
        """
        if not hasattr(self, "_data"):
            self._data = []
            self._additional_label = None

    def append_info(self, file_name, file_size, sample_rate, is_mono, duration, additional):
        """
        Appends the information.

        :param file_name: the file name
        :param file_size: the file size (length of data)
        :param sample_rate: the sample rate
        :param is_mono: whether the data is mono
        :param duration: the duration in seconds
        :param additional: the additional data
        """
        self.init_info()
        self._data.append([file_name, file_size, sample_rate, is_mono, duration, additional])

    def output_text(self, use_stdout, additional_label):
        """
        Outputs the information in simple textual format.

        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        :param additional_label: the label to use for the additional data
        :type additional_label: str
        """
        info = []
        for row in self._data:
            info.append("%s\n  - file_size: %d\n  - sample_rate: %d\n  - mono: %s\n  - duration (sec): %f\n  - %s: %s"
                        % (row[0], row[1], row[2], str(row[3]), row[4], additional_label, str(row[5])))

        if use_stdout:
            print("\n".join(info))
        else:
            with open(self.output_file, "w") as fp:
                fp.write("\n".join(info))

    def output_csv(self, use_stdout, additional_label):
        """
        Outputs the information in CSV format.

        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        :param additional_label: the label to use for the additional data
        :type additional_label: str
        """
        if use_stdout:
            writer = csv.writer(sys.stdout)
            f = None
        else:
            f = open(self.output_file, "w")
            writer = csv.writer(f)

        writer.writerow(["file_name", "file_size", "sample_rate", "mono", "duration_seconds", additional_label])
        for row in self._data:
            writer.writerow(row)

        if f is not None:
            f.close()

    def output_json(self, use_stdout, additional_label):
        """
        Outputs the information in json format.

        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        :param additional_label: the label to use for the additional data
        :type additional_label: str
        """
        data = []
        for row in self._data:
            file_data = {
                "file_name": row[0],
                "file_size": row[1],
                "sample_rate": row[2],
                "mono": row[3],
                "duration_seconds": row[4],
                additional_label: row[5],
            }
            data.append(file_data)

        if use_stdout:
            print(json.dumps(data, indent=2))
        else:
            with open(self.output_file, "w") as f:
                json.dump(data, f, indent=2)

    def output_info(self):
        """
        Outputs the information.
        """
        additional_label = "additional"
        if hasattr(self, "_additional_label") and (self._additional_label is not None):
            additional_label = self._additional_label
        use_stdout = len(self.output_file) == 0

        if self.output_format == OUTPUT_FORMAT_TEXT:
            self.output_text(use_stdout, additional_label)
        elif self.output_format == OUTPUT_FORMAT_CSV:
            self.output_csv(use_stdout, additional_label)
        elif self.output_format == OUTPUT_FORMAT_JSON:
            self.output_json(use_stdout, additional_label)
        else:
            raise Exception("Unhandled output format: %s" % self.output_format)

    def consume_element(self, element: AudioInstance):
        """
        Consumes instances by discarding them.
        """
        if isinstance(element, AudioClassificationInstance):
            self.append_info(
                element.data.filename,
                len(element.data.data),
                element.data.audio_data[1],
                len(element.data.audio_data[0].shape) == 1,
                element.data.get_duration(),
                element.annotations.label)
            if self._additional_label is None:
                self._additional_label = "label"
        elif isinstance(element, SpeechInstance):
            self.append_info(
                element.data.filename,
                len(element.data.data),
                element.data.audio_data[1],
                len(element.data.audio_data[0].shape) == 1,
                element.data.get_duration(),
                element.annotations.transcript)
            if self._additional_label is None:
                self._additional_label = "transcript"

    def finish(self):
        self.init_info()
        self.output_info()

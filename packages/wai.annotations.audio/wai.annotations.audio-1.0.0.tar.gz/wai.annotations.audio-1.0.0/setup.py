from setuptools import setup, find_namespace_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations.audio",
    description="Module with audio plugins for wai.annotations.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-datamining/wai-annotations-audio",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai",
        "wai.annotations"
    ],
    version="1.0.0",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    install_requires=[
        "wai.annotations.core>=0.1.8",
        "librosa",
        "soundfile",
    ],
    entry_points={
        "wai.annotations.plugins": [
            # Sources
            # ISPs
            "convert-to-mono=wai.annotations.audio.isp.convert_to_mono.specifier:ConvertToMonoISPSpecifier",
            "convert-to-wav=wai.annotations.audio.isp.convert_to_wav.specifier:ConvertToWavISPSpecifier",
            "pitch-shift=wai.annotations.audio.isp.pitch_shift.specifier:PitchShiftISPSpecifier",
            "resample-audio=wai.annotations.audio.isp.resample.specifier:ResampleAudioISPSpecifier",
            "trim-audio=wai.annotations.audio.isp.trim.specifier:TrimAudioISPSpecifier",
            "time-stretch=wai.annotations.audio.isp.time_stretch.specifier:TimeStretchISPSpecifier",
            # XDCs
            "mel-spectrogram=wai.annotations.audio.xdc.mel_spectrogram.specifier:MelSpectrogramISPSpecifier",
            "stft-spectrogram=wai.annotations.audio.xdc.stft_spectrogram.specifier:STFTSpectrogramISPSpecifier",
            # Sinks
            "audio-info-ac=wai.annotations.audio.format.audio_info.specifier:AudioInfoACOutputFormatSpecifier",
            "audio-info-sp=wai.annotations.audio.format.audio_info.specifier:AudioInfoSPOutputFormatSpecifier",
        ]
    }
)

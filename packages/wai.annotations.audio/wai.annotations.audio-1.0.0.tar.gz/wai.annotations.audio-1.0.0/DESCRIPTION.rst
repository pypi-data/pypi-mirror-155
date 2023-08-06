Audio processing plugins for wai.annotations:

* `audio-info-ac`: sink for collating/outputting information on the audio classification files
* `audio-info-sp`: sink for collating/outputting information on the speech files
* `convert-to-mono`: ISP for converting MP3/OGG/FLAC/WAV to mono WAV
* `convert-to-wav`: ISP for converting MP3/OGG/FLAC to WAV
* `mel-spectrogram`: XDC for generating plot from a mel spectrogram (outputs image classification instance)
* `pitch-shift`: augmentation ISP for shifting the pitch
* `resample-audio`: ISP for resampling MP3/OGG/FLAC/WAV
* `stft-spectrogram`: XDC for generating plot from a short-time fourier-transform spectrogram (outputs image classification instance)
* `time-stretch`: augmentation ISP for time-stretching audio (speed up/slow down)
* `trim-audio`: ISP for trimming silence from audio

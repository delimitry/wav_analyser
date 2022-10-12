import argparse
import struct
import wave

from PIL import Image
from fft import fft, fft_freqs


def build_spectrogram(
    filename: str,
    chunk_size: int = 512,
    min_freq: int = 20,
    max_freq: int = 4000,
    spectrogram_filename: str = 'spectrogram.png'
) -> None:
    """Builds spectrogram from wav file and saves to spectrogram image."""
    with wave.open(filename, 'r') as in_file:
        (channels_num, _, framerate, frames_num, _, _) = in_file.getparams()
        packed_frames = in_file.readframes(frames_num * channels_num)
        frames = struct.unpack_from(f'{frames_num * channels_num}H', packed_frames)
        if channels_num == 2:
            left = frames[:len(frames):2]
            # right = frames[1:len(frames):2]
        else:
            left = frames
            # right = left
        img = Image.new('RGB', (len(left) // chunk_size, 250))
        pixels = img.load()
        for i in range(len(left) // chunk_size):
            ffts = fft(frames[i * chunk_size: i * chunk_size + chunk_size])
            freqs = fft_freqs(chunk_size, framerate)
            fft_frequencies = [abs(round(x)) for x in freqs if min_freq <= x <= max_freq]
            ffts = [round(abs(x.real)) for x in ffts]
            max_value = max(ffts)
            min_value = min(ffts)
            delta = max_value - min_value
            for freq, value in zip(fft_frequencies, ffts):
                if freq > min_freq:
                    color = int(value / delta * 512) if value else 0
                    pixels[i, img.size[1] - 1 - img.size[1] * freq // max_freq] = (color, 0, color)
        img.save(spectrogram_filename)


def main():
    """Main"""
    parser = argparse.ArgumentParser(description='Wav file analyser')
    parser.add_argument('filename', type=str, help='Wav file')
    parser.add_argument('-o', '--output_spectrogram', type=str, default='spectrogram.png', help='Output spectrogram file')

    args = parser.parse_args()
    build_spectrogram(args.filename, spectrogram_filename=args.output_spectrogram)


if __name__ == '__main__':
    main()

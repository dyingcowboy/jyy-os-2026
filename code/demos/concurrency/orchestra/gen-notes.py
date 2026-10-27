#!/usr/bin/env python3
# Author: claude-3.7-sonnet
#
# 合成 orchestra demo 需要的 84 个音符（C1–B7）。
#
# 原版依赖 numpy；为了 `make` 在干净环境里也能跑，这里改成只用标准库
# （math / wave / struct）。音色算法和原来一致：基频 + 2..5 次谐波，
# 再乘一个「快速起音 - 衰减到持续 - 淡出」的包络。

import math
import os
import struct
import wave

SAMPLE_RATE = 44100
DURATION = 1.0
AMPLITUDE = 0.5
HARMONICS = 5


def generate_piano_note(frequency, duration=DURATION, sample_rate=SAMPLE_RATE,
                        amplitude=AMPLITUDE):
    """合成一个类似钢琴的波形，返回 -1..1 之间的浮点列表。"""
    num_samples = int(duration * sample_rate)
    two_pi = 2.0 * math.pi

    # 基频 + 逐次减弱的高次谐波
    waveform = [0.0] * num_samples
    for i in range(num_samples):
        t = i / sample_rate
        v = math.sin(two_pi * frequency * t)
        for h in range(2, HARMONICS + 1):
            v += (1.0 / h) * math.sin(two_pi * frequency * h * t)
        waveform[i] = v

    # 包络：10ms 起音，100ms 衰减到 0.7，最后 300ms 淡出
    attack_samples = int(0.01 * sample_rate)
    decay_samples = int(0.1 * sample_rate)
    release_samples = int(0.3 * sample_rate)
    sustain_level = 0.7

    for i in range(attack_samples):
        waveform[i] *= i / attack_samples

    for i in range(decay_samples):
        waveform[attack_samples + i] *= (
            1.0 + (sustain_level - 1.0) * i / decay_samples
        )

    release_start = num_samples - release_samples
    start_level = waveform[release_start - 1] if release_start > 0 else 0.0
    for i in range(release_samples):
        waveform[release_start + i] *= start_level * (1.0 - i / release_samples)

    # 归一化到指定响度
    peak = max(abs(v) for v in waveform) or 1.0
    return [v / peak * amplitude for v in waveform]


def save_wave_file(filename, waveform, sample_rate=SAMPLE_RATE):
    """把波形写成 16-bit 单声道 WAV。"""
    frames = bytearray()
    for v in waveform:
        sample = int(max(-1.0, min(1.0, v)) * 32767)
        frames += struct.pack('<h', sample)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(bytes(frames))


def abc_to_frequency(note):
    """把 ABC 记谱的音名（如 C4、A#3、Bb5）换算成频率（Hz）。"""
    notes = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    if len(note) < 2:
        raise ValueError(f"Invalid note format: {note}")

    base_note = note[0].upper()
    offset = 0
    idx = 1
    if idx < len(note) and note[idx] in '#b':
        offset = 1 if note[idx] == '#' else -1
        idx += 1

    octave = int(note[idx:])
    semitones_from_a4 = (octave - 4) * 12 + notes[base_note] + offset - 9
    return 440.0 * (2.0 ** (semitones_from_a4 / 12.0))


def main():
    os.makedirs('notes', exist_ok=True)

    notes = []
    for octave in range(1, 8):
        for note in ['C', 'C#', 'D', 'D#', 'E', 'F',
                     'F#', 'G', 'G#', 'A', 'A#', 'B']:
            notes.append(f"{note}{octave}")

    for note in notes:
        try:
            frequency = abc_to_frequency(note)
            waveform = generate_piano_note(frequency)
            filename = os.path.join('notes', f"{note}.wav")
            save_wave_file(filename, waveform)
            print(f"Generated {filename}")
        except Exception as e:
            print(f"Error generating {note}: {e}")


if __name__ == "__main__":
    main()

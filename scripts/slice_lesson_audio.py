#!/usr/bin/env python3
"""
Slice authentic Friends audio tailored specifically for English Teaching Micro-Lessons.
Uses source audio and precise timestamps from ai_practice.
"""

import os
import subprocess
import tempfile
from pathlib import Path

SRC_AUDIO = "/Users/mayantao/Documents/python-playground/ai_practice/inputs/friends/s1/e01/audio.mp3"
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "media" / "audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def cut_clip(start_sec: float, end_sec: float, output_path: Path):
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{start_sec:.3f}",
        "-to", f"{end_sec:.3f}",
        "-i", SRC_AUDIO,
        "-ar", "44100",
        "-ab", "128k",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
    print(f"  ✓ 生成音频: {output_path.name} ({start_sec:.2f}s -> {end_sec:.2f}s)")

def concat_clips(clips: list[Path], output_path: Path, pause_sec: float = 0.25):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        silence_path = tmp_dir / "silence.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(pause_sec),
            str(silence_path)
        ], check=True)

        inputs = []
        filter_inputs = []
        idx = 0
        for i, clip in enumerate(clips):
            inputs.extend(["-i", str(clip)])
            filter_inputs.append(f"[{idx}:a]")
            idx += 1
            if i < len(clips) - 1:
                inputs.extend(["-i", str(silence_path)])
                filter_inputs.append(f"[{idx}:a]")
                idx += 1

        filter_str = f"{''.join(filter_inputs)}concat=n={len(filter_inputs)}:v=0:a=1[out]"
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            *inputs,
            "-filter_complex", filter_str,
            "-map", "[out]",
            "-ar", "44100",
            "-ab", "128k",
            str(output_path)
        ]
        subprocess.run(cmd, check=True)
        print(f"  ✓ 拼接生成音频: {output_path.name}")

def main():
    if not os.path.exists(SRC_AUDIO):
        print(f"❌ 找不到原始音频文件: {SRC_AUDIO}")
        return

    print("🎙️ 正在为 Lesson 01~03 精准裁切专属微课音频...")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)

        # ==========================================
        # Lesson 01: Monica & Joey & Chandler
        # ==========================================
        print("\n--- Lesson 01 ---")
        # 微场景音频: Monica (00-01) + Joey (02-03) + Chandler (11)
        part_monica_joey = tmp_dir / "l01_mj.mp3"
        part_chandler = tmp_dir / "l01_ch.mp3"
        cut_clip(49.750, 57.400, part_monica_joey)
        cut_clip(74.600, 76.600, part_chandler)
        concat_clips([part_monica_joey, part_chandler], OUTPUT_DIR / "s01e01_scene_01.mp3", pause_sec=0.25)

        # 核心单句: "He's just some guy I work with!" (Monica line 01)
        cut_clip(51.100, 53.150, OUTPUT_DIR / "s01e01_chunk_01.mp3")

        # ==========================================
        # Lesson 02: Rachel Phone Call Metaphor
        # ==========================================
        print("\n--- Lesson 02 ---")
        # 微场景音频: Rachel 连续打电话 (line 100 -> line 109, 含 "It's a metaphor, Daddy!")
        cut_clip(355.000, 378.850, OUTPUT_DIR / "s01e01_scene_02.mp3")

        # 核心单句: "And today I just stopped and I said, 'What if I don't wanna be a shoe?'"
        cut_clip(364.300, 367.850, OUTPUT_DIR / "s01e01_chunk_02.mp3")

        # ==========================================
        # Lesson 03: Joey Ice Cream & Grab a Spoon
        # ==========================================
        print("\n--- Lesson 03 ---")
        # 微场景音频: Joey 冰淇淋论至 Chandler 吐槽 (line 209 -> line 216)
        cut_clip(697.350, 728.050, OUTPUT_DIR / "s01e01_scene_07.mp3")

        # 核心单句 1: Joey "Welcome back to the world! Grab a spoon!" (line 214)
        cut_clip(718.650, 722.500, OUTPUT_DIR / "s01e01_chunk_03_spoon.mp3")

        # 核心单句 2: Ross "I honestly don't know if I'm hungry or horny." (line 215)
        cut_clip(722.750, 726.150, OUTPUT_DIR / "s01e01_chunk_03_hungry.mp3")

    print("\n🎉 音频精准生成完毕！全部存放至: media/audio/")

if __name__ == "__main__":
    main()

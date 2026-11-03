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
        part_monica_joey = tmp_dir / "l01_mj.mp3"
        part_chandler = tmp_dir / "l01_ch.mp3"
        cut_clip(49.750, 57.400, part_monica_joey)
        cut_clip(74.600, 76.600, part_chandler)
        concat_clips([part_monica_joey, part_chandler], OUTPUT_DIR / "s01e01_scene_01.mp3", pause_sec=0.25)
        cut_clip(51.100, 53.150, OUTPUT_DIR / "s01e01_chunk_01.mp3")

        # ==========================================
        # Lesson 02: Rachel Phone Call Metaphor
        # ==========================================
        print("\n--- Lesson 02 ---")
        cut_clip(355.000, 378.850, OUTPUT_DIR / "s01e01_scene_02.mp3")
        cut_clip(364.300, 367.850, OUTPUT_DIR / "s01e01_chunk_02.mp3")

        # ==========================================
        # Lesson 03: Joey Ice Cream & Grab a Spoon
        # ==========================================
        print("\n--- Lesson 03 ---")
        cut_clip(697.350, 728.050, OUTPUT_DIR / "s01e01_scene_07.mp3")
        cut_clip(718.650, 722.500, OUTPUT_DIR / "s01e01_chunk_03_spoon.mp3")
        cut_clip(722.750, 726.150, OUTPUT_DIR / "s01e01_chunk_03_hungry.mp3")

        # ==========================================
        # Lesson 04: Ross Enters & Intestines Monologue
        # ==========================================
        print("\n--- Lesson 04 ---")
        cut_clip(116.000, 131.000, OUTPUT_DIR / "s01e01_scene_04.mp3")
        cut_clip(118.800, 122.000, OUTPUT_DIR / "s01e01_chunk_04_kill.mp3")
        cut_clip(123.500, 130.300, OUTPUT_DIR / "s01e01_chunk_04_throat.mp3")

        # ==========================================
        # Lesson 05: Rachel Aruba & Ross Furniture
        # ==========================================
        print("\n--- Lesson 05 ---")
        cut_clip(522.500, 554.000, OUTPUT_DIR / "s01e01_scene_05.mp3")
        cut_clip(525.200, 531.200, OUTPUT_DIR / "s01e01_chunk_05_aruba.mp3")
        cut_clip(547.800, 554.000, OUTPUT_DIR / "s01e01_chunk_05_alone.mp3")

        # ==========================================
        # Lesson 06: Monica & Paul Restaurant
        # ==========================================
        print("\n--- Lesson 06 ---")
        cut_clip(636.500, 653.200, OUTPUT_DIR / "s01e01_scene_06.mp3")
        cut_clip(638.800, 641.000, OUTPUT_DIR / "s01e01_chunk_06_through.mp3")
        cut_clip(640.800, 645.000, OUTPUT_DIR / "s01e01_chunk_06_breaking.mp3")

        # ==========================================
        # Lesson 07: Frannie Line & Monica Beacon
        # ==========================================
        print("\n--- Lesson 07 ---")
        cut_clip(1051.000, 1072.000, OUTPUT_DIR / "s01e01_scene_07_beacon.mp3")
        cut_clip(1051.200, 1053.800, OUTPUT_DIR / "s01e01_chunk_07_line.mp3")
        cut_clip(1064.800, 1072.000, OUTPUT_DIR / "s01e01_chunk_07_beacon.mp3")

        # ==========================================
        # Lesson 08: Live Off Parents & Welcome to Real World
        # ==========================================
        print("\n--- Lesson 08 ---")
        part_liveoff = tmp_dir / "l08_lo.mp3"
        part_realworld = tmp_dir / "l08_rw.mp3"
        cut_clip(1128.500, 1139.000, part_liveoff)
        cut_clip(1185.200, 1191.000, part_realworld)
        concat_clips([part_liveoff, part_realworld], OUTPUT_DIR / "s01e01_scene_08.mp3", pause_sec=0.3)
        cut_clip(1128.800, 1131.200, OUTPUT_DIR / "s01e01_chunk_08_liveoff.mp3")
        cut_clip(1185.500, 1190.500, OUTPUT_DIR / "s01e01_chunk_08_realworld.mp3")

        # ==========================================
        # Lesson 09: Ross Asks Rachel Out Sometime
        # ==========================================
        print("\n--- Lesson 09 ---")
        cut_clip(1265.000, 1283.000, OUTPUT_DIR / "s01e01_scene_09.mp3")
        cut_clip(1272.800, 1277.200, OUTPUT_DIR / "s01e01_chunk_09_asked.mp3")
        cut_clip(1278.000, 1281.800, OUTPUT_DIR / "s01e01_chunk_09_maybe.mp3")

        # ==========================================
        # Lesson 10: Chandler & Rachel Serving Coffee
        # ==========================================
        print("\n--- Lesson 10 ---")
        cut_clip(1346.000, 1353.000, OUTPUT_DIR / "s01e01_scene_10.mp3")
        cut_clip(1346.500, 1349.500, OUTPUT_DIR / "s01e01_chunk_10_make.mp3")
        cut_clip(1350.500, 1353.000, OUTPUT_DIR / "s01e01_chunk_10_order.mp3")

    print("\n🎉 音频精准生成完毕！全部存放至: media/audio/")

if __name__ == "__main__":
    main()


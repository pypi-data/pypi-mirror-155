from pathlib import Path

import moviepy.editor as mp

from terminhtml_recorder.logger import log


def convert_video_to_gif(in_path: Path, out_path: Path, delay: float = 1.1) -> None:
    clip = mp.VideoFileClip(str(in_path.resolve()))
    # Remove first portion of clip before terminhtml-js loads
    clip = clip.subclip(delay, clip.duration).resize(0.7)
    clip.write_gif(str(out_path.resolve()), program="ffmpeg", fps=10)
    log.info(f"Demo output gif saved to {out_path}")

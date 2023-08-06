from pathlib import Path

import moviepy.editor as mp

from terminhtml_recorder.logger import log


def convert_video_to_gif(clip: mp.VideoFileClip, out_path: Path, fps: int = 10) -> None:
    clip.write_gif(str(out_path.resolve()), program="ffmpeg", fps=fps)
    log.info(f"Demo output gif saved to {out_path}")

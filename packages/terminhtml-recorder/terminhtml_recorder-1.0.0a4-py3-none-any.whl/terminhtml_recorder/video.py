from dataclasses import dataclass
from pathlib import Path

import moviepy.editor as mp


@dataclass
class Video:
    path: Path
    clip: mp.VideoFileClip

    @classmethod
    def from_path(cls, path: Path) -> "Video":
        return cls(path=path, clip=mp.VideoFileClip(str(path.resolve())))

    def transform_clip(self, begin_after: float, scale: float) -> mp.VideoFileClip:
        return self.clip.subclip(begin_after, self.clip.duration).resize(scale)

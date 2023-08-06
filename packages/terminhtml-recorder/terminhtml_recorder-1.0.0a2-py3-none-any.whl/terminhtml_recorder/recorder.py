import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Union

from playwright.sync_api import Locator, Page, sync_playwright

from terminhtml_recorder.converter import convert_video_to_gif
from terminhtml_recorder.formats import OutputFormat
from terminhtml_recorder.logger import log
from terminhtml_recorder.temp_path import create_temp_path


@dataclass
class Recording:
    path: Path
    format: OutputFormat

    def convert_to(
        self, new_format: OutputFormat, out_path: Path, delay: float = 1.1
    ) -> "Recording":
        if new_format == self.format:
            shutil.copy(self.path, out_path)
            # TODO: need to trim for delay in webm output
            return Recording(path=out_path, format=new_format)
        elif new_format == OutputFormat.GIF:
            convert_video_to_gif(self.path, out_path, delay=delay)
            return Recording(path=out_path, format=new_format)
        raise NotImplementedError(
            f"Conversion from {self.format} to {new_format} not implemented"
        )


@dataclass
class PageLocators:
    speed_up: Locator
    speed_down: Locator
    restart: Locator

    @classmethod
    def from_page(cls, page: Page) -> "PageLocators":
        return cls(
            speed_up=page.locator("text=►"),
            speed_down=page.locator("text=◄"),
            restart=page.locator("text=restart ↻"),
        )


PageInteractor = Callable[[PageLocators], None]


def default_page_interactor(page_locators: PageLocators) -> None:
    page_locators.restart.wait_for()


class TerminHTMLRecorder:
    def __init__(self, html: str, interactor: PageInteractor = default_page_interactor):
        self.html = html
        self.interactor = interactor

    def record(
        self,
        out_path: Union[str, Path],
        format: OutputFormat = OutputFormat.GIF,
        delay: float = 1.1,
    ) -> Recording:
        with create_temp_path() as temp_path:
            log.info(f"Creating recording in {temp_path}")
            html_path = temp_path / "termin.html"
            html_path.write_text(self.html)

            with sync_playwright() as p:
                browser = p.chromium.launch()
                dimensions = dict(width=800, height=530)
                context = browser.new_context(
                    viewport=dimensions,
                    record_video_dir=str(temp_path.resolve()),
                    record_video_size=dimensions,
                )
                page = context.new_page()
                page.goto(html_path.as_uri())
                locators = PageLocators.from_page(page)
                self.interactor(locators)
                context.close()
                browser.close()

            for video in temp_path.glob("*.webm"):
                return Recording(
                    path=video,
                    format=OutputFormat.WEBM,
                ).convert_to(format, Path(out_path), delay=delay)

            raise ValueError(f"No video found in temp_path {temp_path}")

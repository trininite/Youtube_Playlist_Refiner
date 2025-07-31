from dataclasses import dataclass, field
import uuid


@dataclass
class SongInfo:
    url: str
    title: str
    channel: str
    local_id: str = field(default_factory=lambda: uuid.uuid4) #uuid4 generates a totally random UUID
    playlist_id: str # all videos have an id in a playlist on youtubes end
    index: int
    export_file_name: str


    @property
    def youtube_id(self) -> str:
        # example link
        # https://www.youtube.com/watch?v=3Ix4cz2ydWA

        return self.url.split("=")


    @property
    def file_name(self) -> str:
        return f"{self.local_id}.mp3"

from dataclasses import dataclass, field, asdict
import uuid



@dataclass
class SongInfo:
    url: str
    title: str
    channel: str
    playlist_id: str # all videos have an id in a playlist on youtubes end
    index: int
    export_file_name: str
    local_id: uuid.UUID = field(default_factory=uuid.uuid4) #uuid4 generates a totally random UUID


    def __post_init__(self):
        if isinstance(self.local_id, str):
            # allow only 32 hex digit strings (no hyphens)
            if len(self.local_id) == 32:
                self.local_id = uuid.UUID(hex=self.local_id)
            else:
                raise ValueError("local_id string must be 32 hexadecimal digits")


    @property
    def youtube_id(self) -> str:
        # example link
        # https://www.youtube.com/watch?v=3Ix4cz2ydWA

        return self.url.split("=")


    @property
    def file_name(self) -> str:
        return f"{self.local_id}.mp3"

    @property
    def as_dict(self):
        return asdict(self)


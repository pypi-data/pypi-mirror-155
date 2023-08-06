from typing import Optional
from enum import auto

from pydantic import BaseModel

from .utils import AutoName


class MediaType(AutoName):
    animation = auto()
    audio = auto()
    document = auto()
    photo = auto()
    video = auto()
    video_note = auto()
    voice = auto()


class PollType(AutoName):
    quiz = auto()
    regular = auto()


class AnimationAttributes(BaseModel):
    thumb: Optional[str] = None
    duration: Optional[int] = 0
    width: Optional[int] = 0
    height: Optional[int] = 0
    file_name: Optional[str] = None
    unsave: Optional[bool] = False


class AudioAttributes(BaseModel):
    thumb: Optional[str] = None
    duration: Optional[int] = 0
    title: Optional[str] = None
    performer: Optional[str] = None
    file_name: Optional[str] = None


class DocumentAttributes(BaseModel):
    thumb: Optional[str] = None
    file_name: Optional[str] = None
    force_document: Optional[bool] = None


class PhotoAttributes(BaseModel):
    pass


class VideoAttributes(BaseModel):
    thumb: Optional[str] = None
    duration: Optional[int] = 0
    width: Optional[int] = 0
    height: Optional[int] = 0
    file_name: Optional[str] = None
    supports_streaming: Optional[bool] = True


class VideoNoteAttributes(BaseModel):
    thumb: Optional[str] = None
    duration: Optional[int] = 0
    length: Optional[int] = 1


class VoiceAttributes(BaseModel):
    duration: Optional[int] = 0

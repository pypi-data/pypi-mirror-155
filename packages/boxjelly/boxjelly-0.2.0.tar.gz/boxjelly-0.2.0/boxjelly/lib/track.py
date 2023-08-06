"""
Track-related models.
"""

from typing import List, Optional
from dataclasses import dataclass
from uuid import UUID
from statistics import mode

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BoundingBox:
    x: int
    y: int
    w: int
    h: int


@dataclass_json
@dataclass
class VisualEvent:
    id: UUID
    box: BoundingBox
    label: str
    confidence: float


@dataclass_json
@dataclass
class Track:
    id: UUID
    start_frame: int
    events: List[Optional[VisualEvent]]
    
    def __len__(self) -> int:
        return len(self.events)

    @property
    def label_mode(self) -> str:
        return mode(event.label for event in self.events if event is not None)
    
    @property
    def slice(self):
        return slice(self.start_frame, self.start_frame + len(self))

"""
File IO operations. 

Each type is encapsulated in a QObject subclass which provides read/write capability.
"""

from collections import defaultdict
from io import BytesIO
import json
import os
import tarfile
from typing import List, Union, Any
from pathlib import Path
from uuid import UUID, uuid4

from PyQt5 import QtCore

from boxjelly.lib.track import BoundingBox, VisualEvent, Track


class AbstractFileIO(QtCore.QObject):
    """
    File IO abstract class.
    """
    
    fileRead = QtCore.pyqtSignal(object)  # payload can be any object
    fileWritten = QtCore.pyqtSignal()
    fileReadFailure = QtCore.pyqtSignal(str)
    fileWriteFailure = QtCore.pyqtSignal(str)
    
    def __init__(self, path: Union[str, Path]):
        super().__init__()
        
        self._path = None
        self.path = path
    
    @property
    def path(self) -> Path:
        return self._path
    
    @path.setter
    def path(self, path: Union[str, Path]):
        self._path = Path(path)  # ensure type Path
    
    def _write(self, data: Any):
        """
        Write data to file. Do not call this directly; instead call write.
        
        Subclasses should implement this method.
        """
        raise NotImplementedError()
        
    def write(self, data: Any):
        """
        Write data to file.
        """
        try:
            self._write(data)
        except Exception as e:
            self.fileWriteFailure.emit(str(e))
            return
        
        self.fileWritten.emit()
    
    def _read(self) -> Any:
        """
        Read data from file. Do not call this directly; instead call read.
        
        Subclasses should implement this method.
        """
        raise NotImplementedError()
    
    def read(self) -> Any:
        """
        Read data from file.
        """
        try:
            data = self._read()
        except Exception as e:
            self.fileReadFailure.emit(str(e))
            return
        
        self.fileRead.emit(data)
        return data


class AbstractTrackFileIO(AbstractFileIO):
    """
    File IO abstract class that deals with collections of tracks.
    """
    
    def _write(self, data: List[Track]):
        return super()._write(data)
    
    def write(self, data: List[Track]):
        """
        Write tracks to file.
        """
        return super().write(data)
    
    def _read(self) -> List[Track]:
        return super()._read()
    
    def read(self) -> List[Track]:
        """
        Read tracks from file.
        """
        return super().read()


class JSONTrackFileIO(AbstractTrackFileIO):
    """
    JSON track file IO.
    """
    
    def _write(self, data: List[Track]):
        track_dicts = [track.to_dict() for track in data]
        
        with self._path.open('w') as f:
            json.dump(track_dicts, f, indent=2)
    
    def _read(self) -> List[Track]:
        with self._path.open('r') as f:
            track_dicts = json.load(f)
        
        tracks = []
        for track_dict in track_dicts:
            tracks.append(Track.from_dict(track_dict))
        return tracks


class YOLOv5DeepSortTrackFileIO(AbstractTrackFileIO):
    """
    YOLOv5-DeepSort track file IO.
    """
    
    def __init__(self, path: Union[str, Path]):
        super().__init__(path)
        
        self._id_uuid_map = dict()
    
    def _write(self, data: List[Track]):
        reverse_id_uuid_map = {v: k for k, v in self._id_uuid_map.items()}
        with open(self._path, 'w') as f:
            for track in data:
                for frame_offset, event in enumerate(track.events):
                    if event is None:  # skip missing events
                        continue
                    
                    frame_number = track.start_frame + frame_offset
                    track_id = reverse_id_uuid_map.get(track.id, max(reverse_id_uuid_map.values()) + 1)  # assign new track ID as max ID + 1 if necessary
                    
                    f.write(f'{frame_number} {track_id} {event.box.x} {event.box.y} {event.box.w} {event.box.h} {event.confidence} {event.label}\n')
    
    def _read(self) -> List[Track]:
        track_dict = {}
        
        with open(self._path, 'r') as f:
            for line in f:
                if not line:  # Empty line, skip
                    continue
                
                # Try to parse line fields
                try:
                    parts = line.strip().split(' ')
                    
                    frame_number = int(parts[0])
                    track_id = int(parts[1])
                    x = int(parts[2])
                    y = int(parts[3])
                    w = int(parts[4])
                    h = int(parts[5])
                    confidence = float(parts[6])
                    label = ' '.join(parts[7:])
                    
                    # Create track if it doesn't exist
                    if track_id not in self._id_uuid_map:
                        track_uuid = uuid4()
                        while track_uuid in self._id_uuid_map.values():
                            track_uuid = uuid4()
                        self._id_uuid_map[track_id] = track_uuid
                        
                        track_dict[track_id] = Track(
                            id=track_uuid,
                            start_frame=frame_number, 
                            events=[], 
                        )
                    
                    track = track_dict[track_id]
                    
                    # Fill in frame jump
                    if track.events:
                        start_frame = track.start_frame
                        while frame_number != start_frame + len(track):
                            track.events.append(None)
                    
                    # Add detection to track
                    track.events.append(
                        VisualEvent(
                            id=uuid4(),
                            box=BoundingBox(x, y, w, h),
                            label=label,
                            confidence=confidence,
                        )
                    )
                    
                except Exception as e:
                    raise ValueError(f'Failed to parse YOLOv5-DeepSort line: {line}') from e
        
        tracks = list(track_dict.values())
        
        return tracks


class DeepseaTrackFileIO(AbstractTrackFileIO):
    """
    Deepsea track file IO.
    """
    
    def _write(self, data: List[Track]):
        # Reformat list of tracks as dict of frame -> deepsea-track "visual event" set
        visual_events_by_frame = dict()
        for track in data:
            for frame_offset, event in enumerate(track.events):
                if event is None:  # skip frame jump
                    continue
                
                frame_num = track.start_frame + frame_offset
                
                if frame_num not in visual_events_by_frame:
                    visual_events_by_frame[frame_num] = []
                
                visual_events_by_frame[frame_num].append({
                    'bounding_box': {
                        'height': int(event.box.h),
                        'width': int(event.box.w),
                        'x': int(event.box.x),
                        'y': int(event.box.y)
                    },
                    'class_name': event.label,
                    'confidence': event.confidence,
                    'frame_num': frame_num,
                    'occlusion': 0,
                    'surprise': 0,
                    'track_uuid': str(track.id),
                    'uuid': str(event.id),
                })
        
        # Get max frame number
        max_frame = max(visual_events_by_frame.keys())
        
        # For each frame, write boxes to JSON in .tar.gz archive
        with tarfile.open(self._path, 'w:gz') as tar:
            for frame in sorted(visual_events_by_frame.keys()):
                visual_events = visual_events_by_frame.get(frame, [])
                filename = f'f{str(frame).zfill(6)}.json'
                
                json_data = [  # wacky format
                    'visualevents',
                    [
                        ['visualevent'] + [visual_event]
                        for visual_event in visual_events
                    ]
                ]
                
                # Encode and describe file
                byte_data = json.dumps(json_data).encode('utf-8')
                buf = BytesIO(byte_data)
                tar_info = tarfile.TarInfo(filename)
                tar_info.size = len(byte_data)
                
                # Add to archive
                tar.addfile(tar_info, buf)
    
    def _read(self) -> List[Track]:
        track_dict = {}
    
        # Open the tar file
        with tarfile.open(self._path) as t:
            # Find archived JSON files
            json_paths = [path for path in t.getnames() if path.endswith('.json') and os.path.basename(path).startswith('f')]
        
            for json_path in json_paths:
                # Try to parse the JSON
                try:
                    with t.extractfile(json_path) as f:
                        data = json.load(f)
                        event_items = data[1]
                        for event_item in event_items:
                            event_data = event_item[1]
                            
                            # Get visualevent values
                            frame_number = int(event_data['frame_num'])
                            label = event_data['class_name']
                            confidence = int(event_data['confidence'])
                            track_uuid = event_data['track_uuid']
                            event_uuid = event_data['uuid']
                            
                            # Get bounding_box values
                            box = event_data['bounding_box']
                            x = int(box['x'])
                            y = int(box['y'])
                            w = int(box['width'])
                            h = int(box['height'])
                            
                            # Create track if it doesn't exist
                            if track_uuid not in track_dict:
                                track_dict[track_uuid] = Track(
                                    id=UUID(track_uuid), 
                                    start_frame=frame_number, 
                                    events=[],
                                )
                            track = track_dict[track_uuid]
                            
                            # Fill in frame jump with None
                            if track.events:
                                start_frame = track.start_frame
                                while frame_number != start_frame + len(track):
                                    track.events.append(None)
                            
                            # Add visual event to track
                            track.events.append(
                                VisualEvent(
                                    id=UUID(event_uuid),
                                    box=BoundingBox(x, y, w, h),
                                    label=label,
                                    confidence=confidence / 100.0,
                                )
                            )
                            
                except Exception as e:
                    raise ValueError(f'Failed to parse {self._path}/{json_path} {e}') from e

        tracks = list(track_dict.values())
        
        return tracks

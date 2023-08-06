from typing import List
from uuid import UUID
from PyQt5 import QtWidgets
from boxjelly.lib.track import Track

from boxjelly.models.TrackListModel import TrackListModel


class TrackListModelCommand(QtWidgets.QUndoCommand):
    def __init__(self, track_model: TrackListModel):
        super().__init__()
        
        self._track_model = track_model
        
        self.setText('Track list model command')


class DeleteTrackByRowCommand(TrackListModelCommand):
    def __init__(self, track_model: TrackListModel, row: int):
        super().__init__(track_model)
        
        self._row = row
        self._track = None
        
        self.setText('Delete track by row {}'.format(row))
    
    def undo(self):
        self._track_model.add_track(self._track)
        self._row = self._track_model.index_by_id(self._track.id)
    
    def redo(self):
        self._track = self._track_model.get_track(self._row)
        self._track_model.delete_track(self._row)


class DeleteTrackByIDCommand(TrackListModelCommand):
    def __init__(self, track_model: TrackListModel, track_id: UUID):
        super().__init__(track_model)
        
        self._track_id = track_id
        self._track = None
        
        self.setText('Delete track {}'.format(track_id))

    def undo(self):
        self._track_model.add_track(self._track)

    def redo(self):
        idx = self._track_model.index_by_id(self._track_id)
        self._track = self._track_model.get_track(idx)
        self._track_model.delete_track(idx)
        

class BatchDeleteTracksByIDCommand(TrackListModelCommand):
    def __init__(self, track_model: TrackListModel, track_ids: List[UUID]):
        super().__init__(track_model)
        
        self._track_ids = track_ids
        self._tracks = []
        
        self.setText('Batch delete tracks {}'.format(', '.join(str(track_id) for track_id in track_ids)))
    
    def undo(self):
        for track in self._tracks:
            self._track_model.add_track(track)
    
    def redo(self):
        self._tracks.clear()
        for track_id in self._track_ids:
            row_idx = self._track_model.index_by_id(track_id)
            track = self._track_model.get_track(row_idx)
            self._tracks.append(track)
            self._track_model.delete_track(row_idx)
        

class BatchRenameTracksCommand(TrackListModelCommand):
    def __init__(self, track_model: TrackListModel, track_ids: list, new_label: str):
        super().__init__(track_model)
        
        self._track_ids = track_ids
        self._new_label = new_label
        self._old_labels = []
        
        self.setText('Rename track(s) {} -> "{}"'.format(', '.join(str(track_id) for track_id in track_ids), new_label))
    
    def undo(self):
        for track_id, label_list in zip(self._track_ids, self._old_labels):
            idx = self._track_model.index_by_id(track_id)
            index = self._track_model.index(idx, 0)
            self._track_model.setData(index, label_list, TrackListModel.EventLabelsRole)
    
    def redo(self):
        self._old_labels.clear()
        for track_id in self._track_ids:
            row_idx = self._track_model.index_by_id(track_id)
            index = self._track_model.index(row_idx, 0)
            track_size = len(self._track_model.get_track(row_idx))
            self._old_labels.append(self._track_model.data(index, TrackListModel.EventLabelsRole))
            self._track_model.setData(index, [self._new_label] * track_size, TrackListModel.EventLabelsRole)


class SplitTrackCommand(TrackListModelCommand):
    def __init__(self, track_model: TrackListModel, track_id: UUID, split_idx: int):
        super().__init__(track_model)
        
        self._track_id = track_id
        self._new_track_id = None
        self._split_idx = split_idx
        
        self.setText('Split track {} at {}'.format(track_id, split_idx))
    
    def undo(self):
        old_track_row_idx = self._track_model.index_by_id(self._track_id)
        old_track_index = self._track_model.index(old_track_row_idx, 0)
        
        new_track_row_idx = self._track_model.index_by_id(self._new_track_id)
        new_track_index = self._track_model.index(new_track_row_idx, 0)
        
        old_events = old_track_index.data(TrackListModel.EventsRole)
        new_events = new_track_index.data(TrackListModel.EventsRole)
        
        self._track_model.setData(old_track_index, old_events + new_events, TrackListModel.EventsRole)  # Concatenate new events back to old track
        self._track_model.delete_track(new_track_row_idx)  # Remove new track
    
    def redo(self):
        row_idx = self._track_model.index_by_id(self._track_id)
        index = self._track_model.index(row_idx, 0)
        
        events = self._track_model.data(index, TrackListModel.EventsRole)
        
        old_events = events[:self._split_idx]
        new_events = events[self._split_idx:]
        
        old_start_frame = index.data(TrackListModel.StartFrameRole)
        
        new_track = Track(
            id=self._track_model.get_new_id(),  # ID = next ID available from model
            start_frame=old_start_frame + self._split_idx,  # Start frame = old start frame + split index
            events=new_events,
        )
        
        self._new_track_id = new_track.id
        
        self._track_model.setData(index, old_events, TrackListModel.EventsRole)  # Clip the old track events
        self._track_model.add_track(new_track)  # Add the new track


class MergeTracksCommand(TrackListModelCommand):
    def __init__(self, track_model: TrackListModel, track_ids: List[UUID]):
        super().__init__(track_model)
        
        self._track_ids = track_ids
        self._original_tracks = []
        self._new_track_id = None
        
        self.setText('Merge tracks {}'.format(', '.join(str(track_id) for track_id in track_ids)))
    
    def undo(self):
        new_track_row_idx = self._track_model.index_by_id(self._new_track_id)
        self._track_model.delete_track(new_track_row_idx)  # Delete the new track
        
        # Restore the original tracks
        for track in self._original_tracks:
            self._track_model.add_track(track)
    
    def redo(self):
        # Collect the tracks and remove them from the model
        self._original_tracks.clear()
        for track_id in self._track_ids:
            row_idx = self._track_model.index_by_id(track_id)
            track = self._track_model.get_track(row_idx)
            self._original_tracks.append(track)
            self._track_model.delete_track(row_idx)
            
        # Sort by start frame
        self._original_tracks.sort(key=lambda track: track.start_frame)
        
        start_frame = self._original_tracks[0].start_frame
        end_frame = max(track.start_frame + len(track) for track in self._original_tracks)
        
        events_by_frame = []
        next_track_idx = 0
        for frame_num in range(start_frame, end_frame + 1):
            if next_track_idx < len(self._original_tracks) and self._original_tracks[next_track_idx].start_frame == frame_num:
                current_track = self._original_tracks[next_track_idx]
                next_track_idx += 1
            
            # Get the index of the event in the current track that corresponds to this frame
            event_idx = frame_num - current_track.start_frame
            
            # Append the corresponding event (or None if there is no box) to the list
            if event_idx < len(current_track.events):
                events_by_frame.append(current_track.events[event_idx])
            else:  # If the box index is out of bounds, then the current track has no boxes for this frame
                events_by_frame.append(None)
        
        # Create the new track
        new_track = Track(
            id=self._track_model.get_new_id(),  # ID = next ID available from model
            start_frame=start_frame,  # Start frame = start frame of first track
            events=events_by_frame,
        )
        
        self._new_track_id = new_track.id

        self._track_model.add_track(new_track)  # Add the new track
        
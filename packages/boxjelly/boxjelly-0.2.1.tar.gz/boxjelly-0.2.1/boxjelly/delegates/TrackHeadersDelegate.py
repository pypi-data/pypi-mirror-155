from PyQt5 import QtWidgets, QtCore, QtGui

from boxjelly.models.TrackListModel import TrackListModel


class TrackHeadersDelegate(QtWidgets.QStyledItemDelegate):
    
    def paint(self, painter: QtGui.QPainter, opt: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        self.initStyleOption(opt, index)
        
        rect = opt.rect
        
        painter.save()
        
        # Get the track ID and label
        id = index.data(TrackListModel.IDRole)
        label = index.data(TrackListModel.LabelRole)
        
        # Draw the highlight if the track is selected
        if opt.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(rect, opt.palette.highlight())
            
        # Define padded contents rect
        contents = rect.adjusted(5, 0, -5, 0)
        
        # Check if mouse hover
        hover = opt.state & QtWidgets.QStyle.State_MouseOver
        
        # Draw the track ID
        str_id = str(id)
        if not hover:
            str_id = str_id[:8] + '...'  # limit to first 8 characters of UUID
        painter.setPen(QtGui.QPen(opt.palette.color(QtGui.QPalette.Text)))
        painter.drawText(contents, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, str_id)
        
        # Draw the track label if not hovering
        if not hover:
            painter.drawText(contents, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, label)
        
        painter.restore()
    
    def sizeHint(self, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        return QtCore.QSize(100, 30)
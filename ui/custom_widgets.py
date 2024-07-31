# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright (c) 2024 沉默の金
from PySide6.QtCore import QEvent, Signal
from PySide6.QtGui import QCursor, QDropEvent, QHelpEvent, QResizeEvent
from PySide6.QtWidgets import QHeaderView, QListWidget, QTableWidget, QTableWidgetItem, QToolTip, QWidget


class HeaderViewResizeMode:
    ResizeToContents = 2


class LyricOrderListWidget(QListWidget):
    droped = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def dropEvent(self, event: QDropEvent) -> None:
        super().dropEvent(event)
        self.droped.emit()


class ProportionallyStretchedTableWidget(QTableWidget):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.props = []
        self.itemChanged.connect(self.adapt_size)

        self.setMouseTracking(True)

    def set_proportions(self, props: list) -> None:
        """设置表格宽度的比例

        ::param : 比例列表
        当比例大于等于0小于等于1时,为比例
        当比例等于2时,自适应内容
        """
        self.props = props

    def adapt_size(self) -> None:
        if not self.props or len(self.props) != self.columnCount():
            return
        width = self.viewport().size().width()
        for i, prop in enumerate(self.props):
            if prop == HeaderViewResizeMode.ResizeToContents:
                self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
                width -= self.columnWidth(i)
        for i in range(self.columnCount()):
            if 0 <= self.props[i] <= 1:

                self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
                self.setColumnWidth(i, self.props[i] * width)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.adapt_size()

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.ToolTip and isinstance(event, QHelpEvent):
            item = self.itemAt(event.x(), event.y() - self.horizontalHeader().height())
            if isinstance(item, QTableWidgetItem):
                text = item.text().strip()  # 考虑表头的高度
                if text:
                    QToolTip.showText(QCursor.pos(), text, self)
            return True
        return super().event(event)

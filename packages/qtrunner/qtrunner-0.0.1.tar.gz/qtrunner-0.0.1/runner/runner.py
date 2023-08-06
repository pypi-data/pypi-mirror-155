#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: hufeng.mao@carota.ai
Date: 2022-04-25 21:23:55
LastEditTime: 2022-06-20 23:55:48
Description: 快速启动器
'''

import json
import sys
import os
import qtawesome as qta
from datetime import datetime

from PyQt5.QtCore import QProcess, QSize, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt5.QtGui import QTextCursor, QIcon

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QStyleFactory, QTextEdit, QListWidgetItem,
    QProgressBar, QVBoxLayout, QHBoxLayout, QMessageBox, QLabel, QWidget, QGraphicsOpacityEffect
)
from PyQt5.QtCore import QFileSystemWatcher
from .highlighter import Highlighter

from .runner_ui import Ui_MainWindow

hl = Highlighter()

class ProcessItemWidget(QWidget):
    # itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, text, process:QProcess,*args, **kwargs):
        super(ProcessItemWidget, self).__init__(*args, **kwargs)
        bar = QProgressBar(self)
        closeButton = QPushButton("终止", self)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(text, self))
        layout.addWidget(bar)
        layout.addWidget(closeButton)
        closeButton.clicked.connect(self.onButtonClick)
        self.closeButton = closeButton
        self.process = process
        self.bar = bar

    def onButtonClick(self):
        self.process.kill()

    def sizeHint(self):
        return QSize(200, 40)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.configPath = "config.json"
        self.maxStdout =    40960       # 单次stdout最大字节
        self.maxLogLines =  150         # log最大行数
        self.logLines =     0           # 当前log行数
        self.defaultEncoding = "gbk"    # stdout默认输出encoding
        self.rp = os.path.dirname(os.path.abspath(__file__))    # 相对目录

        if not os.path.exists(self.configPath):
            self.configPath = os.path.join(self.rp, self.configPath)

        self.setWindowIcon(QIcon("runner.png"))
        self.setupUi()
        self.setupWatcher()

    def setupWatcher(self):
        self.watcher = QFileSystemWatcher(self)
        self.watcher.addPath(self.configPath )
        self.watcher.fileChanged.connect(self.onFileChanged)


    def setupUi(self):
        self.selectIndex = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupButtons()
        self.setupQss()

    def setupToolboxButtons(self, configPath):
        if not os.path.exists(configPath):
            configPath = os.path.join(self.rp, configPath)
        with open(configPath, encoding="utf-8") as f:
            config = json.load(f)

            self.fadeIn(self.ui.toolBox)
            self.removeAll(self.ui.toolBoxLayout)
            for i, item in enumerate(config):
                # print(cmd)
                tag = f'{i+1}.{item["title"]}'
                button = QPushButton(tag, self.ui.toolBox)
                button.userdata = item
                button.clicked.connect(self.buttonClick)
                if "qss" in item:
                    button.setStyleSheet(item["qss"])
                self.ui.toolBoxLayout.addWidget(button)

    def setupButtons(self):
        with open(self.configPath, encoding="utf-8") as f:
            config = json.load(f)
            if "maxLogLines" in config:
                self.maxLogLines = config.get("maxLogLines")
            if "maxStdout" in config:
                self.maxStdout = config.get("maxStdout")
            if "defaultEncoding" in config:
                self.defaultEncoding = config.get("defaultEncoding")

            self.removeAll(self.ui.configLayout)
            for item in config["configs"]:
                # print(cmd)
                tag = f'加载:`{item["title"]}`配置文件'
                button = QPushButton(tag, self)
                button.item = item
                button.clicked.connect(self.onloadConfigButton)
                self.ui.configLayout.addWidget(button)
    
    def setupQss(self):
        self.qss = "app.qss"
        try :
            with open(self.qss, "r", encoding="utf-8") as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        except:
            pass

    def fadeIn(self, widget:QWidget):
        
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b'opacity', self)
        animation.setDuration(500)
        animation.setEasingCurve(QEasingCurve.InOutBack)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.start()

    def shake(self, widget:QWidget):

        animation = QPropertyAnimation(widget, b'pos', self)        

        pos = widget.pos()
        x, y = pos.x(), pos.y()

        animation.setDuration(200)
        animation.setLoopCount(2)
        animation.setKeyValueAt(0, QPoint(x, y))
        animation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
        animation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
        animation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
        animation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
        animation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
        animation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
        animation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
        animation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
        animation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
        animation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
        animation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
        animation.setEndValue(QPoint(x, y))

        animation.start()

    def removeAll(self, layout):
        for i in reversed(range(layout.count())): 
            widgetToRemove = layout.itemAt(i).widget()
            if widgetToRemove:
                layout.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)


    def onFileChanged(self, path):
        self.ui.textEditStatusTrace.append(f"onFileChanged: {path} @ {self.now()}")
        if path == self.configPath:
            self.setupButtons()

    def processText(self, edit:QTextEdit, text, progressBar:QProgressBar, plain=False):
        if not plain:
            skip = False
            for p, show in hl.progess(text):
                progressBar.setValue(p)
                skip = not show
                
            if skip: return

        cursor = edit.textCursor()
        self.logLines = self.logLines + 1
        if self.logLines > self.maxLogLines:
            d = self.logLines - self.maxLogLines + 10
            cursor.movePosition(QTextCursor.Start)
            for _ in range(d):
                cursor.select(QTextCursor.LineUnderCursor)
                cursor.removeSelectedText(); 
                cursor.deleteChar() 
            self.logLines = self.logLines - d
        cursor.movePosition(QTextCursor.End)
        if plain:
            cursor.insertText(text)
            edit.moveCursor(QTextCursor.End)
            return

        n = 0
        t = len(text)
        formats = list(hl.highlight(text))
        formats.sort(key=lambda a: a[0])    # 根据index排序
        for i, l, f in formats:
            if i > n:
                cursor.insertText(text[n:i], highlighter.default)
            cursor.insertText(text[i:i+l], f)
            n = i + l
        if n < t:
            cursor.insertText(text[n:], highlighter.default)

        edit.moveCursor(QTextCursor.End)

    def onProcessStdout(self):
        process:QProcess = self.sender()
        item:QListWidgetItem = process.item
        
        a = process.bytesAvailable()
        if a > self.maxStdout:
            process.read(a - 4096)
            print(f"bytesAvailable to large:{a}, seek to last 4K")
        while True:
            data = process.readLine()
            if not data: return
            text = bytes(data).decode(item.encoding)
            if text.count("\n") > 1:
                print(text.count("\n"), text)
            self.processText(self.ui.textEditAppTrace, text, item.bar, item.plain)

    def onProcessStderr(self):
        process:QProcess = self.sender()
        item:QListWidgetItem = process.item
        data = process.readAllStandardError()
        text = bytes(data).decode(item.encoding)
        self.processText(self.ui.textEditAppTrace, text, item.bar, item.plain)

    def onProcessStarted(self):
        process:QProcess = self.sender()
        btn:QPushButton = process.btn
        btn.setEnabled(False)
        item:QListWidgetItem = process.item
        self.ui.processListWidget.addItem(item)
        cmd = item.text()
        pid = process.processId()
        iw = ProcessItemWidget(f"[{pid}]{cmd}", process)

        item.iw = iw
        item.bar = iw.bar
        item.setText("")
        self.ui.processListWidget.setItemWidget(item, iw)

    def onProcessFinished(self, exitCode):
        process:QProcess = self.sender()
        btn:QPushButton = process.btn
        btn.setEnabled(True)
        item:QListWidgetItem = process.item
        iw:ProcessItemWidget = item.iw
        iw.closeButton.setEnabled(False)
        def finished():
            timer.stop()
            row = self.ui.processListWidget.indexFromItem(item).row()
            self.ui.processListWidget.takeItem(row)
        timer = QTimer(self, timeout=finished)
        timer.start(3000)
        

    def now(self, fn=False):
        if fn:
            return datetime.now().strftime("%Y%m%d_%H%M%S")
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def buttonClick(self):
        btn = self.sender()
        
        title = btn.userdata["title"]
        cmd = btn.userdata["cmd"]
        cwd = btn.userdata.get("cwd", "")
        plain = btn.userdata.get("plain", False)
        encoding = btn.userdata.get("encoding", self.defaultEncoding)
        cwd = os.path.abspath(cwd)
        self.ui.textEditStatusTrace.append(cmd)
        process = QProcess(self)
        time_tag = self.now()
        self.ui.textEditAppTrace.append("="*60)
        self.ui.textEditAppTrace.append(f"{title} @ {time_tag}")
        self.ui.textEditAppTrace.append("="*60)
        self.ui.textEditAppTrace.append("\n")
        
        process.btn = btn
        process.readyReadStandardOutput.connect(self.onProcessStdout)
        process.readyReadStandardError.connect(self.onProcessStderr)

        process.started.connect(self.onProcessStarted)
        process.finished.connect(self.onProcessFinished)
        process.setWorkingDirectory(cwd)

        process.item = QListWidgetItem(qta.icon("ei.arrow-right"), cmd)
        process.item.plain = plain
        process.item.encoding = encoding
        process.start(cmd)

    def onloadConfigButton(self):
        btn = self.sender()
        try:
            self.setupToolboxButtons(btn.item["file"])
            self.fadeIn(btn)
        except:
            self.shake(btn)

    def onStyleSelected(self, style):
        self.setStyle(QStyleFactory.create(style))

    def onClearLog(self):        
        self.ui.textEditAppTrace.clear()
        self.ui.textEditStatusTrace.clear()
        self.logLines = 0
        self.fadeIn(self.ui.pushButtonClearLog)

    def onSaveLog(self):
        self.fadeIn(self.ui.pushButtonSaveLog)
        fn = f"applog_{self.now(True)}.html"
        with open(fn, "w+", encoding="utf-8") as f:  
            f.write(self.ui.textEditAppTrace.toHtml())
            title = f"save log to {fn}"
            QMessageBox.information(self, "Info", title)

    def run(self):
        pass

    def test(self):
        pass

    def export(self):
        pass

    def reset(self):
        self.setupQss()

    def closeEvent(self, a0) -> None:
        return super().closeEvent(a0)

        
def main():

    app = QApplication(sys.argv)

    win = Window()
    win.show()
    rc = app.exec_()
    sys.exit(rc)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import sys

from cxwidgets.aQt.QtWidgets import QWidget, QApplication
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
from cxwidgets import BPMWidget
import pycx4.qcda as cda
# from .menus.general_cm import CXGeneralCM
# from .common_mixin import CommonMixin


class CXBPMWidget(BPMWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.dev_name = kwargs.get('dev_name', None)

        # in order to
        self.cnames = {
            'x': 'x',
            'y': 'z',
            }

        self.chans = {cn: cda.DChan(f'{self.dev_name}.{self.cnames[cn]}') for cn in self.cnames}
        for k in self.chans:
            self.chans[k].valueMeasured.connect(self.data_update)

    def data_update(self, chan):
        print(chan.name, chan.val)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = CXBPMWidget(dev_name="cxhw:3.k500.bpm.e2v2.6PIC2")
    w.show()

    sys.exit(app.exec_())

import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from Database import KEYS, Database


class DetailLogWindow(QMainWindow):
    def __init__(self, data, parent=None):
        super(DetailLogWindow, self).__init__(parent)
        loadUi("UI/DetailLog.ui", self)
        self.data = data
        self.car_image.setScaledContents(True)
        self.license_image.setScaledContents(True)
        self.ticket_button.clicked.connect(self.ticket)
        self.initData()

    def ticket(self):
        file_name = 'tickets/' + str(self.data[KEYS.CARID]) + '.txt'
        with open(file_name, 'w') as file:
            lic_num = str(self.license_number_lineedit.text())
            rule = self.data[KEYS.RULENAME]
            fine = str(self.data[KEYS.RULEFINE])
            file.write('########################################\n')
            file.write('#  License Number                      #\n')
            file.write('#' + ''.join([' ' for i in range(35 - len(lic_num))]) + lic_num + '   #\n')
            file.write('#  Rule Broken :                       #\n')
            file.write('#'+''.join([' ' for i in range(35 - len(rule))]) + rule + '   #\n')
            file.write('#  Fine :                              #\n')
            file.write('#'+''.join([' ' for i in range(35 - len(fine))]) + fine + '   #\n')
            file.write('########################################\n')
        self.destroy()
        import sys
        if sys.platform == "darwin":
            os.popen("open " + file_name)
        elif sys.platform == "win32":
            os.popen("start " + file_name)
        else:
            os.popen("xdg-open " + file_name)

    def initData(self):
        self.cam_id.setText(str(self.data[KEYS.CARID]))
        self.car_color.setText(self.data[KEYS.CARCOLOR])

        if self.data[KEYS.CARIMAGE]:
            self.car_image.setPixmap(QPixmap(self.data[KEYS.CARIMAGE]))
        if self.data[KEYS.LICENSEIMAGE]:
            self.license_image.setPixmap(QPixmap(self.data[KEYS.LICENSEIMAGE]))

        self.license_number_lineedit.setText(self.data[KEYS.LICENSENUMBER])
        self.location.setText(self.data[KEYS.LOCATION])
        self.rule.setText(self.data[KEYS.RULENAME])

        self.close_button.clicked.connect(self.close)
        self.delete_button.clicked.connect(self.deleteRecord)

    def close(self):
        self.destroy()

    def deleteRecord(self):
        qm = QtWidgets.QMessageBox
        prompt = qm.question(self, '', "Are you sure to reset all the values?", qm.Yes | qm.No)
        if prompt == qm.Yes:
            db = Database.get_instance()
            db.delete_violation(carid=self.data[KEYS.CARID], ruleid=self.data[KEYS.RULEID], time=self.data[KEYS.TIME])
            self.destroy()
        else:
            pass

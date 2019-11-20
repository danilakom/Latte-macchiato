from addEditCoffeeForm import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
import sys
import sqlite3


class App(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.c = ["ID", "Сорт", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"]
        self.initUi()
    
    def initUi(self):
        result = list(self.cur.execute("select * from coffee").fetchall())
        self.table.setColumnCount(len(self.c))
        self.table.setHorizontalHeaderLabels(self.c)
        self.table.setRowCount(0)
        for i, row in enumerate(result):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()
        self.table.cellChanged.connect(self.run)

    def run(self, row, column):
        st = self.c[column]
        it = self.table.item(row, column).text()
        id = self.table.item(row, 0).text()
        res = self.cur.execute(f"""update coffee set '{st}' = ? where ID = ?""", (it, int(id)))
        self.con.commit()

    def add(self):
        s = self.lineEdit_s.text()
        o = self.lineEdit_o.text()
        m = self.lineEdit_m.text()
        t = self.lineEdit_t.text()
        p = self.lineEdit_p.text()
        v = self.lineEdit_v.text()
        res = self.cur.execute("""insert into coffee('Сорт', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена', 
        'Объем упаковки') values(?, ?, ?, ?, ?, ?)""", (s, o, m, t, p, v))
        self.con.commit()

        self.initUi()


app = QApplication(sys.argv)
a = App()
a.show()
sys.exit(app.exec_())

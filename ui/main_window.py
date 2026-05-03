from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QMenuBar, QMenu, QGroupBox, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from ui.film_dialog import FilmDialog
from controller.film_controller import load_films, save_film, edit_film, remove_film

NAMA = "Fairuza Luthfiana"
NIM  = "F1D02310111"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinemaku")
        self.setMinimumSize(860, 560)
        self._build_menubar()
        self._build_ui()
        self.refresh()

    def _build_menubar(self):
        menubar = self.menuBar()
        menu_app = menubar.addMenu("Aplikasi")

        act_about = QAction("Tentang Aplikasi", self)
        act_about.triggered.connect(self._show_about)
        menu_app.addAction(act_about)

        act_quit = QAction("Keluar", self)
        act_quit.triggered.connect(self.close)
        menu_app.addAction(act_quit)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(12)

        header = QHBoxLayout()
        lbl_title = QLabel("🎬  Cinemaku")
        lbl_title.setObjectName("label_title")
        lbl_id = QLabel(f"{NAMA}  •  {NIM}")
        lbl_id.setObjectName("label_identity")
        lbl_id.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header.addWidget(lbl_title)
        header.addStretch()
        header.addWidget(lbl_id)
        root.addLayout(header)

        toolbar = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Cari judul atau sutradara...")
        self.search_box.textChanged.connect(self.filter)

        btn_add   = QPushButton("+ Tambah Film")
        btn_edit  = QPushButton("Edit")
        self.btn_del = QPushButton("Hapus")
        self.btn_del.setObjectName("btn_delete")
        btn_add.clicked.connect(self.add)
        btn_edit.clicked.connect(self.edit)
        self.btn_del.clicked.connect(self.delete)

        toolbar.addWidget(self.search_box)
        toolbar.addStretch()
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_edit)
        toolbar.addWidget(self.btn_del)
        root.addLayout(toolbar)

        grp = QGroupBox("Daftar Film")
        grp_layout = QVBoxLayout(grp)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Genre", "Sutradara", "Tahun", "Rating", "Catatan"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(0, True)
        header_h = self.table.horizontalHeader()
        header_h.setSectionResizeMode(1, QHeaderView.Stretch)
        header_h.setSectionResizeMode(6, QHeaderView.Stretch)
        grp_layout.addWidget(self.table)
        root.addWidget(grp)

        self.statusBar().showMessage("Siap")

    def refresh(self, filter_text=""):
        self._all_data = load_films()
        data = self._all_data
        if filter_text:
            ft = filter_text.lower()
            data = [r for r in data if ft in r[1].lower() or ft in r[3].lower()]
        self.table.setRowCount(len(data))
        for row, rec in enumerate(data):
            for col, val in enumerate(rec):
                item = QTableWidgetItem(str(val) if val is not None else "")
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.table.setItem(row, col, item)
        self.statusBar().showMessage(f"{len(data)} film tercatat")

    def filter(self, text):
        self.refresh(filter_text=text)

    def selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None, None
        id_item = self.table.item(row, 0)
        return row, int(id_item.text()) if id_item else None

    def selected_data(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return [self.table.item(row, c).text() if self.table.item(row, c) else "" for c in range(7)]

    def add(self):
        dlg = FilmDialog(self)
        if dlg.exec():
            d = dlg.get_data()
            ok, msg = save_film(d["judul"], d["genre"], d["sutradara"], d["tahun"], d["rating"], d["catatan"])
            if ok:
                self.refresh(self.search_box.text())
                self.statusBar().showMessage(msg, 3000)
            else:
                QMessageBox.warning(self, "Peringatan", msg)

    def edit(self):
        _, film_id = self.selected_id()
        if film_id is None:
            QMessageBox.information(self, "Info", "Pilih film yang ingin diedit.")
            return
        data = self.selected_data()
        # data: [id, judul, genre, sutradara, tahun, rating, catatan]
        data_tuple = (data[0], data[1], data[2], data[3], int(data[4]) if data[4].isdigit() else 2024, data[5], data[6])
        dlg = FilmDialog(self, data=data_tuple)
        if dlg.exec():
            d = dlg.get_data()
            ok, msg = edit_film(film_id, d["judul"], d["genre"], d["sutradara"], d["tahun"], d["rating"], d["catatan"])
            if ok:
                self.refresh(self.search_box.text())
                self.statusBar().showMessage(msg, 3000)
            else:
                QMessageBox.warning(self, "Peringatan", msg)

    def delete(self):
        _, film_id = self.selected_id()
        if film_id is None:
            QMessageBox.information(self, "Info", "Pilih film yang ingin dihapus.")
            return
        judul = self.table.item(self.table.currentRow(), 1).text()
        confirm = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Hapus film \"{judul}\"?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            ok, msg = remove_film(film_id)
            if ok:
                self.refresh(self.search_box.text())
                self.statusBar().showMessage(msg, 3000)

    def _show_about(self):
        QMessageBox.about(
            self, "Tentang Aplikasi",
            "<b>Cinemaku</b><br>"
            "Aplikasi pencatatan film bioskop.<br><br>"
            f"<b>Mahasiswa:</b> {NAMA}<br>"
            f"<b>NIM:</b> {NIM}<br><br>"
            "Dibuat dengan PySide6 + SQLite"
        )

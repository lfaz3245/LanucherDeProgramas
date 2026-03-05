import sys
import os
import json
import subprocess
import psutil
import time

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QFileDialog, QMessageBox, QLineEdit,
    QColorDialog, QListWidgetItem, QLabel, QHBoxLayout
)

from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

APPS_FILE = "apps.json"
USAGE_FILE = "usage.json"
SETTINGS_FILE = "settings.json"
ICON_FOLDER = "icons"


if not os.path.exists(ICON_FOLDER):
    os.makedirs(ICON_FOLDER)


def load_json(file, default):

    if not os.path.exists(file):
        return default

    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return default


def save_json(file, data):

    with open(file, "w") as f:
        json.dump(data, f, indent=4)


class ToggleSwitch(QPushButton):

    def __init__(self):
        super().__init__()

        self.setCheckable(True)
        self.setFixedSize(60, 28)

        self.update_style()

        self.toggled.connect(self.update_style)

    def update_style(self):

        if self.isChecked():

            self.setStyleSheet("""
            QPushButton {
                background-color: #00bcd4;
                border-radius: 14px;
            }
            """)

        else:

            self.setStyleSheet("""
            QPushButton {
                background-color: #777;
                border-radius: 14px;
            }
            """)


class Launcher(QWidget):

    def __init__(self):
        super().__init__()

        self.apps = load_json(APPS_FILE, [])
        self.usage = load_json(USAGE_FILE, {})
        self.settings = load_json(SETTINGS_FILE, {
            "dark_mode": False,
            "theme_color": "#3daee9"
        })

        self.running = {}

        self.setWindowTitle("Universal Launcher")
        self.resize(420, 520)

        layout = QVBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar programa...")
        self.search.textChanged.connect(self.refresh_list)
        layout.addWidget(self.search)

        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(32, 32))
        layout.addWidget(self.listWidget)

        btn_add = QPushButton("Adicionar programa")
        btn_add.clicked.connect(self.add_program)

        btn_launch = QPushButton("Abrir")
        btn_launch.clicked.connect(self.launch_program)

        btn_remove = QPushButton("Remover")
        btn_remove.clicked.connect(self.remove_program)

        btn_color = QPushButton("Cor do tema")
        btn_color.clicked.connect(self.choose_color)

        layout.addWidget(btn_add)
        layout.addWidget(btn_launch)
        layout.addWidget(btn_remove)
        layout.addWidget(btn_color)

        toggle_layout = QHBoxLayout()

        label = QLabel("Dark Mode")

        self.dark_toggle = ToggleSwitch()
        self.dark_toggle.setChecked(self.settings["dark_mode"])
        self.dark_toggle.clicked.connect(self.toggle_dark)

        toggle_layout.addWidget(label)
        toggle_layout.addWidget(self.dark_toggle)

        layout.addLayout(toggle_layout)

        self.setLayout(layout)

        self.apply_theme()

        self.refresh_list()

        self.timer = self.startTimer(5000)

    def refresh_list(self):

        self.listWidget.clear()

        query = self.search.text().lower()

        for app in self.apps:

            name = app["name"]

            if query not in name.lower():
                continue

            seconds = self.usage.get(name, 0)

            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)

            text = f"{name} — {hours}h {minutes}m"

            item = QListWidgetItem(text)

            icon_path = app.get("icon")

            if icon_path and os.path.exists(icon_path):
                item.setIcon(QIcon(icon_path))
            elif os.path.exists(app["path"]):
                item.setIcon(QIcon(app["path"]))

            self.listWidget.addItem(item)

    def add_program(self):

        file, _ = QFileDialog.getOpenFileName(self, "Selecionar programa")

        if not file:
            return

        name = os.path.basename(file)

        icon_path = os.path.join(ICON_FOLDER, name + ".ico")

        try:

            icon = QIcon(file)

            pixmap = icon.pixmap(64, 64)

            pixmap.save(icon_path, "ICO")

        except:
            icon_path = ""

        self.apps.append({
            "name": name,
            "path": file,
            "icon": icon_path
        })

        save_json(APPS_FILE, self.apps)

        self.refresh_list()

    def get_visible_apps(self):

        query = self.search.text().lower()

        visible = []

        for app in self.apps:
            if query in app["name"].lower():
                visible.append(app)

        return visible

    def launch_program(self):

        index = self.listWidget.currentRow()

        if index < 0:
            return

        app = self.get_visible_apps()[index]

        exe_path = app["path"]

        working_dir = os.path.dirname(exe_path)

        try:

            process = subprocess.Popen(
                f'"{exe_path}"',
                cwd=working_dir,
                shell=True
            )

            start = time.time()

            self.running[process.pid] = {
                "name": app["name"],
                "start": start
            }

        except:

            try:

                os.startfile(exe_path)

                start = time.time()

                self.running[exe_path] = {
                    "name": app["name"],
                    "start": start
                }

            except Exception as e:

                QMessageBox.critical(self, "Erro", str(e))

    def remove_program(self):

        index = self.listWidget.currentRow()

        if index < 0:
            return

        target = self.get_visible_apps()[index]

        confirm = QMessageBox.question(
            self,
            "Confirmar",
            f"Remover {target['name']}?"
        )

        if confirm == QMessageBox.Yes:

            self.apps.remove(target)

            save_json(APPS_FILE, self.apps)

            self.refresh_list()

    def check_processes(self):

        finished = []

        for pid, data in self.running.items():

            if isinstance(pid, int) and not psutil.pid_exists(pid):

                duration = time.time() - data["start"]

                name = data["name"]

                self.usage.setdefault(name, 0)
                self.usage[name] += duration

                finished.append(pid)

        for pid in finished:
            del self.running[pid]

        save_json(USAGE_FILE, self.usage)

        self.refresh_list()

    def timerEvent(self, event):

        self.check_processes()

    def toggle_dark(self):

        self.settings["dark_mode"] = self.dark_toggle.isChecked()

        save_json(SETTINGS_FILE, self.settings)

        self.apply_theme()

    def choose_color(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.settings["theme_color"] = color.name()

            save_json(SETTINGS_FILE, self.settings)

            self.apply_theme()

    def apply_theme(self):

        color = self.settings["theme_color"]

        if self.settings["dark_mode"]:

            style = f"""
            QWidget {{
                background-color: #121212;
                color: white;
            }}

            QListWidget {{
                background-color: #1e1e1e;
                border: none;
            }}

            QPushButton {{
                background-color: {color};
                border-radius: 6px;
                padding: 6px;
            }}

            QLineEdit {{
                background-color: #1e1e1e;
                border: 1px solid {color};
                padding: 5px;
            }}
            """

        else:

            style = f"""
            QWidget {{
                background-color: #f2f2f2;
                color: black;
            }}

            QListWidget {{
                background-color: white;
            }}

            QPushButton {{
                background-color: {color};
                border-radius: 6px;
                padding: 6px;
            }}

            QLineEdit {{
                border: 1px solid {color};
                padding: 5px;
            }}
            """

        self.setStyleSheet(style)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Launcher()
    window.show()

    sys.exit(app.exec())
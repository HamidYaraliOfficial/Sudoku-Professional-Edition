import sys
import os
import random
import copy
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QFrame, QGridLayout, QLineEdit,
    QButtonGroup, QMessageBox, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect,
    QScrollArea, QGroupBox, QProgressBar, QInputDialog, QFileDialog
)
from PyQt6.QtCore import Qt, QTranslator, QLocale, QSize, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QUrl
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QLinearGradient, QBrush, QPainter, QPen, QValidator

class SudokuCell(QLineEdit):
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setFixedSize(60, 60)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.setMaxLength(1)
        self.setValidator(SudokuValidator())
        self.original_value = None
        self.setStyleSheet(self.base_style())
        self.apply_shadow()

    def base_style(self):
        return """
            SudokuCell {
                background: transparent;
                border: 2px solid #3A3A3A;
                border-radius: 12px;
                color: #0078D4;
                padding: 8px;
            }
            SudokuCell:focus {
                border: 3px solid #0078D4;
                background: rgba(0, 120, 212, 0.08);
            }
            SudokuCell[readonly="true"] {
                color: #1E1E1E;
                background: rgba(0, 0, 0, 0.03);
                font-weight: bold;
            }
        """

    def apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.setGraphicsEffect(shadow)

    def set_fixed(self, value):
        self.original_value = value
        self.setText(str(value) if value else "")
        self.setReadOnly(True)
        self.setStyleSheet(self.base_style().replace("color: #0078D4;", "color: #1E1E1E;"))

    def set_editable(self):
        self.setReadOnly(False)
        self.setStyleSheet(self.base_style())

class SudokuValidator(QValidator):
    def validate(self, input_str, pos):
        if len(input_str) == 0:
            return (QValidator.State.Acceptable, input_str, pos)
        if input_str in "123456789":
            return (QValidator.State.Acceptable, input_str, pos)
        return (QValidator.State.Invalid, input_str, pos)

class LanguageSelector(QWidget):
    language_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        self.label = QLabel()
        self.label.setFont(QFont("Segoe UI", 10))

        self.combo = QComboBox()
        self.combo.setFixedWidth(220)
        self.combo.setFont(QFont("Segoe UI", 10))
        self.combo.addItems(["English", "فارسی", "中文", "Русский"])
        self.combo.currentIndexChanged.connect(self.on_change)

        layout.addWidget(self.label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(self.combo)
        self.update_text()

    def update_text(self):
        idx = QApplication.instance().property("lang_index") or 0
        texts = ["Select Language:", "انتخاب زبان:", "选择语言：", "Выберите язык:"]
        self.label.setText(texts[idx])

    def on_change(self, index):
        codes = ["en", "fa", "zh", "ru"]
        self.language_changed.emit(codes[index])
        self.update_text()

class ThemeSelector(QWidget):
    theme_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        self.label = QLabel()
        self.label.setFont(QFont("Segoe UI", 10))

        self.combo = QComboBox()
        self.combo.setFixedWidth(220)
        self.combo.setFont(QFont("Segoe UI", 10))
        self.combo.addItems(["Windows Default", "Light", "Dark", "Blue", "Red"])
        self.combo.currentIndexChanged.connect(lambda i: self.theme_changed.emit(self.combo.currentText()))

        layout.addWidget(self.label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(self.combo)
        self.update_text()

    def update_text(self):
        idx = QApplication.instance().property("lang_index") or 0
        texts = ["Theme:", "تم:", "主题：", "Тема:"]
        self.label.setText(texts[idx])

class DifficultySelector(QWidget):
    difficulty_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        self.label = QLabel()
        self.label.setFont(QFont("Segoe UI", 10))

        self.combo = QComboBox()
        self.combo.setFixedWidth(220)
        self.combo.setFont(QFont("Segoe UI", 10))
        self.combo.addItems(["Easy", "Medium", "Hard", "Expert"])
        self.combo.currentIndexChanged.connect(lambda i: self.difficulty_changed.emit(i))

        layout.addWidget(self.label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(self.combo)
        self.update_text()

    def update_text(self):
        idx = QApplication.instance().property("lang_index") or 0
        texts = ["Difficulty:", "سطح دشواری:", "难度：", "Сложность:"]
        self.label.setText(texts[idx])

class SudokuSolver:
    @staticmethod
    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = row // 3 * 3, col // 3 * 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    @staticmethod
    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if SudokuSolver.is_valid(board, row, col, num):
                            board[row][col] = num
                            if SudokuSolver.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    @staticmethod
    def generate_puzzle(difficulty=1):
        board = [[0 for _ in range(9)] for _ in range(9)]
        SudokuSolver.fill_diagonal(board)
        SudokuSolver.solve(board)
        return SudokuSolver.remove_cells(copy.deepcopy(board), difficulty)

    @staticmethod
    def fill_diagonal(board):
        for i in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            idx = 0
            for row in range(i, i+3):
                for col in range(i, i+3):
                    board[row][col] = nums[idx]
                    idx += 1

    @staticmethod
    def remove_cells(board, difficulty):
        cells_to_remove = [45, 50, 55, 60][difficulty]
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        for i in range(cells_to_remove):
            row, col = positions[i]
            board[row][col] = 0
        return board

class SudokuBoard(QWidget):
    puzzle_solved = pyqtSignal()
    hint_used = pyqtSignal()

    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.board = [[0]*9 for _ in range(9)]
        self.solution = [[0]*9 for _ in range(9)]
        self.cells = []
        self.mistakes = 0
        self.hints_used = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.elapsed = 0
        self.setup_ui()
        self.update_texts()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Timer and stats
        stats_layout = QHBoxLayout()
        self.timer_label = QLabel("00:00")
        self.timer_label.setFont(QFont("Segoe UI", 12))
        self.mistakes_label = QLabel("Mistakes: 0/3")
        self.mistakes_label.setFont(QFont("Segoe UI", 10))
        stats_layout.addWidget(self.timer_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.mistakes_label)
        layout.addLayout(stats_layout)

        # Grid
        grid_frame = QFrame()
        grid_frame.setStyleSheet("background: transparent;")
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(9):
            row = []
            for j in range(9):
                cell = SudokuCell(i, j)
                cell.textChanged.connect(lambda text, r=i, c=j: self.on_cell_changed(r, c, text))
                if i % 3 == 2 and i != 8:
                    cell.setStyleSheet(cell.base_style().replace("border-bottom: 2px", "border-bottom: 4px"))
                if j % 3 == 2 and j != 8:
                    cell.setStyleSheet(cell.base_style().replace("border-right: 2px", "border-right: 4px"))
                grid_layout.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)

        # Add thick borders between 3x3 blocks
        for i in range(3, 9, 3):
            for j in range(9):
                cell = self.cells[i-1][j]
                style = cell.styleSheet()
                cell.setStyleSheet(style.replace("border-bottom: 2px", "border-bottom: 4px solid #1E1E1E;"))
        for j in range(3, 9, 3):
            for i in range(9):
                cell = self.cells[i][j-1]
                style = cell.styleSheet()
                cell.setStyleSheet(style.replace("border-right: 2px", "border-right: 4px solid #1E1E1E;"))

        layout.addWidget(grid_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        # Control buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.hint_btn = QPushButton()
        self.hint_btn.setFixedSize(120, 44)
        self.hint_btn.clicked.connect(self.give_hint)

        self.check_btn = QPushButton()
        self.check_btn.setFixedSize(120, 44)
        self.check_btn.clicked.connect(self.check_solution)

        self.new_btn = QPushButton()
        self.new_btn.setFixedSize(120, 44)
        self.new_btn.clicked.connect(self.trigger_new_game)

        btn_layout.addWidget(self.hint_btn)
        btn_layout.addSpacing(12)
        btn_layout.addWidget(self.check_btn)
        btn_layout.addSpacing(12)
        btn_layout.addWidget(self.new_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(8)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background: rgba(0, 0, 0, 0.1);
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0078D4, stop:1 #005A9E);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress)

    def trigger_new_game(self):
        if self.main_window:
            self.main_window.new_game()

    def update_texts(self):
        idx = QApplication.instance().property("lang_index") or 0
        texts = [
            ["Hint", "Check", "New Game", "Mistakes: {}/3", "Time: {}"],
            ["راهنمایی", "بررسی", "بازی جدید", "اشتباهات: {}/۳", "زمان: {}"],
            ["提示", "检查", "新游戏", "错误: {}/3", "时间: {}"],
            ["Подсказка", "Проверить", "Новая игра", "Ошибки: {}/3", "Время: {}"]
        ]
        t = texts[idx]
        self.hint_btn.setText(t[0])
        self.check_btn.setText(t[1])
        self.new_btn.setText(t[2])
        self.update_stats()

    def update_stats(self):
        mins, secs = divmod(self.elapsed, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        idx = QApplication.instance().property("lang_index") or 0
        mistake_text = ["Mistakes: {}/3", "اشتباهات: {}/۳", "错误: {}/3", "Ошибки: {}/3"][idx]
        self.mistakes_label.setText(mistake_text.format(self.mistakes))
        self.timer_label.setText(time_str)

        filled = sum(1 for i in range(9) for j in range(9) if self.board[i][j] != 0)
        self.progress.setValue(int(filled / 81 * 100))

    def start_timer(self):
        self.elapsed = 0
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def update_timer(self):
        self.elapsed += 1
        self.update_stats()

    def load_puzzle(self, puzzle, solution, difficulty):
        self.board = [row[:] for row in puzzle]
        self.solution = [row[:] for row in solution]
        self.mistakes = 0
        self.hints_used = 0
        self.start_timer()
        self.update_stats()

        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                if puzzle[i][j] != 0:
                    cell.set_fixed(puzzle[i][j])
                else:
                    cell.set_editable()
                    cell.setText("")

    def on_cell_changed(self, row, col, text):
        if not text:
            self.board[row][col] = 0
            return

        value = int(text)
        if value == self.solution[row][col]:
            self.board[row][col] = value
            self.cells[row][col].setStyleSheet(self.cells[row][col].base_style())
        else:
            self.board[row][col] = value
            self.cells[row][col].setStyleSheet(self.cells[row][col].base_style().replace(
                "color: #0078D4;", "color: #D40054;"
            ))
            self.mistakes += 1
            self.update_stats()
            if self.mistakes >= 3:
                self.show_game_over()

        if self.is_solved():
            self.stop_timer()
            self.puzzle_solved.emit()

    def is_solved(self):
        return all(self.board[i][j] == self.solution[i][j] for i in range(9) for j in range(9))

    def give_hint(self):
        empty_cells = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.cells[row][col].setText(str(self.solution[row][col]))
            self.cells[row][col].setReadOnly(True)
            self.cells[row][col].setStyleSheet(self.cells[row][col].base_style().replace(
                "color: #0078D4;", "color: #28A745;"
            ))
            self.hints_used += 1
            self.hint_used.emit()

    def check_solution(self):
        correct = all(self.board[i][j] == self.solution[i][j] or self.board[i][j] == 0
                      for i in range(9) for j in range(9))
        msg = QMessageBox()
        msg.setWindowTitle("Check")
        idx = QApplication.instance().property("lang_index") or 0
        if correct:
            msg.setText(["Correct so far!", "تا اینجا درست است!", "目前正确！", "Пока верно!"][idx])
            msg.setIcon(QMessageBox.Icon.Information)
        else:
            msg.setText(["There are mistakes!", "اشتباهاتی وجود دارد!", "有错误！", "Есть ошибки!"][idx])
            msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()

    def show_game_over(self):
        self.stop_timer()
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        idx = QApplication.instance().property("lang_index") or 0
        msg.setText(["Too many mistakes!", "اشتباهات زیاد!", "错误太多！", "Слишком много ошибок!"][idx])
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setFixedSize(900, 760)
        self.setWindowIcon(QIcon(self.resource_path("icon.ico")))
        self.difficulty = 0
        self.setup_ui()
        self.apply_theme("Windows Default")
        self.apply_language("en")

    def resource_path(self, path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, path)
        return os.path.join(os.path.abspath("."), path)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F8F9FA, stop:1 #E9ECEF); border-bottom: 1px solid #DEE2E6;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 20, 25, 20)

        title = QLabel("Sudoku")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #0078D4;")

        self.lang_selector = LanguageSelector()
        self.lang_selector.language_changed.connect(self.change_language)

        self.theme_selector = ThemeSelector()
        self.theme_selector.theme_changed.connect(self.apply_theme)

        self.diff_selector = DifficultySelector()
        self.diff_selector.difficulty_changed.connect(self.set_difficulty)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.diff_selector)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.lang_selector)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.theme_selector)

        # Game board - pass self as main_window
        self.game_board = SudokuBoard(main_window=self)
        self.game_board.puzzle_solved.connect(self.on_solved)
        self.game_board.hint_used.connect(self.on_hint)

        layout.addWidget(header)
        layout.addWidget(self.game_board, 1)

        self.new_game()

    def new_game(self):
        puzzle = SudokuSolver.generate_puzzle(self.difficulty)
        solution = copy.deepcopy(puzzle)
        SudokuSolver.solve(solution)
        self.game_board.load_puzzle(puzzle, solution, self.difficulty)

    def set_difficulty(self, level):
        self.difficulty = level
        self.new_game()

    def on_solved(self):
        msg = QMessageBox()
        msg.setWindowTitle("Congratulations!")
        idx = QApplication.instance().property("lang_index") or 0
        texts = [
            "Puzzle solved in {}!\nHints used: {}",
            "پازل در {} حل شد!\nراهنمایی‌های استفاده شده: {}",
            "在 {} 内解开谜题！\n使用提示：{}",
            "Загадка решена за {}!\nИспользовано подсказок: {}"
        ]
        mins, secs = divmod(self.game_board.elapsed, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        msg.setText(texts[idx].format(time_str, self.game_board.hints_used))
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def on_hint(self):
        pass  # Can add penalty

    def change_language(self, code):
        idx = ["en", "fa", "zh", "ru"].index(code)
        QApplication.instance().setProperty("lang_index", idx)
        self.lang_selector.combo.blockSignals(True)
        self.lang_selector.combo.setCurrentIndex(idx)
        self.lang_selector.combo.blockSignals(False)
        self.lang_selector.update_text()
        self.theme_selector.update_text()
        self.diff_selector.update_text()
        self.game_board.update_texts()

        rtl = code in ["fa"]
        direction = Qt.LayoutDirection.RightToLeft if rtl else Qt.LayoutDirection.LeftToRight
        self.setLayoutDirection(direction)
        self.game_board.setLayoutDirection(direction)

    def apply_language(self, code):
        pass  # Manual translation via update_texts

    def apply_theme(self, theme):
        app = QApplication.instance()
        palette = QPalette()

        styles = {
            "Dark": self.dark_style(),
            "Light": self.light_style(),
            "Blue": self.blue_style(),
            "Red": self.red_style(),
            "Windows Default": self.windows_style()
        }
        app.setStyleSheet(styles.get(theme, self.windows_style()))

        palettes = {
            "Dark": self.dark_palette(),
            "Light": self.light_palette(),
            "Blue": self.blue_palette(),
            "Red": self.red_palette(),
            "Windows Default": QApplication.style().standardPalette()
        }
        app.setPalette(palettes.get(theme, QApplication.style().standardPalette()))
        self.update()

    def dark_style(self):
        return """
        QMainWindow, QWidget { background: #1E1E1E; color: #FFFFFF; }
        QFrame { background: transparent; }
        QLabel { color: #FFFFFF; }
        QPushButton { background: #2D2D2D; border: 1px solid #404040; border-radius: 8px; padding: 10px; color: #FFFFFF; }
        QPushButton:hover { background: #3A3A3A; border: 1px solid #0078D4; }
        QComboBox { background: #2D2D2D; border: 1px solid #404040; border-radius: 8px; padding: 8px; color: #FFFFFF; }
        """

    def light_style(self):
        return """
        QMainWindow, QWidget { background: #FFFFFF; color: #000000; }
        QLabel { color: #000000; }
        QPushButton { background: #E9ECEF; border: 1px solid #CED4DA; border-radius: 8px; padding: 10px; color: #000000; }
        QPushButton:hover { background: #DEE2E6; border: 1px solid #0078D4; }
        """

    def blue_style(self):
        return """
        QMainWindow, QWidget { background: #F8F9FF; color: #00008B; }
        QLabel { color: #00008B; }
        QPushButton { background: #E3F2FD; border: 1px solid #90CAF9; border-radius: 8px; padding: 10px; color: #00008B; }
        QPushButton:hover { background: #BBDEFB; border: 1px solid #0078D4; }
        """

    def red_style(self):
        return """
        QMainWindow, QWidget { background: #FFF5F5; color: #8B0000; }
        QLabel { color: #8B0000; }
        QPushButton { background: #FFEBEE; border: 1px solid #FFCDD2; border-radius: 8px; padding: 10px; color: #8B0000; }
        QPushButton:hover { background: #FFCDD2; border: 1px solid #D40054; }
        """

    def windows_style(self):
        return """
        QMainWindow, QWidget { background: #F3F4F6; color: #000000; }
        QLabel { color: #000000; }
        QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F8F9FA, stop:1 #E9ECEF); border: 1px solid #DEE2E6; border-radius: 8px; padding: 10px; color: #000000; }
        QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E9ECEF, stop:1 #DEE2E6); border: 1px solid #0078D4; }
        """

    def dark_palette(self):
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        p.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        p.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        p.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        p.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        p.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        return p

    def light_palette(self):
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        p.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        p.setColor(QPalette.ColorRole.Base, QColor(240, 240, 240))
        p.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        return p

    def blue_palette(self):
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, QColor(248, 249, 255))
        p.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 139))
        p.setColor(QPalette.ColorRole.Base, QColor(240, 245, 255))
        p.setColor(QPalette.ColorRole.Text, QColor(0, 0, 139))
        return p

    def red_palette(self):
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, QColor(255, 245, 245))
        p.setColor(QPalette.ColorRole.WindowText, QColor(139, 0, 0))
        p.setColor(QPalette.ColorRole.Base, QColor(255, 235, 235))
        p.setColor(QPalette.ColorRole.Text, QColor(139, 0, 0))
        return p

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setProperty("lang_index", 0)

    window = MainWindow()
    window.show()

    app.setStyleSheet("""
        QToolTip { background: #FFFFFF; color: #000000; border: 1px solid #CCCCCC; padding: 5px; border-radius: 6px; }
    """)

    sys.exit(app.exec())
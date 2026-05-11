# ============================================================
#  ui_settings.py – Dialog cài đặt ván chơi
# ============================================================
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QGroupBox,
    QRadioButton, QButtonGroup, QFrame, QCheckBox, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette

from constants import (
    MODE_PVP, MODE_PVC, MODE_CVC,
    PLAYER_1, PLAYER_2,
    DIFF_EASY, DIFF_MEDIUM, DIFF_HARD, DIFF_EXPERT,
    MIN_BOARD, MAX_BOARD, DEFAULT_WIN_LENGTH,
    get_win_length_options,
    COLOR_BG, COLOR_BG2, COLOR_PANEL, COLOR_BORDER,
    COLOR_ACCENT1, COLOR_ACCENT2, COLOR_PLAYER1, COLOR_PLAYER2,
)
from game import GameConfig


DIFFS = [DIFF_EASY, DIFF_MEDIUM, DIFF_HARD, DIFF_EXPERT]

STYLE = f"""
QDialog {{
    background: {COLOR_BG};
    color: #e0e0f0;
}}
QGroupBox {{
    background: {COLOR_PANEL};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    margin-top: 12px;
    color: #c0c0e0;
    font-weight: bold;
    font-size: 12px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
    color: {COLOR_ACCENT1};
}}
QLabel {{
    color: #c0c0e0;
    font-size: 12px;
}}
QComboBox, QSpinBox {{
    background: {COLOR_BG2};
    border: 1px solid {COLOR_BORDER};
    border-radius: 5px;
    color: #e0e0f0;
    padding: 5px 8px;
    font-size: 12px;
    min-width: 80px;
}}
QComboBox:hover, QSpinBox:hover {{
    border-color: {COLOR_ACCENT1};
}}
QComboBox QAbstractItemView {{
    background: {COLOR_BG2};
    color: #e0e0f0;
    selection-background-color: {COLOR_ACCENT1};
    border: 1px solid {COLOR_BORDER};
}}
QRadioButton {{
    color: #c0c0e0;
    font-size: 12px;
    spacing: 6px;
}}
QRadioButton::indicator {{
    width: 14px; height: 14px;
    border-radius: 7px;
    border: 2px solid {COLOR_BORDER};
    background: {COLOR_BG2};
}}
QRadioButton::indicator:checked {{
    background: {COLOR_ACCENT1};
    border-color: {COLOR_ACCENT1};
}}
QCheckBox {{
    color: #c0c0e0;
    font-size: 12px;
}}
QCheckBox::indicator {{
    width: 14px; height: 14px;
    border-radius: 3px;
    border: 2px solid {COLOR_BORDER};
    background: {COLOR_BG2};
}}
QCheckBox::indicator:checked {{
    background: {COLOR_ACCENT1};
    border-color: {COLOR_ACCENT1};
}}
QPushButton {{
    border-radius: 7px;
    font-size: 13px;
    font-weight: bold;
    padding: 10px 24px;
    border: none;
}}
QPushButton#btnStart {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {COLOR_ACCENT1}, stop:1 {COLOR_ACCENT2});
    color: white;
}}
QPushButton#btnStart:hover {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #9575ff, stop:1 #ff7599);
}}
QPushButton#btnCancel {{
    background: {COLOR_PANEL};
    color: #888;
    border: 1px solid {COLOR_BORDER};
}}
QPushButton#btnCancel:hover {{
    background: {COLOR_BORDER};
    color: #ccc;
}}
"""


class SettingsDialog(QDialog):
    config_ready = pyqtSignal(object)   # GameConfig

    def __init__(self, parent=None, current: GameConfig = None):
        super().__init__(parent)
        self.setWindowTitle("⚙  Cài đặt ván chơi")
        self.setMinimumWidth(520)
        self.setStyleSheet(STYLE)
        self.setModal(True)

        cfg = current or GameConfig()
        self._build_ui(cfg)
        self._on_mode_changed()
        self._on_board_changed()

    # ── Xây UI ──────────────────────────────────────────────
    def _build_ui(self, cfg: GameConfig):
        root = QVBoxLayout(self)
        root.setSpacing(12)
        root.setContentsMargins(20, 20, 20, 20)

        # Tiêu đề
        title = QLabel("CÀI ĐẶT VÁN CHƠI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 18px; font-weight: 900; letter-spacing: 3px;
            color: {COLOR_ACCENT1}; padding-bottom: 6px;
        """)
        root.addWidget(title)

        # ── Chế độ chơi ──────────────────────────────────────
        grp_mode = QGroupBox("Chế độ chơi")
        lay_mode = QHBoxLayout(grp_mode)
        lay_mode.setContentsMargins(14, 18, 14, 12)
        self._rb_pvp = QRadioButton("🧑 Người vs Người")
        self._rb_pvc = QRadioButton("🧑 Người vs 🤖 Máy")
        self._rb_cvc = QRadioButton("🤖 Máy vs 🤖 Máy")
        self._mode_grp = QButtonGroup()
        for rb in (self._rb_pvp, self._rb_pvc, self._rb_cvc):
            self._mode_grp.addButton(rb)
            lay_mode.addWidget(rb)
        {MODE_PVP: self._rb_pvp, MODE_PVC: self._rb_pvc,
         MODE_CVC: self._rb_cvc}.get(cfg.mode, self._rb_pvp).setChecked(True)
        self._mode_grp.buttonClicked.connect(self._on_mode_changed)
        root.addWidget(grp_mode)

        # ── Bàn cờ ───────────────────────────────────────────
        grp_board = QGroupBox("Bàn cờ")
        lay_board = QGridLayout(grp_board)
        lay_board.setContentsMargins(14, 18, 14, 12)
        lay_board.setSpacing(10)

        lay_board.addWidget(QLabel("Kích thước:"), 0, 0)
        self._spin_size = QSpinBox()
        self._spin_size.setRange(MIN_BOARD, MAX_BOARD)
        self._spin_size.setValue(cfg.board_size)
        self._spin_size.setSuffix(" × " + str(cfg.board_size))
        self._spin_size.valueChanged.connect(self._on_board_changed)
        lay_board.addWidget(self._spin_size, 0, 1)

        lay_board.addWidget(QLabel("Số quân liên tiếp để thắng:"), 0, 2)
        self._combo_win = QComboBox()
        lay_board.addWidget(self._combo_win, 0, 3)

        lay_board.addWidget(QLabel("Số hiệp thắng:"), 1, 0)
        self._spin_wins = QSpinBox()
        self._spin_wins.setRange(1, 20)
        self._spin_wins.setValue(cfg.wins_needed)
        lay_board.addWidget(self._spin_wins, 1, 1)

        lay_board.addWidget(QLabel("Người đi trước:"), 1, 2)
        self._combo_first = QComboBox()
        self._combo_first.addItems(["Người chơi 1 (X)", "Người chơi 2 (O)"])
        self._combo_first.setCurrentIndex(0 if cfg.first_player == PLAYER_1 else 1)
        lay_board.addWidget(self._combo_first, 1, 3)

        root.addWidget(grp_board)

        # ── Cài đặt AI ───────────────────────────────────────
        self._grp_ai = QGroupBox("Cài đặt AI")
        lay_ai = QGridLayout(self._grp_ai)
        lay_ai.setContentsMargins(14, 18, 14, 12)
        lay_ai.setSpacing(10)

        # AI 1 (Người chơi 1 / Máy 1)
        self._lbl_ai1 = QLabel("🤖 Máy 1 (X) – Độ khó:")
        lay_ai.addWidget(self._lbl_ai1, 0, 0)
        self._combo_diff1 = QComboBox()
        self._combo_diff1.addItems(DIFFS)
        self._combo_diff1.setCurrentText(cfg.diff_ai1)
        lay_ai.addWidget(self._combo_diff1, 0, 1)

        self._chk_ai1 = QCheckBox("Bật Máy 1")
        self._chk_ai1.setChecked(cfg.ai1_enabled)
        lay_ai.addWidget(self._chk_ai1, 0, 2)

        # AI 2 (Máy 2)
        lay_ai.addWidget(QLabel("🤖 Máy 2 (O) – Độ khó:"), 1, 0)
        self._combo_diff2 = QComboBox()
        self._combo_diff2.addItems(DIFFS)
        self._combo_diff2.setCurrentText(cfg.diff_ai2)
        lay_ai.addWidget(self._combo_diff2, 1, 1)

        self._chk_ai2 = QCheckBox("Bật Máy 2")
        self._chk_ai2.setChecked(cfg.ai2_enabled)
        lay_ai.addWidget(self._chk_ai2, 1, 2)

        root.addWidget(self._grp_ai)

        # ── Nút ──────────────────────────────────────────────
        row_btn = QHBoxLayout()
        btn_cancel = QPushButton("Huỷ")
        btn_cancel.setObjectName("btnCancel")
        btn_cancel.clicked.connect(self.reject)
        btn_start = QPushButton("▶  Bắt đầu")
        btn_start.setObjectName("btnStart")
        btn_start.clicked.connect(self._on_start)
        row_btn.addWidget(btn_cancel)
        row_btn.addStretch()
        row_btn.addWidget(btn_start)
        root.addLayout(row_btn)

    # ── Slot ────────────────────────────────────────────────
    def _on_mode_changed(self):
        mode = self._current_mode()
        show_ai  = mode in (MODE_PVC, MODE_CVC)
        show_ai1 = mode == MODE_CVC
        self._grp_ai.setVisible(show_ai)
        self._lbl_ai1.setVisible(show_ai1)
        self._combo_diff1.setVisible(show_ai1)
        self._chk_ai1.setVisible(show_ai1)
        # PVC: chỉ hiện AI2 (Máy là O)
        if mode == MODE_PVC:
            self._lbl_ai1.setVisible(False)

    def _on_board_changed(self):
        size = self._spin_size.value()
        self._spin_size.setSuffix(f" × {size}")
        opts = get_win_length_options(size)
        current = self._combo_win.currentText()
        self._combo_win.blockSignals(True)
        self._combo_win.clear()
        for o in opts:
            self._combo_win.addItem(str(o))
        # Khôi phục giá trị nếu hợp lệ
        if current and int(current) in opts:
            self._combo_win.setCurrentText(current)
        else:
            self._combo_win.setCurrentText(str(DEFAULT_WIN_LENGTH.get(size, opts[0])))
        self._combo_win.blockSignals(False)

    def _on_start(self):
        mode = self._current_mode()
        cfg  = GameConfig(
            board_size   = self._spin_size.value(),
            win_length   = int(self._combo_win.currentText()),
            mode         = mode,
            first_player = PLAYER_1 if self._combo_first.currentIndex() == 0 else PLAYER_2,
            wins_needed  = self._spin_wins.value(),
            diff_ai1     = self._combo_diff1.currentText(),
            diff_ai2     = self._combo_diff2.currentText(),
            ai1_enabled  = self._chk_ai1.isChecked(),
            ai2_enabled  = self._chk_ai2.isChecked(),
        )
        self.config_ready.emit(cfg)
        self.accept()

    def _current_mode(self) -> str:
        if self._rb_pvp.isChecked(): return MODE_PVP
        if self._rb_pvc.isChecked(): return MODE_PVC
        return MODE_CVC

# ============================================================
#  constants.py – Hằng số và cấu hình toàn dự án
# ============================================================

# ── Chế độ chơi ──────────────────────────────────────────────
MODE_PVP   = "pvp"    # Người vs Người
MODE_PVC   = "pvc"    # Người vs Máy
MODE_CVC   = "cvc"    # Máy vs Máy

# ── Người chơi ───────────────────────────────────────────────
PLAYER_1   = 1        # X
PLAYER_2   = 2        # O
EMPTY      = 0

PLAYER_SYMBOL = {PLAYER_1: "X", PLAYER_2: "O", EMPTY: ""}

# ── Độ khó ───────────────────────────────────────────────────
DIFF_EASY   = "Dễ"
DIFF_MEDIUM = "Trung bình"
DIFF_HARD   = "Khó"
DIFF_EXPERT = "Siêu khó"

# Số tầng tìm kiếm (depth) theo độ khó và kích thước bàn cờ
# Format: {board_size: {difficulty: depth}}
DEPTH_TABLE = {
    3:  {DIFF_EASY: 1, DIFF_MEDIUM: 3, DIFF_HARD: 6,  DIFF_EXPERT: 9},
    4:  {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 4,  DIFF_EXPERT: 6},
    5:  {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 3,  DIFF_EXPERT: 5},
    6:  {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 3,  DIFF_EXPERT: 4},
    7:  {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 3,  DIFF_EXPERT: 4},
    8:  {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 3,  DIFF_EXPERT: 4},
    9:  {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 3,  DIFF_EXPERT: 3},
    10: {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 3,  DIFF_EXPERT: 3},
    11: {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 2,  DIFF_EXPERT: 3},
    12: {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 2,  DIFF_EXPERT: 3},
    13: {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 2,  DIFF_EXPERT: 3},
    14: {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 2,  DIFF_EXPERT: 3},
    15: {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 2,  DIFF_EXPERT: 2},
    16: {DIFF_EASY: 1, DIFF_MEDIUM: 2, DIFF_HARD: 2,  DIFF_EXPERT: 2},
}

def get_depth(board_size: int, difficulty: str) -> int:
    size = min(max(board_size, 3), 16)
    return DEPTH_TABLE.get(size, DEPTH_TABLE[16]).get(difficulty, 2)

# ── Kích thước bàn cờ ────────────────────────────────────────
MIN_BOARD = 3
MAX_BOARD = 16

# Số quân liên tiếp tối thiểu để thắng theo kích thước
DEFAULT_WIN_LENGTH = {
    3:  3,
    4:  3,
    5:  4,
    6:  4,
    7:  5,
    8:  5,
    9:  5,
    10: 5,
    11: 5,
    12: 5,
    13: 5,
    14: 5,
    15: 5,
    16: 5,
}

def get_win_length_options(board_size: int) -> list:
    """Trả về danh sách số quân liên tiếp hợp lệ cho kích thước bàn."""
    if board_size == 3:
        return [3]
    elif board_size == 4:
        return [3, 4]
    elif board_size == 5:
        return [3, 4, 5]
    elif board_size <= 8:
        return [3, 4, 5, board_size] if board_size > 5 else [3, 4, 5]
    else:
        return [3, 4, 5, 6]

# ── Giao diện ────────────────────────────────────────────────
WINDOW_MIN_W = 1100
WINDOW_MIN_H = 700

# Màu sắc palette (dark theme)
COLOR_BG          = "#0f0f1a"
COLOR_BG2         = "#16162a"
COLOR_PANEL       = "#1e1e35"
COLOR_BORDER      = "#2e2e55"
COLOR_ACCENT1     = "#7c5cfc"   # Tím chính
COLOR_ACCENT2     = "#fc5c7d"   # Hồng accent
COLOR_PLAYER1     = "#5cf5fc"   # Xanh cyan – X
COLOR_PLAYER2     = "#fc9a5c"   # Cam – O
COLOR_EMPTY       = "#2a2a4a"
COLOR_HOVER       = "#3a3a6a"
COLOR_WIN_CELL    = "#ffd700"   # Vàng – ô thắng

# Màu heatmap AI
COLOR_HEAT_LOW    = "#1a3a1a"   # Xanh đậm – điểm thấp
COLOR_HEAT_MID    = "#4a4a00"   # Vàng đậm – điểm trung bình
COLOR_HEAT_HIGH   = "#4a0000"   # Đỏ đậm – điểm cao

COLOR_PRUNED      = "#333355"   # Ô bị cắt tỉa
COLOR_EVALUATED   = "#2a4a2a"   # Ô đã đánh giá

# ── Tốc độ máy vs máy ────────────────────────────────────────
CVC_DELAY_MS = 800   # ms giữa các nước đi của máy

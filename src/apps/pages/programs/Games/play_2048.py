import pygame
import random
import numpy as np
import streamlit as st

# Constants
GRID_SIZE = 4
CELL_SIZE = 100
WINNING_TILE = 2048

# Colors
GRID_COLOR = (187, 173, 160)
CELL_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Game Functions
def init_game():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

def add_random_tile(grid):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i, j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i, j] = random.choice([2, 4])

def move_left(grid):
    new_grid = np.zeros_like(grid)
    for i in range(GRID_SIZE):
        pos = 0
        for j in range(GRID_SIZE):
            if grid[i, j] != 0:
                if new_grid[i, pos] == 0:
                    new_grid[i, pos] = grid[i, j]
                elif new_grid[i, pos] == grid[i, j]:
                    new_grid[i, pos] *= 2
                    pos += 1
                else:
                    pos += 1
                    new_grid[i, pos] = grid[i, j]
    return new_grid

def move_right(grid):
    new_grid = np.fliplr(grid)
    new_grid = move_left(new_grid)
    return np.fliplr(new_grid)

def move_up(grid):
    new_grid = np.transpose(grid)
    new_grid = move_left(new_grid)
    return np.transpose(new_grid)

def move_down(grid):
    new_grid = np.transpose(grid)
    new_grid = move_right(new_grid)
    return np.transpose(new_grid)

def check_win(grid):
    return np.any(grid == WINNING_TILE)

def check_game_over(grid):
    if np.any(grid == 0):
        return False
    if np.any(grid == move_left(grid)) or np.any(grid == move_right(grid)) or np.any(grid == move_up(grid)) or np.any(grid == move_down(grid)):
        return False
    return True

# 2048 Game in Streamlit
def play_2048():
    st.title("🎮 2048 Game 🎮")

    def initialize_game():
        st.session_state.grid = init_game()
        st.session_state.won = False
        st.session_state.game_over = False

    # Initialize grid and game state
    if "grid" not in st.session_state:
        initialize_game()

    # Display the 2048 grid
    with st.container():
        st.subheader("2048 Board")
        for row in st.session_state.grid:
            cols = st.columns(GRID_SIZE)
            for j, val in enumerate(row):
                cols[j].button(
                    label=str(val) if val != 0 else " ",
                    key=f"{j}",
                    disabled=True,
                    help="This is a tile."
                )

        # Check win or game over
        if st.session_state.won:
            st.success("🎉 Congratulations! You won by reaching 2048! 🎉")
        elif st.session_state.game_over:
            st.error("Game Over! No more valid moves! 💀")
        else:
            st.write("Keep going!")

    # Handle key events
    key_press = st.selectbox("Move the tiles", ["", "Left", "Right", "Up", "Down"])

    if key_press:
        if key_press == "Left":
            st.session_state.grid = move_left(st.session_state.grid)
        elif key_press == "Right":
            st.session_state.grid = move_right(st.session_state.grid)
        elif key_press == "Up":
            st.session_state.grid = move_up(st.session_state.grid)
        elif key_press == "Down":
            st.session_state.grid = move_down(st.session_state.grid)

        # Add a random tile and check for game state
        add_random_tile(st.session_state.grid)

        if check_win(st.session_state.grid):
            st.session_state.won = True
        elif check_game_over(st.session_state.grid):
            st.session_state.game_over = True

    # Restart button
    if st.button("Restart Game"):
        initialize_game()
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global variable to store the board and the current player
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'

# Function to check for a win
def check_win(board, player):
    # Check rows, columns and diagonals
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

# Function to check if the board is full
def is_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Route for the game board
@app.route('/')
def index():
    global current_player
    return render_template('index.html', board=board, current_player=current_player)

# Route to handle a move
@app.route('/move', methods=['POST'])
def move():
    global current_player
    
    # Get the row and column from the form input
    move_data = request.form['move']
    row, col = map(int, move_data.split('-'))
    
    # If the selected spot is empty, update the board
    if board[row][col] == ' ':
        board[row][col] = current_player
        
        # Check if current player wins
        if check_win(board, current_player):
            return render_template('game_over.html', winner=current_player)
        
        # Check for draw
        if is_full(board):
            return render_template('game_over.html', winner="Draw")

        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'
    
    return redirect(url_for('index'))


# Route to reset the game
@app.route('/reset', methods=['POST'])
def reset():
    global board, current_player
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

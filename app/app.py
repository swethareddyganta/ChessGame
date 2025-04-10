from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import chess
import json
import os
import threading
from models.chess_rl_agent import ChessRLAgent

app = Flask(__name__)
CORS(app)

agent = ChessRLAgent()
board = chess.Board()

# Load existing model if available
if os.path.exists("chess_rl_model.pkl"):
    agent.load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    global board
    board = chess.Board()
    return jsonify({
        'fen': board.fen(),
        'legal_moves': [move.uci() for move in board.legal_moves]
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    global board
    data = request.json
    move_uci = data.get('move')
    
    if move_uci:
        try:
            move = chess.Move.from_uci(move_uci)
            if move in board.legal_moves:
                # Make human move
                board.push(move)
                
                # Check if game is over after human move
                if board.is_game_over():
                    return jsonify({
                        'fen': board.fen(),
                        'game_over': True,
                        'result': get_game_result()
                    })
                
                # AI's turn
                ai_move = agent.choose_action(board)
                board.push(ai_move)
                
                # Update Q-values
                last_state = agent.get_state_key(board)
                reward = agent.get_reward(board)
                agent.update_q_value(last_state, ai_move.uci(), reward, agent.get_state_key(board))
                
                return jsonify({
                    'fen': board.fen(),
                    'ai_move': ai_move.uci(),
                    'legal_moves': [move.uci() for move in board.legal_moves],
                    'game_over': board.is_game_over(),
                    'result': get_game_result() if board.is_game_over() else None
                })
        except ValueError as e:
            return jsonify({'error': f'Invalid move: {str(e)}'}), 400
    
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/train_ai', methods=['POST'])
def train_ai():
    num_games = request.json.get('num_games', 100)  # Default to 100 games if not specified
    thread = threading.Thread(target=train_agent_in_background, args=(num_games,))
    thread.daemon = True
    thread.start()
    return jsonify({'status': 'Training started'})

def train_agent_in_background(num_games):
    """Train the agent in a background thread."""
    for game in range(num_games):
        board = chess.Board()
        while not board.is_game_over():
            move = agent.choose_action(board)
            last_state = agent.get_state_key(board)
            board.push(move)
            current_state = agent.get_state_key(board)
            reward = agent.get_reward(board)
            agent.update_q_value(last_state, move.uci(), reward, current_state)
        
        if (game + 1) % 10 == 0:
            print(f"Completed game {game + 1}/{num_games}")
            agent.save_model()
    
    print("Training completed!")
    agent.save_model()

def get_game_result():
    if board.is_checkmate():
        return "Checkmate! " + ("Black" if board.turn == chess.WHITE else "White") + " wins!"
    elif board.is_stalemate():
        return "Stalemate!"
    elif board.is_insufficient_material():
        return "Draw by insufficient material!"
    return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 
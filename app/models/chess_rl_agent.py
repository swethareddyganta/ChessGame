import chess
import random
import pickle
import os
from typing import Dict, Optional

class ChessRLAgent:
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9, exploration_rate: float = 0.3):
        self.q_table: Dict[str, Dict[str, float]] = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        
    def get_state_key(self, board: chess.Board) -> str:
        """Convert board position to a string key."""
        return board.fen()
    
    def get_legal_actions(self, board: chess.Board) -> Dict[str, chess.Move]:
        """Get all legal moves as a dictionary of move strings to Move objects."""
        return {move.uci(): move for move in board.legal_moves}
    
    def get_q_value(self, state: str, action: str) -> float:
        """Get Q-value for a state-action pair."""
        return self.q_table.get(state, {}).get(action, 0.0)
    
    def update_q_value(self, state: str, action: str, reward: float, next_state: str) -> None:
        """Update Q-value using Q-learning update rule."""
        if state not in self.q_table:
            self.q_table[state] = {}
        
        current_q = self.get_q_value(state, action)
        next_max_q = max([self.get_q_value(next_state, a) for a in self.get_legal_actions(chess.Board(next_state))], default=0.0)
        
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state][action] = new_q
    
    def choose_action(self, board: chess.Board) -> chess.Move:
        """Choose an action using epsilon-greedy strategy."""
        state = self.get_state_key(board)
        legal_actions = self.get_legal_actions(board)
        
        if random.random() < self.exploration_rate:
            # Exploration: choose random action
            return random.choice(list(legal_actions.values()))
        else:
            # Exploitation: choose best action
            if state not in self.q_table or not self.q_table[state]:
                return random.choice(list(legal_actions.values()))
            
            # Get the action with highest Q-value
            best_action = max(legal_actions.keys(), key=lambda a: self.get_q_value(state, a))
            return legal_actions[best_action]
    
    def get_reward(self, board: chess.Board) -> float:
        """Calculate reward based on game outcome."""
        if board.is_checkmate():
            return 100.0 if board.turn == chess.BLACK else -100.0
        elif board.is_stalemate():
            return 0.0
        else:
            # Simple material-based reward
            piece_values = {
                chess.PAWN: 1,
                chess.KNIGHT: 3,
                chess.BISHOP: 3,
                chess.ROOK: 5,
                chess.QUEEN: 9,
                chess.KING: 0
            }
            
            score = 0
            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece:
                    value = piece_values[piece.piece_type]
                    if piece.color == chess.WHITE:
                        score += value
                    else:
                        score -= value
            return score
    
    def save_model(self, filename: str = "chess_rl_model.pkl") -> None:
        """Save the Q-table to a file."""
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)
    
    def load_model(self, filename: str = "chess_rl_model.pkl") -> None:
        """Load the Q-table from a file."""
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f) 
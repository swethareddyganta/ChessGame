# Chess Game with Reinforcement Learning AI

A web-based chess game implementation with a reinforcement learning AI opponent. The AI uses Q-learning to improve its gameplay through self-play training.

## Features

- Interactive web-based chess board
- Legal move validation and highlighting
- Move history display
- AI opponent using reinforcement learning
- Training capability for the AI
- Responsive design for different screen sizes

## Requirements

- Python 3.7 or higher
- Flask 2.0.1
- Flask-CORS 3.0.10
- python-chess 1.999.0
- Werkzeug 2.0.1

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd chess_game_project
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app/app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5001
```

## Playing the Game

1. The game starts with you playing as White
2. Click on a piece to see its legal moves
3. Click on a highlighted square to make your move
4. The AI will automatically respond with its move
5. Use the "New Game" button to start a fresh game
6. Use the "Train AI" button to improve the AI through self-play

## Training the AI

1. Click the "Train AI" button to start training
2. The AI will play against itself for the specified number of games
3. Training progress is displayed in the server console
4. The AI model is automatically saved every 10 games
5. You can continue playing while the AI trains in the background

## Project Structure

```
chess_game_project/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   ├── templates/
│   │   └── index.html
│   ├── models/
│   │   └── chess_rl_agent.py
│   └── app.py
├── tests/
├── config/
├── requirements.txt
└── README.md
```

## How the AI Works

The AI uses Q-learning, a reinforcement learning algorithm, with the following components:

- State: Current board position (FEN notation)
- Actions: Legal chess moves
- Reward: Based on material advantage and game outcome
- Q-table: Stores state-action values
- Exploration: Epsilon-greedy strategy

The AI improves by:
1. Playing games against itself
2. Learning from the outcomes
3. Updating its Q-values
4. Saving the learned knowledge

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
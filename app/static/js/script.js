// Initialize chess game
const game = new Chess();
let selectedSquare = null;

// Create chess board
function createBoard() {
    const board = document.querySelector('.chess-board');
    board.innerHTML = '';
    
    // Create board squares from black's perspective (a8 to h1)
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.className = `square ${(row + col) % 2 === 0 ? 'white' : 'black'}`;
            square.dataset.row = row;
            square.dataset.col = col;
            square.addEventListener('click', handleSquareClick);
            board.appendChild(square);
        }
    }
    
    updateBoard();
}

// Update board display
function updateBoard() {
    const squares = document.querySelectorAll('.square');
    squares.forEach(square => {
        const row = parseInt(square.dataset.row);
        const col = parseInt(square.dataset.col);
        const piece = game.board()[row][col];
        
        // Clear previous piece
        square.dataset.piece = '';
        square.classList.remove('selected', 'highlight');
        
        // Set new piece if exists
        if (piece) {
            const symbol = getPieceSymbol(piece);
            square.dataset.piece = symbol;
        }
    });
}

// Get Unicode symbol for chess piece
function getPieceSymbol(piece) {
    const symbols = {
        'p': '♟', 'P': '♙',
        'n': '♞', 'N': '♘',
        'b': '♝', 'B': '♗',
        'r': '♜', 'R': '♖',
        'q': '♛', 'Q': '♕',
        'k': '♚', 'K': '♔'
    };
    return symbols[piece.color === 'w' ? piece.type.toUpperCase() : piece.type.toLowerCase()];
}

// Handle square click
function handleSquareClick(event) {
    const square = event.target.closest('.square');
    if (!square) return;

    const row = parseInt(square.dataset.row);
    const col = parseInt(square.dataset.col);
    const moveFrom = selectedSquare ? 
        algebraic(parseInt(selectedSquare.dataset.row), parseInt(selectedSquare.dataset.col)) : null;
    const moveTo = algebraic(row, col);

    if (selectedSquare) {
        // Try to make the move
        const move = {
            from: moveFrom,
            to: moveTo,
            promotion: 'q' // Always promote to queen for simplicity
        };

        try {
            const result = game.move(move);
            if (result) {
                updateBoard();
                clearHighlights();
                selectedSquare = null;

                // Add move to history
                addMoveToHistory(moveFrom + moveTo);

                // Make AI move
                setTimeout(makeAIMove, 300);
            } else {
                // Invalid move, try selecting new piece
                clearHighlights();
                trySelectPiece(square);
            }
        } catch (e) {
            console.error('Invalid move:', e);
            clearHighlights();
            trySelectPiece(square);
        }
    } else {
        trySelectPiece(square);
    }
}

// Try to select a piece
function trySelectPiece(square) {
    const row = parseInt(square.dataset.row);
    const col = parseInt(square.dataset.col);
    const piece = game.board()[row][col];

    if (piece && piece.color === (game.turn() === 'w' ? 'w' : 'b')) {
        selectedSquare = square;
        square.classList.add('selected');
        highlightLegalMoves(row, col);
    }
}

// Convert row/col to algebraic notation
function algebraic(row, col) {
    return String.fromCharCode(97 + col) + (8 - row);
}

// Highlight legal moves
function highlightLegalMoves(row, col) {
    const moves = game.moves({ square: algebraic(row, col), verbose: true });
    moves.forEach(move => {
        const targetRow = 8 - parseInt(move.to[1]);
        const targetCol = move.to.charCodeAt(0) - 97;
        const targetSquare = document.querySelector(
            `.square[data-row="${targetRow}"][data-col="${targetCol}"]`
        );
        if (targetSquare) {
            targetSquare.classList.add('highlight');
        }
    });
}

// Clear all highlights
function clearHighlights() {
    document.querySelectorAll('.square').forEach(square => {
        square.classList.remove('selected', 'highlight');
    });
}

// Make AI move
function makeAIMove() {
    if (game.game_over()) {
        updateGameStatus();
        return;
    }

    const moves = game.moves();
    if (moves.length > 0) {
        const move = moves[Math.floor(Math.random() * moves.length)];
        game.move(move);
        updateBoard();
        updateGameStatus();
        addMoveToHistory(move);
    }
}

// Update game status
function updateGameStatus() {
    const status = document.getElementById('gameStatus');
    if (game.game_over()) {
        if (game.in_checkmate()) {
            status.textContent = `Game Over - ${game.turn() === 'w' ? 'Black' : 'White'} wins by checkmate!`;
        } else if (game.in_draw()) {
            status.textContent = 'Game Over - Draw!';
        } else if (game.in_stalemate()) {
            status.textContent = 'Game Over - Stalemate!';
        }
    } else {
        status.textContent = `${game.turn() === 'w' ? 'White' : 'Black'} to move`;
    }
}

// Add move to history
function addMoveToHistory(move) {
    const moveHistory = document.getElementById('moveHistory');
    const moveElement = document.createElement('div');
    moveElement.className = 'move';
    moveElement.textContent = `${game.turn() === 'w' ? 'Black' : 'White'}: ${move}`;
    moveHistory.appendChild(moveElement);
    moveHistory.scrollTop = moveHistory.scrollHeight;
}

// Start new game
function startNewGame() {
    game.reset();
    selectedSquare = null;
    createBoard();
    updateGameStatus();
    document.getElementById('moveHistory').innerHTML = '';
}

// Initialize game
document.addEventListener('DOMContentLoaded', () => {
    createBoard();
    document.getElementById('newGame').addEventListener('click', startNewGame);
    document.getElementById('trainAI').addEventListener('click', function() {
        const status = document.getElementById('gameStatus');
        status.textContent = 'Training AI for 1000 games...';
        $.ajax({
            url: '/train_ai',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ num_games: 1000 }),
            success: function(response) {
                status.textContent = 'AI training started! This may take a while...';
            },
            error: function(error) {
                status.textContent = 'Error starting AI training.';
                console.error('Error:', error);
            }
        });
    });
}); 
# Lichess link (Open DB): https://database.lichess.org/#puzzles
# Last Date: This file was last updated on 06/11/2024.

import chess;
import chess.svg;
import pandas as pd;
import telegram;
from cairosvg import svg2png;
from datetime import datetime;
import asyncio;

# Telegram Bot Token and Channel
BOT_TOKEN_TEST = '8083520152:AAG7djDn1kGP-z8AUneCCAT14noiE-bf6Qw'
CHANNEL_ID_TEST = '@chessTesting' # Actual ID: -1002342940537


def prepare_puzzle(fen, moves):
    """
    Adjust the FEN to reflect the board state after the first move.

    Args:
        fen (str): The initial FEN string.
        moves (str): A space-separated string of moves in algebraic notation.

    Returns:
        tuple: Updated FEN, the remaining moves, and the first move as a chess.Move object.
    """
    board = chess.Board(fen)
    move_list = moves.split()

   # Apply the first move
    first_move = board.parse_san(move_list[0])
    board.push(first_move)


    # Return the updated FEN, remaining moves, and the first move
    return board.fen(), " ".join(move_list[1:]), first_move


# Function to create a chessboard image from FEN
def generate_chess_image(fen, last_move=None):
    """
    Generate a chessboard image with the last move highlighted.

    Args:
        fen (str): The FEN string representing the board state.
        last_move (chess.Move, optional): The last move to highlight.

    Returns:
        str: The path to the generated PNG image.
    """
    # Get current date and time for dynamic filenames
    # Use the `/tmp` directory for writable file operations
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_svg = f"/tmp/chess_puzzle_{timestamp}.svg"
    output_png = f"/tmp/chess_puzzle_{timestamp}.png"

    board = chess.Board(fen)

    # Dynamically flip the board if Black is to move
    is_black_turn = board.turn == chess.BLACK
    board_svg = chess.svg.board(board=board, lastmove=last_move, flipped=is_black_turn)

    # Save SVG & PNG
    with open(output_svg, "w") as f:
        f.write(board_svg)
    
    # Convert SVG to PNG with high resolution
    svg2png(bytestring=board_svg, write_to=output_png, dpi=1200, scale=4.0)

    return output_png


async def send_chess_puzzle(path):
    """
    Select a high-rated puzzle, update its FEN, generate an image, and send it to Telegram.

    Args:
        path (str): Path to the CSV file containing puzzle data.
    """
    # Load the CSV and filter puzzles with a rating > 2000
    puzzles = pd.read_csv(path)
    high_rated_puzzles = puzzles[puzzles['Rating'] > 2000]

    # Randomly select a puzzle
    selected_puzzle = high_rated_puzzles.sample(1).iloc[0]

    # Generate a chessboard image & Prepare the puzzle (update FEN, highlight last move)
    fen = selected_puzzle['FEN']
    moves = selected_puzzle["Moves"]

    # Update FEN and moves
    updated_fen, remaining_moves, first_move = prepare_puzzle(fen, moves)

    png_path = generate_chess_image(updated_fen, last_move=first_move)

    # Format the message
    message = (
        f"*Problem of the day* 🧩\n\n"
        f"🚀 *Rating:* {selected_puzzle['Rating']}\n"
        # f"*Popularity:* {selected_puzzle['Popularity']}\n"
        # f"🏷️ **Topics:** {selected_puzzle['Themes']}\n\n"
        f"**We need to find the *best continuation*. Let's throw in some emotions 😎?**\n\n"
        f"[🌐 Solve online](https://lichess.org/training/{selected_puzzle['PuzzleId']})"
        # f"[🌐 View game with solution]({selected_puzzle['GameUrl']})"
    )

    # Send the message with the image to Telegram
    bot = telegram.Bot(token=BOT_TOKEN_TEST)
    with open(png_path, 'rb') as image:
        await bot.send_photo(chat_id=CHANNEL_ID_TEST, photo=image, caption=message, parse_mode='Markdown')



# def lambda_handler(event, context):
#     csv_file_path = "./first_100K_batch.csv"
#     asyncio.run(send_chess_puzzle(csv_file_path))

csv_file_path = "./assets/first_15K_batch.csv"
asyncio.run(send_chess_puzzle(csv_file_path))
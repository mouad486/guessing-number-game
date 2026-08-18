## 🎮 Guessing Game

A console-based number guessing game with multiple modes, encrypted save data, and tamper detection. Built in Python, organized into 14+ sections for clarity.

## ✨ Features
Single Player Modes

- Easy (1–10)

- Medium (1–50)

- Hard (1–100)

- Nightmare (1–1000)

Two Player Mode  
Pass-and-play style with alternating setter/guesser roles.

Boss AI Mode  
Face off against an AI that uses binary search logic.

If the AI wins → bossAI_losses increases.

If the AI fails → bossAI_wins increases (player victory).

Secure Save System

Encrypted with Fernet.

Tamper detection using Blake3 checksum.

Auto-save on exit (finally block ensures data is always saved).

Reset Options

Solo reset (resets single-player stats).

Full reset (optional: wipes save files and key for a fresh start).

## 📂 Project Structure
Code
guessing_game.py   # Main script
game_data.enc      # Encrypted save file
secret.key         # Encryption key

## 🛠️ Requirements
- Python 3.8+

Install dependencies with:
```bash
pip install -r requirements.txt
```

## ▶️ How to Play
Run the game:

bash
python guessing_game.py
Menu options:

1 → Single player (choose difficulty)

2 → Two player mode

3 → Boss AI mode

4 → Reset solo stats

reset all → Full reset (wipe save + key)

5 → Quit

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 👤 Author
Created by Mouad
Created by Mouad


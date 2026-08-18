# ====== LIB ======
import json
import time
import random
from cryptography.fernet import Fernet
import blake3
import os

# ====== VARIABLE ======
numbers_easy = [n for n in range(1,11)]
numbers_medium = [n for n in range(1,51)]
numbers_hard = [n for n in range(1,101)]
numbers_nightmare = [n for n in range(1,1001)]
KEY_FILE = "secret.key"
SAVE_FILE = "game_data.enc"

# ====== KEY LOADER ======
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key
        
key = load_key()
fernet = Fernet(key)

# ====== SCORE SAVER ======
def save_score(win,loss,p1_wins,p2_wins,bossAI_wins,bossAI_losses):
    data = {
        "wins": max(0, win),
        "losses": max(0, loss),
        "P1_total": max(0, p1_wins),
        "P2_total": max(0, p2_wins),
        "bossAI_wins": max(0, bossAI_wins),
        "bossAI_losses": max(0, bossAI_losses)
    }
    
    data["checksum"] = make_checksum(data)
    
    encrypted = fernet.encrypt(json.dumps(data).encode())
    with open(SAVE_FILE, "wb") as f:
        f.write(encrypted)
        
# ====== CHECK SUM ======
def make_checksum(data):
    s = f"{data.get('wins',0)}-{data.get('losses',0)}-{data.get('P1_total',0)}-{data.get('P2_total',0)}-{data.get('bossAI_wins',0)}-{data.get('bossAI_losses',0)}"
    return blake3.blake3(s.encode()).hexdigest()  

# ====== SCORE LOADER ======
def load_score():
    win, loss, p1, p2, boss_wins, boss_losses = 0, 0, 0, 0, 0, 0
    if not os.path.exists(SAVE_FILE):
        return win, loss, p1, p2, boss_wins, boss_losses 
    try:
        with open(SAVE_FILE, "rb") as f:
            data = json.loads(fernet.decrypt(f.read()).decode())
            
        
        temp_data = {
            "wins": data.get("wins", 0),
            "losses": data.get("losses", 0),
            "P1_total": data.get("P1_total", 0),
            "P2_total": data.get("P2_total", 0),
            "bossAI_wins": data.get("bossAI_wins", 0),
            "bossAI_losses": data.get("bossAI_losses", 0)
        }
        
        saved_checksum = data.get("checksum", "")
        real_checksum = make_checksum(temp_data)
        
        if "version" not in data:
            data["version"] = 3
            data["checksum"] = make_checksum(temp_data)
            save_score(temp_data.get('wins', 0), temp_data.get('losses', 0),
                      temp_data.get('P1_total', 0), temp_data.get('P2_total', 0),
                      temp_data.get('bossAI_wins', 0), temp_data.get('bossAI_losses', 0))
        
        if saved_checksum and saved_checksum != real_checksum:
            print("Save file tampered. Resetting...")
            time.sleep(2)
            return 0,0,0,0,0,0
        
        for k, val in temp_data.items():
            if not isinstance(val, int) or val < 0:
                temp_data[k] = 0
    
        return (
            temp_data.get("wins", 0),
            temp_data.get("losses", 0),
            temp_data.get("P1_total", 0),
            temp_data.get("P2_total", 0),
            temp_data.get("bossAI_wins", 0),
            temp_data.get("bossAI_losses", 0)
        )
        
    except:
        print("Save file corrupted. Resetting...")
        time.sleep(2)
        return 0,0,0,0,0,0
    

# ====== GET SECRET NUMBER (2 PLAYER MODE) ======     
def get_secret_number():
    while True:
        try:
            num = int(input("Enter secret number 1-100: "))
            if 1 <= num <= 100:
                return num
            else:
                print("Must be between 1-100")
        except ValueError:
            print("Numbers only bro")
            
# ====== GUESSES PER ROUND (2 PLAYER MODE) ======
def guess_round(secret):
    attempt = 0
    max_attempt = 10
    while attempt < max_attempt:
        try:
            guess = int(input(f"Guess {attempt+1}/{max_attempt}: "))
            attempt += 1
            if guess == secret:
                print(f"Correct got in {attempt} tries")
                return True
            elif guess < secret:
                print("higher")
            else:
                print("lower")
        except ValueError:
            print("number only")
    print(f"Out of attempt! The number was {secret}")
    return False
    


# ====== 2 PLAYER MODE ======
def two_player_mode(p1_wins, p2_wins):
    target = 3
    round_num = 1
    setter = 1
    match_p1, match_p2 = 0,0
    
    while match_p1 < target and match_p2 < target:
        guesser = 2 if setter == 1 else 1
        
        print(f"\n---MATCH | P1 {match_p1} - {match_p2} P2 | Total: P1 {p1_wins} - {p2_wins} P2 ---")
        print(f"ROUND {round_num} | PLAYER {setter} sets | PLAYER {guesser} guesses")
        
        print(f"\nPLAYER {setter}: Set the secret number 1-100")
        input(f"Press Enter when P{guesser} looks away...")
        secret = get_secret_number()
        os.system('cls' if os.name == "nt" else 'clear')
        
        print(f"PLAYER {guesser}: You turn to guess!")
        if guess_round(secret):
            print(f"PLAYER {guesser}: WINS THIS ROUND!")
            if guesser == 1:
                match_p1 += 1
            else:
                match_p2 += 1
        else:
            print(F"PLAYER {setter} WINS THIS ROUND!")
            if setter == 1:
                match_p1 += 1
            else:
                match_p2 += 1
        
        setter = 2 if setter == 1 else 1
        input(f"\nPress Unter for next round... ")
        os.system('cls' if os.name == "nt" else 'clear')
        round_num += 1
        
    if match_p1 == target:
        p1_wins += 1
        print("\nP1 wins this game")
    else:
        p2_wins += 1
        print("\nP2 wins this game")
        
    return p1_wins, p2_wins
    
# ====== BOSS AI MODE ======
def boss_ai_mode(bossAI_wins, bossAI_losses):
    print("\n--- BOSS AI MODE ---")
    print("think of number 1-100. Dont tell me!")
    input("Press Enter when ready")
    
    low, high = 1, 100
    guesses = 0
    max_guesses = 6
    
    while low <= high and guesses < max_guesses:
        guess = (low + high) // 2
        guesses += 1
        print(f"\nBoss guess #{guesses}: {guess}")
        
        feedback = input("Is it [h]igher, [l]ower, or [c]orrect?").lower()
        
        if feedback == 'c':
            print(f"BOSS WON IN {guesses} guesses! You lose")
            bossAI_losses += 1
            return bossAI_wins, bossAI_losses
            
        elif feedback == 'h':
            low = guess + 1
            
        elif feedback == 'l':
            high = guess - 1
            
        else:
            print("Invalid. Use h/l/c")
            guesses -= 1
            continue
            
        if low > high:
            print("Caught you lying! Forfeit. -1 boss loss")
            bossAI_losses += 1
            return bossAI_wins, bossAI_losses
        
    print(f"BOSS FAILED after {guesses} guesses! you win +2!")
    bossAI_wins += 2
    return bossAI_wins, bossAI_losses
        
# ====== EASY MODE ======
def guess_number_easy(win,loss):
    attempt = 3
    num_easy = random.choice(numbers_easy)
    print(f"try and guess the easy 1-10 one you only have {attempt} attempt, good luck\n")
    
    while attempt > 0:
        try:
            guess = input(f"\nguess a number [{attempt} attempts left] or quit: ")

            if guess in ['q', 'quit']:
                print("goodbye")
                time.sleep(2)
                return win,loss
            else:     
                
                guess_num_easy = int(guess)
            
            if guess_num_easy == num_easy:
                print("\ncorrect, good job")
                win += 1
                time.sleep(2)
                break
            else:
                attempt -= 1
                if attempt > 0:
                    
                    if guess_num_easy > num_easy:
                        
                        print(f"\nwrong. HINT: number is lower")
                    
                    else:
                        print(f"\nwrong. HINT: number is higher")
                

        except ValueError:
            print(f"\nerror: type intger not etc")
            time.sleep(1)
            continue

    
    if attempt == 0:
        print(f"\ngame over number is {num_easy}")
        loss += 1
        time.sleep(2)

    play_again = input("play again? y/n: ")
    if play_again.lower() in ["y", "yes"]:
        
        os.system('cls' if os.name == "nt" else 'clear')
        return guess_number_easy(win,loss)
    
    else:
        print("goodbye. returning to menu...")
        time.sleep(2)
        return win,loss
        
        
        
# ====== MEDIUM MODE ======
def guess_number_medium(win,loss):
    attempt = 3
    num_medium = random.choice(numbers_medium)
    print(f"try and guess the medium one 1-50 you only have {attempt} attempt, good luck\n")
    
    while attempt > 0:
        try:
            guess = input(f"\nguess a number [{attempt} attempts left] or quit: ")

            if guess in ['q', 'quit']:
                print("goodbye")
                time.sleep(2)
                return win,loss
            
            else:     
                
                guess_num_medium = int(guess)
            
            if guess_num_medium == num_medium:
                print("\ncorrect, good job")
                win += 2
                time.sleep(2)
                break
            
            else:
                attempt -= 1
                if attempt > 0:
                    
                    if guess_num_medium > num_medium:
                        
                        print(f"\nwrong. HINT: number is lower")
                    
                    else:
                        print(f"\nwrong. HINT: number is higher")
                

        except ValueError:
            print(f"\nerror: type intger not etc")
            time.sleep(1)
            continue

    
    if attempt == 0:
        print(f"\ngame over number is {num_medium}")
        loss += 1
        time.sleep(2)

    play_again = input("play again? y/n: ")
    
    if play_again.lower() in ["y", "yes"]:
        
        os.system('cls' if os.name == "nt" else 'clear')
        return guess_number_medium(win,loss)
    
    else:
        print("goodbye. returning to menu...")
        time.sleep(2)
        return win,loss
                
        
# ====== HARD MODE ======
def guess_number_hard(win,loss):
    attempt = 3
    num_hard = random.choice(numbers_hard)
    print(f"try and guess the hard one 1-100 you only have {attempt} attempt, good luck\n")
    
    while attempt > 0:
        try:
            guess = input(f"\nguess a number [{attempt} attempts left] or quit: ")

            if guess in ['q', 'quit']:
                print("goodbye")
                time.sleep(2)
                return win,loss
                
            else:
                 
                guess_num_hard = int(guess)
            
            if guess_num_hard == num_hard:
                print("\ncorrect, good job")
                win += 3
                time.sleep(2)
                break
            
            else:
                attempt -= 1
                if attempt > 0:
                    
                    if guess_num_hard > num_hard:
                        
                        print(f"\nwrong. HINT: number is lower")
                    
                    else:
                        print(f"\nwrong. HINT: number is higher")
                

        except ValueError:
            print(f"\nerror: type intger not etc")
            time.sleep(1)
            continue

    
    if attempt == 0:
        print(f"\ngame over number is {num_hard}")
        loss += 1
        time.sleep(2)

    play_again = input("play again? y/n: ")
    
    if play_again.lower() in ["y", "yes"]:
        
        os.system('cls' if os.name == "nt" else 'clear')
        return guess_number_hard(win,loss)
    
    else:
        print("goodbye. returning to menu...")
        time.sleep(2)
        return win,loss
                
                
        

 # ====== NIGHMARE MODE ======
def guess_number_nightmare(win,loss):
    attempt = 3
    num_nightmare = random.choice(numbers_nightmare)
    print(f"try and guess the nightmare 1-1000 one you only have {attempt} attempt, good luck\n")

    while attempt > 0:
        try:
            guess = input(f"\nguess a number [{attempt} attempt left] or quit: ")

            if guess in ['q', 'quit']:
                print("goodbye")
                time.sleep(2)
                return win,loss
            
            else:     
                
                guess_num_nightmare = int(guess)
            
            if guess_num_nightmare == num_nightmare:
                print("\ncorrect, good job")
                win += 4
                time.sleep(2)
                break
            else:
                attempt -= 1
                if attempt > 0:
                    
                    if guess_num_nightmare > num_nightmare:
                        print(f"\nwrong. HINT: number is lower")
                    
                    else:
                        print(f"\nwrong. HINT: number is higher")
                

        except ValueError:
            print(f"\nerror: type intger not etc")
            time.sleep(1)
            continue

    
    if attempt == 0:
        print(f"\ngame over number is {num_nightmare}")
        loss += 1
        time.sleep(2)

    play_again = input("play again? y/n: ")
    
    if play_again.lower() in ["y", "yes"]:
        os.system('cls' if os.name == "nt" else 'clear')
        return guess_number_nightmare(win,loss)
    
    else:
        print("goodbye. returning to menu...")
        time.sleep(2)
        return win,loss
                
    
# ====== MAIN ======        
def main():
    try:
        win,loss,p1_wins,p2_wins,bossAI_wins,bossAI_losses = load_score()
        while True:
            os.system('cls' if os.name == "nt" else 'clear')
            print("\n=== guessing game===")
            print(f"Score: WINS: {win} LOSSES: {loss} | P1 WINS: {p1_wins} P2 WINS: {p2_wins} | bossAI_wins: {bossAI_wins} bossAI_losses: {bossAI_losses}")
            print("1: 1 player solo")
            print("2: 2 player pass-and-play")
            print("3: player vs ai")
            print("4: Reset Stats of 1 player solo")
            print("5: Full reset")
            print("6: Quit")
            
            choice = input("choose: ").lower().strip()
            
            if choice in ['6', 'q', 'quit']:
                print("good bye")
                break
                
            if choice in ["4", "reset", "r"]:
                confirm_reset = input("Are you sure? this reset your solo stats. y/n: ").lower()
                
                if confirm in ["yes", "y"]:
                    win,loss = 0,0
                    print("Stat Reset. back to 0")
                    time.sleep(2)
                else:
                    print("Reset cancelled")
                    time.sleep(2)
                    continue
                    
            if choice in ["5", "reset all", "ra"]:
                
                confirm_full_reset = input("Are You Sure? this delete your keys and your game data. y/n: ")
                
                if confirm_full_reset in ["y","yes"]:
                    
                    if os.path.exists(SAVE_FILE):
                        os.remove(SAVE_FILE)
                        
                    if os.path.exists(KEY_FILE):
                        
                        os.remove(KEY_FILE)
                        print("Full reset Complete!")
                        time.sleep(2)
                        
                else:
                    
                    print("Full reset Cancelled.")
                    time.sleep(2)
                    continue
                    
            if choice == "2":
                p1_wins,p2_wins = two_player_mode(p1_wins, p2_wins)
                
            if choice ==  "1":
                diffculty_chooser = input(f"score: win: {win} loss : {loss}, choose diffculty (easy,medium,hard,nightmare): ")
                
                if diffculty_chooser == "easy":
                    
                    win,loss = guess_number_easy(win,loss)
            
                elif diffculty_chooser == "medium":
                    win,loss = guess_number_medium(win,loss)
            
                elif diffculty_chooser == "hard":
                    win,loss = guess_number_hard(win,loss)
            
                elif diffculty_chooser == "nightmare":
                    win,loss = guess_number_nightmare(win,loss)
            
                else:
                    print("invald option try again")
                    time.sleep(2)
                    
            if choice == "3":
                bossAI_wins, bossAI_losses = boss_ai_mode(bossAI_wins, bossAI_losses)
                
                
    except KeyboardInterrupt:
        save_score(win,loss,p1_wins,p2_wins,bossAI_wins,bossAI_losses)
        print("\ngame closed")
    
    except TypeError as e:
        print(f"error: TypeError: {e}")
    
    finally:
        save_score(win,loss,p1_wins,p2_wins,bossAI_wins,bossAI_losses)
        print("\ngame saved")
                
# ====== UNTRY POINT ======
if __name__ == "__main__":
    main()
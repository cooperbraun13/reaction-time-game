import time
import random
# Import the Circuit Playground Express module
from adafruit_circuitplayground.express import cpx

# Settings
NUM_ROUNDS = 5
# Will save the best average reaction time to the text file
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    # Load the high score, lowest average reaction time, from text file
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return float(f.read().strip())
    except Exception:
        return None
    
def save_high_score(score):
    # Save a new high score to the text file
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))
        
def wait_for_button_release():
    # Wait until button A is released
    # This allows next round to start with the button in an unpressed state
    while cpx.button_a:
        pass
    
def indicate_false_start():
    # Blink red and play a sound to indicate a false start
    for i in range(3):
        cpx.pixels.fill((255, 0, 0))
        # Middle C tone
        cpx.play_tone(262, 0.2)
        time.sleep(0.2)
        cpx.pixels.fill((0, 0, 0))
        time.sleep(0.2)
        
def run_round(round_number):
    """
    Run one round of the reaction time test
    The round will not count if a false start occurs
    The function repeats itself until a valid reaction time is recorded
    Returns the reaction time in milliseconds
    """
    while True:
        # Make sure button is not held from previous round
        wait_for_button_release()
        
        # Signal start of round with blue
        cpx.pixels.fill((0, 0, 255))
        print("Round {}: Get ready...".format(round_number))
        # Give the user a second to prepare
        time.sleep(1)
        
        # Generate a random delay between 2 and 5 seconds
        delay = random.uniform(2, 5)
        start_delay = time.monotonic()
        false_start = False
        
        # During the delay, continuously check for a button press
        while (time.monotonic() - start_delay) < delay:
            if cpx.button_a:
                false_start = True
                break
            
        if false_start:
            # Indicate a false start with a blinking red and a sound
            print("False start! Try again")
            indicate_false_start()
            # Return to blue to restart the round
            cpx.pixels.fill((0, 0, 255))
            wait_for_button_release()
            # Restart the round and do not count the round as extra
            continue
        
        # Signal a valid start with green
        cpx.pixels.fill((0, 255, 0))
        print("GO!")
        # Ensure the button is released before timing
        wait_for_button_release()
        start_time = time.monotonic()
        
        # Wait for user to press button A
        while not cpx.button_a:
            pass
        
        # Calculate reaction time in milliseconds (ms)
        reaction_time = (time.monotonic() - start_time) * 1000
        print("Reaction time: {:.0f} ms".format(reaction_time))
        cpx.pixels.fill((0, 0, 0))
        time.sleep(0.5)
        wait_for_button_release()
        return reaction_time
        
def main():
    # Run the reaction time test for multiple rounds and update high score if applicable
    reaction_times = []
    high_score = load_high_score()
    
    if high_score is not None:
        print("Current best score: {:.0f} ms".format(high_score))
    else:
        print("No high score yet, try playing!")
    
    round_count = 1
    while len(reaction_times) < NUM_ROUNDS:
        rt = run_round(round_count)
        reaction_times.append(rt)
        round_count += 1
        time.sleep(1)
        
    # Calculate the average reaction time
    avg_reaction_time = sum(reaction_times) / len(reaction_times)
    print("\nAverage reaction time over {} rounds: {:.0f} ms".format(NUM_ROUNDS, avg_reaction_time))
    
    # Update high score if the new average is lower
    if (high_score is None) or (avg_reaction_time < high_score):
        print("Congratulations! You scored a new best!")
        save_high_score(avg_reaction_time)
    else:
        print("Best score remains: {:.0f} ms".format(high_score))
        
    # Final indicator
    cpx.pixels.fill((0, 255, 255))
    time.sleep(2)
    cpx.pixels.fill((0, 0, 0))
    
if __name__ = "__main__":
    main()
import time
import random
# Import the Circuit Playground Express module
from adafruit_circuitplayground.express import cpx

def reaction_time_test():
    # Set all NeoPixels initially to blue to signal the device is ready to start the game
    cpx.pixels.fill((0, 0, 255))
    print("Get ready...")
    # Give the user a second to see the blue light
    time.sleep(1)
    
    # Wait for the random delay, between 2 and 5 seconds, to avoid anticipation
    delay = random.uniform(2, 5)
    time.sleep(delay)
    
    # Change the NeoPixels to green, signaling the player to press button A on the board
    cpx.pixels.fill((0, 255, 0))
    print("GO!")
    
    # Record the time immediately when the green light appears
    start_time = time.monotonic()
    
    # Wait for the user to press button A
    while not cpx.button_a:
        # Loops continuously until button A is pressed
        pass
    
    # Calculate the reaction time in milliseconds
    reaction_time = (time.monotonic() - start_time) * 1000
    print("Your reaction time is: {:.0f} ms".format(reaction_time))
    
    # Change the color to red to indicate the game is over
    cpx.pixels.fill((255, 0, 0))
    time.sleep(2)
    
    # Turn off the LEDs
    cpx.pixels.fill((0, 0, 0))
    
# Run the reaction time test
reaction_time_test()
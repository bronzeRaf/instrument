from pysinewave import SineWave
from time import sleep

# sinewave = SineWave(pitch = 12)
# sinewave.play()
# sleep(3)
# sinewave = SineWave(pitch = 3)
# sleep(3)
# sinewave.stop()




# Create a sine wave, with a starting pitch of 12, and a pitch change speed of 10/second.
sinewave = SineWave(pitch = 2)

# Turn the sine wave on.
sinewave.play()

# Sleep for 2 seconds, as the sinewave keeps playing.
sleep(2)

# Set the goal pitch to -5.
# sinewave.set_pitch(-5)

SineWave.set_frequency(frequency=70)

# Sleep for 3 seconds, as the sinewave smoothly slides its pitch down from 12 to -5, and stays there.
sleep(3)

sinewave.set_pitch(-7)
sleep(3)
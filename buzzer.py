import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)
buzzer_pin = 18
# Configure the GPIO pin as an output
GPIO.setup(buzzer_pin, GPIO.OUT)

note_frequencies_low=   100.00  
note_frequencies_high =  4000
initial_duty_cycle = 50  

def playoctave(note_frequencies):
    pwm_frequency = note_frequencies
    pwm = GPIO.PWM(buzzer_pin, pwm_frequency)    
    pwm.ChangeFrequency(pwm_frequency)
    pwm.start(initial_duty_cycle)
    time.sleep(0.1) # Play for the specified duration
    pwm.stop()  # Stop the tone

        
def playarrived():
    pwm_frequency =  20
    pwm = GPIO.PWM(buzzer_pin, pwm_frequency)
    pwm.ChangeFrequency(pwm_frequency)
    pwm.start(initial_duty_cycle)
    time.sleep(0.3)  
    pwm.stop()  # Stop the tone

def playalert(freq,duration):
    pwm_frequency = freq
    pwm = GPIO.PWM(buzzer_pin, pwm_frequency)    
    pwm.ChangeFrequency(pwm_frequency)
    pwm.start(initial_duty_cycle)
    time.sleep(duration) # Play for the specified duration
    pwm.stop()  # Stop the tone



if __name__ == "__main__":
    print("This is the buzzer")
    
    for _ in range (10):
        playalert(note_frequencies_low,0.1)
    time.sleep(1)    
    for _ in range (10):
        playalert(note_frequencies_high,0.1)
    time.sleep(1)
    for _ in range (10):
        playalert(20,0.3)
    
    
       
    GPIO.cleanup()



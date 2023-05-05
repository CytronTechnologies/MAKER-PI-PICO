import machine
import uos
import ustruct
import utime

def play_wav(filename, left_channel, right_channel):
    left_pwm = machine.PWM(left_channel)
    right_pwm = machine.PWM(right_channel)
    pwm_freq = 62500
    left_pwm.freq(pwm_freq)
    right_pwm.freq(pwm_freq)
    left_pwm.duty_u16(0)
    right_pwm.duty_u16(0)
    
    def set_duty_cycle(pwm, value):
        if value < 0:
            value = 0
        if value > 65535:
            value = 65535
        pwm.duty_u16(value)
    
    with open(filename, 'rb') as f:
        # Read WAV header
        header = f.read(44)
        if len(header) < 44:
            raise RuntimeError("Invalid WAV file")

        # Check format
        if header[0:4] != b'RIFF' or header[8:12] != b'WAVE':
            raise RuntimeError("Invalid WAV file")
        
        # Read and play audio data in chunks
        chunk_size = 1024
        while True:
            audio_data = f.read(chunk_size)
            if not audio_data:
                break

            audio_sample_count = len(audio_data) // 4
            audio_samples = ustruct.unpack('<%dh' % (audio_sample_count * 2), audio_data)

            # Play audio samples
            for i in range(0, len(audio_samples), 2):
                left_sample = audio_samples[i]
                right_sample = audio_samples[i + 1]
                set_duty_cycle(left_pwm, (left_sample + 32768) << 1)
                set_duty_cycle(right_pwm, (right_sample + 32768) << 1)
                #utime.sleep_us(20)  # Assuming 48 kHz sample rate

    left_pwm.deinit()
    right_pwm.deinit()


import pyaudio
import wave

def print_audio_devices():
    p = pyaudio.PyAudio()
    devices_info = {}

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        max_channels = device_info['maxInputChannels']
        sample_rate = device_info['defaultSampleRate']
        device_name = device_info['name']

        if max_channels > 0:
            if device_name not in devices_info:
                devices_info[device_name] = {
                    'id': i,
                    'max_channels': max_channels,
                    'sample_rate': sample_rate
                }
            else:
                if sample_rate > devices_info[device_name]['sample_rate']:
                    devices_info[device_name]['max_channels'] = max_channels
                    devices_info[device_name]['sample_rate'] = sample_rate
                elif sample_rate == devices_info[device_name]['sample_rate'] and max_channels > devices_info[device_name]['max_channels']:
                    devices_info[device_name]['max_channels'] = max_channels

    device_list = []
    for device_name, info in devices_info.items():
        device_list.append(f"🔉 Device <b>{info['id']}</b>: <b>{device_name}</b>, Max channels: <b>{info['max_channels']}</b>, Supported rate: <b>{info['sample_rate']}</b>")

    return "\n\n".join(device_list)

def select_audio_device():
    p = pyaudio.PyAudio()
    device_id = None

    while True:
        print_audio_devices()
        try:
            device_id = int(input("Inserisci l'ID del dispositivo audio desiderato: "))
            if not (0 <= device_id < p.get_device_count()):
                return "NError"
            
            device_info = p.get_device_info_by_index(device_id)
            max_channels = device_info['maxInputChannels']
            default_sample_rate = device_info['defaultSampleRate']
            

            channels = max_channels
            rate = int(default_sample_rate)

            break
        except ValueError as ve:
            return "Error"

    p.terminate()
    return device_id, channels, rate

def audio_recorder(seconds, device_id, channels, rate):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    WAVE_OUTPUT_FILENAME = "audio_record.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=rate,
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=CHUNK)

    frames = []


    for i in range(0, int(rate / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def main():
    try:
        device_id, channels, rate = select_audio_device()
        audio_recorder(5, device_id, channels, rate)
    except OSError:
        return "OError"


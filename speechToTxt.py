# realtime_vosk.py
import queue
import sys
import json
import os
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import emailAlert
import checking1

abuseModel,hateModel,offenseModel = checking1.load_detection_models()

# -- CONFIG --
MODEL_PATH = r"D:\ACADEMICS ALL\sem5\CN\Project\HateBERT_fine_tuned_models\vosk-model-en-in-0.5" # path to the folder
SAMPLE_RATE = 16000    # common for VOSK models
CHUNK_SIZE = 4000      # bytes per read (keep small for low latency)
# --------------


if not os.path.exists(MODEL_PATH):
    print(f"Model not found at '{MODEL_PATH}'. Download and unzip a VOSK model and set MODEL_PATH.")
    sys.exit(1)

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        # print status messages (overflows, etc.)
        print("Audio status:", status, file=sys.stderr)
    # indata is a numpy array of dtype float32 by default; convert to bytes 16-bit PCM
    q.put(bytes(indata))

def main():
    print("Loading model... (this may take a few seconds)")
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)  # include word timestamps (optional)

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE,
                               dtype='int16', channels=1, callback=audio_callback):
            print("Listening... Press Ctrl+C to stop.")
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    text = res.get("text", "")
                    if text:
                        # Final result for that chunk
                        print("\n>>", text)
                        check,detectList = checking1.detect(text,abuseModel,hateModel,offenseModel)
                        if check==1:
                            emailAlert.alert_email(text,detectList)
                            
                        
                else:
                    # Partial (intermediate) result
                    partial = json.loads(rec.PartialResult())
                    p = partial.get("partial", "")
                    if p:
                        # Overwrite the same line for nicer live feel (works in many terminals)
                        print("\r… " + p, end="", flush=True)

    except KeyboardInterrupt:
        print("\nStopping...")
        final = json.loads(rec.FinalResult())
        if final.get("text"):
            print("Final:", final["text"])
        print("Goodbye.")

if __name__ == "__main__":
    main()

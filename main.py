import asyncio
import os
import wave
import io
from playsound import playsound # For playing the audio file
from google import genai
from google.generativeai.types import LiveConnectConfig, GenerateContentRequest

# --- Configuration ---
# Fetch API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=GEMINI_API_KEY)

# Model specifically designed for live, potentially audio interaction
LIVE_MODEL_NAME = "gemini-2.0-flash-live-001"
OUTPUT_FILENAME = "output_speech.wav"

# Audio parameters expected from the Live API output
# (Refer to Gemini API documentation for the most up-to-date specs)
OUTPUT_SAMPLE_RATE = 24000 # Hz (Typically 24kHz for Live API audio output)
OUTPUT_CHANNELS = 1       # Mono
OUTPUT_SAMPLE_WIDTH = 2   # Bytes per sample (16-bit PCM)

# --- Main Async Function ---
async def generate_and_speak(text_prompt: str):
    """Connects to Gemini Live API, sends text, receives audio, saves & plays it."""

    print(f"Connecting to model: {LIVE_MODEL_NAME}...")

    # Configure the connection for AUDIO output
    live_config = LiveConnectConfig(
        response_modalities=["AUDIO"],
        # Optional: Configure specific voice if needed and available
        # speech_config=genai.types.SpeechConfig(
        #     voice_config=genai.types.VoiceConfig(
        #         prebuilt_voice_config=genai.types.PrebuiltVoiceConfig(voice_name="Kore") # Example voice
        #     )
        # )
    )

    audio_data_bytes = io.BytesIO() # Use BytesIO to collect audio chunks in memory

    try:
        # Establish the asynchronous connection
        async with genai.alive.connect(model=LIVE_MODEL_NAME, config=live_config) as session:
            print("Connection established. Sending text prompt...")

            # Create the request with the text prompt
            request = GenerateContentRequest(
                contents=[{"parts": [{"text": text_prompt}]}]
            )

            # Send the request
            await session.send_request(request)
            print("Prompt sent. Waiting for audio response...")

            # Receive responses asynchronously
            async for response in session:
                # Check if the chunk contains audio data
                if response.chunk and response.chunk.audio_chunk and response.chunk.audio_chunk.data:
                    audio_data_bytes.write(response.chunk.audio_chunk.data)
                    print(".", end="", flush=True) # Indicate receiving audio data

            print("\nAudio stream finished.")

        # --- Save received audio bytes to a WAV file ---
        audio_data_bytes.seek(0) # Rewind the buffer to the beginning
        received_audio = audio_data_bytes.read()

        if not received_audio:
            print("No audio data received.")
            return

        print(f"Saving audio to {OUTPUT_FILENAME}...")
        with wave.open(OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(OUTPUT_CHANNELS)
            wf.setsampwidth(OUTPUT_SAMPLE_WIDTH)
            wf.setframerate(OUTPUT_SAMPLE_RATE)
            wf.writeframes(received_audio)
        print("Audio saved successfully.")

        # --- Play the saved WAV file ---
        print(f"Playing {OUTPUT_FILENAME}...")
        try:
            playsound(OUTPUT_FILENAME)
            print("Playback finished.")
        except Exception as e:
            print(f"Error playing sound: {e}")
            print("You might need to install an appropriate backend for playsound or check file permissions.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Clean up the generated file (optional)
        if os.path.exists(OUTPUT_FILENAME):
             try:
                 # os.remove(OUTPUT_FILENAME)
                 # print(f"Cleaned up {OUTPUT_FILENAME}")
                 # Commented out so you can inspect the file after running
                 pass
             except OSError as e:
                 print(f"Error removing temporary file {OUTPUT_FILENAME}: {e}")

# --- Run the Demo ---
if __name__ == "__main__":
    print("Gemini Text-to-Speech Demo (using Live API)")
    print("-----------------------------------------")
    user_text = input("Enter the text you want Gemini to speak: ")

    if user_text:
        # Run the asynchronous function
        asyncio.run(generate_and_speak(user_text))
    else:
        print("No text entered.")
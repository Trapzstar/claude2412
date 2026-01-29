# ============================================
# HYBRID VOICE RECOGNIZER (CLEAN VERSION)
# No external dependencies, self-contained
# ============================================
import speech_recognition as sr
import pyaudio
import numpy as np
import time
from typing import Optional, List, Dict, Any

class HybridVoiceRecognizer:
    def __init__(self, debug_mode: bool = True, config: Optional[Dict[str, Any]] = None) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_ready = False
        self.device_index = None
        self.speech_history = []
        self.debug_mode = debug_mode
        self.noise_reduction_enabled = False
        
        # Settings
        self.listen_timeout = 5
        self.phrase_limit = 4
        self.google_language = "id-ID"
        self.max_retries = 3
        self.retry_delay = 0.5
        
        # Adaptive threshold
        self.base_energy_threshold = 300

    def initialize(self) -> bool:
        """Initialize Hybrid Speech Recognition"""
        try:
            # List devices
            self.list_audio_devices()

            # Microphone setup
            try:
                if self.device_index is not None:
                    self.microphone = sr.Microphone(device_index=self.device_index)
                    print(f"✅ Microphone selected: Device {self.device_index}")
                else:
                    self.microphone = sr.Microphone()
                    print("✅ Microphone ready (default)")

                # Calibrate microphone
                with self.microphone as source:
                    print("🎤 Calibrating microphone...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("🎤 Microphone calibrated")

            except Exception as mic_error:
                print(f"❌ Microphone setup error: {mic_error}")
                print("💡 Solutions:")
                print("   1. Check microphone connection")
                print("   2. Restart application")
                print("   3. Check Windows Sound Settings")
                return False

            self.is_ready = True
            print("🔄 Hybrid mode: Google API (primary)")
            return True

        except Exception as e:
            print(f"❌ Initialization error: {e}")
            self.is_ready = False
            return False

    def list_audio_devices(self) -> None:
        """List available audio input devices"""
        try:
            audio = pyaudio.PyAudio()
            print("\n🎙️  AUDIO INPUT DEVICES:")
            print("-" * 40)
            for i in range(audio.get_device_count()):
                device_info = audio.get_device_info_by_index(i)
                if device_info.get('maxInputChannels') > 0:
                    print(f"  {i}: {device_info.get('name')} (Channels: {device_info.get('maxInputChannels')})")
            print("-" * 40)
            audio.terminate()
        except Exception as e:
            print(f"⚠️  Cannot list devices: {e}")

    def select_device(self, device_index: int) -> None:
        """Select specific audio device"""
        self.device_index = device_index
        if self.debug_mode:
            print(f"🎙️  Device {device_index} selected")

    def add_to_history(self, text: str) -> None:
        """Add recognized text to history"""
        self.speech_history.append(text)
        if len(self.speech_history) > 10:
            self.speech_history.pop(0)

    def listen_google_primary(self) -> Optional[str]:
        """Try Google Speech API with retry logic"""
        for attempt in range(self.max_retries):
            try:
                with self.microphone as source:
                    if self.debug_mode:
                        print("    🔊 Listening...", end="", flush=True)

                    # Listen for audio
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.listen_timeout,
                        phrase_time_limit=self.phrase_limit
                    )

                    if self.debug_mode:
                        print("\r    ⏳ Recognizing...", end="", flush=True)

                    # Recognize with Google Speech API
                    text = self.recognizer.recognize_google(audio, language=self.google_language)

                    if self.debug_mode:
                        print(f"\r    📝 Google: '{text}'")

                    self.add_to_history(text)
                    return text

            except sr.WaitTimeoutError:
                if self.debug_mode:
                    print("\r    ⏰ No speech detected")
                return None
                
            except sr.UnknownValueError:
                if self.debug_mode:
                    print("\r    🤔 Speech unclear")
                
                # Retry with lower threshold
                if attempt < self.max_retries - 1:
                    if self.debug_mode:
                        print(f"    🔄 Retry {attempt + 1}/{self.max_retries}")
                    time.sleep(self.retry_delay)
                    continue
                return None
                
            except sr.RequestError as e:
                if self.debug_mode:
                    print(f"\r    ❌ API Error: {str(e)[:50]}")
                
                if attempt < self.max_retries - 1:
                    if self.debug_mode:
                        print(f"    🔄 Retry {attempt + 1}/{self.max_retries}")
                    time.sleep(self.retry_delay)
                    continue
                return None
                
            except Exception as e:
                if self.debug_mode:
                    print(f"\r    ❌ Error: {str(e)[:50]}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                return None
        
        return None

    def listen(self, timeout: Optional[int] = None, phrase_limit: Optional[int] = None) -> Optional[str]:
        """Main listen method with smart retry"""
        if not self.is_ready:
            return None

        # Use provided parameters or defaults
        if timeout:
            self.listen_timeout = timeout
        if phrase_limit:
            self.phrase_limit = phrase_limit

        # Try listening with retries
        text = self.listen_google_primary()
        return text

    def listen_quick(self, timeout: int = 2) -> Optional[str]:
        """Quick listen for confirmation"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=2
                )
                text = self.recognizer.recognize_google(audio, language=self.google_language)
                return text
        except:
            return None

    def get_history(self) -> List[str]:
        """Get speech recognition history"""
        return self.speech_history.copy()

    def clear_history(self) -> None:
        """Clear speech recognition history"""
        self.speech_history.clear()
        print("🗑️  History cleared")

    def show_history(self) -> None:
        """Show speech recognition history"""
        if not self.speech_history:
            print("📝 History empty")
            return

        print("\n📝 SPEECH RECOGNITION HISTORY:")
        print("-" * 40)
        for i, text in enumerate(self.speech_history[-10:], 1):
            print(f"  {i}. '{text}'")
        print("-" * 40)

    def save_history(self, filename: str = "speech_history.txt") -> None:
        """Save speech history to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Speech Recognition History\n")
                f.write("=" * 30 + "\n")
                for text in self.speech_history:
                    f.write(f"{text}\n")
            print(f"💾 History saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save history: {e}")

    def test_microphone(self, duration: int = 3) -> bool:
        """Test microphone input"""
        print(f"\n🎙️  TESTING MICROPHONE ({duration} seconds)...")
        print("-" * 40)

        try:
            with self.microphone as source:
                print("   Recording... speak now!")
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)

                print("   Recognizing...")
                text = self.recognizer.recognize_google(audio, language=self.google_language)

                print(f"   ✅ Detected: '{text}'")
                print("   🎉 Microphone test successful!")
                return True

        except sr.WaitTimeoutError:
            print("   ⏰ Timeout - no speech detected")
            print("   ⚠️  Check microphone connection")
            return False
        except sr.UnknownValueError:
            print("   🤔 Speech detected but unclear")
            print("   💡 Try speaking clearer or closer")
            return False
        except sr.RequestError as e:
            print(f"   ❌ API Error: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Test error: {e}")
            return False

    def toggle_noise_reduction(self) -> None:
        """Toggle noise reduction"""
        self.noise_reduction_enabled = not self.noise_reduction_enabled
        status = "ON" if self.noise_reduction_enabled else "OFF"
        print(f"🔊 Noise reduction: {status}")
        
        if self.noise_reduction_enabled:
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_threshold = 400
        else:
            self.recognizer.dynamic_energy_threshold = False
            self.recognizer.energy_threshold = 300

    def set_debug_mode(self, enabled: bool = True) -> None:
        """Enable or disable debug mode"""
        self.debug_mode = enabled
        print(f"🔧 Debug mode: {'ON' if enabled else 'OFF'}")
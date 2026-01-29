"""
SlideSense - Main Application
Voice-Controlled PowerPoint Presentation with Accessibility Features
"""

import sys
import time
from typing import Optional, Dict, List, Any, Tuple
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Infrastructure
from src.infrastructure.logger import get_logger
from src.infrastructure.config import get_config
from src.infrastructure.exceptions import (
    MicrophoneError, VoiceRecognitionError, CommandExecutionError,
    SlideSenseException
)

# GUI
from src.gui.manager import ui, console

# Core modules
from src.core.voice_detector import SmartVoiceDetector
from src.core.voice_recognizer import HybridVoiceRecognizer
from src.core.powerpoint_controller import PowerPointController
from src.core.accessibility_popup import AccessibilityPopup

# Utilities
from src.utils.helpers import get_audio_devices, find_best_device, print_status, pause_and_continue

logger = get_logger(__name__)
config = get_config()

class SlideSenseApp:
    """Main application controller"""
    
    def __init__(self) -> None:
        self.voice: Optional[HybridVoiceRecognizer] = None
        self.detector: Optional[SmartVoiceDetector] = None
        self.ppt: Optional[PowerPointController] = None
        self.popup: Optional[AccessibilityPopup] = None
        self.running: bool = False
    
    def initialize_components(self) -> bool:
        """Initialize all components"""
        
        logger.info("Starting component initialization")
        console.print("[bold cyan]Initializing components...[/bold cyan]")
        
        try:
            # Initialize detector
            logger.debug("Initializing voice detector...")
            self.detector = SmartVoiceDetector()
            console.print("  [green][OK][/green] Voice Detector")
            logger.info("Voice detector initialized")
            
            # Initialize PowerPoint controller
            logger.debug("Initializing PowerPoint controller...")
            self.ppt = PowerPointController()
            console.print("  [green][OK][/green] PowerPoint Controller")
            logger.info("PowerPoint controller initialized")
            
            # Initialize popup system
            logger.debug("Initializing accessibility popup...")
            self.popup = AccessibilityPopup()
            self.popup.start()
            self.ppt.set_popup_system(self.popup)
            console.print("  [green][OK][/green] Accessibility Popup")
            logger.info("Accessibility popup initialized")
            
            # Initialize voice recognizer
            logger.debug("Initializing voice recognizer...")
            debug_mode = config.get("application.debug", False)
            self.voice = HybridVoiceRecognizer(debug_mode=debug_mode)
            console.print("  [green][OK][/green] Voice Recognizer")
            logger.info("Voice recognizer initialized")
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Component initialization failed: {e}", exc_info=True)
            ui.show_error(
                "Initialization Error",
                f"Failed to initialize components: {str(e)}",
                [
                    "Ensure all dependencies are installed",
                    "Try restarting the program"
                ]
            )
            return False
    
    def setup_microphone(self) -> bool:
        """Setup microphone - Simplified & Reliable"""
        
        # Get available devices
        devices = get_audio_devices()
        
        if not devices:
            ui.show_error(
                "Microphone Not Detected",
                "No audio input device detected.",
                [
                    "Ensure microphone is connected",
                    "Check Device Manager in Windows",
                    "Try restarting the computer"
                ]
            )
            return False
        
        # Show setup wizard
        setup_method = ui.show_microphone_setup(devices)
        
        if setup_method == "auto":
            # SIMPLE AUTO-DETECT
            ui.show_auto_detect_progress()
            
            # Find best device using utility function
            best_device = find_best_device(devices)
            device_name = devices[best_device]['name']
            
            # Show found device
            confirmed = ui.show_device_found(device_name, best_device)
            
            if confirmed:
                self.voice.select_device(best_device)
                return True
            else:
                return self._manual_device_selection(devices)
        
        else:
            # Manual selection
            return self._manual_device_selection(devices)
    
    def _find_best_device(self, devices: List[Dict[str, Any]]) -> int:
        """
        DEPRECATED: Use utils.find_best_device() instead
        Kept for backward compatibility
        """
        return find_best_device(devices)
    
    def _manual_device_selection(self, devices: List[Dict[str, Any]]) -> bool:
        """Manual device selection"""
        
        device_index = ui.show_microphone_list(devices)
        
        if device_index is None:
            return False
        
        self.voice.select_device(device_index)
        console.print(f"[green][OK] Device {device_index} selected[/green]\n")
        time.sleep(0.5)
        return True
    
    def test_microphone(self) -> None:
        """Test microphone"""
        
        if not self.voice or not self.voice.microphone:
            ui.show_error(
                "Microphone Belum Disetup",
                "Silakan setup microphone terlebih dahulu.",
                ["Select 'Start Voice Control' from the main menu"]
            )
            return
        
        ui.show_microphone_test_start(duration=3)
        ui.show_test_progress(duration=3)
        
        # Actual test
        result = self.voice.test_microphone(duration=3)
        
        if result:
            ui.show_test_result(True, "Microphone berfungsi dengan baik!")
        else:
            ui.show_test_result(
                False, 
                "Test failed. Try speaking louder."
            )
    
    def start_voice_control(self) -> None:
        """Start voice control loop"""
        
        # Initialize if not done
        if not self.voice:
            if not self.initialize_components():
                return
        
        # Setup microphone
        if not self.setup_microphone():
            console.print("[yellow][WARN] Microphone setup cancelled[/yellow]\n")
            ui.pause()
            return
        
        # Initialize voice system
        ui.show_voice_control_starting()
        
        if not self.voice.initialize():
            ui.show_error(
                "Voice System Error",
                "Failed to initialize voice recognition system.",
                [
                    "Check microphone connection",
                    "Ensure microphone is not used by another application"
                ]
            )
            ui.pause()
            return
        
        # Show active interface
        ui.show_voice_control_active()
        
        # Connect popup to voice for caption
        self.popup.voice_recognizer = self.voice
        
        console.print("[bold green][OK] System ready![/bold green]")
        console.print("[yellow][TIP] Open PowerPoint and press F5 to start slideshow[/yellow]")
        console.print("[dim]   Then return to this window for control\n[/dim]")
        
        time.sleep(2)
        
        # Main control loop
        self.running = True
        
        try:
            while self.running:
                ui.show_listening()
                
                # Listen for voice
                text = self.voice.listen()
                
                if text is None:
                    ui.show_no_speech()
                    time.sleep(0.3)
                    continue
                
                # Show caption if enabled
                if self.popup.caption_running:
                    try:
                        self.popup.show_caption(text)
                    except:
                        pass
                
                # Detect command
                result = self.detector.detect(text)
                
                if result and result.get("command") != "unknown":
                    # Get confidence
                    confidence = (result.get('score', 0) / result.get('max_score', 10)) * 100
                    
                    # Show detection
                    ui.show_command_detected(
                        result.get("command"),
                        text,
                        confidence
                    )
                    
                    # Execute command
                    feedback = self.ppt.execute_command(result)
                    ui.show_command_feedback(feedback)
                    
                    # Check for stop command
                    if result.get("command") == "stop":
                        console.print("\n[bold yellow][STOP] Stopping Voice Control...[/bold yellow]")
                        self.running = False
                        break
                    
                    # Check for help command
                    elif result.get("command") == "help":
                        console.print()
                        self.detector.show_help()
                        ui.pause()
                        ui.show_voice_control_active()
                
                else:
                    # Unknown command
                    ui.show_unknown_command(text)
                
                time.sleep(0.3)
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow][WARN] Voice Control stopped (Ctrl+C)[/yellow]")
            self.running = False
        
        # Show statistics
        console.print("\n" + "="*60)
        console.print("[bold cyan][STAT] Session Statistics[/bold cyan]")
        console.print("="*60)
        self.ppt.show_statistics()
        
        ui.pause()
    
    def run(self) -> None:
        """Main application loop"""
        
        logger.info("Starting SlideSense application")
        
        try:
            # Show welcome
            ui.show_welcome()
            logger.debug("Welcome screen displayed")
            
            # Main menu loop
            while True:
                try:
                    action = ui.show_main_menu()
                    logger.debug(f"User selected menu action: {action}")
                    
                    if action == "start":
                        logger.info("User started voice control")
                        self.start_voice_control()
                    
                    elif action == "test_mic":
                        logger.info("User started microphone test")
                        # Initialize if needed
                        if not self.voice:
                            if not self.initialize_components():
                                logger.warning("Component initialization failed, continuing")
                                continue
                            if not self.setup_microphone():
                                logger.warning("Microphone setup failed, continuing")
                                continue
                            if not self.voice.initialize():
                                logger.warning("Voice initialization failed, continuing")
                                continue
                        
                        self.test_microphone()
                    
                    elif action == "tutorial":
                        logger.info("User opened tutorial")
                        ui.show_tutorial()
                    
                    elif action == "about":
                        logger.info("User opened about screen")
                        ui.show_about()
                    
                    elif action == "exit":
                        logger.info("User selected exit")
                        break
                    
                    elif action == "invalid":
                        logger.warning("User entered invalid menu choice")
                        console.print("[yellow][WARN] Invalid choice[/yellow]\n")
                        time.sleep(1)
                
                except KeyboardInterrupt:
                    logger.info("Keyboard interrupt detected")
                    break
                except Exception as e:
                    logger.error(f"Error in menu loop: {e}", exc_info=True)
                    ui.show_error("Menu Error", f"An error occurred: {str(e)}")
            
            # Cleanup
            if self.popup:
                try:
                    self.popup.stop()
                    logger.info("Accessibility popup stopped")
                except:
                    pass
            
            # Show goodbye
            ui.show_goodbye()
            logger.info("SlideSense application closed normally")
        
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
            console.print("\n\n[yellow]Program terminated by user[/yellow]")
        
        except Exception as e:
            ui.show_error(
                "Unexpected Error",
                f"An error occurred: {str(e)}",
                [
                    "Try restarting the program",
                    "Report issue if error persists"
                ]
            )
            import traceback
            traceback.print_exc()


def main() -> None:
    """Entry point"""
    
    # Check requirements
    required_modules = [
        ('pyautogui', 'PyAutoGUI'),
        ('speech_recognition', 'SpeechRecognition'),
        ('rich', 'rich'),
    ]
    
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            console.print(f"[red]❌ {display_name} tidak terinstall![/red]")
            console.print(f"   Install dengan: [cyan]pip install {module_name}[/cyan]")
            input("\nPress Enter to exit...")
            sys.exit(1)
    
    # Run application
    app = SlideSenseApp()
    app.run()


if __name__ == "__main__":
    main()
"""
UI Manager - Simple Fallback Version (No InquirerPy)
Menggunakan input() biasa untuk compatibility
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import os
import sys
import time
from typing import Optional, List, Dict, Any

console = Console()

class UIManager:
    """Simple UI Manager without InquirerPy - Maximum Compatibility"""
    
    def __init__(self) -> None:
        self.version: str = "2.0.0"
        
    def clear(self) -> None:
        """Clear screen safely"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self) -> None:
        """Show welcome screen"""
        self.clear()
        
        welcome = Panel.fit(
            "[bold cyan][MIC] SlideSense[/bold cyan]\n"
            "[dim]Voice-Controlled PowerPoint Presentation[/dim]\n\n"
            "[green][STAR] Control presentations with your voice[/green]\n"
            "[yellow][ACCESSIBLE] Accessibility features for all audiences[/yellow]\n\n"
            f"[dim]Version {self.version}[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(welcome)
        console.print()
        time.sleep(0.8)
    
    def show_main_menu(self) -> str:
        """Main menu - simple input version"""
        
        self.clear()
        
        # Header
        console.print(Panel(
            "[bold cyan]Main Menu[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
        
        # Menu options
        menu_table = Table(show_header=False, box=box.SIMPLE)
        menu_table.add_column("No", style="cyan bold", width=4)
        menu_table.add_column("Menu", style="white")
        
        menu_table.add_row("1", "[ROCKET] Start Voice Control")
        menu_table.add_row("2", "[MIC] Test Microphone")
        menu_table.add_row("3", "[BOOK] Tutorial & Help")
        menu_table.add_row("4", "[INFO] About Program")
        menu_table.add_row("0", "[EXIT] Exit")
        
        console.print(menu_table)
        console.print()
        
        # Get input
        try:
            choice = console.input("[cyan]Choose menu (0-4): [/cyan]").strip()
            
            menu_map = {
                "1": "start",
                "2": "test_mic",
                "3": "tutorial",
                "4": "about",
                "0": "exit"
            }
            
            return menu_map.get(choice, "invalid")
            
        except (KeyboardInterrupt, EOFError):
            return "exit"
    
    def show_microphone_setup(self, devices_list: List[Dict[str, Any]]) -> str:
        """Simple microphone setup"""
        
        console.print("\n[bold cyan][MIC] Setup Microphone[/bold cyan]\n")
        
        console.print("1. [STAR] Auto-detect (Recommended)")
        console.print("2. [TOOL] Choose manually from list")
        console.print()
        
        try:
            choice = console.input("[cyan]Choose (1/2): [/cyan]").strip()
            return "auto" if choice == "1" else "manual"
        except (KeyboardInterrupt, EOFError):
            return "manual"
    
    def show_microphone_list(self, devices: List[Dict[str, Any]]) -> Optional[int]:
        """Show microphone list for manual selection"""
        
        if not devices:
            console.print("[red]❌ No microphone detected[/red]")
            return None
        
        console.print("\n[bold cyan]Choose Microphone:[/bold cyan]\n")
        
        for device in devices:
            idx = device.get('index', 0)
            name = device.get('name', 'Unknown')
            channels = device.get('channels', 0)
            console.print(f"  {idx}. {name} [{channels} channels]")
        
        console.print()
        
        try:
            choice = console.input("[cyan]Choose device number: [/cyan]").strip()
            return int(choice) if choice.isdigit() else None
        except (KeyboardInterrupt, EOFError, ValueError):
            return None
    
    def show_auto_detect_progress(self) -> None:
        """Show progress while auto-detecting microphone"""
        console.print("[cyan]🔍 Mencari microphone terbaik...[/cyan]")
        time.sleep(1)
        console.print("[green][OK] Auto-detect complete![/green]\n")
    
    def show_device_found(self, device_name: str, device_index: int) -> bool:
        """Show device found message"""
        
        console.print(Panel(
            f"[bold green][OK] Microphone Detected[/bold green]\n\n"
            f"[cyan]Device:[/cyan] {device_name}\n"
            f"[cyan]Index:[/cyan] {device_index}",
            border_style="green"
        ))
        console.print()
        
        try:
            confirm = console.input("[cyan]Gunakan microphone ini? (y/n): [/cyan]").strip().lower()
            return confirm in ['y', 'yes', '']
        except (KeyboardInterrupt, EOFError):
            return False
    
    def show_microphone_test_start(self, duration: int = 3) -> None:
        """Show microphone test starting"""
        console.print(f"\n[bold cyan][MIC] Testing Microphone ({duration} sec)[/bold cyan]")
        console.print("[yellow][TIP] Speak now to test...[/yellow]\n")
    
    def show_test_progress(self, duration: int = 3) -> None:
        """Show test progress"""
        console.print("[cyan]Recording...[/cyan]")
        for i in range(duration):
            console.print(f"  {i+1}...", end=" ")  # Remove flush=True
            time.sleep(1)
        console.print()  # New line
    
    def show_test_result(self, success: bool, message: str = "") -> None:
        """Show test result"""
        if success:
            console.print("[bold green]✅ Test Berhasil![/bold green]")
            if message:
                console.print(f"[green][OK] {message}[/green]")
        else:
            console.print("[bold red][FAIL] Test Failed[/bold red]")
            if message:
                console.print(f"[yellow][TIP] {message}[/yellow]")
        
        console.print()
        input("Press Enter to continue...")
    
    def show_voice_control_starting(self) -> None:
        """Show voice control is starting"""
        self.clear()
        console.print(Panel(
            "[bold green][MIC] Voice Control Starting...[/bold green]\n"
            "[dim]Mempersiapkan sistem...[/dim]",
            border_style="green"
        ))
        time.sleep(1)
    
    def show_voice_control_active(self) -> None:
        """Show voice control active interface"""
        self.clear()
        
        header = Panel(
            "[bold green][MIC] VOICE CONTROL ACTIVE[/bold green]\n"
            "[dim]Bicara perintah atau tekan Ctrl+C untuk berhenti[/dim]",
            border_style="green"
        )
        console.print(header)
        
        guide = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        guide.add_column(style="cyan bold", width=15)
        guide.add_column()
        
        guide.add_row("Status", "[green]● Listening[/green]")
        guide.add_row("Mode", "Voice Only")
        guide.add_row("Help", "Katakan 'help menu'")
        guide.add_row("Stop", "Katakan 'stop program'")
        
        console.print(guide)
        console.print()
    
    def show_listening(self) -> None:
        """Show listening indicator"""
        console.print("[MIC] " + "="*56)
        console.print("[bold cyan]LISTENING...[/bold cyan] (speak now)")
        console.print("="*60)
    
    def show_command_detected(self, command: str, text: str, confidence: float) -> None:
        """Show command detected with confidence"""
        if confidence >= 80:
            color = "green"
            icon = "[OK]"
        elif confidence >= 60:
            color = "yellow"
            icon = "[WARN]"
        else:
            color = "red"
            icon = "[FAIL]"
        
        console.print(f"\n    [MSG] Detected: '{text}'")
        console.print(f"    {icon} [{color}]Command: {command}[/{color}]")
        console.print(f"    [STAT] Confidence: {confidence:.0f}%")
    
    def show_command_feedback(self, feedback_text: str) -> None:
        """Show command execution feedback"""
        console.print(f"    {feedback_text}")
    
    def show_no_speech(self) -> None:
        """Show no speech detected"""
        console.print("    [yellow]⏰ Tidak mendengar suara[/yellow]")
        console.print("    [dim][TIP] Try speaking louder or closer to the microphone[/dim]")
    
    def show_unknown_command(self, text: str) -> None:
        """Show unknown command"""
        console.print(f"    [yellow]❓ Perintah tidak dikenali: '{text}'[/yellow]")
        console.print("    [dim][TIP] Say 'help menu' for list of commands[/dim]")
    
    def show_tutorial(self) -> None:
        """Show tutorial"""
        self.clear()
        
        console.print(Panel(
            "[bold cyan][BOOK] Tutorial SlideSense[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
        
        console.print("[bold cyan][TARGET] Basic Commands[/bold cyan]")
        console.print("  • [green]'next slide'[/green] - Next slide")
        console.print("  • [green]'back slide'[/green] - Previous slide")
        console.print("  • [green]'help menu'[/green] - Help")
        console.print("  • [green]'stop program'[/green] - Exit\n")
        
        console.print("[bold cyan][MIC] Microphone Tips[/bold cyan]")
        console.print("  • Ideal distance: 15-30cm from your mouth")
        console.print("  • Speak clearly but calmly")
        console.print("  • Reduce background noise\n")
        
        input("Press Enter to go back...")
    
    def show_about(self) -> None:
        """Show about screen"""
        self.clear()
        
        about = Panel.fit(
            "[bold cyan]SlideSense[/bold cyan]\n"
            f"[dim]Version {self.version}[/dim]\n\n"
            "Voice-controlled PowerPoint presentation\n"
            "with accessibility features.\n\n"
            "[yellow]Created with [HEART] for education[/yellow]\n\n"
            "[dim]License: Apache 2.0[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(about)
        console.print()
        
        input("Press Enter to go back...")
    
    def show_error(self, title: str, message: str, suggestions: Optional[List[str]] = None) -> None:
        """Show error with helpful suggestions"""
        content = f"[bold red]{title}[/bold red]\n\n{message}"
        
        if suggestions:
            content += "\n\n[yellow][TIP] Suggestions:[/yellow]"
            for suggestion in suggestions:
                content += f"\n  • {suggestion}"
        
        error_panel = Panel(content, border_style="red", padding=(1, 2))
        console.print("\n")
        console.print(error_panel)
        console.print()
    
    def show_goodbye(self) -> None:
        """Show goodbye message"""
        self.clear()
        
        goodbye = Panel.fit(
            "[bold cyan]Thank you for using[/bold cyan]\n"
            "[bold cyan]SlideSense[/bold cyan]\n\n"
            "[yellow]See you next time! [WAVE][/yellow]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(goodbye)
        console.print()
    
    def show_initializing(self) -> None:
        """Show initializing message"""
        console.print("\n[bold cyan][INIT] Initializing System...[/bold cyan]")
    
    def show_initialization_step(self, step_name: str, success: bool = True) -> None:
        """Show initialization step result"""
        if success:
            console.print(f"  [green][OK] {step_name}[/green]")
        else:
            console.print(f"  [red][FAIL] {step_name}[/red]")
    
    def pause(self, message: str = "Press Enter to continue...") -> None:
        """Pause with message"""
        console.print(f"\n[dim]{message}[/dim]")
        input()


# Global instance
ui = UIManager()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI_UNIFIED_APP.py - Main Integrated GUI Application

Menggabungkan:
1. Home dashboard
2. Tutorial system
3. Statistics panel
4. Settings
5. Voice control integration
"""

import customtkinter as ctk
from src.gui.home import GUIHome
from src.gui.tutorial import InteractiveTutorial
from src.gui.stats import StatsPanel
from src.core.voice_detector import SmartVoiceDetector as PendeteksiSuaraCerdas
import threading
from datetime import datetime

class UnifiedGUIApp:
    def __init__(self):
        """Initialize unified GUI app"""
        self.root = None
        self.gui_home = None
        self.tutorial = None
        self.stats_panel = StatsPanel()
        self.detector = PendeteksiSuaraCerdas()
        
        self.listening = False
        self.listen_thread = None
        
        # Setup theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def create_main_window(self):
        """Create main application window"""
        self.root = ctk.CTk()
        self.root.title("SlideSense Voice Control - Complete Dashboard")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Configure layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create widgets
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
        
        return self.root
    
    def _create_header(self):
        """Create header with title and controls"""
        header_frame = ctk.CTkFrame(self.root, fg_color="#0a0a0a", height=60)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎤 SlideSense Voice Control Dashboard",
            font=("Arial", 20, "bold"),
            text_color="#00bfff"
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        # Status indicator
        self.status_indicator = ctk.CTkLabel(
            header_frame,
            text="● READY",
            font=("Arial", 11, "bold"),
            text_color="#00ff00"
        )
        self.status_indicator.pack(side="right", padx=15, pady=10)
    
    def _create_main_content(self):
        """Create main content area with tabs"""
        # Tabview for different sections
        tab_view = ctk.CTkTabview(self.root)
        tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Home Dashboard
        home_tab = tab_view.add("📊 Dashboard")
        self._create_dashboard_tab(home_tab)
        
        # Tab 2: Voice Commands
        commands_tab = tab_view.add("🎤 Voice Commands")
        self._create_commands_tab(commands_tab)
        
        # Tab 3: Tutorial
        tutorial_tab = tab_view.add("🎓 Tutorial")
        self._create_tutorial_tab(tutorial_tab)
        
        # Tab 4: Statistics
        stats_tab = tab_view.add("📈 Statistics")
        self._create_stats_tab(stats_tab)
        
        # Tab 5: Settings
        settings_tab = tab_view.add("⚙️ Settings")
        self._create_settings_tab(settings_tab)
    
    def _create_dashboard_tab(self, parent):
        """Create dashboard tab"""
        # Top section: Quick commands
        quick_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        quick_frame.pack(fill="x", padx=10, pady=10)
        
        quick_title = ctk.CTkLabel(
            quick_frame,
            text="⚡ Quick Actions",
            font=("Arial", 12, "bold"),
            text_color="#00bfff"
        )
        quick_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Quick buttons
        buttons_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        quick_commands = [
            ("➡️ Next", "next_slide"),
            ("⬅️ Back", "previous_slide"),
            ("▶️ Start", "open_slideshow"),
            ("⏹️ Stop", "close_slideshow"),
        ]
        
        for label, cmd in quick_commands:
            btn = ctk.CTkButton(
                buttons_frame,
                text=label,
                width=100,
                command=lambda c=cmd: self._execute_command(c)
            )
            btn.pack(side="left", padx=5)
        
        # Middle section: System info
        info_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="ℹ️ System Information",
            font=("Arial", 12, "bold"),
            text_color="#95e1d3"
        )
        info_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        info_items = [
            ("Status", "Ready & Listening"),
            ("Commands Available", "6 Core Commands"),
            ("Recognition Phrases", "9,431 variants"),
            ("Auto-Learning", "Enabled ✓"),
            ("Confidence Threshold", "70% (Adaptive)"),
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=10, pady=3)
            
            label_widget = ctk.CTkLabel(
                item_frame,
                text=label,
                font=("Arial", 10),
                text_color="#888888",
                width=150
            )
            label_widget.pack(side="left", anchor="w")
            
            value_widget = ctk.CTkLabel(
                item_frame,
                text=value,
                font=("Arial", 10, "bold"),
                text_color="#00ff00"
            )
            value_widget.pack(side="left", anchor="w", padx=20)
    
    def _create_commands_tab(self, parent):
        """Create voice commands tab"""
        # Commands list with buttons
        from constants import MAIN_COMMANDS
        
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(
            scroll_frame,
            text="🎯 6 CORE VOICE COMMANDS",
            font=("Arial", 14, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        for cmd_name, cmd_data in MAIN_COMMANDS.items():
            card = self._create_command_card(scroll_frame, cmd_name, cmd_data)
            card.pack(pady=10, padx=10, fill="x")
    
    def _create_command_card(self, parent, cmd_name: str, cmd_data: dict):
        """Create command card widget"""
        card_frame = ctk.CTkFrame(
            parent,
            fg_color="#1a1a1a",
            border_width=2,
            border_color="#00bfff"
        )
        
        # Header with button
        header = ctk.CTkFrame(card_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))
        
        cmd_label = ctk.CTkLabel(
            header,
            text=cmd_name.upper(),
            font=("Arial", 11, "bold"),
            text_color="#00ff00"
        )
        cmd_label.pack(side="left", anchor="w")
        
        execute_btn = ctk.CTkButton(
            header,
            text="Test",
            width=50,
            command=lambda c=cmd_name: self._execute_command(c)
        )
        execute_btn.pack(side="right", anchor="e")
        
        # Description
        desc_label = ctk.CTkLabel(
            card_frame,
            text=cmd_data.get('description', ''),
            font=("Arial", 9),
            text_color="#cccccc"
        )
        desc_label.pack(anchor="w", padx=10, pady=2)
        
        # Keywords
        keywords_text = ", ".join(cmd_data['keywords'][:6])
        if len(cmd_data['keywords']) > 6:
            keywords_text += f"... +{len(cmd_data['keywords']) - 6}"
        
        keywords_label = ctk.CTkLabel(
            card_frame,
            text=f"Keywords: {keywords_text}",
            font=("Arial", 8),
            text_color="#666666"
        )
        keywords_label.pack(anchor="w", padx=10, pady=(2, 10))
        
        return card_frame
    
    def _create_tutorial_tab(self, parent):
        """Create tutorial tab"""
        tutorial_frame = ctk.CTkFrame(parent)
        tutorial_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(
            tutorial_frame,
            text="🎓 Interactive Tutorial",
            font=("Arial", 14, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        description = ctk.CTkLabel(
            tutorial_frame,
            text="Learn all 6 voice commands step-by-step",
            font=("Arial", 11),
            text_color="#cccccc"
        )
        description.pack(pady=5)
        
        start_btn = ctk.CTkButton(
            tutorial_frame,
            text="▶ Start Tutorial",
            font=("Arial", 12, "bold"),
            width=200,
            height=50,
            fg_color="#00ff00",
            text_color="black",
            command=self._start_tutorial
        )
        start_btn.pack(pady=20)
        
        # Tutorial content preview
        preview_frame = ctk.CTkScrollableFrame(tutorial_frame, fg_color="#1a1a1a")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        preview_title = ctk.CTkLabel(
            preview_frame,
            text="What you'll learn:",
            font=("Arial", 11, "bold"),
            text_color="#95e1d3"
        )
        preview_title.pack(anchor="w", padx=10, pady=10)
        
        lessons = [
            "• All 6 core voice commands",
            "• Multiple ways to say each command",
            "• Tips for best recognition",
            "• How the system learns over time",
            "• Troubleshooting common issues",
        ]
        
        for lesson in lessons:
            lesson_label = ctk.CTkLabel(
                preview_frame,
                text=lesson,
                font=("Arial", 10),
                text_color="#cccccc"
            )
            lesson_label.pack(anchor="w", padx=20, pady=3)
    
    def _create_stats_tab(self, parent):
        """Create statistics tab"""
        stats_widget = self.stats_panel.create_widget(parent)
        stats_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_settings_tab(self, parent):
        """Create settings tab"""
        settings_frame = ctk.CTkScrollableFrame(parent)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(
            settings_frame,
            text="⚙️ SETTINGS",
            font=("Arial", 14, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        settings = [
            ("Microphone", "Default input device"),
            ("Auto-Learning", "Enabled"),
            ("Confidence Threshold", "70% (Adaptive)"),
            ("Feedback Sound", "On"),
            ("Display Confidence", "On"),
            ("Language", "Indonesian + English"),
        ]
        
        for setting, current in settings:
            setting_frame = ctk.CTkFrame(settings_frame, fg_color="#1a1a1a")
            setting_frame.pack(pady=10, padx=10, fill="x")
            
            label = ctk.CTkLabel(
                setting_frame,
                text=setting,
                font=("Arial", 11, "bold"),
                text_color="#00bfff"
            )
            label.pack(anchor="w", padx=10, pady=(10, 3))
            
            value = ctk.CTkLabel(
                setting_frame,
                text=f"• {current}",
                font=("Arial", 9),
                text_color="#888888"
            )
            value.pack(anchor="w", padx=10, pady=(0, 10))
    
    def _create_status_bar(self):
        """Create status bar"""
        status_frame = ctk.CTkFrame(self.root, fg_color="#0a0a0a", height=40)
        status_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        status_frame.pack_propagate(False)
        
        # Left: Status info
        left_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=10, pady=5)
        
        self.status_text = ctk.CTkLabel(
            left_frame,
            text="✓ System Ready | Phase 1: Complete | Phase 2: GUI Active",
            font=("Arial", 9),
            text_color="#888888"
        )
        self.status_text.pack(side="left")
        
        # Right: Control buttons
        right_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=10, pady=5)
        
        start_listen_btn = ctk.CTkButton(
            right_frame,
            text="🔴 Start Listening",
            width=120,
            fg_color="#00ff00",
            text_color="black",
            command=self._toggle_listening
        )
        start_listen_btn.pack(side="left", padx=5)
        self.listen_btn = start_listen_btn
        
        help_btn = ctk.CTkButton(
            right_frame,
            text="? Help",
            width=80,
            command=self._show_help
        )
        help_btn.pack(side="left", padx=5)
    
    def _execute_command(self, command: str):
        """Execute a command (for testing)"""
        print(f"Executing: {command}")
        self.stats_panel.record_command(command)
        self.status_text.configure(
            text=f"✓ Executed: {command} | {datetime.now().strftime('%H:%M:%S')}"
        )
    
    def _toggle_listening(self):
        """Toggle voice listening"""
        self.listening = not self.listening
        if self.listening:
            self.listen_btn.configure(text="🔴 Stop Listening", fg_color="#ff6b6b")
            self.status_indicator.configure(text="● LISTENING...")
        else:
            self.listen_btn.configure(text="🟢 Start Listening", fg_color="#00ff00")
            self.status_indicator.configure(text="● READY")
    
    def _start_tutorial(self):
        """Start interactive tutorial"""
        tutorial = InteractiveTutorial()
        window = tutorial.create_window()
        tutorial.run()
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """
SlideSense Voice Control - Help

6 CORE COMMANDS:
1. next_slide - Move to next slide
2. previous_slide - Go to previous slide
3. open_slideshow - Start presentation (F5)
4. close_slideshow - End presentation (ESC)
5. show_help - Display help
6. stop_program - Exit program

TIPS FOR BEST RESULTS:
• Speak clearly and naturally
• Microphone 6-12 inches away
• Avoid background noise
• The system learns from your usage
• Try different keywords for same command

Need more help? Check the Tutorial tab!
"""
        from tkinter import messagebox
        messagebox.showinfo("Help - SlideSense", help_text)
    
    def run(self):
        """Start the application"""
        if self.root is None:
            self.create_main_window()
        self.root.mainloop()

def main():
    """Main entry point"""
    app = UnifiedGUIApp()
    app.run()

if __name__ == "__main__":
    main()

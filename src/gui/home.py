#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI_HOME.py - Main GUI Dashboard for SlideSense Voice Control

Fitur:
1. Interactive home screen dengan 6 commands
2. Visual command reference
3. Quick tutorial
4. Usage statistics
5. Settings quick access
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import os
import json
from src.infrastructure.constants import MAIN_COMMANDS, get_command_description
from typing import Callable, Optional

class GUIHome:
    def __init__(self, on_command_selected: Optional[Callable] = None):
        """
        Initialize GUI Home Dashboard
        
        Args:
            on_command_selected: Callback when user selects a command
        """
        self.on_command_selected = on_command_selected
        self.root = None
        self.current_page = "home"  # home, tutorial, stats
        
        # Setup theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def create_window(self):
        """Create main application window"""
        self.root = ctk.CTk()
        self.root.title("SlideSense Voice Control - Home")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self._create_header()
        self._create_body()
        self._create_footer()
        
        return self.root
    
    def _create_header(self):
        """Create header with title and navigation"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎤 SlideSense Voice Control",
            font=("Arial", 24, "bold"),
            text_color="#00bfff"
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Status indicator
        status_label = ctk.CTkLabel(
            header_frame,
            text="● Ready",
            font=("Arial", 12),
            text_color="#00ff00"
        )
        status_label.pack(side="right", padx=10, pady=10)
    
    def _create_body(self):
        """Create main content area"""
        body_frame = ctk.CTkFrame(self.main_frame)
        body_frame.pack(fill="both", expand=True)
        
        # Left sidebar - Commands
        left_frame = ctk.CTkFrame(body_frame, fg_color="#0a0a0a", width=300)
        left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        self._create_commands_panel(left_frame)
        
        # Right content area
        right_frame = ctk.CTkFrame(body_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        self._create_content_area(right_frame)
    
    def _create_commands_panel(self, parent):
        """Create left panel with 6 commands"""
        # Title
        title = ctk.CTkLabel(
            parent,
            text="6 COMMANDS",
            font=("Arial", 14, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        # Commands
        commands_data = [
            ("next_slide", "➡️ Next Slide", "#ff6b6b"),
            ("previous_slide", "⬅️ Previous Slide", "#ff6b6b"),
            ("open_slideshow", "▶️ Open Slideshow", "#4ecdc4"),
            ("close_slideshow", "⏹️ Close Slideshow", "#4ecdc4"),
            ("show_help", "❓ Show Help", "#95e1d3"),
            ("stop_program", "⛔ Stop Program", "#f38181"),
        ]
        
        self.command_buttons = {}
        
        for cmd_id, label, color in commands_data:
            btn = ctk.CTkButton(
                parent,
                text=label,
                fg_color=color,
                text_color="white",
                font=("Arial", 11, "bold"),
                height=50,
                command=lambda cid=cmd_id: self._on_command_click(cid)
            )
            btn.pack(pady=5, padx=10, fill="x")
            self.command_buttons[cmd_id] = btn
    
    def _on_command_click(self, command_id: str):
        """Handle command button click"""
        self._show_command_details(command_id)
        if self.on_command_selected:
            self.on_command_selected(command_id)
    
    def _create_content_area(self, parent):
        """Create right content area (changes based on page)"""
        self.content_frame = ctk.CTkFrame(parent)
        self.content_frame.pack(fill="both", expand=True)
        
        # Navigation tabs
        tabs_frame = ctk.CTkFrame(self.content_frame)
        tabs_frame.pack(fill="x", pady=(0, 10))
        
        tab_items = [
            ("Overview", "overview"),
            ("Tutorial", "tutorial"),
            ("Statistics", "stats"),
            ("Settings", "settings"),
        ]
        
        for label, page in tab_items:
            btn = ctk.CTkButton(
                tabs_frame,
                text=label,
                width=100,
                command=lambda p=page: self._show_page(p)
            )
            btn.pack(side="left", padx=5)
        
        # Content display area
        self.content_display = ctk.CTkScrollableFrame(self.content_frame)
        self.content_display.pack(fill="both", expand=True)
        
        # Show initial overview
        self._show_page("overview")
    
    def _show_page(self, page: str):
        """Switch to different page"""
        self.current_page = page
        
        # Clear previous content
        for widget in self.content_display.winfo_children():
            widget.destroy()
        
        if page == "overview":
            self._show_overview()
        elif page == "tutorial":
            self._show_tutorial()
        elif page == "stats":
            self._show_statistics()
        elif page == "settings":
            self._show_settings()
    
    def _show_overview(self):
        """Show overview of 6 commands"""
        title = ctk.CTkLabel(
            self.content_display,
            text="🎯 6 CORE COMMANDS",
            font=("Arial", 16, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        description = ctk.CTkLabel(
            self.content_display,
            text="Simplified voice commands for PowerPoint presentations",
            font=("Arial", 11),
            text_color="#cccccc"
        )
        description.pack(pady=5)
        
        # Commands grid
        for cmd_name, cmd_data in MAIN_COMMANDS.items():
            self._create_command_card(cmd_name, cmd_data)
    
    def _create_command_card(self, cmd_name: str, cmd_data: dict):
        """Create a command card in overview"""
        card_frame = ctk.CTkFrame(
            self.content_display,
            fg_color="#1a1a1a",
            border_width=2,
            border_color="#00bfff"
        )
        card_frame.pack(pady=10, padx=10, fill="x")
        
        # Command name
        name_label = ctk.CTkLabel(
            card_frame,
            text=cmd_name.upper(),
            font=("Arial", 12, "bold"),
            text_color="#00ff00"
        )
        name_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Description
        desc_label = ctk.CTkLabel(
            card_frame,
            text=cmd_data.get('description', 'No description'),
            font=("Arial", 10),
            text_color="#cccccc"
        )
        desc_label.pack(anchor="w", padx=10, pady=5)
        
        # Keywords
        keywords_text = ", ".join(cmd_data['keywords'][:5])
        if len(cmd_data['keywords']) > 5:
            keywords_text += f"... ({len(cmd_data['keywords']) - 5} more)"
        
        keywords_label = ctk.CTkLabel(
            card_frame,
            text=f"Keywords: {keywords_text}",
            font=("Arial", 9),
            text_color="#888888"
        )
        keywords_label.pack(anchor="w", padx=10, pady=(5, 10))
    
    def _show_command_details(self, cmd_id: str):
        """Show detailed information about a command"""
        if cmd_id not in MAIN_COMMANDS:
            return
        
        cmd_data = MAIN_COMMANDS[cmd_id]
        
        # Clear previous details
        for widget in self.content_display.winfo_children():
            widget.destroy()
        
        # Command title
        title = ctk.CTkLabel(
            self.content_display,
            text=cmd_id.upper(),
            font=("Arial", 18, "bold"),
            text_color="#00ff00"
        )
        title.pack(pady=15)
        
        # Description
        desc = ctk.CTkLabel(
            self.content_display,
            text=cmd_data.get('description', 'No description'),
            font=("Arial", 12),
            text_color="#cccccc"
        )
        desc.pack(pady=10)
        
        # All keywords
        keywords_label = ctk.CTkLabel(
            self.content_display,
            text="📋 ALL KEYWORDS:",
            font=("Arial", 11, "bold"),
            text_color="#00bfff"
        )
        keywords_label.pack(pady=(15, 5))
        
        keywords_text = ", ".join(cmd_data['keywords'])
        keywords_display = ctk.CTkLabel(
            self.content_display,
            text=keywords_text,
            font=("Arial", 10),
            text_color="#888888",
            wraplength=400
        )
        keywords_display.pack(padx=10, pady=5)
        
        # Example usage
        examples_label = ctk.CTkLabel(
            self.content_display,
            text="💬 EXAMPLE USAGE:",
            font=("Arial", 11, "bold"),
            text_color="#00bfff"
        )
        examples_label.pack(pady=(15, 5))
        
        examples = [
            f'Try saying: "{cmd_data["keywords"][0]}"',
            f'Or say: "{cmd_data["keywords"][1]}"' if len(cmd_data['keywords']) > 1 else "",
        ]
        
        for example in examples:
            if example:
                ex_label = ctk.CTkLabel(
                    self.content_display,
                    text=f"• {example}",
                    font=("Arial", 10),
                    text_color="#cccccc"
                )
                ex_label.pack(anchor="w", padx=20, pady=3)
    
    def _show_tutorial(self):
        """Show interactive tutorial"""
        title = ctk.CTkLabel(
            self.content_display,
            text="🎓 QUICK TUTORIAL",
            font=("Arial", 16, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        steps = [
            ("1. SPEAK CLEARLY", "Use one of the 6 commands in a clear voice"),
            ("2. LISTEN FOR FEEDBACK", "The system will beep and show recognition"),
            ("3. WAIT FOR ACTION", "PowerPoint will respond to your command"),
            ("4. TRY DIFFERENT PHRASES", "Each command has multiple keyword options"),
            ("5. SYSTEM LEARNS", "Rare phrases are automatically learned over time"),
        ]
        
        for step_title, step_desc in steps:
            step_frame = ctk.CTkFrame(
                self.content_display,
                fg_color="#1a1a1a",
                border_width=1,
                border_color="#00bfff"
            )
            step_frame.pack(pady=8, padx=10, fill="x")
            
            title_label = ctk.CTkLabel(
                step_frame,
                text=step_title,
                font=("Arial", 11, "bold"),
                text_color="#00ff00"
            )
            title_label.pack(anchor="w", padx=10, pady=(8, 3))
            
            desc_label = ctk.CTkLabel(
                step_frame,
                text=step_desc,
                font=("Arial", 10),
                text_color="#cccccc"
            )
            desc_label.pack(anchor="w", padx=10, pady=(0, 8))
        
        # Tips
        tips_label = ctk.CTkLabel(
            self.content_display,
            text="💡 TIPS FOR BEST RESULTS:",
            font=("Arial", 11, "bold"),
            text_color="#95e1d3"
        )
        tips_label.pack(pady=(15, 5))
        
        tips = [
            "Speak naturally, not too fast or slow",
            "Microphone should be 6-12 inches away",
            "Avoid background noise when possible",
            "Use keywords that feel natural to you",
        ]
        
        for tip in tips:
            tip_label = ctk.CTkLabel(
                self.content_display,
                text=f"• {tip}",
                font=("Arial", 10),
                text_color="#cccccc"
            )
            tip_label.pack(anchor="w", padx=20, pady=2)
    
    def _show_statistics(self):
        """Show usage statistics"""
        title = ctk.CTkLabel(
            self.content_display,
            text="📊 STATISTICS",
            font=("Arial", 16, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        # Load stats if available
        stats_file = "command_stats.json"
        stats = {}
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            except:
                pass
        
        # System stats
        stats_frame = ctk.CTkFrame(self.content_display, fg_color="#1a1a1a")
        stats_frame.pack(pady=10, padx=10, fill="x")
        
        stat_items = [
            ("6 Main Commands", "Simplified voice control"),
            ("95+ Keywords", "Multiple ways to say each command"),
            ("9,431 Phrases", "Including phoneme variants"),
            ("Auto-Learning", "Continuous improvement"),
        ]
        
        for label, value in stat_items:
            stat_row = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_row.pack(fill="x", padx=10, pady=5)
            
            label_widget = ctk.CTkLabel(
                stat_row,
                text=label,
                font=("Arial", 10, "bold"),
                text_color="#00ff00",
                width=150
            )
            label_widget.pack(side="left", anchor="w")
            
            value_widget = ctk.CTkLabel(
                stat_row,
                text=value,
                font=("Arial", 10),
                text_color="#cccccc"
            )
            value_widget.pack(side="left", anchor="w")
    
    def _show_settings(self):
        """Show settings panel"""
        title = ctk.CTkLabel(
            self.content_display,
            text="⚙️ SETTINGS",
            font=("Arial", 16, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        settings = [
            ("Microphone Input", "Default device"),
            ("Confidence Threshold", "70% (adaptive)"),
            ("Auto-Learning", "Enabled"),
            ("Feedback Sound", "On"),
            ("Display Confidence", "On"),
        ]
        
        for setting, value in settings:
            setting_frame = ctk.CTkFrame(self.content_display, fg_color="#1a1a1a")
            setting_frame.pack(pady=8, padx=10, fill="x")
            
            label = ctk.CTkLabel(
                setting_frame,
                text=setting,
                font=("Arial", 10, "bold"),
                text_color="#00bfff"
            )
            label.pack(anchor="w", padx=10, pady=(5, 3))
            
            value_label = ctk.CTkLabel(
                setting_frame,
                text=f"• {value}",
                font=("Arial", 9),
                text_color="#888888"
            )
            value_label.pack(anchor="w", padx=10, pady=(0, 5))
    
    def _create_footer(self):
        """Create footer with info and controls"""
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color="#0a0a0a")
        footer_frame.pack(fill="x", pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            footer_frame,
            text="✓ System Ready | Phase 1: Complete | Auto-Learning: Active",
            font=("Arial", 9),
            text_color="#888888"
        )
        info_label.pack(side="left", padx=10, pady=5)
        
        # Control buttons
        buttons_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=10, pady=5)
        
        start_btn = ctk.CTkButton(
            buttons_frame,
            text="▶ Start Listening",
            width=120,
            fg_color="#00ff00",
            text_color="black"
        )
        start_btn.pack(side="left", padx=5)
        
        help_btn = ctk.CTkButton(
            buttons_frame,
            text="? Help",
            width=80,
            fg_color="#00bfff",
            text_color="white"
        )
        help_btn.pack(side="left", padx=5)
    
    def run(self):
        """Start GUI"""
        if self.root is None:
            self.create_window()
        self.root.mainloop()

def main():
    """Test GUI Home"""
    gui = GUIHome()
    gui.create_window()
    gui.run()

if __name__ == "__main__":
    main()

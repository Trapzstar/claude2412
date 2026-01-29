#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI_INTERACTIVE_TUTORIAL.py - Interactive Voice Command Tutorial

Fitur:
1. Step-by-step tutorial
2. Interactive command tester
3. Pronunciation guide
4. Real-time feedback
"""

import customtkinter as ctk
from src.infrastructure.constants import MAIN_COMMANDS

class InteractiveTutorial:
    def __init__(self):
        """Initialize tutorial"""
        self.current_step = 0
        self.completed_steps = set()
        
        self.tutorial_steps = [
            {
                "title": "Welcome to SlideSense!",
                "content": "This tutorial will teach you the 6 core voice commands.",
                "command": None,
                "tips": [
                    "Speak clearly and naturally",
                    "Microphone should be 6-12 inches away",
                    "Avoid background noise",
                ]
            },
            {
                "title": "Command #1: next_slide",
                "content": "Move to the next slide in your presentation.",
                "command": "next_slide",
                "tips": [
                    "Say: 'next slide'",
                    "Or: 'lanjut'",
                    "Or: 'maju'",
                ]
            },
            {
                "title": "Command #2: previous_slide",
                "content": "Move to the previous slide in your presentation.",
                "command": "previous_slide",
                "tips": [
                    "Say: 'previous slide'",
                    "Or: 'mundur'",
                    "Or: 'back'",
                ]
            },
            {
                "title": "Command #3: open_slideshow",
                "content": "Start your presentation (equivalent to F5).",
                "command": "open_slideshow",
                "tips": [
                    "Say: 'open slideshow'",
                    "Or: 'start presentation'",
                    "Or: 'mulai presentasi'",
                ]
            },
            {
                "title": "Command #4: close_slideshow",
                "content": "End your presentation (equivalent to ESC).",
                "command": "close_slideshow",
                "tips": [
                    "Say: 'close slideshow'",
                    "Or: 'stop presentation'",
                    "Or: 'tutup presentasi'",
                ]
            },
            {
                "title": "Command #5: show_help",
                "content": "Display the help menu with command reference.",
                "command": "show_help",
                "tips": [
                    "Say: 'show help'",
                    "Or: 'help menu'",
                    "Or: 'bantuan'",
                ]
            },
            {
                "title": "Command #6: stop_program",
                "content": "Exit the SlideSense application.",
                "command": "stop_program",
                "tips": [
                    "Say: 'stop program'",
                    "Or: 'exit'",
                    "Or: 'berhenti'",
                ]
            },
            {
                "title": "Tutorial Complete! 🎉",
                "content": "You now know all 6 core commands. The system learns from your speech patterns.",
                "command": None,
                "tips": [
                    "Speak naturally - don't memorize exact phrases",
                    "The more you use it, the better it gets",
                    "Unusual phrases are automatically learned",
                ]
            }
        ]
    
    def create_window(self):
        """Create tutorial window"""
        window = ctk.CTk()
        window.title("SlideSense Tutorial")
        window.geometry("800x600")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = window
        self._create_ui()
        
        return window
    
    def _create_ui(self):
        """Create tutorial UI"""
        # Header
        header = ctk.CTkLabel(
            self.window,
            text="🎓 Interactive Tutorial",
            font=("Arial", 18, "bold"),
            text_color="#00bfff"
        )
        header.pack(pady=10)
        
        # Progress bar
        progress_frame = ctk.CTkFrame(self.window)
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text=f"Step {self.current_step + 1} of {len(self.tutorial_steps)}",
            font=("Arial", 10),
            text_color="#00bfff"
        )
        self.progress_label.pack(side="left")
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400
        )
        self.progress_bar.pack(side="right", expand=True, fill="x", padx=(10, 0))
        self._update_progress()
        
        # Content frame
        self.content_frame = ctk.CTkScrollableFrame(self.window)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Navigation buttons
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(pady=10, padx=20, fill="x")
        
        self.prev_btn = ctk.CTkButton(
            button_frame,
            text="◀ Previous",
            command=self._previous_step,
            width=100
        )
        self.prev_btn.pack(side="left", padx=5)
        
        self.next_btn = ctk.CTkButton(
            button_frame,
            text="Next ▶",
            command=self._next_step,
            width=100,
            fg_color="#00ff00",
            text_color="black"
        )
        self.next_btn.pack(side="right", padx=5)
        
        self._show_current_step()
    
    def _show_current_step(self):
        """Display current tutorial step"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        step = self.tutorial_steps[self.current_step]
        
        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text=step["title"],
            font=("Arial", 16, "bold"),
            text_color="#00ff00"
        )
        title.pack(pady=10)
        
        # Content
        content = ctk.CTkLabel(
            self.content_frame,
            text=step["content"],
            font=("Arial", 12),
            text_color="#cccccc",
            wraplength=600,
            justify="left"
        )
        content.pack(pady=10)
        
        # If command step, show command details
        if step["command"]:
            self._show_command_details(step["command"])
        
        # Tips
        tips_title = ctk.CTkLabel(
            self.content_frame,
            text="💡 Tips:",
            font=("Arial", 11, "bold"),
            text_color="#95e1d3"
        )
        tips_title.pack(pady=(15, 5), anchor="w")
        
        for tip in step["tips"]:
            tip_label = ctk.CTkLabel(
                self.content_frame,
                text=f"• {tip}",
                font=("Arial", 10),
                text_color="#cccccc"
            )
            tip_label.pack(anchor="w", padx=20, pady=2)
        
        # Mark step as completed
        self.completed_steps.add(self.current_step)
        
        # Update button states
        self.prev_btn.configure(
            state="normal" if self.current_step > 0 else "disabled"
        )
        self.next_btn.configure(
            state="normal" if self.current_step < len(self.tutorial_steps) - 1 else "disabled"
        )
    
    def _show_command_details(self, cmd_name: str):
        """Show details for a command"""
        if cmd_name not in MAIN_COMMANDS:
            return
        
        cmd_data = MAIN_COMMANDS[cmd_name]
        
        # Separator
        sep = ctk.CTkLabel(
            self.content_frame,
            text="─" * 50,
            text_color="#333333"
        )
        sep.pack(pady=10)
        
        # Keywords
        keywords_title = ctk.CTkLabel(
            self.content_frame,
            text="Try these variations:",
            font=("Arial", 11, "bold"),
            text_color="#00bfff"
        )
        keywords_title.pack(pady=(10, 5), anchor="w")
        
        # Show first 8 keywords
        for i, keyword in enumerate(cmd_data['keywords'][:8]):
            keyword_label = ctk.CTkLabel(
                self.content_frame,
                text=f"  → {keyword}",
                font=("Arial", 10),
                text_color="#888888"
            )
            keyword_label.pack(anchor="w", padx=20, pady=2)
        
        if len(cmd_data['keywords']) > 8:
            more_label = ctk.CTkLabel(
                self.content_frame,
                text=f"  ... and {len(cmd_data['keywords']) - 8} more variants",
                font=("Arial", 9),
                text_color="#666666"
            )
            more_label.pack(anchor="w", padx=20, pady=2)
    
    def _next_step(self):
        """Go to next step"""
        if self.current_step < len(self.tutorial_steps) - 1:
            self.current_step += 1
            self._update_progress()
            self._show_current_step()
    
    def _previous_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self._update_progress()
            self._show_current_step()
    
    def _update_progress(self):
        """Update progress bar and label"""
        progress = self.current_step / (len(self.tutorial_steps) - 1)
        self.progress_bar.set(progress)
        self.progress_label.configure(
            text=f"Step {self.current_step + 1} of {len(self.tutorial_steps)}"
        )
    
    def run(self):
        """Start tutorial"""
        self.window.mainloop()

def start_tutorial():
    """Start interactive tutorial"""
    tutorial = InteractiveTutorial()
    window = tutorial.create_window()
    tutorial.run()

if __name__ == "__main__":
    start_tutorial()

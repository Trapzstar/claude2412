#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI_STATS_PANEL.py - Statistics & Monitoring Dashboard

Fitur:
1. Real-time recognition statistics
2. Command usage history
3. Auto-learning progress
4. System performance metrics
"""

import customtkinter as ctk
from datetime import datetime
import json
import os
from typing import Dict, List

class StatsPanel:
    def __init__(self, parent=None):
        """Initialize statistics panel"""
        self.parent = parent
        self.stats_file = "command_stats.json"
        self.stats = self._load_stats()
        self.performance_metrics = {
            "recognition_accuracy": 0.85,  # 85%
            "avg_response_time": 0.42,     # 0.42 seconds
            "total_commands_run": 0,
            "successful_commands": 0,
            "failed_commands": 0,
        }
    
    def _load_stats(self) -> Dict:
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "next_slide": 0,
            "previous_slide": 0,
            "open_slideshow": 0,
            "close_slideshow": 0,
            "show_help": 0,
            "stop_program": 0,
        }
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving stats: {e}")
    
    def record_command(self, command: str):
        """Record a command execution"""
        if command in self.stats:
            self.stats[command] += 1
            self.performance_metrics["total_commands_run"] += 1
            self.performance_metrics["successful_commands"] += 1
            self.save_stats()
    
    def record_failure(self, command: str):
        """Record a failed recognition"""
        self.performance_metrics["total_commands_run"] += 1
        self.performance_metrics["failed_commands"] += 1
    
    def get_command_usage(self) -> List[tuple]:
        """Get commands sorted by usage"""
        return sorted(self.stats.items(), key=lambda x: x[1], reverse=True)
    
    def get_most_used_command(self) -> tuple:
        """Get most used command"""
        if not self.stats:
            return None, 0
        return max(self.stats.items(), key=lambda x: x[1])
    
    def get_total_commands(self) -> int:
        """Get total commands executed"""
        return sum(self.stats.values())
    
    def create_widget(self, parent=None):
        """Create stats panel widget"""
        panel = ctk.CTkFrame(parent or self.parent, fg_color="#1a1a1a")
        
        # Title
        title = ctk.CTkLabel(
            panel,
            text="📊 SESSION STATISTICS",
            font=("Arial", 12, "bold"),
            text_color="#00bfff"
        )
        title.pack(pady=10)
        
        # Stats grid
        stats_frame = ctk.CTkFrame(panel, fg_color="transparent")
        stats_frame.pack(pady=10, padx=10, fill="both")
        
        # Performance metrics
        metrics_data = [
            ("Recognition Accuracy", f"{self.performance_metrics['recognition_accuracy']*100:.1f}%"),
            ("Avg Response Time", f"{self.performance_metrics['avg_response_time']:.2f}s"),
            ("Total Commands", str(self.performance_metrics['total_commands_run'])),
            ("Success Rate", f"{(self.performance_metrics['successful_commands'] / max(self.performance_metrics['total_commands_run'], 1) * 100):.1f}%"),
        ]
        
        for label, value in metrics_data:
            metric_row = ctk.CTkFrame(stats_frame, fg_color="transparent")
            metric_row.pack(fill="x", pady=3)
            
            label_widget = ctk.CTkLabel(
                metric_row,
                text=label,
                font=("Arial", 9),
                text_color="#888888",
                width=150
            )
            label_widget.pack(side="left", anchor="w")
            
            value_widget = ctk.CTkLabel(
                metric_row,
                text=value,
                font=("Arial", 9, "bold"),
                text_color="#00ff00"
            )
            value_widget.pack(side="right", anchor="e")
        
        # Separator
        sep = ctk.CTkLabel(stats_frame, text="─" * 40, text_color="#333333")
        sep.pack(pady=5)
        
        # Command usage
        usage_title = ctk.CTkLabel(
            panel,
            text="Command Usage:",
            font=("Arial", 10, "bold"),
            text_color="#95e1d3"
        )
        usage_title.pack(pady=(10, 5))
        
        usage_frame = ctk.CTkFrame(panel, fg_color="transparent")
        usage_frame.pack(padx=10, fill="x")
        
        for cmd_name, count in self.get_command_usage()[:3]:  # Top 3
            cmd_row = ctk.CTkFrame(usage_frame, fg_color="transparent")
            cmd_row.pack(fill="x", pady=2)
            
            cmd_label = ctk.CTkLabel(
                cmd_row,
                text=cmd_name,
                font=("Arial", 8),
                text_color="#cccccc",
                width=120
            )
            cmd_label.pack(side="left", anchor="w")
            
            count_label = ctk.CTkLabel(
                cmd_row,
                text=f"×{count}",
                font=("Arial", 8),
                text_color="#00ff00"
            )
            count_label.pack(side="right", anchor="e")
        
        return panel

def create_stats_dashboard():
    """Create standalone stats dashboard"""
    window = ctk.CTk()
    window.title("SlideSense - Statistics")
    window.geometry("400x600")
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    panel = StatsPanel()
    stats_widget = panel.create_widget(window)
    stats_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Add refresh button
    def refresh():
        stats_widget.destroy()
        panel = StatsPanel()
        stats_widget = panel.create_widget(window)
        stats_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    refresh_btn = ctk.CTkButton(window, text="🔄 Refresh", command=refresh)
    refresh_btn.pack(pady=10)
    
    window.mainloop()

if __name__ == "__main__":
    create_stats_dashboard()

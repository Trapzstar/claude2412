#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN_COMMANDS.py - 6 Perintah Utama SlideSense.id

Definisi centralized untuk 6 perintah utama voice control.
Mudah untuk diupdate dan maintain.
"""

# 6 MAIN COMMANDS CONFIGURATION
MAIN_COMMANDS = {
    "next_slide": {
        "keywords": [
            "next", "lanjut", "maju", "slide next", "next slide", 
            "lanjut slide", "slide lanjut", "slide berikutnya", "berikutnya",
            "nxt", "nexs", "nex", "majuu", "maju slide"
        ],
        "aliases": ["next", "forward", "proceed", "advance"],
        "description": "Lanjutkan ke slide berikutnya",
        "description_en": "Move to next slide",
        "weight": 10,
        "action": "next_slide"
    },
    
    "previous_slide": {
        "keywords": [
            "back", "previous", "mundur", "kembali", "prev",
            "sebelumnya", "slide back", "back slide", "slide mundur",
            "mundur slide", "slide sebelumnya", "kembali slide",
            "bak", "previus", "previeus", "back slide"
        ],
        "aliases": ["back", "previous", "prior", "retreat"],
        "description": "Kembali ke slide sebelumnya",
        "description_en": "Go to previous slide",
        "weight": 10,
        "action": "previous_slide"
    },
    
    "open_slideshow": {
        "keywords": [
            "open", "buka", "start", "mulai", "f5",
            "open slideshow", "buka slideshow", "start slideshow",
            "mulai slideshow", "open presentation", "buka presentasi",
            "start presentation", "mulai presentasi", "open slide show",
            "buka slide show", "presentasi mulai", "open", "opn"
        ],
        "aliases": ["open", "start", "launch", "begin"],
        "description": "Buka presentasi slideshow (F5)",
        "description_en": "Open slideshow (F5)",
        "weight": 15,
        "action": "open_slideshow"
    },
    
    "close_slideshow": {
        "keywords": [
            "close", "tutup", "stop", "exit", "keluar", "berhenti",
            "close slideshow", "tutup slideshow", "stop slideshow",
            "exit slideshow", "keluar slideshow", "tutup presentasi",
            "close presentation", "stop presentation", "akhiri presentasi",
            "presentasi berhenti", "end slideshow", "klos", "cls"
        ],
        "aliases": ["close", "exit", "stop", "end"],
        "description": "Tutup slideshow (ESC)",
        "description_en": "Close slideshow (ESC)",
        "weight": 15,
        "action": "close_slideshow"
    },
    
    "show_help": {
        "keywords": [
            "help", "bantuan", "menu help", "help menu",
            "show help", "tampilkan bantuan", "bantuan menu",
            "menu bantuan", "helm", "halp", "hlp", "bantuan menu"
        ],
        "aliases": ["help", "assist", "support", "guide"],
        "description": "Tampilkan daftar bantuan",
        "description_en": "Show help menu",
        "weight": 8,
        "action": "show_help"
    },
    
    "stop_program": {
        "keywords": [
            "stop", "berhenti", "exit", "quit", "keluar", "hentikan",
            "stop program", "berhenti program", "exit program",
            "quit program", "keluar program", "program stop",
            "program berhenti", "program exit", "stp", "stap"
        ],
        "aliases": ["stop", "exit", "quit", "end"],
        "description": "Hentikan program",
        "description_en": "Stop program",
        "weight": 15,
        "action": "stop_program"
    }
}

# COMMAND SHORTCUTS (untuk akses cepat)
COMMAND_BY_ACTION = {cmd_data["action"]: cmd_name 
                     for cmd_name, cmd_data in MAIN_COMMANDS.items()}

KEYWORDS_INDEX = {}
for cmd_name, cmd_data in MAIN_COMMANDS.items():
    for keyword in cmd_data["keywords"]:
        KEYWORDS_INDEX[keyword.lower()] = cmd_name

# PHONEME VARIANTS PER COMMAND
# Ini akan diperluas dengan speech_history_analyzer.py
PHONEME_VARIANTS_BY_COMMAND = {
    "next_slide": ["next", "nex", "nek", "neks", "nexs", "nxt", "nx"],
    "previous_slide": ["back", "bak", "prev", "previus", "privieus"],
    "open_slideshow": ["open", "opn", "open", "opin"],
    "close_slideshow": ["close", "klos", "cls", "clous", "kloz"],
    "show_help": ["help", "hlp", "halp", "helm"],
    "stop_program": ["stop", "stp", "stap", "stope"]
}

# DESCRIPTION UNTUK UI
COMMAND_DESCRIPTIONS = {
    "next_slide": {
        "id": "Lanjutkan ke slide berikutnya",
        "en": "Move to next slide",
        "keywords": "next, lanjut, maju, berikutnya",
        "example": "Katakan: 'next' atau 'lanjut'"
    },
    "previous_slide": {
        "id": "Kembali ke slide sebelumnya",
        "en": "Go to previous slide",
        "keywords": "previous, back, mundur, kembali",
        "example": "Katakan: 'back' atau 'mundur'"
    },
    "open_slideshow": {
        "id": "Buka presentasi dalam mode slideshow (F5)",
        "en": "Open presentation in slideshow mode (F5)",
        "keywords": "open, buka, start, mulai",
        "example": "Katakan: 'open' atau 'buka presentasi'"
    },
    "close_slideshow": {
        "id": "Tutup slideshow dan kembali ke editor (ESC)",
        "en": "Close slideshow and return to editor (ESC)",
        "keywords": "close, tutup, stop, exit",
        "example": "Katakan: 'close' atau 'tutup'"
    },
    "show_help": {
        "id": "Tampilkan daftar lengkap perintah suara yang tersedia",
        "en": "Show list of available voice commands",
        "keywords": "help, bantuan, menu",
        "example": "Katakan: 'help' atau 'bantuan'"
    },
    "stop_program": {
        "id": "Hentikan program SlideSense.id",
        "en": "Stop SlideSense.id program",
        "keywords": "stop, berhenti, exit, keluar",
        "example": "Katakan: 'stop' atau 'berhenti'"
    }
}

# TESTING & VALIDATION
def get_command_by_keyword(keyword: str) -> str:
    """Cari perintah berdasarkan keyword"""
    return KEYWORDS_INDEX.get(keyword.lower(), None)

def get_all_keywords() -> list:
    """Dapatkan semua keywords"""
    return list(KEYWORDS_INDEX.keys())

def get_command_description(command: str, language: str = "id") -> dict:
    """Dapatkan deskripsi perintah"""
    if command not in COMMAND_DESCRIPTIONS:
        return None
    desc = COMMAND_DESCRIPTIONS[command]
    return {
        "description": desc.get(language, desc.get("id")),
        "keywords": desc.get("keywords"),
        "example": desc.get("example")
    }

def validate_command(command: str) -> bool:
    """Validasi apakah perintah valid"""
    return command in MAIN_COMMANDS

# CONSTANTS UNTUK ERROR HANDLING
DEFAULT_CONFIDENCE_THRESHOLD = 6.0
COOLDOWN_SECONDS = 2

# Test jika file dijalankan langsung
if __name__ == "__main__":
    print("\n=== 6 MAIN COMMANDS ===\n")
    for idx, (cmd_name, cmd_data) in enumerate(MAIN_COMMANDS.items(), 1):
        print(f"{idx}. {cmd_name.upper()}")
        print(f"   Description: {cmd_data['description']}")
        print(f"   Keywords: {', '.join(cmd_data['keywords'][:3])}...")
        print(f"   Weight: {cmd_data['weight']}\n")
    
    print(f"Total Keywords: {len(KEYWORDS_INDEX)}")
    print(f"Total Commands: {len(MAIN_COMMANDS)}")

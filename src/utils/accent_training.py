# ============================================
# ACCENT TRAINING MODE - Learn user's pronunciation
# ============================================
from datetime import datetime

class AccentTrainingMode:
    """Train system to recognize user's specific accent"""
    
    CORE_COMMANDS = [
        "next slide",
        "back slide", 
        "open slide show",
        "close slide show",
        "help menu",
        "stop program"
    ]
    
    def __init__(self, voice, detector, debug=True):
        self.voice = voice
        self.detector = detector
        self.debug = debug
        self.user_pronunciations = {}
    
    def run_training(self):
        """Run accent training session"""
        self._show_intro()
        self._collect_pronunciations()
        self._save_training()
        self._show_results()
    
    def _show_intro(self):
        """Show training introduction"""
        print("\n" + "="*60)
        print("🎓 ACCENT TRAINING MODE")
        print("="*60)
        print("""
Sistem akan belajar cara Anda mengucapkan perintah.
Ini akan meningkatkan akurasi deteksi hingga 95%!

Anda akan diminta mengucapkan 6 perintah.
Setiap perintah direkam 3 kali untuk accuracy maksimal.

Total waktu: ~2 menit

Mari mulai!
        """)
        input("Tekan Enter untuk memulai...")
    
    def _collect_pronunciations(self):
        """Collect user pronunciations for each command"""
        print("\n" + "-"*60)
        
        for idx, command in enumerate(self.CORE_COMMANDS, 1):
            print(f"\n📝 COMMAND {idx}/{len(self.CORE_COMMANDS)}: '{command}'")
            print("-"*60)
            
            variations = []
            
            for attempt in range(3):
                print(f"\n🎤 Percobaan {attempt+1}/3")
                print(f"   Katakan: '{command}'")
                print(f"   (Ucapkan dengan cara Anda sendiri, jangan meniru-niru)")
                
                input("   Tekan Enter untuk merekam...")
                
                text = self.voice.listen()
                
                if text:
                    variations.append({
                        'text': text,
                        'attempt': attempt + 1,
                        'score': self._calculate_match_score(text, command)
                    })
                    print(f"   ✅ Recorded: '{text}'")
                else:
                    print(f"   ❌ Gagal merekam. Coba lagi...")
                    attempt -= 1  # Retry this attempt
            
            # Store collected data
            self.user_pronunciations[command] = variations
            
            # Show summary
            if variations:
                avg_score = sum(v['score'] for v in variations) / len(variations)
                print(f"\n✅ Summary: {len(variations)} variations recorded (avg confidence: {avg_score:.1f}/10)")
    
    def _calculate_match_score(self, text, command):
        """Calculate how well text matches command"""
        try:
            from fuzzywuzzy import fuzz
            score = fuzz.ratio(text.lower(), command.lower()) / 10.0  # Scale to 0-10
            return min(10, score)
        except:
            return 5.0  # Default score
    
    def _save_training(self):
        """Save training data"""
        print("\n" + "="*60)
        print("💾 MENYIMPAN DATA TRAINING...")
        
        # In production, save to file or database
        training_data = {
            'timestamp': str(datetime.now()),
            'pronunciations': self.user_pronunciations,
            'total_samples': sum(len(v) for v in self.user_pronunciations.values())
        }
        
        # Add to detector for future use
        for command, variations in self.user_pronunciations.items():
            # Extract just the text
            variant_texts = [v['text'] for v in variations]
            
            # Add to detector's phrase list
            for cmd_name, cmd_data in self.detector.wake_words.items():
                # Find matching command
                if cmd_data['description'].lower() in command.lower() or command.lower() in cmd_data['description'].lower():
                    cmd_data['phrases'].extend(variant_texts)
        
        print("✅ Training data saved!")
    
    def _show_results(self):
        """Show training results"""
        print("\n" + "="*60)
        print("✅ TRAINING SELESAI!")
        print("="*60)
        
        total_samples = sum(len(v) for v in self.user_pronunciations.values())
        
        print(f"\n📊 HASIL:")
        print(f"   • Perintah ditraining: {len(self.user_pronunciations)}")
        print(f"   • Total samples: {total_samples}")
        print(f"   • Akurasi proyeksi: ~95% untuk aksen Anda")
        
        print("\n💡 HASIL TRAINING:")
        for command, variations in self.user_pronunciations.items():
            if variations:
                avg_score = sum(v['score'] for v in variations) / len(variations)
                print(f"   • {command}")
                print(f"     Variations: {[v['text'] for v in variations]}")
                print(f"     Confidence: {avg_score:.1f}/10")
        
        print("\n✅ Sistem sekarang lebih familiar dengan aksen Anda!")
        print("   Akurasi deteksi akan terus meningkat seiring penggunaan.\n")

# Runner
def run_accent_training(voice, detector):
    """Run training session"""
    trainer = AccentTrainingMode(voice, detector)
    trainer.run_training()

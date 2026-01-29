# ============================================
# KELAS VOICE DETECTOR (SMART DETECTION)
# ============================================
import time
from typing import Optional, Dict, List, Any, Tuple, Set
from src.utils.validators import InputValidator, get_validator
from src.utils.feedback import get_feedback_ui
from src.infrastructure.config import get_config
from src.utils.matcher import AdaptiveMatcher
from src.core.phoneme_variants import PhonemeVariants

class SmartVoiceDetector:
    def __init__(self, config: Optional[Dict[str, Any]] = None, feedback_ui: Optional[Any] = None) -> None:
        # Import libraries for fuzzy matching and phonetic algorithms
        try:
            from fuzzywuzzy import fuzz
            import jellyfish
            self.fuzzy_available = True
        except ImportError:
            print("[WARN] Fuzzy matching libraries not available. Install with: pip install fuzzywuzzy jellyfish")
            self.fuzzy_available = False
        
        self.validator = get_validator()
        self.feedback_ui = feedback_ui or get_feedback_ui()
        self.config = config or get_config()
        self.adaptive_matcher = AdaptiveMatcher(base_threshold=6.0)

        # Wake words (frasa lengkap) + auto-generated phoneme variants
        self.wake_words = {
            "next": {
                "phrases": self._expand_with_variants(["next slide", "slide next", "lanjut slide", "slide lanjut"]),
                "weight": 10,
                "description": "Slide maju"
            },
            "previous": {
                "phrases": self._expand_with_variants(["back slide", "slide back", "mundur slide", "slide mundur", "previous slide", "slide previous"]),
                "weight": 10,
                "description": "Slide mundur"
            },
            "open_slideshow": {
                "phrases": ["open slide show", "slide show open", "start slide show", "slide show start", "mulai slide show", "slide show mulai", "buka slide show", "slide show buka", "f5", "mulai presentasi", "presentasi mulai", "buka presentasi", "presentasi buka", "start presentation", "presentation start", "open slide", "open side show", "open slideshows"],
                "weight": 18,  # Increased weight to prioritize 3-word commands
                "description": "Buka slideshow (F5)"
            },
            "close_slideshow": {
                "phrases": ["close slide show", "slide show close", "quit slide show", "slide show quit", "keluar slide show", "slide show keluar", "tutup slide show", "slide show tutup", "stop slide show", "slide show stop", "akhiri presentasi", "presentasi akhiri", "tutup presentasi", "presentasi tutup", "end presentation", "presentation end", "exit slideshow", "slideshow exit", "close slide", "close side show", "close slideshows"],
                "weight": 18,  # Increased weight to prioritize 3-word commands
                "description": "Tutup slideshow (ESC)"
            },
            "help": {
                "phrases": ["help menu", "menu help", "bantuan menu", "menu bantuan", "helm menu", "hal menu", "helmmu", "menu bantu", "menu bantuanmu", "menu bantuin", "held menu", "hell menu", "help me menu"],
                "weight": 8,
                "description": "Tampilkan bantuan"
            },
            "stop": {
                "phrases": ["stop program", "program stop", "berhenti program", "program berhenti", "stop", "berhenti", "stok program", "setiap program", "top program", "stop programnya", "stop progran"],
                "weight": 15,  # Tinggi untuk stop
                "description": "Stop program"
            },
            "test": {
                "phrases": ["test mic", "mic test", "test microphone", "microphone test", "test audio", "audio test"],
                "weight": 8,
                "description": "Test microphone"
            },
            "noise": {
                "phrases": ["toggle noise", "noise toggle", "noise reduction", "reduction noise", "noise on", "noise off"],
                "weight": 8,
                "description": "Toggle noise reduction"
            },
            "popup_on": {
                "phrases": ["popup on", "show popup", "popup show", "enable popup", "popup enable", "turn on popup", "popup turn on"],
                "weight": 8,
                "description": "Tampilkan popup bantu"
            },
            "popup_off": {
                "phrases": ["popup off", "hide popup", "popup hide", "disable popup", "popup disable", "turn off popup", "popup turn off"],
                "weight": 8,
                "description": "Sembunyikan popup bantu"
            },
            "caption_on": {
                "phrases": ["caption on", "start caption", "caption start", "enable caption", "caption enable", "turn on caption", "caption turn on", "live caption on", "caption live on"],
                "weight": 8,
                "description": "Tampilkan teks caption dan mulai live captioning real-time"
            },
            "caption_off": {
                "phrases": ["caption off", "stop caption", "caption stop", "disable caption", "caption disable", "turn off caption", "caption turn off", "live caption off", "caption live off"],
                "weight": 12,
                "description": "Teks caption berhenti dan sembunyikan live captioning real-time"
            },
            "change_language": {
                "phrases": ["change language", "language change", "switch language", "language switch", "ganti bahasa", "bahasa ganti"],
                "weight": 7,
                "description": "Change caption language"
            },
            "show_analytics": {
                "phrases": ["show analytics", "analytics show", "display analytics", "analytics display", "session stats", "stats session"],
                "weight": 7,
                "description": "Show session analytics"
            }
        }
        self.last_execution_time = 0
        self.cooldown_seconds = 2  # Cooldown 2 detik setelah eksekusi
    
    def _expand_with_variants(self, phrases: List[str]) -> List[str]:
        """Expand phrase list with phoneme variants - minimal filtering"""
        expanded = set()
        
        for phrase in phrases:
            # Add original
            expanded.add(phrase)
            
            # Add phoneme variants (minimal filtering to avoid breaking valid matches)
            variants = PhonemeVariants.generate_variants(phrase)
            # Only skip extremely short variants
            for variant in variants:
                if len(variant) >= 2:  # Keep anything 2+ chars
                    expanded.add(variant)
            
            # Add regional variants
            regional = PhonemeVariants.add_regional_variants(phrase, region='mixed')
            for variant in regional:
                if len(variant) >= 2:
                    expanded.add(variant)
        
        return list(expanded)
    
    def detect(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Deteksi perintah suara dengan proses:
        1. User berbicara
        2. Program mendengarkan (sudah di hybrid_voice_recognizer)
        3. Menampilkan apa yang didengar
        4. Mencari perintah terdekat
        5. Jika tidak ditemukan, tunjukkan saran atau simpan ke file
        """
        # SECURITY: Validate and sanitize input
        sanitized, error = InputValidator.validate_and_sanitize(text)
        if error:
            print(f"    [WARN] Input validation error: {error}")
            return None
        
        text = sanitized
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_execution_time < self.cooldown_seconds:
            print(f"    [WAIT] Cooldown aktif, tunggu {self.cooldown_seconds - (current_time - self.last_execution_time):.1f} detik lagi")
            return None
        
        if not text or len(text.strip()) < 2:
            return None
        
        text_lower = text.lower().strip()
        
        # STEP 3: Menampilkan apa yang didengar
        print(f"\n    [HEARD] Anda berkata: '{text_lower}'")
        
        results = []
        
        # STEP 4: Mencari perintah terdekat dengan scoring lebih ketat
        for command, data in self.wake_words.items():
            for phrase in data["phrases"]:
                score = 0
                
                # EXACT MATCH - poin tertinggi
                if phrase == text_lower:
                    score = data["weight"] + 20
                # PHRASE CONTAINS - poin tinggi
                elif phrase in text_lower:
                    score = data["weight"] + 10
                # PARTIAL MATCH - dengan batasan ketat untuk membedakan open/close
                else:
                    phrase_words = phrase.split()
                    text_words = text_lower.split()
                    
                    # Hitung matching words
                    matching_words = [w for w in phrase_words if w in text_words]
                    if len(matching_words) >= 2:  # Minimal 2 kata cocok
                        score = data["weight"] + (len(matching_words) * 3)
                    elif len(matching_words) == 1 and len(phrase_words) <= 2:  # 1 kata dari 2 kata phrase
                        score = data["weight"] + 1
                
                # Fuzzy Matching hanya untuk sisa yang score 0
                if score == 0 and self.fuzzy_available:
                    try:
                        from fuzzywuzzy import fuzz
                        similarity = fuzz.ratio(text_lower, phrase)
                        if similarity >= 85:  # Threshold ketat 85%
                            score = data["weight"] + (similarity / 20)
                    except:
                        pass
                
                if score > 0:
                    results.append({
                        "command": command,
                        "phrase": phrase,
                        "score": score,
                        "max_score": data["weight"] + 20,
                        "description": data["description"]
                    })
        
        # Sort by score - highest first, with tie-breaking:
        # When scores are equal, prefer commands with exact/closer phrase matches
        def sort_key(result):
            score = result["score"]
            # Secondary sort: prefer exact/longer phrase matches
            phrase_length = len(result["phrase"].split())
            phrase_match_quality = 0
            
            # Check how well the phrase matches the input
            phrase_words = set(result["phrase"].split())
            text_words = set(text_lower.split())
            matching_words = len(phrase_words & text_words)
            phrase_match_quality = matching_words / max(len(phrase_words), 1)
            
            # Return tuple: (score descending, match quality descending, phrase length descending)
            return (-score, -phrase_match_quality, -phrase_length)
        
        results.sort(key=sort_key)
        
        # STEP 5: Jika tidak ada hasil, simpan ke file
        if not results:
            self._save_unrecognized_command(text_lower)
            print(f"    [NOT FOUND] Perintah tidak dikenali: '{text_lower}'")
            print(f"    [TIP] Ucapkan: 'next slide', 'back slide', 'open slide show', 'close slide show', 'help menu', atau 'stop program'")
            return {
                "command": "unknown",
                "reason": "No matching command found",
                "user_input": text_lower
            }
        
        best_match = results[0]
        
        # Cek apakah skor cukup tinggi
        min_score_threshold = 8.0
        
        if best_match["score"] >= min_score_threshold:
            # SECURITY: Validate command is safe
            if not InputValidator.validate_command(best_match["command"]):
                print(f"    [WARN] Command validation failed: {best_match['command']}")
                return None
            
            self.last_execution_time = current_time
            
            # Tampilkan hasil detection
            print(f"    [OK] Cocok: {best_match['description']}")
            print(f"    [CONF] Keyakinan: {best_match['score']:.1f}/{best_match['max_score']}")
            
            # Record success for adaptive learning
            if hasattr(self.adaptive_matcher, 'record_success'):
                self.adaptive_matcher.record_success(best_match["command"], best_match["score"])
            
            return best_match
        
        else:
            # Score rendah - tunjukkan saran yang mirip
            print(f"    [LOW] Keyakinan rendah: {best_match['score']:.1f} (butuh >= {min_score_threshold})")
            print(f"    [TIP] Yang Anda maksud adalah: {best_match['description']}?")
            print(f"    [INPUT] Ucapkan: 'yes' untuk lanjut, atau ulangi perintah")
            
            # Simpan ke file unrecognized
            self._save_unrecognized_command(
                text_lower, 
                best_match["command"],
                best_match["score"],
                best_match["description"]
            )
            
            # Record failure
            if hasattr(self.adaptive_matcher, 'record_failure'):
                self.adaptive_matcher.record_failure(text, best_match["score"])
            
            return {
                "command": "unknown",
                "score": best_match["score"],
                "reason": f"Low confidence: {best_match['score']:.1f}/{min_score_threshold}",
                "suggestion": best_match["description"],
                "user_input": text_lower
            }
    
    def show_help(self) -> None:
        """Tampilkan bantuan wake words"""
        print("\n" + "[SPEAKER] " + "="*50)
        print("[LIST] DAFTAR WAKE WORDS (FRASE LENGKAP):")
        print("="*50)
        
        for cmd, data in self.wake_words.items():
            print(f"\n[TARGET] {data['description'].upper()}:")
            phrases = ", ".join(data['phrases'])
            print(f"   Frasa: {phrases}")
        
        print(f"\n[WAIT] Cooldown: {self.cooldown_seconds} detik setelah setiap eksekusi")
        print("\n[INFO] FITUR TOLERANSI:")
        print("   • Fuzzy Matching: Mendeteksi frasa mirip (80%+ similarity)")
        print("   • Phonetic Algorithms: Mendeteksi kata dengan bunyi serupa")
        print("   • Daftar Sinonim: Mendukung variasi pengucapan")
        print("   • Accessibility Popup: Popup bantu untuk audiens difabel")
        print("\n[TIP] Gunakan frasa lengkap untuk hasil terbaik")
        print("\n" + "[GAME] " + "="*50)
        print("KONTROL PROGRAM:")
        print("  Voice Mode: Bicara langsung")
        print("  Help      : Katakan 'help menu' untuk bantuan ini")
        print("  Popup     : Katakan 'popup on'/'popup off' untuk popup accessibility")
        print("  Caption   : Katakan 'caption on'/'caption off' untuk live caption")
        print("  Language  : Katakan 'change language' untuk ganti bahasa")
        print("  Analytics : Katakan 'show analytics' untuk statistik")
        print("  Exit      : Katakan 'stop program' untuk keluar")
        print("  Ctrl+C    : Emergency stop")
        print("="*50 + "\n")
    
    def _save_unrecognized_command(self, user_input: str, closest_match: Optional[str] = None, confidence: float = 0.0, suggestion: Optional[str] = None) -> None:
        """Simpan perintah yang tidak dikenali ke file untuk analisis"""
        import json
        from datetime import datetime
        
        try:
            # Load existing data
            try:
                with open("unrecognized_commands.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                data = {"unrecognized_commands": [], "metadata": {"total_unrecognized": 0}}
            
            # Add new entry
            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_input": user_input,
                "closest_match": closest_match or "none",
                "confidence": round(confidence, 2),
                "suggestions": [suggestion] if suggestion else []
            }
            
            data["unrecognized_commands"].append(entry)
            data["metadata"]["total_unrecognized"] = len(data["unrecognized_commands"])
            data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save back
            with open("unrecognized_commands.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"    [SAVED] Disimpan ke unrecognized_commands.json")
        except Exception as e:
            print(f"    [WARN] Error saving unrecognized command: {e}")
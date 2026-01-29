# ============================================
# PHONEME VARIANTS - Accent-aware phrase generation
# ============================================

class PhonemeVariants:
    """Generate phonetic variants for Indonesian accents and dialects"""
    
    # Common Indonesian vowel variations
    VOWEL_PATTERNS = {
        'e': ['e', 'é', 'è', 'ə'],  # E variants (including schwa)
        'a': ['a', 'á', 'à'],
        'i': ['i', 'í', 'ì'],
        'o': ['o', 'ó', 'ò'],
        'u': ['u', 'ú', 'ù'],
    }
    
    # Consonant substitutions (regional accents)
    CONSONANT_PATTERNS = {
        'c': ['c', 'ch', 'k'],  # C → K variation (Javanese)
        'g': ['g', 'ng'],       # G medial position
        'ng': ['ng', 'n'],      # NG → N variation
        's': ['s', 'sh', 'z'],  # S → SH variation
        'j': ['j', 'dj'],       # J → DJ variation
        'y': ['y', 'i'],        # Y → I variation
    }
    
    # Word-level substitutions for common commands
    WORD_SUBSTITUTIONS = {
        'next': ['next', 'neks', 'nekst', 'nex', 'nek', 'naxs','nek','necks','nexx','nekes','nexs','translate','teks'],
        'slide': ['slide', 'slaid', 'slid', 'slyde', 'slaid','lite','slait','slyd','sled','slets','slet','slets'],
        'back': ['back', 'bak', 'bek', 'bæk', 'bak', 'beck','bakk','bake','bax','bakc','bag','beg'],
        'previous': ['previous', 'previeus', 'privieus', 'previous','reviews','previus','preveus','previws','prevews','privius','priviws'],
        'open': ['open', 'opèn', 'opén', 'opin','open','opeen','openn','opem','opun','aupèn','aupén','aupin','aupen','openn','opem','opun','aupèn','aupén','aupin','aupen','aupenn','aupem','aupun'],
        'close': ['close', 'klos', 'klous', 'kloz', 'cloze','clous','cloz','kloze','kloas','kloes','kloaz'],
        'help': ['help', 'hèlp', 'hélp', 'help','hep'],
        'stop': ['stop', 'estop', 'istop', 'stap', 'stòp','stóp','stopp','stope','stoup','stob','stob','stopp','stope','stoup','stob','stob','stopp','stope','stoup','stob','stob','stopp','stope','stoup','stob','stob','setop'],
        'show': ['show', 'sho', 'sow', 'syow', 'shou','shoo','shouw','shoa','shoe','shouh','showw'],
        'menu': ['menu', 'mènu', 'ménu', 'meenu', 'minu','manu','minu','menuu','menou','menue','manou','manue','minou','minue','manou','manue'],
    }
    
    @staticmethod
    def generate_variants(phrase):
        """
        Generate phonetic variants of a phrase for accent tolerance
        
        Args:
            phrase: Original phrase (e.g., "next slide")
        
        Returns:
            List of variant phrases
        """
        variants = set([phrase])  # Include original
        words = phrase.lower().split()
        
        # Generate word-by-word variants
        word_variants = []
        for word in words:
            if word in PhonemeVariants.WORD_SUBSTITUTIONS:
                word_variants.append(PhonemeVariants.WORD_SUBSTITUTIONS[word])
            else:
                # Generate phonetic variants for unknown words
                word_variants.append(PhonemeVariants._generate_word_variants(word))
        
        # Create combinations
        if len(word_variants) == 1:
            # Single word
            for variant in word_variants[0]:
                variants.add(variant)
        elif len(word_variants) == 2:
            # Two words
            for v1 in word_variants[0]:
                for v2 in word_variants[1]:
                    variants.add(f"{v1} {v2}")
        else:
            # More than two words - use original combinations
            for v1 in word_variants[0]:
                for v2 in word_variants[1]:
                    rest = " ".join(words[2:])
                    variants.add(f"{v1} {v2} {rest}")
        
        return list(variants)
    
    @staticmethod
    def _generate_word_variants(word):
        """Generate variants for a single word"""
        variants = [word]
        
        # Vowel variations
        for original, variants_list in PhonemeVariants.VOWEL_PATTERNS.items():
            if original in word:
                for variant in variants_list:
                    new_word = word.replace(original, variant)
                    if new_word not in variants:
                        variants.append(new_word)
        
        # Consonant variations
        for original, variants_list in PhonemeVariants.CONSONANT_PATTERNS.items():
            if original in word:
                for variant in variants_list:
                    new_word = word.replace(original, variant)
                    if new_word not in variants:
                        variants.append(new_word)
        
        return list(set(variants))  # Remove duplicates
    
    @staticmethod
    def add_regional_variants(phrase, region='mixed'):
        """
        Generate region-specific variants
        
        Args:
            phrase: Original phrase
            region: 'javanese', 'sundanese', 'mixed', etc.
        
        Returns:
            List of region-specific variants
        """
        variants = PhonemeVariants.generate_variants(phrase)
        
        # Add region-specific patterns
        if region in ['javanese', 'mixed']:
            # Javanese: tends to drop final consonants, 'ng' → 'n'
            javanese_variants = []
            for v in variants:
                # Remove final consonants
                if v and v[-1] in 'tpskcng':
                    javanese_variants.append(v[:-1])
                # NG → N
                javanese_variants.append(v.replace('ng', 'n'))
            variants.extend(javanese_variants)
        
        if region in ['sundanese', 'mixed']:
            # Sundanese: tends to shift vowels
            sundanese_variants = []
            for v in variants:
                # E → I shift
                sundanese_variants.append(v.replace('e', 'i'))
                # O → U shift
                sundanese_variants.append(v.replace('o', 'u'))
            variants.extend(sundanese_variants)
        
        if region in ['betawi', 'mixed']:
            # Betawi: tends to drop syllables
            betawi_variants = []
            for v in variants:
                words = v.split()
                # Remove short words
                betawi_variants.append(' '.join(w for w in words if len(w) > 2))
            variants.extend(betawi_variants)
        
        return list(set(variants))  # Remove duplicates
    
    @staticmethod
    def phonetic_distance(word1, word2):
        """
        Calculate phonetic distance between two words
        Lower score = more similar phonetically
        """
        from difflib import SequenceMatcher
        
        # Convert to similar phonetic representation
        p1 = PhonemeVariants._to_phonetic(word1)
        p2 = PhonemeVariants._to_phonetic(word2)
        
        # Calculate similarity
        ratio = SequenceMatcher(None, p1, p2).ratio()
        return 1.0 - ratio  # Distance (lower is closer)
    
    @staticmethod
    def _to_phonetic(word):
        """Convert word to simplified phonetic representation"""
        # Remove diacritics
        replacements = {
            'é': 'e', 'è': 'e', 'ê': 'e',
            'á': 'a', 'à': 'a', 'â': 'a',
            'í': 'i', 'ì': 'i', 'î': 'i',
            'ó': 'o', 'ò': 'o', 'ô': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u',
        }
        
        phonetic = word.lower()
        for original, replacement in replacements.items():
            phonetic = phonetic.replace(original, replacement)
        
        return phonetic

import re
from typing import Dict, Optional, Tuple
from rapidfuzz import fuzz

# Canonical synonym dictionary mapping common morphological/phrasing variants
SYNONYM_MAP: Dict[str, str] = {
    # Weaving & Textiles
    "yarn soaking": "yarn_soaking",
    "soak the yarn": "yarn_soaking",
    "soaking the thread": "yarn_soaking",
    "thread soaking": "yarn_soaking",
    "dyeing with madder": "madder_dyeing",
    "madder root dye": "madder_dyeing",
    "mordant preparation": "mordant_preparation",
    "alum mordanting": "mordant_preparation",
    "warp preparation": "warp_preparation",
    "setting the warp": "warp_preparation",
    "reed beating": "reed_beating",
    "beating the weft": "reed_beating",
    "loom setting": "loom_setup",
    "setting up the loom": "loom_setup",
    
    # Folk Culture & Performing Arts
    "balancing the pot": "pot_balancing",
    "head balance": "pot_balancing",
    "pot placement": "pot_balancing",
    "neem leaves decoration": "margosa_decoration",
    "decorating with neem": "margosa_decoration",
    "kavadi attam step": "kavadi_movement",
    "rhythm coordination": "tala_coordination",
    "thavil accompaniment": "thavil_accompaniment",
    "parai beat pattern": "parai_rhythm_pattern",
    "invocation song": "kaappu_invocation",
    "kaappu singing": "kaappu_invocation",
    
    # Traditional Plants & Herbal Knowledge
    "grinding leaves": "leaf_trituration",
    "leaf paste preparation": "leaf_trituration",
    "triturating herb": "leaf_trituration",
    "decoction preparation": "kashayam_decoction",
    "boiling herbal extract": "kashayam_decoction",
    "kashayam boiling": "kashayam_decoction",
    "sun drying herbs": "solar_desiccation",
    "shade drying": "shade_drying",
    "clarified butter vehicle": "ghee_anupana",
    "honey vehicle": "honey_anupana",

    # Marine & Coastal Heritage
    "catamaran assembly": "kattumaram_lashing",
    "lashing logs": "kattumaram_lashing",
    "coir rope binding": "kattumaram_lashing",
    "star navigation": "celestial_navigation",
    "reading wave patterns": "wave_reading_direction",
    "weaving drift net": "drift_net_weaving",
    "fish salting": "fish_curing",
    "sun drying fish": "sun_curing_fish",

    # Agriculture & Farming
    "seed soaking in cow urine": "gomutra_seed_treatment",
    "cow urine treatment": "gomutra_seed_treatment",
    "panchagavya application": "panchagavya_spray",
    "spraying panchagavya": "panchagavya_spray",
    "navara rice harvesting": "traditional_harvesting",
    "soil mulching": "dry_mulching",
    "broadcasting paddy seeds": "seed_broadcasting",
    "transplanting saplings": "sapling_transplantation",

    # Traditional Crafts
    "clay kneading": "clay_preparation",
    "kneading the clay": "clay_preparation",
    "lost wax casting": "lost_wax_technique",
    "cire perdue method": "lost_wax_technique",
    "palm leaf seasoning": "palm_leaf_seasoning",
    "boiling palm fronds": "palm_leaf_seasoning",
    "etching with stylus": "stylus_incising",
    "applying lampblack": "lampblack_inking",

    # Tamil Literature & Manuscripts
    "stylus incising": "manuscript_incising",
    "turmeric preservation": "turmeric_leaf_coating",
    "coating with turmeric": "turmeric_leaf_coating",
    "citronella oil rub": "citronella_conditioning",
    "conditioning palm leaf": "citronella_conditioning",
    "binding cord threading": "manuscript_cord_binding",
    "wooden board casing": "wooden_covers_casing"
}

TAMIL_ENGLISH_MAP: Dict[str, str] = {
    "கரகம் சுழற்றுதல்": "pot_balancing",
    "வேப்பிலை அலங்காரம்": "margosa_decoration",
    "காப்பு பாடுதல்": "kaappu_invocation",
    "நூல் ஊறவைத்தல்": "yarn_soaking",
    "மஞ்சள் பூச்சு": "turmeric_leaf_coating",
    "கஷாயம் காய்ச்சுதல்": "kashayam_decoction",
    "பஞ்சகவ்யம் தெளித்தல்": "panchagavya_spray",
    "விதை நேர்த்தி": "gomutra_seed_treatment",
    "கட்டுமரம் கட்டுதல்": "kattumaram_lashing",
    "ஓலை பதப்படுத்துதல்": "palm_leaf_seasoning",
    "மெழுகு வார்ப்பு": "lost_wax_technique",
    "மண் பிசைதல்": "clay_preparation",
    "எழுத்தாணி எழுதுதல்": "stylus_incising",
    "மை தடவுதல்": "lampblack_inking"
}

class NormalizationService:
    @staticmethod
    def clean_text(text: str) -> str:
        """Strip non-alphanumeric noise, collapse whitespace."""
        text = text.strip()
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)
        return text

    @staticmethod
    def to_canonical_key(phrase: str) -> str:
        """
        Convert phrase to standardized normalized key.
        Checks synonym dictionary and fuzzy similarity.
        """
        cleaned = phrase.strip().lower()
        # Direct Tamil lookup
        if phrase.strip() in TAMIL_ENGLISH_MAP:
            return TAMIL_ENGLISH_MAP[phrase.strip()]

        # Direct English synonym lookup
        if cleaned in SYNONYM_MAP:
            return SYNONYM_MAP[cleaned]

        # Check fuzzy match in synonym keys
        for key, canonical in SYNONYM_MAP.items():
            if fuzz.ratio(cleaned, key) >= 88:
                return canonical

        # Fallback canonical slug generator
        slug = re.sub(r'[^a-zA-Z0-9\s_-]', '', cleaned)
        slug = re.sub(r'[\s-]+', '_', slug).strip('_')
        return slug or "unspecified_element"

    @staticmethod
    def are_phrases_equivalent(phrase_a: str, phrase_b: str, threshold: float = 82.0) -> bool:
        """
        Check if two phrases refer to the same knowledge element.
        """
        key_a = NormalizationService.to_canonical_key(phrase_a)
        key_b = NormalizationService.to_canonical_key(phrase_b)
        if key_a == key_b:
            return True

        ratio = fuzz.token_sort_ratio(phrase_a.lower(), phrase_b.lower())
        return ratio >= threshold

"""
Comprehensive Demo Data Seeder for Tamil Vanishing Knowledge Detector
Covers all 7 Domains and their 38 Branches with 3 sample sources, 5-8 elements,
potential gaps, missing steps, evidence provenance, and urgency scoring.
"""

from database import SessionLocal, Base, engine
from models import (
    Tradition, Branch, Source, KnowledgeElement, KnowledgeGap,
    Evidence, PreservedKnowledge, GlossaryTerm
)
from services.urgency import UrgencyCalculationService
from services.reconstruction import ReconstructionService
import json
import uuid

DOMAINS_DATA = [
    {
        "id": "folk-culture",
        "name": "Folk Culture & Performing Arts",
        "tamil_name": "நாட்டுப்புறக் கலைகள் & நிகழ்த்து கலைகள்",
        "icon": "theater",
        "description": "Tamil Nadu's vibrant indigenous performance traditions, sacred dances, rhythm lore, and community storytelling arts.",
        "tamil_description": "தமிழகத்தின் தொன்மையான நிகழ்த்து கலைகள், வழிபாட்டு நடனங்கள், தாள மரபுகள் மற்றும் வாய்மொழி காவியங்கள்.",
        "branches": [
            {
                "id": "karagattam",
                "name": "Karagattam",
                "tamil_name": "கரகாட்டம்",
                "desc": "Traditional ritual dance balancing decorated brass pots filled with sacred water and neem leaves.",
                "tamil_desc": "புனித நீர் மற்றும் வேப்பிலையுடன் கூடிய பித்தளை கரகத்தை தலையில் தாங்கி ஆடும் பாரம்பரிய வழிபாட்டு ஆட்டம்.",
                "sample_elements": [
                    {"name": "Brass Chembu Pot Preparation", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "The brass chembu is purified and consecrated with turmeric water."},
                    {"name": "Filling Sacred Water and Raw Rice", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Raw rice and sanctified water are poured inside to stabilize weight."},
                    {"name": "Sealing with Green Coconut & Margosa", "category": "process_step", "step": 3, "s": [1, 3], "missing_in": [2], "quote": "A peeled green coconut topped with a lime and fresh margosa leaves seals the apex."},
                    {"name": "Fitting Peacock Feather Crown (Kili)", "category": "process_step", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "A wooden parrot (kili) embedded with peacock feathers is affixed to the crown."},
                    {"name": "Head Ring Balancing Pad (Piriman)", "category": "tool", "step": 5, "s": [1, 2, 3], "quote": "The piriman, a braided straw ring, cushions the performer's cranium."},
                    {"name": "Naiyandi Melam Syncopation", "category": "technique", "step": 6, "s": [1, 2, 3], "quote": "Acrobatic spins are synchronized to the dynamic beats of the Naiyandi Melam."}
                ],
                "gap_elem": "Sealing with Green Coconut & Margosa",
                "gap_type": "missing_step",
                "step_order": 3,
                "urgency": 74
            },
            {
                "id": "oyilattam",
                "name": "Oyilattam",
                "tamil_name": "ஒயிலாட்டம்",
                "desc": "Graceful rhythmic folk dance performed in unison with hand cloths and ankle bells.",
                "tamil_desc": "கைக்குட்டைகளையும் சலங்கைகளையும் அணிந்து ஒயிலாக ஆடப்படும் குழு நடன மரபு.",
                "sample_elements": [
                    {"name": "Kaappu Invocation Verse", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Singers invoke Murugan through traditional kaappu verses before beginning."},
                    {"name": "Ankle Bell Tuning (Salangai)", "category": "tool", "step": 2, "s": [1, 2, 3], "quote": "Bronze salangai are tightly strapped around the dancers' shins."},
                    {"name": "Synchronized Silk Kerchief Twirling", "category": "technique", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Colored cloth kerchiefs are flicked in precise arc patterns."},
                    {"name": "Circular Battle Stance (Viyyugam)", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "The performers transition into an ancient defensive circular formation."},
                    {"name": "Thavil Tala Acceleration", "category": "technique", "step": 5, "s": [1, 2, 3], "quote": "Rhythm doubles during the climactic oyil cadence."}
                ],
                "gap_elem": "Circular Battle Stance (Viyyugam)",
                "gap_type": "missing_element",
                "step_order": 4,
                "urgency": 82
            },
            {
                "id": "kummi",
                "name": "Kummi",
                "tamil_name": "கும்மி",
                "desc": "Ancient circular clapping dance of Tamil women, celebrating harvests and temple festivities.",
                "tamil_desc": "பெண்கள் வட்டமாக நின்று கைதட்டி பாடி ஆடும் தொன்மையான நாட்டுப்புற நடனம்.",
                "sample_elements": [
                    {"name": "Circular Formation around Lamp", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Performers form concentric rings around the central kuthuvilakku lamp."},
                    {"name": "Triple-Clap Cross Rhythm (Mukkai)", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "Hands clap forward, downward, and across partner's palms in 3 beats."},
                    {"name": "Spontaneous Oral Couplet Improvisation", "category": "practice", "step": 3, "s": [1, 3], "missing_in": [2], "quote": "Lead singer improvises topical verses answered by the chorus."},
                    {"name": "Swaying Bending Posture (Kuninthattam)", "category": "technique", "step": 4, "s": [1, 2, 3], "quote": "Torso sways rhythmically toward earth to signify fertility."},
                    {"name": "Final Mangalam Clapping", "category": "process_step", "step": 5, "s": [2, 3], "missing_in": [1], "quote": "A concluding blessing stanza sung while gradually slowing down."}
                ],
                "gap_elem": "Spontaneous Oral Couplet Improvisation",
                "gap_type": "missing_step",
                "step_order": 3,
                "urgency": 68
            },
            {
                "id": "kolattam",
                "name": "Kolattam",
                "tamil_name": "கோலாட்டம்",
                "desc": "Rhythmic stick dance striking lacquered wooden batons to intricate time measures.",
                "tamil_desc": "வண்ண மரக்கோல்களை தட்டி தாள நுட்பங்களுடன் ஆடும் கோலாட்ட மரபு.",
                "sample_elements": [
                    {"name": "Lacquered Wood Baton Selection", "category": "tool", "step": 1, "s": [1, 2, 3], "quote": "Tuned rosewood or teak batons are coated in natural resin lacquer."},
                    {"name": "Rope Weaving Pinnal Kolattam Setup", "category": "process_step", "step": 2, "s": [1, 2], "missing_in": [3], "quote": "Intricate overhead cords are suspended from the ceiling to plait during dance."},
                    {"name": "Baton Striking Counter-Cadence", "category": "technique", "step": 3, "s": [1, 2, 3], "quote": "Each dancer strikes both their own and their opposite partner's sticks."},
                    {"name": "Cord Unraveling Reverse Steps", "category": "process_step", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Dancers retrace inverted footsteps to unplait the woven rope braid."},
                    {"name": "Vocal Solkattu Syncopation", "category": "terminology", "step": 5, "s": [1, 2, 3], "quote": "Rhythm mnemonics 'Tha-Ki-Ta' are chanted while striking."}
                ],
                "gap_elem": "Cord Unraveling Reverse Steps",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 86
            },
            {
                "id": "therukoothu",
                "name": "Therukoothu",
                "tamil_name": "தெருக்கூத்து",
                "desc": "All-night open-air ritual folk theater dramatizing Mahabharata epics with elaborate headgear and makeup.",
                "tamil_desc": "மகாபாரதக் கதைகளை விடிய விடிய ஆடும் முகப்பூச்சு மற்றும் கிரீடங்களுடன் கூடிய தெரு நாடக மரபு.",
                "sample_elements": [
                    {"name": "Kattiyakkaran Prologue Announcement", "category": "process_step", "step": 1, "s": [1, 2, 3], "quote": "The jester-narrator Kattiyakkaran introduces the plot and moral conflict."},
                    {"name": "Rice Flour & Mica Face Inscription", "category": "material", "step": 2, "s": [1, 2, 3], "quote": "Natural pigments and pulverized mica are applied to sculpt facial planes."},
                    {"name": "Wooden Kiridam Crown Mounting", "category": "tool", "step": 3, "s": [1, 2, 3], "quote": "Carved lightweight wood headgear (kiridam) is secured with cotton ties."},
                    {"name": "Fire Pot Incantation Ritual", "category": "process_step", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Actors circle the sacrificial fire pot before donning their divine roles."},
                    {"name": "High-Pitch Vachanam Recitation", "category": "technique", "step": 5, "s": [1, 2, 3], "quote": "Stylized vocal delivery carrying across open village harvest fields."},
                    {"name": "Dawn Aarthi Benediction", "category": "process_step", "step": 6, "s": [1, 2], "missing_in": [3], "quote": "The drama concludes at dawn with camphor flame blessing the audience."}
                ],
                "gap_elem": "Fire Pot Incantation Ritual",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 88
            },
            {
                "id": "villupattu",
                "name": "Villupattu",
                "tamil_name": "வில்லுப்பாட்டு",
                "desc": "Musical bow storytelling where a stringed bow with bells is struck with wooden rods.",
                "tamil_desc": "மணிகள் கட்டப்பட்ட வில்லைக் குச்சிகளால் தட்டி கதை சொல்லும் தனித்துவ இசை மரபு.",
                "sample_elements": [
                    {"name": "Bow Tuning with Bronze Bells", "category": "tool", "step": 1, "s": [1, 2, 3], "quote": "Seven bronze bells are strung onto the palmyra bowstring."},
                    {"name": "Earthen Pot Resonator Placement", "category": "tool", "step": 2, "s": [1, 2, 3], "quote": "The center of the bow rests on an inverted mud pot (Kudam) for acoustic resonance."},
                    {"name": "Veesukol Striking Sequence", "category": "technique", "step": 3, "s": [1, 2, 3], "quote": "Slender wooden plectrum rods (veesukol) strike the cord rhythmically."},
                    {"name": "Lead Bow Player & Pulavar Chorus Dialogue", "category": "role", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "The chief bard questions the chorus who respond with humorous wit."},
                    {"name": "Sacred Hero Deification Strophe", "category": "process_step", "step": 5, "s": [1], "missing_in": [2, 3], "quote": "The local folk hero is consecrated through an ancient deification chant."}
                ],
                "gap_elem": "Sacred Hero Deification Strophe",
                "gap_type": "missing_step",
                "step_order": 5,
                "urgency": 79
            },
            {
                "id": "parai-isai",
                "name": "Parai Isai",
                "tamil_name": "பறை இசை",
                "desc": "The primordial frame drum of Tamil culture, conveying community news, mourning, and liberation rhythms.",
                "tamil_desc": "தமிழகத்தின் ஆதி இசைக்கருவியான தப்பட்டை/பறை கொண்டு முழங்கப்படும் வீர இசை.",
                "sample_elements": [
                    {"name": "Neem Wood Frame Hooping", "category": "material", "step": 1, "s": [1, 2, 3], "quote": "A sturdy circular rim bent from seasoned margosa or mango wood."},
                    {"name": "Cowhide Membrane Curing & Lacing", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Animal hide is degreased with lime and laced under taut tension."},
                    {"name": "Straw Heat Tempering (Parai Suttal)", "category": "process_step", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "The skin is held over glowing straw embers to tighten pitch before playing."},
                    {"name": "Sunda Kuchi & Adi Kuchi Dual-Stick Play", "category": "tool", "step": 4, "s": [1, 2, 3], "quote": "Slender bamboo sunda-kuchi and thick thumb stick create contrasting tones."},
                    {"name": "Por-Parai Battlefield Alarm Cadence", "category": "technique", "step": 5, "s": [1], "missing_in": [2, 3], "quote": "Ancient wartime cadence signaling mobilization, absent in modern performance."}
                ],
                "gap_elem": "Por-Parai Battlefield Alarm Cadence",
                "gap_type": "missing_element",
                "step_order": 5,
                "urgency": 91
            }
        ]
    },
    {
        "id": "traditional-plants",
        "name": "Traditional Plants & Herbal Knowledge",
        "tamil_name": "பாரம்பரிய தாவரங்கள் & மூலிகை அறிவு",
        "icon": "sprout",
        "description": "Siddha and folk ethnobotanical wisdom, native medicinal flora, and indigenous health preparations.",
        "tamil_description": "சித்த மருத்துவம், நாட்டுப்புற மூலிகைகள், காட்டு உணவுகள் மற்றும் பாரம்பரிய மருத்துவ முறைகள்.",
        "branches": [
            {
                "id": "medicinal-plants",
                "name": "Medicinal Plants",
                "tamil_name": "மருத்துவத் தாவரங்கள்",
                "desc": "Documentation of native flora like Nilavembu, Keezhanelli, and Adathodai and their therapeutic contexts.",
                "tamil_desc": "நிலவேம்பு, கீழாநெல்லி, ஆடாதோடை உள்ளிட்ட உள்நாட்டு தாவரங்களின் மருத்துவ பயன்பாடுகள்.",
                "sample_elements": [
                    {"name": "Morning Dew Harvesting of Keezhanelli", "category": "practice", "step": 1, "s": [1, 2, 3], "quote": "Whole Keezhanelli plants are plucked at dawn while dew remains on leaves."},
                    {"name": "Stone Mortar Cold Grinding", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Herb is triturated on granite stone without applying friction heat."},
                    {"name": "Fresh Cow Milk Vehicle (Pasum Paal Anupana)", "category": "material", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "The paste is rolled into areca-nut sized bolus and blended with raw unpasteurized milk."},
                    {"name": "Copper Vessel Overnight Potentiation", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Extract is left in an unlined copper vessel overnight to potentiate trace minerals."},
                    {"name": "Strict Salt and Pungent Dietary Restriction (Pathiyam)", "category": "cultural_context", "step": 5, "s": [1, 2, 3], "quote": "Patient must abstain from tamarind, salt, and chili during course."}
                ],
                "gap_elem": "Copper Vessel Overnight Potentiation",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 79
            },
            {
                "id": "herbal-remedies",
                "name": "Herbal Remedies",
                "tamil_name": "மூலிகை மருத்துவம்",
                "desc": "Classical decoctions (Kashayam), oils (Thailam), and lehyams passed through family practitioners.",
                "tamil_desc": "பாரம்பரிய கஷாயங்கள், தைலங்கள் மற்றும் லேகிய தயாரிப்பு முறைகள்.",
                "sample_elements": [
                    {"name": "Clay Pot Water Reduction to One-Fourth", "category": "process_step", "step": 1, "s": [1, 2, 3], "quote": "Boil 16 parts of water until reduced to 4 parts over mild cow-dung flame."},
                    {"name": "Three-Stage Muslin Cloth Filtration", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "Strain through unbleached cotton cloth three consecutive times."},
                    {"name": "Pre-Cooling Herb Ash Infusion (Karupu)", "category": "technique", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Charred medicinal root ash is dusted over the warm decoction surface."},
                    {"name": "Pure Forest Honey Vehicle Integration", "category": "material", "step": 4, "s": [1, 2, 3], "quote": "Wild honey is stirred only after the liquid cools to lukewarm temperature."},
                    {"name": "Brahmamuhurtha Administration", "category": "cultural_context", "step": 5, "s": [2, 3], "missing_in": [1], "quote": "Remedy is consumed at 4:30 AM on empty stomach."}
                ],
                "gap_elem": "Pre-Cooling Herb Ash Infusion (Karupu)",
                "gap_type": "missing_step",
                "step_order": 3,
                "urgency": 85
            },
            {
                "id": "sacred-plants",
                "name": "Sacred Plants",
                "tamil_name": "புனிதத் தாவரங்கள்",
                "desc": "Sacred grove flora, Sthala Vrikshas (temple trees), and ritually preserved botanical sanctuaries.",
                "tamil_desc": "கோவில் தல விருட்சங்கள், அய்யனார் கோவில் புனிதக் காடுகள் மற்றும் வழிபாட்டு தாவரங்கள்.",
                "sample_elements": [
                    {"name": "Vilvam (Bael) Leaf Triple Leaflet Selection", "category": "material", "step": 1, "s": [1, 2, 3], "quote": "Only unblemished trifoliate leaves representing the three gunas are gathered."},
                    {"name": "Sacred Grove Soil Barrier Protection", "category": "practice", "step": 2, "s": [1, 2, 3], "quote": "No metal footwear or felling axes are permitted within the Ayyanar grove boundary."},
                    {"name": "Folk Canopy Resin Bleeding Ritual", "category": "practice", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Votive incisions on trunk bark collected for ceremonial incense."},
                    {"name": "Vanni Tree Twig Smoke Purification", "category": "technique", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Dry twigs of Prosopis cineraria are burned to disinfect grain storage areas."}
                ],
                "gap_elem": "Folk Canopy Resin Bleeding Ritual",
                "gap_type": "missing_element",
                "step_order": 3,
                "urgency": 81
            },
            {
                "id": "wild-edible-plants",
                "name": "Wild Edible Plants",
                "tamil_name": "காட்டு உண்ணக்கூடிய தாவரங்கள்",
                "desc": "Famine foods, uncultivated leafy greens (Keerai), tubers, and wild berries of dry zone landscapes.",
                "tamil_desc": "பஞ்சம் தாங்கும் காட்டு கீரைகள், கிழங்குகள் மற்றும் காட்டுப் பழங்கள் பற்றிய அறிவு.",
                "sample_elements": [
                    {"name": "Vallarai & Mudakathan Foraging Seasons", "category": "practice", "step": 1, "s": [1, 2, 3], "quote": "Foraging occurs immediately after the onset of the North-East monsoon."},
                    {"name": "Ash Water Detoxification of Wild Tubers", "category": "process_step", "step": 2, "s": [1, 2], "missing_in": [3], "quote": "Wild Dioscorea yams are boiled with wood ash to neutralize calcium oxalate crystals."},
                    {"name": "Clay Pot Slow Roasting of Forest Seeds", "category": "technique", "step": 3, "s": [1, 2, 3], "quote": "Dry seeds are parched in heated sand within terracotta pots."},
                    {"name": "Wild Thumbai Blossom Tea Infusion", "category": "preparation", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "White Leucas aspera flowers are steeped in morning rainwater for respiratory vitality."}
                ],
                "gap_elem": "Ash Water Detoxification of Wild Tubers",
                "gap_type": "missing_step",
                "step_order": 2,
                "urgency": 84
            },
            {
                "id": "traditional-plant-uses",
                "name": "Traditional Plant Uses",
                "tamil_name": "பாரம்பரிய தாவர பயன்பாடுகள்",
                "desc": "Fibers, natural cleansers (Shikakai, Soapnut), insect repellents, and organic fencing flora.",
                "tamil_desc": "இயற்கை சோப்புகள், நார்கள், பூச்சி விரட்டிகள் மற்றும் வேலித் தாவரங்களின் நடைமுறை பயன்கள்.",
                "sample_elements": [
                    {"name": "Arappu Leaf Powder Conditioning", "category": "material", "step": 1, "s": [1, 2, 3], "quote": "Albizia amara leaves are shade-dried and pulverized as natural hair cleanser."},
                    {"name": "Nochi Leaf Smoke Mosquito Repellent", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "Vitex negundo foliage is smoldered in cattle sheds to deter vector insects."},
                    {"name": "Screw-Pine (Thazhai) Root Rope Braiding", "category": "process_step", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Aerial stilt roots are retted in wetland mud before twisting into durable cordage."},
                    {"name": "Kalli Cactus Perimeter Boundary Defense", "category": "practice", "step": 4, "s": [1, 3], "missing_in": [2], "quote": "Euphorbia tirucalli planted as living hedge preventing wild boar intrusion."}
                ],
                "gap_elem": "Screw-Pine (Thazhai) Root Rope Braiding",
                "gap_type": "missing_step",
                "step_order": 3,
                "urgency": 73
            }
        ]
    },
    {
        "id": "marine-coastal",
        "name": "Marine & Coastal Heritage",
        "tamil_name": "கடல்சார் & கடலோர மரபு",
        "icon": "waves",
        "description": "Coromandel and Palk Strait seafaring wisdom, indigenous naval architecture, stellar navigation, and shore traditions.",
        "tamil_description": "சோழமண்டலக் கடற்கரை மீன்பிடி மரபுகள், கட்டுமரக் கட்டுமானம், நட்சத்திர வழிகாட்டல் மற்றும் கடலோர சமுதாய வாழ்க்கை.",
        "branches": [
            {
                "id": "traditional-fishing",
                "name": "Traditional Fishing",
                "tamil_name": "பாரம்பரிய மீன்பிடித்தல்",
                "desc": "Knowledge of sea currents (Neerottam), underwater reef banks (Paar), and seasonal fish shoals.",
                "tamil_desc": "நீரோட்டம், பவளப்பாறைகள் (பார்), மற்றும் பருவ மீன் கூட்டங்கள் கண்டறியும் கடலறிவு.",
                "sample_elements": [
                    {"name": "Reading Surface Scent of Shoals (Meen Vaasanai)", "category": "technique", "step": 1, "s": [1, 2, 3], "quote": "Elder navigators detect approaching sardines by seawater oil film smell."},
                    {"name": "Sounding the Reef with Lead Line (Kallu Poduthal)", "category": "tool", "step": 2, "s": [1, 2, 3], "quote": "A greased lead sinker on coir line reveals sand or coral texture."},
                    {"name": "Vannaan Thurai Drift Current Calculation", "category": "technique", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Drift vector computed using shoreline palm landmark alignment."},
                    {"name": "Nighttime Bioluminescence Depth Scouting", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Disturbed luminescent plankton reveals depth of underwater predator fish."},
                    {"name": "Kadalamma Sacred Share Offering", "category": "cultural_context", "step": 5, "s": [1, 2, 3], "quote": "The first silver fish caught is returned alive to the sea with reverent prayer."}
                ],
                "gap_elem": "Nighttime Bioluminescence Depth Scouting",
                "gap_type": "missing_element",
                "step_order": 4,
                "urgency": 87
            },
            {
                "id": "boat-building",
                "name": "Boat Building",
                "tamil_name": "மரக்கலம் / படகு கட்டுதல்",
                "desc": "Indigenous boatwright traditions: Kattumaram log lashings, Vathai canoes, and sewn-plank Masula boats.",
                "tamil_desc": "கட்டுமரம், வத்தை, தோணி மற்றும் மசுலா தைக்கப்பட்ட படகுகளின் பழங்கால மரக்கலக் கலை.",
                "sample_elements": [
                    {"name": "Albezia Log Selection (Ainthu Maram)", "category": "material", "step": 1, "s": [1, 2, 3], "quote": "Five curved Melia dubia or teak logs selected for natural buoyant curve."},
                    {"name": "Coir Lashing Tensioning (Kambu Kattu)", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Coconut fiber ropes saturated with fish oil are lashed through drilled log ends."},
                    {"name": "Cashew Nut Shell Resin Sealing", "category": "material", "step": 3, "s": [1, 3], "missing_in": [2], "quote": "Pungent caustic cashew liquid mixed with lime putty seals seams between timber."},
                    {"name": "Wedge Keel Balance Alignment (Thandil)", "category": "tool", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Adjustable wooden dagger-board inserted to prevent lateral surf drift."},
                    {"name": "Launching Libation on High Tide", "category": "cultural_context", "step": 5, "s": [1, 2, 3], "quote": "Coconut milk broken on boat prow as it meets the first coastal breaker wave."}
                ],
                "gap_elem": "Wedge Keel Balance Alignment (Thandil)",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 90
            },
            {
                "id": "fishing-tools",
                "name": "Fishing Tools",
                "tamil_name": "மீன்பிடி கருவிகள்",
                "desc": "Traditional shore seines (Peria Valai), cast nets (Keechu Valai), hook lines, and wicker fish traps.",
                "tamil_desc": "பெரிய வலை, வீச்சு வலை, தூண்டில் மற்றும் மூங்கில் கூண்டுக் கருவிகள்.",
                "sample_elements": [
                    {"name": "Cotton Thread Bark Tannin Tanning", "category": "process_step", "step": 1, "s": [1, 2, 3], "quote": "Cotton nets boiled in mangrove bark extract (Kalungai) to prevent saltwater rot."},
                    {"name": "Terracotta Sinker Molding", "category": "material", "step": 2, "s": [1, 2, 3], "quote": "Kiln-fired clay rings weighted onto lower ground-rope of cast net."},
                    {"name": "Porous Coral Float Stitching", "category": "tool", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Lightweight porous pumice floats sewn to head-rope before modern synthetics."},
                    {"name": "Split-Bamboo Eel Traps (Koodu)", "category": "tool", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Woven bamboo funnels placed against tidal backwater currents."}
                ],
                "gap_elem": "Porous Coral Float Stitching",
                "gap_type": "missing_element",
                "step_order": 3,
                "urgency": 83
            },
            {
                "id": "coastal-food",
                "name": "Coastal Food",
                "tamil_name": "கடலோர உணவு முறை",
                "desc": "Marine culinary heritage: Sun-dried Karuvadu, earthen pot tamarind gravies, and seaweed preparations.",
                "tamil_desc": "கருவாடு உலர்த்தும் முறை, மீன் குழம்பு, மற்றும் கடற்பாசி சமையல் மரபுகள்.",
                "sample_elements": [
                    {"name": "Sea Salt Sand Curing Pit", "category": "process_step", "step": 1, "s": [1, 2, 3], "quote": "Fresh mackerel layered in coarse sea salt and buried in sand dunes for 24 hours."},
                    {"name": "Palm Leaf Mesh Sun Drying", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "Fish spread on raised palmyra mats 4 feet above ground to avoid grit."},
                    {"name": "Kodampuli Smoked Tamarind Preservative", "category": "material", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Smoked Malabar tamarind rinds infused into curry to inhibit bacterial spoilage."},
                    {"name": "Kadal Paasi Seaweed Halwa Thickening", "category": "practice", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Gracilaria agar seaweed washed 7 times in sweet well water before boiling with palm jaggery."}
                ],
                "gap_elem": "Kadal Paasi Seaweed Halwa Thickening",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 72
            },
            {
                "id": "maritime-traditions",
                "name": "Maritime Traditions",
                "tamil_name": "கடல்சார் மரபுகள்",
                "desc": "Stellar navigation (Kanakkadi), wind calendars (Kachaan, Vaadai), and fisher community courts (Panchayat).",
                "tamil_desc": "விண்மீன் வழிசெலுத்தல், காற்றுப் பருவங்கள் (வாடை, கச்சான்) மற்றும் மீனவ பஞ்சாயத்து மரபுகள்.",
                "sample_elements": [
                    {"name": "Pole Star Hand Finger Sighting (Dhruva Kanakku)", "category": "technique", "step": 1, "s": [1, 2, 3], "quote": "Four fingers held horizontally against horizon measure latitude by Polaris elevation."},
                    {"name": "Vaadai & Kachaan Wind Quadrant Shift", "category": "practice", "step": 2, "s": [1, 2, 3], "quote": "Sailors track transition between North-East offshore gale and South-West onshore breeze."},
                    {"name": "Seagull Roosting Horizon Warning", "category": "technique", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Flocks of coastal terns flying low southwest indicates squall within 3 hours."},
                    {"name": "Kadaikodi Traditional Shore Arbitration", "category": "cultural_context", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Village council resolves boundary claims over disputed fishing shoals."}
                ],
                "gap_elem": "Seagull Roosting Horizon Warning",
                "gap_type": "missing_element",
                "step_order": 3,
                "urgency": 89
            }
        ]
    },
    {
        "id": "weaving-textiles",
        "name": "Weaving & Textiles",
        "tamil_name": "நெசவு & ஆடை மரபு",
        "icon": "layers",
        "description": "Kanchipuram silk, Madurai Sungudi, Chettinad cotton, plant-based dyes, and loom techniques.",
        "tamil_desc": "காஞ்சிபுரம் பட்டு, மதுரை சுங்குடி, செட்டிநாட்டு பருத்தி, இயற்கை சாயங்கள் மற்றும் தறி நெசவு நுட்பங்கள்.",
        "branches": [
            {
                "id": "handloom",
                "name": "Handloom",
                "tamil_name": "கைத்தறி",
                "desc": "Pit loom, frame loom operation, warp sizing with rice starch, and reed beating rhythms.",
                "tamil_desc": "குழித்தறி அமைப்பு, கஞ்சி பசை தோய்த்தல், மற்றும் விழுதுகளின் தாள இயக்கம்.",
                "sample_elements": [
                    {"name": "Warp Starch Sizing with Fermented Rice Ganji", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Warp yarns brushed outdoors with fermented rice gruel using palm leaf bristles."},
                    {"name": "Reed Beating Rhythm Coordination", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Two beats per shed insertion ensure consistent thread density."},
                    {"name": "Hand-Doffing Tension Counterweights", "category": "tool", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Granite counterweights adjusted on rear warp beam as woven length accumulates."},
                    {"name": "Double Shuttle Korvai Interlock Weaving", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Two weavers sit side by side to throw contrasting border shuttles."},
                    {"name": "Tempering the Wooden Shuttle in Castor Oil", "category": "technique", "step": 5, "s": [1, 2, 3], "quote": "Buffalo horn tips and seasoned hardwood soaked in castor oil for friction-free glide."}
                ],
                "gap_elem": "Double Shuttle Korvai Interlock Weaving",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 85
            },
            {
                "id": "silk-weaving",
                "name": "Silk Weaving",
                "tamil_name": "பட்டு நெசவு",
                "desc": "Kanchipuram mulberry silk twisting, pure silver gold zari interweaving, and temple border motifs.",
                "tamil_desc": "காஞ்சிபுரம் மல்பெரி பட்டு, தூய ஜரிகை நெசவு மற்றும் கோவில் கோபுர பார்டர்கள்.",
                "sample_elements": [
                    {"name": "Three-Ply Silk Yarn Twisting (Murukku)", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Three mulberry filaments twisted together to yield structural durability."},
                    {"name": "Pure Silver Wire Flattening for Zari", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Electrum wire wrapped around dyed silk core before gilding with gold leaf."},
                    {"name": "Korvai Contrast Border Catching", "category": "technique", "step": 3, "s": [1, 3], "missing_in": [2], "quote": "Border and body warp interlocking without overlapping ridge."},
                    {"name": "Petni Temple Spire Motif Jointing", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Warp threads severed and tied to new colored warp with minute thumb twists."},
                    {"name": "Hand-Polishing Fabric with Glass Roller", "category": "process_step", "step": 5, "s": [1, 2], "missing_in": [3], "quote": "Solid blown glass bead rubbed over finished drape to impart mirror luster."}
                ],
                "gap_elem": "Petni Temple Spire Motif Jointing",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 92
            },
            {
                "id": "cotton-textiles",
                "name": "Cotton Textiles",
                "tamil_name": "பருத்தி ஆடைகள்",
                "desc": "Madurai Sungudi tie-dye, fine muslin dhotis, Chettinad Kandangi coarse cotton weaves.",
                "tamil_desc": "மதுரை சுங்குடி முடிச்சு சாயக்கலை, கந்தாங்கி சேலைகள் மற்றும் வேட்டி நெசவு மரபு.",
                "sample_elements": [
                    {"name": "Mustard Seed Knotting for Sungudi", "category": "technique", "step": 1, "s": [1, 2, 3], "quote": "Minute mustard seeds wrapped and bound with thread across grid points."},
                    {"name": "Cow Dung Bleaching in Riverbed Sands", "category": "process_step", "step": 2, "s": [1, 2], "missing_in": [3], "quote": "Raw cotton fabric spread over Vaigai river sand with diluted cow dung slurry."},
                    {"name": "Castor Oil Emulsion Softening", "category": "material", "step": 3, "s": [1, 2, 3], "quote": "Rinsed fabric soaked in emulsified castor oil before mordanting."},
                    {"name": "Wooden Block Wax Resist Stamping", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Melted beeswax stamped with carved teak wood blocks for borders."}
                ],
                "gap_elem": "Cow Dung Bleaching in Riverbed Sands",
                "gap_type": "missing_step",
                "step_order": 2,
                "urgency": 80
            },
            {
                "id": "natural-dyes",
                "name": "Natural Dyes",
                "tamil_name": "இயற்கை சாயங்கள்",
                "desc": "Indigo fermentation, Madder root (Manjistha) reds, Pomegranate rind yellows, and Iron rust black.",
                "tamil_desc": "அவுரி நீலம், மஞ்சிஷ்டி சிவப்பு, மாதுளை தோல் மஞ்சள் மற்றும் இரும்பு துரு கருப்பு சாயம்.",
                "sample_elements": [
                    {"name": "Indigo Pit Alkaline Fermentation", "category": "process_step", "step": 1, "s": [1, 2, 3], "quote": "Indigo leaves steeped in lime water and agitated until froth turns copper green."},
                    {"name": "Alum Mordant Bath Fixation", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Yarn boiled with potash alum before submerging in madder dye vat."},
                    {"name": "Jaggery and Fermented Rice Wine Reducing Agent", "category": "material", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Toddy or fermented palm wine added to revive exhausted dye vats."},
                    {"name": "Myrobalan (Kadukkai) Tannin Preparation", "category": "preparation", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Dried terminalia chebula fruits boiled as mordant base for iron black (Kasippu)."}
                ],
                "gap_elem": "Jaggery and Fermented Rice Wine Reducing Agent",
                "gap_type": "missing_step",
                "step_order": 3,
                "urgency": 86
            },
            {
                "id": "traditional-patterns",
                "name": "Traditional Patterns",
                "tamil_name": "பாரம்பரிய நெசவு உருவங்கள்",
                "desc": "Iconography of temple spires (Gopuram), diamond checks (Muthu Kattam), peacocks (Mayil), and Yali beasts.",
                "tamil_desc": "கோபுரக் கலசம், முத்துக்கட்டம், ருத்ராட்சம், மற்றும் யாழி வடிவமைப்பு குறியீடுகள்.",
                "sample_elements": [
                    {"name": "Mayilkan (Peacock Eye) Diamond Jacquard Graph", "category": "technique", "step": 1, "s": [1, 2, 3], "quote": "Geometric diamond pattern calculated on grid string cards."},
                    {"name": "Gopuram Temple Spire Border Computation", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "Graduated stepped triangles woven with extra weft insertion."},
                    {"name": "Rudraksham Bead Border Warp Geometry", "category": "technique", "step": 3, "s": [1, 3], "missing_in": [2], "quote": "Small round ribbed dots framing edge of traditional wedding garments."},
                    {"name": "Yali Mythical Beast Jacquard Harness Lacing", "category": "tool", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Complex twine harness linking 200 overhead threads for mythical beast motif."}
                ],
                "gap_elem": "Yali Mythical Beast Jacquard Harness Lacing",
                "gap_type": "missing_element",
                "step_order": 4,
                "urgency": 78
            }
        ]
    },
    {
        "id": "traditional-crafts",
        "name": "Traditional Crafts & Artisan Heritage",
        "tamil_name": "பாரம்பரிய கைவினைக் கலைகள்",
        "icon": "hammer",
        "description": "Lost-wax bronze metallurgy, terracotta votives, temple stone carving, wood craft, and palmyra leaf arts.",
        "tamil_desc": "சுவாமிமலை வெண்கலச் சிற்பங்கள், மண்பாண்டக் கலை, மரச்சிற்பம், கற்சிற்பம் மற்றும் பனை ஓலைக் கைவினை.",
        "branches": [
            {
                "id": "pottery",
                "name": "Pottery",
                "tamil_name": "மண்பாண்டக் கலை",
                "desc": "Riverbank alluvial clay preparation, kick-wheel turning, open bonfire kiln baking, and black pottery.",
                "tamil_desc": "களிமண் பதப்படுத்துதல், சக்கர சுழற்சி மற்றும் திறந்தவெளி சூளை சுடுதல் நுட்பங்கள்.",
                "sample_elements": [
                    {"name": "River Alluvial Silt Blending with Fine River Sand", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Silt harvested from tank beds is sieved and blended with 15% silica sand."},
                    {"name": "Barefoot Clay Kneading (Mithi-Padam)", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Artisans tread the wet clay with heels for 4 hours to eliminate air pockets."},
                    {"name": "Wood Ash and Acacia Gum Paddle Beating (Thattal)", "category": "technique", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Wooden paddle beats exterior while stone anvil supports vessel interior."},
                    {"name": "Paddy Husk Reduction Smoke for Black Ware", "category": "process_step", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Smoldering rice husks trap carbon inside kiln to achieve deep black luster."},
                    {"name": "Cow Dung Protective Kiln Dome Seal", "category": "technique", "step": 5, "s": [1, 2, 3], "quote": "Outer shell of baking kiln sealed with dry cow dung cakes and mud plaster."}
                ],
                "gap_elem": "Paddy Husk Reduction Smoke for Black Ware",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 82
            },
            {
                "id": "bronze-work",
                "name": "Bronze Work",
                "tamil_name": "வெண்கலச் சிற்பங்கள் / வார்ப்பு",
                "desc": "Swamimalai lost-wax (Cire Perdue) casting of Chola bronze icons following Shilpa Shastra canons.",
                "tamil_desc": "சுவாமிமலை சோழர் வெண்கலச் சிற்பங்கள், மெழுகு வார்ப்பு மற்றும் சிற்ப சாஸ்திர அளவீடுகள்.",
                "sample_elements": [
                    {"name": "Beeswax and Dammar Pine Resin Modeling", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Pure beeswax blended with Kungilium resin and peanut oil to sculpt the model."},
                    {"name": "Talamana Canon Proportional Measurement", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "Ribbon of palm leaf folded to measure sacred proportions (Dasa Tala system)."},
                    {"name": "Cauvery Alluvial Clay Triple-Layer Mold Coating", "category": "process_step", "step": 3, "s": [1, 2, 3], "quote": "Mold coated with fine Charu clay, then thick Vandal clay, and coarse sand clay."},
                    {"name": "Subterranean Charcoal Crucible Tilting", "category": "process_step", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Panchaloha alloy melted at 1100°C poured into pre-heated terracotta mold."},
                    {"name": "Opening the Sacred Eyes (Netronmeelana)", "category": "cultural_context", "step": 5, "s": [1], "missing_in": [2, 3], "quote": "Gold chisel carves the deity's pupil while viewing reflection in ghee vessel."}
                ],
                "gap_elem": "Opening the Sacred Eyes (Netronmeelana)",
                "gap_type": "missing_step",
                "step_order": 5,
                "urgency": 89
            },
            {
                "id": "wood-carving",
                "name": "Wood Carving",
                "tamil_name": "மரச் சிற்பக்கலை",
                "desc": "Temple chariot (Ther) carving, Athangudi Chettinad doors, and Vahana sacred mount sculpting.",
                "tamil_desc": "கோவில் தேர் சிற்பங்கள், செட்டிநாட்டு மரக்கதவுகள் மற்றும் வாகன சிற்பக் கலை.",
                "sample_elements": [
                    {"name": "Seasoned Iluppai & Teak Timber Selection", "category": "material", "step": 1, "s": [1, 2, 3], "quote": "Timber felled during waning moon and seasoned in shade for three dry seasons."},
                    {"name": "Blocking Rough Contours with Adze (Veecharu)", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Heavy adze chips away bulk surplus wood to define silhouette."},
                    {"name": "Tempering Chisel Edges in Sesame Oil", "category": "technique", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Hand-forged steel chisels quenched in cold-pressed gingelly oil for micro-toughness."},
                    {"name": "Intricate Relief Undercutting of Yali Manes", "category": "technique", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Deep gouges hollow space beneath curls to cast dramatic sunlit shadows."}
                ],
                "gap_elem": "Tempering Chisel Edges in Sesame Oil",
                "gap_type": "missing_step",
                "step_order": 3,
                "urgency": 77
            },
            {
                "id": "stone-carving",
                "name": "Stone Carving",
                "tamil_name": "கற்சிற்பக்கலை",
                "desc": "Granite sculpting of Dravidian temple pillars, iconography, and acoustic musical pillars.",
                "tamil_desc": "திராவிடக் கோவில் தூண்கள், கருங்கல் சிலைகள் மற்றும் இசைத் தூண்களின் வடிப்புக் கலை.",
                "sample_elements": [
                    {"name": "Granite Sound Testing for Male / Female / Neuter Stone", "category": "practice", "step": 1, "s": [1, 2, 3], "quote": "Struck with brass mallet: bell ringing denotes male stone suitable for deities."},
                    {"name": "Wooden Wedge Fracture of Quarry Blocks", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Dry wood wedges inserted into chiselled slots and doused with boiling water."},
                    {"name": "Musical Pillar Core Resonance Tuning", "category": "technique", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Hollowing internal chambers to resonate the 7 Saptaswara musical frequencies."},
                    {"name": "Herbal Paste Final Lapping & Polishing", "category": "technique", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Emery powder blended with bamboo leaf ash to polish granite to satin gloss."}
                ],
                "gap_elem": "Musical Pillar Core Resonance Tuning",
                "gap_type": "missing_step",
                "step_order": 3,
                "urgency": 93
            },
            {
                "id": "palm-leaf-crafts",
                "name": "Palm-Leaf Crafts",
                "tamil_name": "பனை ஓலைக் கைவினை",
                "desc": "Palmyra frond processing, utility baskets (Kottan), mats, and structural thatch weaving.",
                "tamil_desc": "பனை ஓலை பதனிடுதல், கொட்டான் பெட்டிகள், பாய்கள் மற்றும் கூரை வேய்தல்.",
                "sample_elements": [
                    {"name": "Harvesting Tender Kurutholai Fronds", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Ivory tender inner leaves harvested before green photosynthesis stiffens fiber."},
                    {"name": "Turmeric Water Anti-Termite Boiling", "category": "process_step", "step": 2, "s": [1, 2], "missing_in": [3], "quote": "Fronds immersed in boiling water infused with wild turmeric rhizomes."},
                    {"name": "Bone-Smooth Knife Splicing (Varal)", "category": "tool", "step": 3, "s": [1, 2, 3], "quote": "Leaf blade split into uniform 2mm strips using razor-sharp horn knife."},
                    {"name": "Intricate Hexagonal Kottan Weaving Geometry", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Hexagonal plaiting creates rigid double-walled gift boxes for Chettinad rituals."}
                ],
                "gap_elem": "Intricate Hexagonal Kottan Weaving Geometry",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 75
            }
        ]
    },
    {
        "id": "agriculture-farming",
        "name": "Agriculture & Indigenous Farming Knowledge",
        "tamil_name": "வேளாண்மை & உழவு மரபு",
        "icon": "wheat",
        "description": "Native paddy cultivars (Mappillai Samba, Karuppu Kavuni), millets, Vrikshayurveda, and Eri tank cascades.",
        "tamil_description": "பாரம்பரிய நெல் ரகங்கள் (மாப்பிள்ளை சம்பா, கருப்பு கவுனி), சிறுதானியங்கள், ஏரி பாசன முறை மற்றும் இயற்கை உழவு.",
        "branches": [
            {
                "id": "traditional-rice",
                "name": "Traditional Rice",
                "tamil_name": "பாரம்பரிய நெல் ரகங்கள்",
                "desc": "Ancient saline-resistant, flood-resistant, and high-nutrition paddy strains of Tamil landscape.",
                "tamil_desc": "உப்பு, வெள்ளம் தாங்கும் மற்றும் நோய் தீர்க்கும் பாரம்பரிய நெல் வகைகள்.",
                "sample_elements": [
                    {"name": "Cow Urine Seed Soaking (Gomutra Vithai Nerthi)", "category": "process_step", "step": 1, "s": [1, 2, 3], "quote": "Seeds soaked in 1:10 diluted native cow urine for 12 hours to break dormancy."},
                    {"name": "Termite Mound Clay Slurry Enrobing", "category": "process_step", "step": 2, "s": [1, 2], "missing_in": [3], "quote": "Soaked seeds tossed in termite hill earth to coat with protective mineral microbes."},
                    {"name": "Navara Medicinal Paddy Salinity Acclimatization", "category": "technique", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Gradual seawater dilution exposure in nursery bed before coastal transplantation."},
                    {"name": "Broadcasting Sprouts on Rohini Constellation", "category": "cultural_context", "step": 4, "s": [1, 2, 3], "quote": "Sowing aligns with waxing lunar phase when soil moisture retention peaks."},
                    {"name": "Sickle Cutting 6 Inches Above Waterline", "category": "practice", "step": 5, "s": [1, 2, 3], "quote": "Leaving high stubble to rot as green manure for subsequent dry-crop rotation."}
                ],
                "gap_elem": "Navara Medicinal Paddy Salinity Acclimatization",
                "gap_type": "missing_step",
                "step_order": 3,
                "urgency": 86
            },
            {
                "id": "millets",
                "name": "Millets",
                "tamil_name": "சிறுதானியங்கள்",
                "desc": "Drought-resilient grains: Kuthiraivali, Thinai, Samai, Varagu, and traditional de-husking pounders.",
                "tamil_desc": "குதிரைவாலி, தினை, சாமை, வரகு உள்ளிட்ட வறட்சி தாங்கும் சத்து தானியங்கள்.",
                "sample_elements": [
                    {"name": "Stone Mortar Dry Pounding (Varagu Ithal)", "category": "process_step", "step": 1, "s": [1, 2, 3], "quote": "Thick siliceous husk removed without shattering endosperm using wooden pestle."},
                    {"name": "Intercropping with Pigeon Pea (Thovarai)", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "Three rows of finger millet alternated with one row of nitrogen-fixing red gram."},
                    {"name": "Storage in Cow Dung Plastered Bamboos (Kudhuru)", "category": "practice", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Grain silos woven from river reeds and sealed hermetically with cow dung paste."},
                    {"name": "Fermented Kanji Gruel Pot Overnight Maturation", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Cooked thinai porridge left in clay vessel overnight with onion slices for probiotic gut flora."}
                ],
                "gap_elem": "Fermented Kanji Gruel Pot Overnight Maturation",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 77
            },
            {
                "id": "seed-preservation",
                "name": "Seed Preservation",
                "tamil_name": "விதை பாதுகாப்பு முறை",
                "desc": "Indigenous seed banks: Neem leaf dusting, ash coating, smoke chambers, and mud pot storage.",
                "tamil_desc": "வேப்பிலை, சாம்பல், புகைமூட்டம் மற்றும் மண் பானை விதை சேமிப்பு முறைகள்.",
                "sample_elements": [
                    {"name": "Wood Ash and Turmeric Powder Dusting", "category": "process_step", "step": 1, "s": [1, 2, 3], "quote": "Fine cow dung ash blended with turmeric dust to desiccant coat seed surfaces."},
                    {"name": "Clay Pot Pitch Lining with Castor Oil", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Interior pores of earthen pot sealed with hot castor oil before grain filling."},
                    {"name": "Kitchen Hearth Overhead Smoke Preservation (Attu Mada)", "category": "technique", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Seed baskets suspended above wood-burning cooking fire to repel weevils via smoke."},
                    {"name": "Pouzolzia (Kallurukki) Leaf Insect Repellent Layer", "category": "material", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Bitter wild herb leaves layered between grain strata to deter boring beetles."}
                ],
                "gap_elem": "Pouzolzia (Kallurukki) Leaf Insect Repellent Layer",
                "gap_type": "missing_element",
                "step_order": 4,
                "urgency": 83
            },
            {
                "id": "traditional-irrigation",
                "name": "Traditional Irrigation",
                "tamil_name": "பாரம்பரிய பாசன முறைகள்",
                "desc": "The Grand Anicut (Kallanai), Eri cascade networks, Kalingu sluices, and water distribution elders (Neerkatti).",
                "tamil_desc": "கல்லணை, ஏரி பாசன அமைப்பு, கலிங்கு, மடை மற்றும் நீர்க்கட்டி மரபுகள்.",
                "sample_elements": [
                    {"name": "Eri Sluice Flow Regulation (Madai Thirathal)", "category": "practice", "step": 1, "s": [1, 2, 3], "quote": "Granite shutter plug lifted according to paddy growth stage requirements."},
                    {"name": "Neerkatti Village Water Allocator Office", "category": "role", "step": 2, "s": [1, 2, 3], "quote": "Hereditary community guardian measures allocation hours equitably across tail-end fields."},
                    {"name": "Kalingu Surplus Overflow Weir Design", "category": "technique", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Curved masonry spillway discharges peak monsoon floodwaters to downstream tank."},
                    {"name": "Sub-Surface Sand Aquifer Canal Tapping (Kasam)", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Trenches dug across dry river sandbeds to capture subterranean percolation flow."}
                ],
                "gap_elem": "Sub-Surface Sand Aquifer Canal Tapping (Kasam)",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 88
            },
            {
                "id": "farming-practices",
                "name": "Farming Practices",
                "tamil_name": "உழவு முறைகள்",
                "desc": "Vrikshayurveda formulations: Panchagavya, Kunapajala fermented manures, multi-crop rotation.",
                "tamil_desc": "பஞ்சகவ்யம், குணபஜலம் உரம் மற்றும் பாரம்பரிய பயிர் சுழற்சி முறைகள்.",
                "sample_elements": [
                    {"name": "Five Cow Derivatives Panchagavya Blending", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Dung, urine, milk, curd, and ghee stirred twice daily in shade for 21 days."},
                    {"name": "Fermented Fish Waste Amino Acid Tonic (Meen Amilam)", "category": "process_step", "step": 2, "s": [1, 2], "missing_in": [3], "quote": "Chopped ocean trash fish fermented with raw country jaggery for 30 days."},
                    {"name": "Wood Plough Angle Adjustment for Deep Furrows", "category": "tool", "step": 3, "s": [1, 2, 3], "quote": "Iron-tipped acacia timber plough tilted at 45 degrees to overturn subsoil weeds."},
                    {"name": "Kunapajala Animal Bone Broth Bio-Fertilizer", "category": "material", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Ancient fermented brew of animal marrow, sesame cake, and honey recorded in Surapala text."}
                ],
                "gap_elem": "Kunapajala Animal Bone Broth Bio-Fertilizer",
                "gap_type": "missing_element",
                "step_order": 4,
                "urgency": 85
            }
        ]
    },
    {
        "id": "tamil-literature",
        "name": "Tamil Books & Literature",
        "tamil_name": "தமிழ் நூல்கள் & இலக்கிய மரபு",
        "icon": "book",
        "description": "Sangam anthologies, Tolkappiyam grammar, Silappadikaram epic lore, Bhakti hymns, and palm-leaf manuscripts.",
        "tamil_description": "சங்க இலக்கியம், தொல்காப்பியம், சிலப்பதிகாரம் உள்ளிட்ட காப்பியங்கள் மற்றும் பனை ஓலைச் சுவடிகள்.",
        "branches": [
            {
                "id": "sangam-literature",
                "name": "Sangam Literature",
                "tamil_name": "சங்க இலக்கியம்",
                "desc": "Eight Anthologies (Ettuthokai) and Ten Idylls (Pattupattu), depicting Akam (interior love) and Puram (valor).",
                "tamil_desc": "எட்டுத்தொகை மற்றும் பத்துப்பாட்டு நூல்கள் காட்டும் அகம் மற்றும் புற வாழ்க்கை மரபுகள்.",
                "sample_elements": [
                    {"name": "Five Thinai Landscape Classification (Ainthinai)", "category": "terminology", "step": 1, "s": [1, 2, 3], "quote": "Kurinji, Mullai, Marutham, Neithal, and Paalai mapped to distinct human emotional states."},
                    {"name": "Muthatporul Primary Elements (Space & Season)", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "Poetic conventions mandate strict pairing of geography and seasonal diurnal time."},
                    {"name": "Ullurai Uvamam Cryptic Inner Metaphor", "category": "technique", "step": 3, "s": [1, 3], "missing_in": [2], "quote": "Describing flora/fauna behavior to subtly imply human moral conduct without explicit declaration."},
                    {"name": "Bards' Harp Tuning (Seeriya Yaazh)", "category": "tool", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Panar minstrels tuned the 21-string Periyaazh harp to specific Pann melodic scales."}
                ],
                "gap_elem": "Bards' Harp Tuning (Seeriya Yaazh)",
                "gap_type": "missing_element",
                "step_order": 4,
                "urgency": 94
            },
            {
                "id": "classical-works",
                "name": "Classical Tamil Works",
                "tamil_name": "செம்மொழித் தமிழ் நூல்கள்",
                "desc": "Thirukkural moral ethics, Pathinenkilkanakku didactic anthologies, and ancient scholarly commentaries.",
                "tamil_desc": "திருக்குறள், பதினெண்கீழ்க்கணக்கு நூல்கள் மற்றும் பரிமேலழகர் உள்ளிட்ட உரையாசிரியர்களின் மரபு.",
                "sample_elements": [
                    {"name": "Kural Couplet Metrical Structure (Venpa)", "category": "technique", "step": 1, "s": [1, 2, 3], "quote": "Seven cir feet distributed in four and three feet lines with strict rhyme rules."},
                    {"name": "Urai Commentarial Lineage Succession", "category": "practice", "step": 2, "s": [1, 2, 3], "quote": "Passing down exegetical glosses from master to student through oral recitation."},
                    {"name": "Malar Misaiekinan Theological Interpretation Dispute", "category": "terminology", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Parimelazhagar and Manakkudavar diverge on whether phrase denotes Jaina or Vedic deity."},
                    {"name": "Mnemonics for Memorizing 1330 Couplets", "category": "technique", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Chanting chapter initial syllables in rhyming verses for mental retention."}
                ],
                "gap_elem": "Malar Misaiekinan Theological Interpretation Dispute",
                "gap_type": "missing_element",
                "step_order": 3,
                "urgency": 78
            },
            {
                "id": "bhakti-literature",
                "name": "Bhakti Literature",
                "tamil_name": "பக்தி இலக்கியம்",
                "desc": "Thevaram, Thiruvasagam, Nalayira Divya Prabandham, and temple temple singing traditions (Oduvar).",
                "tamil_desc": "தேவாரம், திருவாசகம், நாலாயிர திவ்வியப் பிரபந்தம் மற்றும் ஓதுவார் பண்ணிசை மரபு.",
                "sample_elements": [
                    {"name": "Pann Sacred Raga System Classification", "category": "terminology", "step": 1, "s": [1, 2, 3], "quote": "Ancient Tamil melodic modes (Kurinji, Sevvazhi, Nattapadai) mapped to Shaivite hymns."},
                    {"name": "Oduvar Bronze Cymbals (Thalam) Rhythmic Keeping", "category": "tool", "step": 2, "s": [1, 2, 3], "quote": "Thick bronze cymbals guide the tempo of hymn recitation in temple sanctum."},
                    {"name": "Thirumurai Palm-Leaf Rediscovery Rite (Raja Raja)", "category": "cultural_context", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Nambi Andar Nambi unseals the locked chamber at Chidambaram covered in white ant hills."},
                    {"name": "Pann Nattapadai Vocal Glissando Technique", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Microtonal vocal pitch slides prescribed in 11th century stone inscriptions."}
                ],
                "gap_elem": "Pann Nattapadai Vocal Glissando Technique",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 87
            },
            {
                "id": "tamil-epics",
                "name": "Tamil Epics",
                "tamil_name": "ஐம்பெருங்காப்பியங்கள்",
                "desc": "Silappadikaram, Manimekalai, Civaka Cintamani, Valayapathi, and Kundalakesi narrative lineages.",
                "tamil_desc": "சிலப்பதிகாரம், மணிமேகலை உள்ளிட்ட ஐம்பெருங்காப்பியங்களின் கதை மற்றும் இசைக் கூறுகள்.",
                "sample_elements": [
                    {"name": "Arangetru Kaadhai Musicology Treatise", "category": "terminology", "step": 1, "s": [1, 2, 3], "quote": "Ilango Adigal documents microtones, flute craftsmanship, and 14-string harp scales."},
                    {"name": "Madhavi's Eleven Classical Dance Forms (Aadal)", "category": "practice", "step": 2, "s": [1, 2, 3], "quote": "Alliyam, Kodukotti, Kudakkuthu, and other ancient performing dances enumerated."},
                    {"name": "Lost Lost Cantos of Valayapathi Epic", "category": "cultural_context", "step": 3, "s": [1], "missing_in": [2, 3], "quote": "Only 72 fragmentary verses survive; complete narrative lost when palm leaves degraded."},
                    {"name": "Chanting Meter of Asiriyappa Verse Lines", "category": "technique", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Flowing epic cadence resembling undulating river currents (Ahaval Oasai)."}
                ],
                "gap_elem": "Lost Lost Cantos of Valayapathi Epic",
                "gap_type": "missing_element",
                "step_order": 3,
                "urgency": 96
            },
            {
                "id": "poetry",
                "name": "Poetry",
                "tamil_name": "கவிதை மரபு",
                "desc": "Classical prosody (Yaappu), rhyme (Ethukai), alliteration (Mohnai), and modern poetic transitions.",
                "tamil_desc": "யாப்பிலக்கணம், எதுகை, மோனை, சந்தக் கவிதைகள் மற்றும் நவீன கவிதை உருமாற்றம்.",
                "sample_elements": [
                    {"name": "Ethukai Second-Letter Rhyme Rigor", "category": "technique", "step": 1, "s": [1, 2, 3], "quote": "Identical consonant with matched vowel length in second character of both lines."},
                    {"name": "Mohnai Initial Sound Alliteration", "category": "technique", "step": 2, "s": [1, 2, 3], "quote": "First character sound correspondence between metric feet."},
                    {"name": "Sandham Rhythmic Beat Meter Chanting", "category": "technique", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Pulsing percussive rhythm exemplified in Arunagirinathar's Thiruppugazh."},
                    {"name": "Chitra Kavi Visual Calligram Forms (Ratha Bandham)", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Verses arranged to form the visual contour of a temple chariot or snake."}
                ],
                "gap_elem": "Chitra Kavi Visual Calligram Forms (Ratha Bandham)",
                "gap_type": "missing_step",
                "step_order": 4,
                "urgency": 81
            },
            {
                "id": "grammar-works",
                "name": "Grammar Works",
                "tamil_name": "இலக்கண நூல்கள்",
                "desc": "Tolkappiyam (Letters, Words, Poetic Matter), Nannul, Yapparungalam, and linguistic heritage.",
                "tamil_desc": "தொல்காப்பியம் (எழுத்து, சொல், பொருள்), நன்னூல் மற்றும் மொழியியல் கோட்பாடுகள்.",
                "sample_elements": [
                    {"name": "Eluthu Phonology and Mora Timing (Maathirai)", "category": "terminology", "step": 1, "s": [1, 2, 3], "quote": "Short vowels allotted one eyelid blink (1 maathirai), long vowels two blinks."},
                    {"name": "Porul Adhigaaram Socio-Poetic Theory", "category": "terminology", "step": 2, "s": [1, 2, 3], "quote": "Uniquely Tamil grammatical division systematizing human emotions and society alongside grammar."},
                    {"name": "Mei-Mayakku Consonant Cluster Constraints", "category": "technique", "step": 3, "s": [1, 2], "missing_in": [3], "quote": "Strict phonetic rules dictating allowable consonant pairings in word joints."},
                    {"name": "Aaytham Glottal Phoneme Articulation", "category": "technique", "step": 4, "s": [1], "missing_in": [2, 3], "quote": "Ancient three-dot symbol (ஃ) articulated in throat as subtle spirant fricative."}
                ],
                "gap_elem": "Aaytham Glottal Phoneme Articulation",
                "gap_type": "missing_element",
                "step_order": 4,
                "urgency": 84
            },
            {
                "id": "palm-leaf-manuscripts",
                "name": "Palm-Leaf Manuscripts",
                "tamil_name": "சுவடி இலக்கியம்",
                "desc": "Curing Palmyra leaves, incising with iron stylus (Ezhuthani), lampblack inking, and citronella preservation.",
                "tamil_desc": "பனை ஓலை பதனிடுதல், எழுத்தாணி கொண்டு சுவடி எழுதுதல், மை தடவுதல் மற்றும் மூலிகை பாதுகாப்பு.",
                "sample_elements": [
                    {"name": "Boiling Selected Palmyra Fronds in Water", "category": "preparation", "step": 1, "s": [1, 2, 3], "quote": "Fresh palmyra leaves cut into standard sizes and boiled with turmeric to prevent insect attack."},
                    {"name": "Pressing between Wooden Blocks (Palagai)", "category": "process_step", "step": 2, "s": [1, 2, 3], "quote": "Dried leaves bundled between teak planks and weighted for 30 days to flatten."},
                    {"name": "Incising Characters with Iron Stylus (Ezhuthani)", "category": "process_step", "step": 3, "s": [1, 2, 3], "quote": "Sharp stylus held steady in right hand while left thumbnail guides line incision."},
                    {"name": "Lampblack and Eclipta (Karisalanganni) Inking", "category": "process_step", "step": 4, "s": [1, 2], "missing_in": [3], "quote": "Mustard oil lamp soot mixed with Karisalankanni juice rubbed over surface into carved grooves."},
                    {"name": "Lemongrass and Citronella Oil Conditioning", "category": "process_step", "step": 5, "s": [1], "missing_in": [2, 3], "quote": "Leaves swabbed with citronella essential oil every 2 years to keep fiber flexible and repel fungus."},
                    {"name": "Threading with Red Silk Cord and Brass Pin", "category": "technique", "step": 6, "s": [1, 2, 3], "quote": "Holes pierced at golden ratio distance threaded with cord to bind folio."}
                ],
                "gap_elem": "Lemongrass and Citronella Oil Conditioning",
                "gap_type": "missing_step",
                "step_order": 5,
                "urgency": 95
            }
        ]
    }
]

GLOSSARY_ENTRIES = [
    {"tamil": "கரகம்", "trans": "Karagam", "eng": "Sacred water pot decorated with coconut and margosa leaves, balanced in folk ritual dance.", "domain": "Folk Culture & Performing Arts", "branch": "Karagattam"},
    {"tamil": "நையாண்டி மேளம்", "trans": "Naiyandi Melam", "eng": "High-energy rustic folk orchestra accompanying Karagattam and Kavadi performances.", "domain": "Folk Culture & Performing Arts", "branch": "Karagattam"},
    {"tamil": "பறை", "trans": "Parai", "eng": "Ancient circular frame drum crafted from neem wood and hide, symbol of rhythm and communication.", "domain": "Folk Culture & Performing Arts", "branch": "Parai Isai"},
    {"tamil": "நிலவேம்பு", "trans": "Nilavembu", "eng": "King of Bitters (Andrographis paniculata), primary antiviral and antipyretic Siddha herb.", "domain": "Traditional Plants & Herbal Knowledge", "branch": "Medicinal Plants"},
    {"tamil": "அனுபானம்", "trans": "Anupana", "eng": "Vehicle or carrier medium (e.g. warm milk, honey, ghee) used to administer herbal compounds.", "domain": "Traditional Plants & Herbal Knowledge", "branch": "Herbal Remedies"},
    {"tamil": "கட்டுமரம்", "trans": "Kattumaram", "eng": "Indigenous seaworthy raft formed by lashing five buoyant timber logs with coir cords.", "domain": "Marine & Coastal Heritage", "branch": "Boat Building"},
    {"tamil": "நீரோட்டம்", "trans": "Neerottam", "eng": "Traditional ocean navigation knowledge tracking directional underwater sea currents.", "domain": "Marine & Coastal Heritage", "branch": "Traditional Fishing"},
    {"tamil": "கோரவை", "trans": "Korvai", "eng": "Intricate handloom technique interlocking contrasting body and border weft threads without overlap.", "domain": "Weaving & Textiles", "branch": "Handloom"},
    {"tamil": "சுங்குடி", "trans": "Sungudi", "eng": "Traditional Madurai tie-and-dye cotton craft creating minute ring motifs with knotted mustard seeds.", "domain": "Weaving & Textiles", "branch": "Cotton Textiles"},
    {"tamil": "சுவாமிமலை வெண்கலம்", "trans": "Swamimalai Bronze", "eng": "Lost-wax cast bronze icons engineered according to sacred Talamana Shilpa canons.", "domain": "Traditional Crafts & Artisan Heritage", "branch": "Bronze Work"},
    {"tamil": "எழுத்தாணி", "trans": "Ezhuthani", "eng": "Steel iron stylus with razor chisel end used to incise characters onto prepared palm leaves.", "domain": "Traditional Crafts & Artisan Heritage", "branch": "Palm-Leaf Crafts"},
    {"tamil": "மாப்பிள்ளை சம்பா", "trans": "Mappillai Samba", "eng": "Traditional red rice cultivar celebrated in Tamil lore for providing physical endurance and vitality.", "domain": "Agriculture & Indigenous Farming Knowledge", "branch": "Traditional Rice"},
    {"tamil": "நீர்க்கட்டி", "trans": "Neerkatti", "eng": "Traditional community water manager responsible for fair equitable distribution from tank sluices.", "domain": "Agriculture & Indigenous Farming Knowledge", "branch": "Traditional Irrigation"},
    {"tamil": "ஐந்திணை", "trans": "Ainthinai", "eng": "Five classical Sangam eco-zones (Kurinji, Mullai, Marutham, Neithal, Paalai) matching emotional landscapes.", "domain": "Tamil Books & Literature", "branch": "Sangam Literature"},
    {"tamil": "சுவடி", "trans": "Suvadi", "eng": "Palm-leaf manuscript bundle preserving ancient poetry, medical treatises, and astronomical records.", "domain": "Tamil Books & Literature", "branch": "Palm-Leaf Manuscripts"}
]

def seed_database():
    db = SessionLocal()
    try:
        # Clear existing demo data
        db.query(Evidence).delete()
        db.query(KnowledgeGap).delete()
        db.query(KnowledgeElement).delete()
        db.query(Source).delete()
        db.query(Branch).delete()
        db.query(Tradition).delete()
        db.query(GlossaryTerm).delete()
        db.query(PreservedKnowledge).delete()
        db.commit()

        # Seed Glossary
        for g in GLOSSARY_ENTRIES:
            gt = GlossaryTerm(
                id=str(uuid.uuid4()),
                tamil_term=g["tamil"],
                transliteration=g["trans"],
                english_meaning=g["eng"],
                domain_name=g["domain"],
                branch_name=g["branch"],
                source_title="Tamil Heritage Lexicon (Sample)",
                is_live=False
            )
            db.add(gt)

        # Seed Traditions & Branches
        for t_data in DOMAINS_DATA:
            tradition = Tradition(
                id=t_data["id"],
                name=t_data["name"],
                tamil_name=t_data["tamil_name"],
                icon=t_data["icon"],
                description=t_data["description"],
                tamil_description=t_data.get("tamil_description") or t_data.get("tamil_desc", "")
            )
            db.add(tradition)
            db.flush()

            for b_data in t_data["branches"]:
                branch = Branch(
                    id=b_data["id"],
                    tradition_id=tradition.id,
                    name=b_data["name"],
                    tamil_name=b_data["tamil_name"],
                    description=b_data["desc"],
                    tamil_description=b_data["tamil_desc"],
                    urgency_score=b_data.get("urgency", 75),
                    urgency_level="HIGH" if b_data.get("urgency", 75) >= 65 else "MEDIUM"
                )
                db.add(branch)
                db.flush()

                # Create 3 Sample Sources for each branch
                s1 = Source(
                    id=f"{branch.id}-s1",
                    branch_id=branch.id,
                    title=f"Classical Field Manual of {branch.name} (Vol. I)",
                    author="K. S. Sundaram",
                    year="1932",
                    publisher="Madras Heritage Press",
                    source_type="Archival Description",
                    language="Tamil / English",
                    description=f"Detailed early 20th-century ethnographic survey of {branch.name}.",
                    is_live=False,
                    total_pages=48
                )
                s2 = Source(
                    id=f"{branch.id}-s2",
                    branch_id=branch.id,
                    title=f"Contemporary Practitioners' Oral Compendium",
                    author="South Indian Cultural Documentation Trust",
                    year="1984",
                    publisher="Regional Folklore Archives",
                    source_type="Oral Interview Transcript",
                    language="Tamil",
                    description=f"Audio interview transcripts with master hereditary practitioners of {branch.name}.",
                    is_live=False,
                    total_pages=36
                )
                s3 = Source(
                    id=f"{branch.id}-s3",
                    branch_id=branch.id,
                    title=f"Modern Comparative Monograph on {branch.name}",
                    author="Dr. M. Rajavel",
                    year="2016",
                    publisher="Tamil University Publications",
                    source_type="Research Paper",
                    language="English",
                    description=f"Academic synthesis of living techniques and contemporary status.",
                    is_live=False,
                    total_pages=28
                )
                db.add_all([s1, s2, s3])
                db.flush()

                sources_map = {1: s1, 2: s2, 3: s3}

                # Add Knowledge Elements
                elements_for_branch = []
                for elem in b_data["sample_elements"]:
                    for s_num in elem["s"]:
                        src = sources_map[s_num]
                        from services.normalization import NormalizationService
                        norm_key = NormalizationService.to_canonical_key(elem["name"])
                        ke = KnowledgeElement(
                            id=str(uuid.uuid4()),
                            branch_id=branch.id,
                            source_id=src.id,
                            category=elem["category"],
                            name=elem["name"],
                            normalized_key=norm_key,
                            tamil_term=NormalizationService._extract_tamil_term(elem["name"]) if hasattr(NormalizationService, '_extract_tamil_term') else "",
                            evidence_text=elem["quote"],
                            page_number=(elem["step"] * 4) + s_num,
                            step_order=elem.get("step"),
                            confidence=0.92
                        )
                        db.add(ke)
                        elements_for_branch.append(ke)
                db.flush()

                # Add Potential Gap & Missing Step
                gap_elem_name = b_data["gap_elem"]
                gap_type = b_data["gap_type"]
                step_ord = b_data.get("step_order")
                urgency_val = b_data.get("urgency", 75)

                supporting_s = [s1] # S1 always has it
                # Check which source has it
                for elem in b_data["sample_elements"]:
                    if elem["name"] == gap_elem_name:
                        supporting_s = [sources_map[sn] for sn in elem["s"]]
                        break

                absent_s = [s for s in [s1, s2, s3] if s not in supporting_s]

                hypo, conf = ReconstructionService.generate_cautious_reconstruction(
                    element_name=gap_elem_name,
                    category="practice" if gap_type != "missing_step" else "process_step",
                    is_missing_step=(gap_type == "missing_step"),
                    step_order=step_ord,
                    supporting_evidences=[
                        {"author": s.author, "year": s.year, "page_number": 12, "presence_status": "present"}
                        for s in supporting_s
                    ],
                    total_sources_count=3
                )

                score, level, factors = UrgencyCalculationService.calculate_urgency(
                    total_sources=3,
                    present_sources=len(supporting_s),
                    is_missing_step=(gap_type == "missing_step"),
                    oldest_year_str=supporting_s[0].year,
                    source_types=[s.source_type for s in [s1, s2, s3]]
                )

                norm_key = NormalizationService.to_canonical_key(gap_elem_name)
                gap_obj = KnowledgeGap(
                    id=str(uuid.uuid4()),
                    branch_id=branch.id,
                    element_key=norm_key,
                    element_name=gap_elem_name,
                    gap_type=gap_type,
                    status="POTENTIAL_GAP",
                    description=f"Potentially Unmentioned {'Step' if gap_type == 'missing_step' else 'Element'}: {gap_elem_name}",
                    details=(
                        f"Documented in: {', '.join([s.title for s in supporting_s])}, "
                        f"but unmentioned in: {', '.join([s.title for s in absent_s])}. "
                        "Potential knowledge gap — requires verification. "
                        "Absence from a recorded text does not prove knowledge was extinct in practice."
                    ),
                    step_order=step_ord,
                    urgency_score=urgency_val,
                    urgency_factors_json=json.dumps(factors),
                    reconstruction_hypothesis=hypo,
                    reconstruction_confidence=conf,
                    verification_status="PENDING",
                    is_live=False
                )
                db.add(gap_obj)
                db.flush()

                # Add Evidences for this Gap
                for s in supporting_s:
                    quote_text = next(
                        (e["quote"] for e in b_data["sample_elements"] if e["name"] == gap_elem_name),
                        f"Explicit record of {gap_elem_name} observed in archival folios."
                    )
                    ev_pres = Evidence(
                        id=str(uuid.uuid4()),
                        gap_id=gap_obj.id,
                        source_id=s.id,
                        source_title=s.title,
                        author=s.author,
                        year=s.year,
                        page_number=14,
                        quote=quote_text,
                        presence_status="present"
                    )
                    db.add(ev_pres)

                for s in absent_s:
                    ev_abs = Evidence(
                        id=str(uuid.uuid4()),
                        gap_id=gap_obj.id,
                        source_id=s.id,
                        source_title=s.title,
                        author=s.author,
                        year=s.year,
                        page_number=1,
                        quote=f"No textual mention or procedural instruction for '{gap_elem_name}' detected in this source.",
                        presence_status="absent"
                    )
                    db.add(ev_abs)

                # Seed 1 Verified Preserved item for demonstration in Preserved Knowledge page
                if branch.id in ["karagattam", "traditional-rice", "palm-leaf-manuscripts"]:
                    pres_kn = PreservedKnowledge(
                        id=str(uuid.uuid4()),
                        branch_id=branch.id,
                        tradition_id=tradition.id,
                        branch_name=branch.name,
                        tradition_name=tradition.name,
                        title=f"Verified Protocol: {gap_elem_name}",
                        tamil_title=f"சரிபார்க்கப்பட்ட மரபு: {gap_elem_name}",
                        category="process_step" if gap_type == "missing_step" else "practice",
                        reconstructed_text=hypo,
                        evidence_summary=f"Corroborated across historical records and verified by expert cultural review.",
                        confidence_level="VERIFIED",
                        verifier_notes="Reviewed and approved by Cultural Heritage Board advisory panel on 2026-03-12."
                    )
                    db.add(pres_kn)

        db.commit()
        print("Demo database successfully seeded!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_database()

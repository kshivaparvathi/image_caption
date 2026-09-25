"""
Showcase benchmark samples for VisionCaption AI.
Contains curated real-world visual scenes with detailed
multilingual analyses across major languages (English, Telugu, Hindi, Spanish, French, Japanese).
"""

from typing import Dict, Any, List
from pydantic import BaseModel

class SampleImageInfo(BaseModel):
    id: str
    title: str
    category: str
    description: str
    filename: str
    dominant_color: str
    analyses: Dict[str, Dict[str, Any]]

SAMPLE_DATA: Dict[str, SampleImageInfo] = {
    "street_market": SampleImageInfo(
        id="street_market",
        title="Vibrant Open-Air Market",
        category="Outdoor Market / Commercial Street",
        description="A bustling street food and fresh produce market with vendors, produce stalls, and active shoppers.",
        filename="street_market.jpg",
        dominant_color="#E07A5F",
        analyses={
            "en": {
                "short_caption": "A bustling open-air market vibrant with fresh produce stalls, wooden awnings, and active shoppers interacting in warm daylight.",
                "detailed_description": "The scene depicts an active morning marketplace lined with wooden produce crates and colorful fabric awnings. In the foreground, an assortment of citrus fruits, leafy greens, and exotic spices are neatly displayed on rustic stands. In the midground, several pedestrians and local merchants are engaged in casual exchanges and inspecting goods. The background reveals historic brick storefront facades under filtered natural sunlight, giving the environment an authentic, energetic street atmosphere.",
                "scene_context": {
                    "category": "Outdoor Market / Street",
                    "is_ambiguous": False,
                    "explanation": "Open-air commercial pedestrian lane surrounded by historic masonry buildings and temporary market canopies."
                },
                "important_elements": [
                    {"name": "Fresh Produce Displays", "detail": "Crates loaded with ripe oranges, apples, and leafy greens in the foreground.", "prominence": "primary"},
                    {"name": "Market Awnings", "detail": "Striped canvas and wooden canopies providing shade to vendor stalls.", "prominence": "secondary"},
                    {"name": "Historic Brick Architecture", "detail": "Multi-story brick facades with decorative lintels framing the market lane.", "prominence": "background"}
                ],
                "activities_actions": [
                    "Customers inspecting fruit freshness and conversing with merchants.",
                    "Vendors arranging crates and weighing items for purchase.",
                    "Pedestrians casually strolling along the market thoroughfare."
                ],
                "people_information": {
                    "detected": True,
                    "approximate_count": "6 to 8 visible individuals",
                    "visible_roles_or_activities": "Shoppers carrying canvas bags and merchants tending to their stalls wearing aprons and casual daytime attire.",
                    "clarity_notes": "Facial features in the background are naturally softened by distance and depth of field; identities are not inferred."
                },
                "visual_insights": {
                    "lighting_and_atmosphere": "Diffused morning sunlight with soft directional shadows casting warm golden reflections on produce surfaces.",
                    "composition_and_colors": "Warm palette dominated by terracotta oranges, forest greens, and deep brick reds, guided by a diagonal perspective vanishing into the market street.",
                    "notable_observations": [
                        "Handcrafted wooden pricing signs visible on several crates.",
                        "Subtle steam or morning mist rising near food preparation stations in the background."
                    ]
                },
                "read_aloud_summary": "This image captures a vibrant open-air market filled with wooden crates of fresh produce, striped awnings, and morning shoppers. Merchants and patrons engage across stalls bathed in warm daylight, set against classic brick architecture with a welcoming, energetic community atmosphere."
            },
            "te": {
                "short_caption": "తాజా పండ్ల దుకాణాలు, చెక్క పందిళ్ళు మరియు ఉల్లాసంగా బేరమాడుతున్న కొనుగోలుదారులతో కళకళలాడుతున్న బహిరంగ మార్కెట్ దృశ్యం.",
                "detailed_description": "ఈ చిత్రంలో ఉదయపు పూట కిటకిటలాడే బహిరంగ సంత స్పష్టంగా కనిపిస్తోంది. ముందుభాగంలో చెక్క పెట్టెలలో చక్కగా అమర్చిన నారింజ పండ్లు, ఆకుకూరలు మరియు వివిధ తాజా కూరగాయలు ఉన్నాయి. మధ్యభాగంలో వ్యాపారులు మరియు ప్రజలు సామగ్రిని పరిశీలిస్తూ సంభాషిస్తున్నారు. వెనుకభాగంలో సాంప్రదాయ ఇటుక భవనాల వరుసలు మరియు రంగురంగుల గుడారాలు ఆహ్లాదకరమైన వీధి వాతావరణాన్ని ప్రతిబింబిస్తున్నాయి.",
                "scene_context": {
                    "category": "బహిరంగ సంత / వీధి మార్కెట్",
                    "is_ambiguous": False,
                    "explanation": "చారిత్రక నగర వీధిలో ఏర్పాటు చేయబడిన తాత్కాలిక వాణిజ్య మార్కెట్ ప్రాంగణం."
                },
                "important_elements": [
                    {"name": "తాజా కూరగాయలు & పండ్ల స్టాళ్లు", "detail": "రంగురంగుల పండ్లు మరియు ఆకుకూరలతో నిండిన చెక్క ట్రేలు.", "prominence": "primary"},
                    {"name": "రంగుల గుడారాలు", "detail": "ఎండ నుండి రక్షణ కల్పించే తీరైన వస్త్రపు పందిళ్ళు.", "prominence": "secondary"},
                    {"name": "ఇటుక భవనాలు", "detail": "వీధికి ఇరువైపులా ఉన్న పాతకాలపు నగర నిర్మాణ శైలి.", "prominence": "background"}
                ],
                "activities_actions": [
                    "కొనుగోలుదారులు పండ్ల నాణ్యతను పరిశీలిస్తూ బేరమాడటం.",
                    "దుకాణదారులు వస్తువులను తూకం వేసి సంచుల్లో సర్దడం.",
                    "పాదచారులు వీధి మార్కెట్లో తీరిగ్గా నడవడం."
                ],
                "people_information": {
                    "detected": True,
                    "approximate_count": "సుమారు 6 నుండి 8 మంది వ్యక్తులు",
                    "visible_roles_or_activities": "సాధారణ రోజువారీ దుస్తులు మరియు ఏప్రాన్లు ధరించిన వ్యాపారులు మరియు షాపింగ్ బ్యాగులతో ఉన్న కస్టమర్లు.",
                    "clarity_notes": "దూరంగా ఉన్న వ్యక్తుల ముఖాలు స్పష్టంగా లేవు; ఎవరి వ్యక్తిగత గుర్తింపు ప్రతిపాదించబడలేదు."
                },
                "visual_insights": {
                    "lighting_and_atmosphere": "వెచ్చని ఉదయపు సహజ సూర్యకాంతి మరియు ఆహ్లాదకరమైన జీవకళతో కూడిన వాతావరణం.",
                    "composition_and_colors": "నారింజ, పచ్చదనం మరియు ఇటుక ఎరుపు రంగుల ఆకర్షణీయమైన కలయిక.",
                    "notable_observations": [
                        "చెక్క బోర్డులపై చేతితో రాసిన ధరల వివరాలు.",
                        "ప్రజల మధ్య సహజమైన సామాజిక అనుబంధం కనిపిస్తోంది."
                    ]
                },
                "read_aloud_summary": "ఈ చిత్రంలో రంగురంగుల తాజా కూరగాయలు మరియు పండ్లతో కళకళలాడుతున్న ఒక ఉదయపు బహిరంగ మార్కెట్ కనిపిస్తోంది. వ్యాపారులు, వినియోగదారులు ఉత్సాహంగా కొనుగోళ్లు జరుపుతున్నారు. చక్కని సూర్యకాంతి మరియు చారిత్రక భవనాల నేపథ్యంలో ఈ దృశ్యం ఎంతో ఆహ్లాదకరంగా ఉంది."
            },
            "hi": {
                "short_caption": "ताजा फलों और सब्जियों के स्टालों, रंगीन तंबुओं और खरीदारी करते लोगों से भरा एक जीवंत खुला बाजार।",
                "detailed_description": "यह दृश्य एक चहल-पहल भरे सुबह के खुले बाजार को दर्शाता है। अग्रभूमि में लकड़ी के बक्सों में ताजे संतरे, हरी सब्जियां और मसाले करीने से सजाए गए हैं। मध्य भाग में कई ग्राहक दुकानदारों से बातचीत करते और सामान की जांच करते दिखाई दे रहे हैं। पृष्ठभूमि में पारंपरिक ईंटों की इमारतें और धूप से बचाने वाले शेड एक ऊर्जावान शहरी माहौल बनाते हैं।",
                "scene_context": {
                    "category": "खुला बाजार / सड़क",
                    "is_ambiguous": False,
                    "explanation": "पारंपरिक इमारतों के बीच स्थित एक पैदल यात्री अनुकूल दैनिक फल एवं सब्जी बाजार।"
                },
                "important_elements": [
                    {"name": "ताजा फल और सब्जी स्टॉल", "detail": "सामने रखे लकड़ी के क्रेट्स में सजे रंग-बिरंगे फल।", "prominence": "primary"},
                    {"name": "मार्केट शेड और कैनोपी", "detail": "दुकानों को छाया देने वाले कपड़े के छज्जे।", "prominence": "secondary"},
                    {"name": "पारंपरिक ईंट की इमारतें", "detail": "बाजार के पीछे नजर आने वाली पुरानी वास्तुकला।", "prominence": "background"}
                ],
                "activities_actions": [
                    "ग्राहक फलों की ताजगी परख रहे हैं और बातचीत कर रहे हैं।",
                    "दुकानदार वस्तुओं को तौल रहे हैं और ग्राहकों को दे रहे हैं।",
                    "लोग सड़क पर चहलकदमी कर रहे हैं।"
                ],
                "people_information": {
                    "detected": True,
                    "approximate_count": "लगभग 6 से 8 लोग",
                    "visible_roles_or_activities": "दुकानदार एप्रन पहने हुए और ग्राहक थैलों के साथ खरीदारी करते नजर आ रहे हैं।",
                    "clarity_notes": "दूरी और बैकग्राउंड के कारण चेहरों की पहचान नहीं की जा सकती; किसी की पहचान नहीं बताई गई है।"
                },
                "visual_insights": {
                    "lighting_and_atmosphere": "सुबह की हल्की प्राकृतिक धूप, जिससे दृश्य में एक गर्म और स्वागतयोग्य माहौल बनता है।",
                    "composition_and_colors": "नारंगी, हरे और लाल रंगों का सुंदर संतुलन।",
                    "notable_observations": [
                        "लकड़ी के तख्तों पर लिखे मूल्य संकेत।",
                        "सक्रिय और सामंजस्यपूर्ण सामुदायिक व्यापारिक परिवेश।"
                    ]
                },
                "read_aloud_summary": "यह तस्वीर एक जीवंत और व्यस्त खुले बाजार को दिखाती है, जहाँ ताजे फल, सब्जियां और रंगीन छतरियां सजी हैं। लोग सुबह की सुनहरी धूप में खरीदारी कर रहे हैं, जो एक सुखद और स्वाभाविक वातावरण प्रस्तुत करता है।"
            },
            "es": {
                "short_caption": "Un animado mercado al aire libre repleto de puestos de productos frescos, toldos de colores y compradores activos.",
                "detailed_description": "La imagen muestra un mercado matutino lleno de vitalidad. En primer plano, cajones de madera exhiben cítricos, verduras de hoja verde y especias de manera ordenada. En el plano medio, varios compradores y comerciantes conversan e inspeccionan los productos. Al fondo, fachadas históricas de ladrillo bajo una suave luz solar completan una atmósfera urbana vibrante y acogedora.",
                "scene_context": {
                    "category": "Mercado al aire libre / Calle comercial",
                    "is_ambiguous": False,
                    "explanation": "Calle peatonal tradicional acondicionada para el comercio diario de productos frescos."
                },
                "important_elements": [
                    {"name": "Puestos de productos frescos", "detail": "Cajas de madera con naranjas, manzanas y verduras en primer plano.", "prominence": "primary"},
                    {"name": "Toldos y marquesinas", "detail": "Telas a rayas que brindan sombra a los vendedores.", "prominence": "secondary"},
                    {"name": "Arquitectura de ladrillo", "detail": "Edificios tradicionales que enmarcan el callejón del mercado.", "prominence": "background"}
                ],
                "activities_actions": [
                    "Clientes inspeccionando la calidad de los productos y dialogando con vendedores.",
                    "Comerciantes acomodando mercancía y pesando alimentos.",
                    "Transeúntes caminando por la vía peatonal."
                ],
                "people_information": {
                    "detected": True,
                    "approximate_count": "Aproximadamente 6 a 8 personas visibles",
                    "visible_roles_or_activities": "Vendedores con delantales y clientes con bolsas de compras en vestimenta informal de día.",
                    "clarity_notes": "Los rostros a media distancia no son identificables individualmente; se respeta la privacidad."
                },
                "visual_insights": {
                    "lighting_and_atmosphere": "Luz solar matutina suave y dorada que resalta los colores brillantes de las frutas.",
                    "composition_and_colors": "Gama cromática cálida con predominio de tonos terracota, verdes intensos y ocres.",
                    "notable_observations": [
                        "Pequeños carteles de madera con precios escritos a mano.",
                        "Profundidad de campo que guía la mirada a lo largo de la calle."
                    ]
                },
                "read_aloud_summary": "Esta imagen retrata un vibrante mercado callejero al aire libre con cajas de madera llenas de frutas frescas, toldos a rayas y vecinos haciendo sus compras matutinas bajo una cálida luz solar."
            }
        }
    ),
    "tech_collaboration": SampleImageInfo(
        id="tech_collaboration",
        title="Modern Agile Workspace",
        category="Indoor Office / Technology Workspace",
        description="A software and design team actively collaborating around a modern wooden desk with laptops, monitors, and whiteboard notes.",
        filename="tech_collaboration.jpg",
        dominant_color="#3D5A80",
        analyses={
            "en": {
                "short_caption": "A collaborative technology team working together around a modern conference desk with laptops, notes, and ambient natural lighting.",
                "detailed_description": "The photograph captures a focused collaborative session inside a modern, open-concept technology workplace. Three professionals are seated and standing around a sleek wooden conference table equipped with open laptops, tablets, wireframe sketches, and ceramic coffee mugs. In the background, a translucent glass whiteboard displays architectural diagrams and colorful sticky notes. Large floor-to-ceiling windows introduce diffused exterior daylight, complemented by minimalist ceiling pendant fixtures.",
                "scene_context": {
                    "category": "Office / Technology Studio",
                    "is_ambiguous": False,
                    "explanation": "Professional indoor workplace featuring contemporary ergonomic furnishings, collaborative technology, and architectural design."
                },
                "important_elements": [
                    {"name": "Laptops & Digital Tablets", "detail": "Multiple open modern laptops displaying code editors and design mockups.", "prominence": "primary"},
                    {"name": "Glass Whiteboard & Sticky Notes", "detail": "Brainstorming board featuring multi-colored sticky notes and workflow charts.", "prominence": "secondary"},
                    {"name": "Pendant Lighting & Large Windows", "detail": "Minimalist architectural lighting and natural window illumination.", "prominence": "background"}
                ],
                "activities_actions": [
                    "One person gesturing toward an open laptop screen while explaining a concept.",
                    "A colleague taking handwritten notes on a notepad while listening attentively.",
                    "Another team member reviewing architectural diagrams on the glass whiteboard."
                ],
                "people_information": {
                    "detected": True,
                    "approximate_count": "3 to 4 individuals",
                    "visible_roles_or_activities": "Knowledge workers in smart-casual modern workwear actively participating in an agile sprint review or design workshop.",
                    "clarity_notes": "Visible from side and back angles; individual identities are not inferred."
                },
                "visual_insights": {
                    "lighting_and_atmosphere": "Balanced dual lighting combining cool natural daylight from tall windows with warm overhead pendant illumination.",
                    "composition_and_colors": "Cool corporate palette featuring slate blues, natural pine wood tones, and vibrant accent colors from sticky notes.",
                    "notable_observations": [
                        "Ergonomic mesh chairs indicating modern workplace safety standards.",
                        "Indoor potted succulents adding an organic touch to the technology setting."
                    ]
                },
                "read_aloud_summary": "This scene displays an active team of tech professionals collaborating around a contemporary wooden table with laptops and coffee cups. Behind them, a glass whiteboard holds colorful brainstorming notes in a bright, modern studio illuminated by daylight."
            },
            "te": {
                "short_caption": "ఆధునిక కార్యాలయంలో ల్యాప్‌టాప్‌లు, నోట్స్ మరియు సహజ కాంతితో కలిసి పనిచేస్తున్న టెక్నాలజీ బృందం.",
                "detailed_description": "ఈ చిత్రంలో ఆధునిక సాఫ్ట్‌వేర్ కార్యాలయంలో జరుగుతున్న ఒక సమీక్షా సమావేశం కనిపిస్తోంది. సాంకేతిక నిపుణులు చెక్క కాన్ఫరెన్స్ టేబుల్ చుట్టూ కూర్చొని ల్యాప్‌టాప్‌లు, టాబ్లెట్‌లు మరియు నోట్‌బుక్‌లతో చర్చల్లో నిమగ్నమై ఉన్నారు. వెనుకభాగంలో ఉన్న గాజు వైట్‌బోర్డుపై రంగురంగుల స్టిక్కీ నోట్లు మరియు ప్రాజెక్ట్ ఫ్లోచార్ట్‌లు ఉన్నాయి. పెద్ద కిటికీల నుండి వచ్చే ఆహ్లాదకరమైన పగటి వెలుతురు కార్యాలయానికి హుందాతనాన్ని తెచ్చిపెట్టింది.",
                "scene_context": {
                    "category": "కార్యాలయం / టెక్నాలజీ స్టూడియో",
                    "is_ambiguous": False,
                    "explanation": "ఆధునిక ఎర్గోనామిక్ ఫర్నిచర్ మరియు సహకార సాంకేతికతతో కూడిన ప్రొఫెషనల్ పని ప్రదేశం."
                },
                "important_elements": [
                    {"name": "ల్యాప్‌టాప్‌లు మరియు గాడ్జెట్లు", "detail": "కోడింగ్ మరియు డిజైన్ స్క్రీన్లను ప్రదర్శిస్తున్న ఓపెన్ ల్యాప్‌టాప్‌లు.", "prominence": "primary"},
                    {"name": "గాజు వైట్‌బోర్డ్", "detail": "రంగురంగుల స్టిక్కీ నోట్లు మరియు ఆలోచనల పటాలు ఉన్న బోర్డు.", "prominence": "secondary"},
                    {"name": "పెద్ద కిటికీలు మరియు లైట్లు", "detail": "సహజ పగటి కాంతిని ఇచ్చే పెద్ద గాజు కిటికీలు.", "prominence": "background"}
                ],
                "activities_actions": [
                    "ఒక వ్యక్తి ల్యాప్‌టాప్ స్క్రీన్ చూపిస్తూ వివరిస్తుండటం.",
                    "మరొక సహోద్యోగి శ్రద్ధగా వింటూ నోట్స్ రాసుకోవడం.",
                    "బృందం కొత్త ప్రాజెక్ట్ ప్లానింగ్‌పై చర్చిస్తుండటం."
                ],
                "people_information": {
                    "detected": True,
                    "approximate_count": "సుమారు 3 నుండి 4 మంది వ్యక్తులు",
                    "visible_roles_or_activities": "సాధారణ కార్యాలయ దుస్తుల్లో ఉన్న ఐటీ ఉద్యోగులు సమావేశంలో చురుగ్గా పాల్గొంటున్నారు.",
                    "clarity_notes": "ముఖాలు పక్కనుండి లేదా వెనుకనుండి మాత్రమే కనిపిస్తున్నాయి; ఎవరి గుర్తింపు ప్రతిపాదించబడలేదు."
                },
                "visual_insights": {
                    "lighting_and_atmosphere": "కిటికీల నుండి వచ్చే స్వచ్ఛమైన సహజ కాంతి మరియు ఆహ్లాదకరమైన ప్రొఫెషనల్ వాతావరణం.",
                    "composition_and_colors": "నీలం, బూడిద మరియు లేత చెక్క రంగుల ఆధునిక కలయిక.",
                    "notable_observations": [
                        "టేబుల్‌పై కాఫీ కప్పులు మరియు ఆర్గానిక్ మొక్కలు.",
                        "సృజనాత్మక ఆలోచనలకు అనువైన ఆధునిక పని వాతావరణం."
                    ]
                },
                "read_aloud_summary": "ఈ చిత్రంలో ఆధునిక సాంకేతిక కార్యాలయంలో ఒక బృందం ల్యాప్‌టాప్‌లు, నోట్‌బుక్‌లతో చర్చలు జరుపుతున్న దృశ్యం కనిపిస్తోంది. వెనుకవైపు రంగురంగుల నోట్లతో కూడిన వైట్‌బోర్డ్ మరియు విశాలమైన కిటికీలతో కూడిన ఆహ్లాదకరమైన పని వాతావరణం స్పష్టంగా తెలుస్తోంది."
            }
        }
    ),
    "nature_wildlife": SampleImageInfo(
        id="nature_wildlife",
        title="Alpine Mountain Lake",
        category="Nature / Mountain Wilderness",
        description="A serene alpine lake reflecting jagged snow-capped mountain peaks and evergreen pine forests in crystal clear water.",
        filename="nature_wildlife.jpg",
        dominant_color="#2A9D8F",
        analyses={
            "en": {
                "short_caption": "A breathtaking alpine lake perfectly mirroring rugged snow-dusted mountain peaks and dense pine forests under a crisp blue sky.",
                "detailed_description": "The landscape showcases an unspoiled mountain wilderness during early summer. In the foreground, smooth granite pebbles and tranquil turquoise water create a glass-like mirror effect. The midground features slopes covered in dense evergreen coniferous forest, with towering Douglas firs and spruce trees. Rising majestically in the background are jagged, snow-capped rocky summits illuminated by radiant morning sunlight under a cloudless azure sky.",
                "scene_context": {
                    "category": "Nature / Mountain Wilderness",
                    "is_ambiguous": False,
                    "explanation": "High-altitude glacial alpine lake ecosystem located in an untouched national park wilderness."
                },
                "important_elements": [
                    {"name": "Glacial Mountain Lake", "detail": "Crystal-clear turquoise water producing a symmetrical mirror reflection.", "prominence": "primary"},
                    {"name": "Snow-Capped Peaks", "detail": "Rugged granite summits retaining pockets of winter snow under direct sunlight.", "prominence": "primary"},
                    {"name": "Coniferous Pine Forest", "detail": "Thick evergreen slopes bordering the shoreline.", "prominence": "secondary"}
                ],
                "activities_actions": [
                    "Gentle natural water ripple propagating softly near the shoreline.",
                    "Distant wildlife bird soaring high near mountain thermals."
                ],
                "people_information": {
                    "detected": False,
                    "approximate_count": "0 (No human presence detected)",
                    "visible_roles_or_activities": "Pristine uninhabited natural environment.",
                    "clarity_notes": "Entirely natural landscape with no artificial structures or human occupants visible."
                },
                "visual_insights": {
                    "lighting_and_atmosphere": "Brilliant direct morning sunlight casting high-contrast clarity on rock textures with zero haze.",
                    "composition_and_colors": "Stunning cool color harmony composed of turquoise blues, deep emerald greens, and gleaming white snow reflections.",
                    "notable_observations": [
                        "Remarkable optical symmetry created by the calm water surface.",
                        "Pristine air quality evidenced by sharp clarity of distant ridge lines."
                    ]
                },
                "read_aloud_summary": "This breathtaking landscape reveals a pristine alpine lake mirroring majestic snow-capped peaks and thick pine forests. The crystal-clear turquoise water and peaceful mountain wilderness offer an awe-inspiring vista of untamed nature."
            }
        }
    ),
    "classroom_lecture": SampleImageInfo(
        id="classroom_lecture",
        title="Interactive University Lecture",
        category="Indoor Classroom / Educational",
        description="A university professor delivering an engaging interactive robotics lecture to attentive students in a tiered modern hall.",
        filename="classroom_lecture.jpg",
        dominant_color="#F4A261",
        analyses={
            "en": {
                "short_caption": "An engaging university lecture hall where an instructor explains robotics concepts to attentive students seated at tiered desks.",
                "detailed_description": "The photograph captures an educational session inside a bright, tiered university lecture theater. At the podium in the front, an instructor gestures toward a large presentation screen displaying mechanical schematics and mathematical formulas. Seated in ascending rows are dozens of diverse adult students, many with open notebooks, tablets, and laptops actively following along. The auditorium features warm wood acoustic paneling and recessed ambient lighting that fosters an inspiring academic environment.",
                "scene_context": {
                    "category": "Classroom / Educational Lecture Hall",
                    "is_ambiguous": False,
                    "explanation": "Tiered higher-education auditorium equipped with audiovisual teaching displays and acoustic treatments."
                },
                "important_elements": [
                    {"name": "Audiovisual Projection Screen", "detail": "Large dual projection screens displaying robotic arm engineering diagrams.", "prominence": "primary"},
                    {"name": "Tiered Student Desks", "detail": "Continuous wooden desks fitted with charging outlets and study materials.", "prominence": "secondary"},
                    {"name": "Instructor Podium", "detail": "Front lecture station with a microphone and reference tablet.", "prominence": "secondary"}
                ],
                "activities_actions": [
                    "The instructor gesturing with an outstretched arm toward the presentation slide.",
                    "Students writing notes in spiral notebooks and typing on portable computers.",
                    "A student in the third row raising a hand to pose a question."
                ],
                "people_information": {
                    "detected": True,
                    "approximate_count": "15 to 25 visible students plus 1 instructor",
                    "visible_roles_or_activities": "College students seated in study postures and an educator delivering an instructional talk.",
                    "clarity_notes": "Audience members are viewed primarily from behind and in profile; no private identity is established."
                },
                "visual_insights": {
                    "lighting_and_atmosphere": "Even, glare-free ceiling downlights designed for screen readability and notebook writing.",
                    "composition_and_colors": "Warm amber wood acoustic textures balanced with clean white presentation projections and dark auditorium seating.",
                    "notable_observations": [
                        "Robotic kinematic equation visible on the whiteboard section.",
                        "Attentive body postures indicating an interactive, focused learning atmosphere."
                    ]
                },
                "read_aloud_summary": "This view shows a modern university lecture hall during an engaging robotics presentation. The professor illustrates engineering concepts on a large display while students across tiered rows take notes and participate actively in the lecture."
            }
        }
    )
}

def get_sample(sample_id: str) -> SampleImageInfo:
    return SAMPLE_DATA.get(sample_id)

def get_sample_analysis(sample_id: str, lang_code: str) -> Dict[str, Any]:
    sample = SAMPLE_DATA.get(sample_id)
    if not sample:
        return None
    # Check if analysis exists in requested language
    if lang_code in sample.analyses:
        return sample.analyses[lang_code]
    # Check English fallback
    if "en" in sample.analyses:
        return sample.analyses["en"]
    # Return first available
    return next(iter(sample.analyses.values()))

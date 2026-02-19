"""
AI Agriculture Chatbot
Provides personalized agricultural guidance to farmers.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
import os


@dataclass
class ChatMessage:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)


class AgriChatbot:
    """
    AI Chatbot for agricultural guidance.
    Provides advice on crops, diseases, fertilizers, irrigation, and more.
    """

    def __init__(self, knowledge_path: str = None):
        self.name = "AgriBot"
        self.version = "1.0"
        self.conversation_history: List[ChatMessage] = []

        # Load knowledge base
        if knowledge_path and os.path.exists(knowledge_path):
            with open(knowledge_path, 'r') as f:
                self.knowledge = json.load(f)
        else:
            self.knowledge = self._get_default_knowledge()

        # Intent patterns
        self.intents = {
            'greeting': r'\b(hello|hi|hey|good morning|good evening|namaste)\b',
            'crop_info': r'\b(grow|plant|cultivate|crop|farming)\b.*\b(wheat|rice|maize|cotton|tomato|potato|soybean)\b',
            'disease': r'\b(disease|infection|sick|yellow|brown|spots|wilting|dying)\b',
            'fertilizer': r'\b(fertilizer|npk|nitrogen|phosphorus|potassium|nutrient|deficiency)\b',
            'pest': r'\b(pest|insect|bug|aphid|caterpillar|worm|beetle|mite)\b',
            'irrigation': r'\b(water|irrigation|irrigate|watering|moisture|dry|wet)\b',
            'weather': r'\b(weather|rain|temperature|frost|heat|cold|monsoon)\b',
            'price': r'\b(price|market|sell|rate|mandi|cost)\b',
            'season': r'\b(season|when to plant|sowing time|harvest time|kharif|rabi)\b',
            'soil': r'\b(soil|ph|acidic|alkaline|clay|sandy|loamy)\b',
            'yield': r'\b(yield|production|output|harvest|tons|quintals)\b',
            'organic': r'\b(organic|natural|chemical-free|bio|compost)\b',
            'help': r'\b(help|what can you do|options|commands)\b',
            'thanks': r'\b(thank|thanks|thankyou|appreciate)\b',
            'goodbye': r'\b(bye|goodbye|see you|quit|exit)\b'
        }

    def _get_default_knowledge(self) -> Dict:
        """Default knowledge base"""
        return {
            "crop_info": {
                "wheat": {
                    "growing_season": "October to April (Rabi)",
                    "optimal_temperature": "15-25°C",
                    "water_requirement": "450-650 mm",
                    "soil_type": "Well-drained loamy soil",
                    "ph_range": "6.0-7.5"
                },
                "rice": {
                    "growing_season": "June to November (Kharif)",
                    "optimal_temperature": "20-35°C",
                    "water_requirement": "1200-1400 mm",
                    "soil_type": "Clay or clay loam",
                    "ph_range": "5.5-6.5"
                }
            },
            "disease_treatments": {
                "rust": {"treatment": "Apply Propiconazole 1ml/L"},
                "blight": {"treatment": "Apply Mancozeb 2.5g/L"}
            },
            "fertilizer_guide": {
                "nitrogen_deficiency": "Apply urea at 50-100 kg/ha",
                "phosphorus_deficiency": "Apply DAP at 50-75 kg/ha"
            }
        }

    def _detect_intent(self, message: str) -> Tuple[str, float]:
        """Detect the intent of a message"""
        message_lower = message.lower()

        for intent, pattern in self.intents.items():
            if re.search(pattern, message_lower, re.IGNORECASE):
                return intent, 0.85

        return 'general', 0.5

    def _extract_crop(self, message: str) -> Optional[str]:
        """Extract crop name from message"""
        crops = ['wheat', 'rice', 'maize', 'cotton', 'tomato', 'potato', 'soybean', 'sugarcane', 'onion']
        message_lower = message.lower()

        for crop in crops:
            if crop in message_lower:
                return crop
        return None

    def _handle_greeting(self) -> str:
        """Handle greeting intent"""
        greetings = [
            "Hello! I'm AgriBot, your agricultural assistant. How can I help you today?",
            "Namaste! Welcome to AgriBot. I can help you with crop information, disease identification, fertilizer recommendations, and more. What would you like to know?",
            "Hi there! I'm here to help with all your farming questions. Ask me about crops, pests, irrigation, or anything agriculture-related!"
        ]
        import random
        return random.choice(greetings)

    def _handle_crop_info(self, message: str) -> str:
        """Handle crop information queries"""
        crop = self._extract_crop(message)

        if crop and crop in self.knowledge.get('crop_info', {}):
            info = self.knowledge['crop_info'][crop]
            response = f"📌 **{crop.title()} Growing Guide:**\n\n"
            response += f"🗓️ **Season:** {info.get('growing_season', 'Varies by region')}\n"
            response += f"🌡️ **Temperature:** {info.get('optimal_temperature', '20-30°C')}\n"
            response += f"💧 **Water Requirement:** {info.get('water_requirement', '500-800mm')}\n"
            response += f"🌱 **Soil Type:** {info.get('soil_type', 'Well-drained loamy soil')}\n"
            response += f"⚗️ **pH Range:** {info.get('ph_range', '6.0-7.0')}\n\n"

            if 'major_diseases' in info:
                response += f"⚠️ **Common Diseases:** {', '.join(info['major_diseases'])}\n"
            if 'fertilizer_npk' in info:
                response += f"🧪 **Recommended NPK:** {info['fertilizer_npk']}\n"
            if 'yield_potential' in info:
                response += f"📊 **Yield Potential:** {info['yield_potential']}\n"

            return response
        elif crop:
            return f"I have basic information about {crop}. For detailed guidance, please consult your local agricultural extension office or use our Crop Yield Predictor tool."
        else:
            return "Which crop would you like to know about? I can provide information on wheat, rice, maize, cotton, tomato, potato, and more."

    def _handle_disease(self, message: str) -> str:
        """Handle disease-related queries"""
        response = "🔬 **Crop Disease Guidance:**\n\n"

        # Check for specific symptoms
        symptoms = {
            'yellow': "Yellow leaves may indicate nitrogen deficiency or viral infection.",
            'brown': "Brown spots often indicate fungal diseases like leaf blight.",
            'spots': "Spots on leaves could be bacterial or fungal infections.",
            'wilting': "Wilting may indicate root rot, fusarium wilt, or water stress.",
            'powder': "White powdery coating suggests powdery mildew infection."
        }

        found_symptoms = []
        message_lower = message.lower()
        for symptom, advice in symptoms.items():
            if symptom in message_lower:
                found_symptoms.append(f"• **{symptom.title()} leaves:** {advice}")

        if found_symptoms:
            response += "Based on your description:\n"
            response += "\n".join(found_symptoms)
            response += "\n\n**Recommendations:**\n"
            response += "1. Take clear photos of affected plants\n"
            response += "2. Use our Disease Detection tool for AI-based diagnosis\n"
            response += "3. Isolate severely affected plants\n"
            response += "4. Avoid overhead irrigation\n"
        else:
            response += "To help identify the disease, please describe:\n"
            response += "• What symptoms do you see? (spots, wilting, color changes)\n"
            response += "• Which crop is affected?\n"
            response += "• How long have you noticed this?\n\n"
            response += "💡 **Tip:** Use our Disease Detection feature to upload a photo for instant AI diagnosis!"

        return response

    def _handle_fertilizer(self, message: str) -> str:
        """Handle fertilizer-related queries"""
        response = "🧪 **Fertilizer Guidance:**\n\n"

        message_lower = message.lower()

        if 'nitrogen' in message_lower or 'yellow' in message_lower:
            response += "**Nitrogen Deficiency:**\n"
            response += "• Symptoms: Yellowing of older leaves, stunted growth\n"
            response += "• Solution: Apply Urea (46% N) at 50-100 kg/ha\n"
            response += "• Timing: Split application - 50% at sowing, 50% after 30 days\n\n"

        if 'phosphorus' in message_lower or 'purple' in message_lower:
            response += "**Phosphorus Deficiency:**\n"
            response += "• Symptoms: Purple coloration, poor root development\n"
            response += "• Solution: Apply DAP or SSP at 50-75 kg/ha\n"
            response += "• Timing: At sowing time (basal application)\n\n"

        if 'potassium' in message_lower or 'edge' in message_lower:
            response += "**Potassium Deficiency:**\n"
            response += "• Symptoms: Brown leaf edges, weak stems\n"
            response += "• Solution: Apply MOP at 40-60 kg/ha\n"
            response += "• Timing: At sowing or first irrigation\n\n"

        crop = self._extract_crop(message)
        if crop:
            npk_recommendations = {
                'wheat': '120:60:40',
                'rice': '100:50:50',
                'maize': '150:75:40',
                'cotton': '80:40:40',
                'tomato': '100:50:50',
                'potato': '150:100:100'
            }
            if crop in npk_recommendations:
                response += f"**Recommended NPK for {crop.title()}:** {npk_recommendations[crop]} kg/ha\n\n"

        if len(response) < 100:  # No specific query matched
            response += "**General NPK Guidelines:**\n"
            response += "• N (Nitrogen): For leafy growth\n"
            response += "• P (Phosphorus): For roots and flowers\n"
            response += "• K (Potassium): For overall plant health\n\n"
            response += "Tell me your crop and I'll provide specific recommendations!"

        return response

    def _handle_pest(self, message: str) -> str:
        """Handle pest-related queries"""
        response = "🐛 **Pest Control Guidance:**\n\n"

        pests = {
            'aphid': {
                'identification': 'Small soft-bodied insects (green/black)',
                'damage': 'Suck sap, transmit viruses',
                'organic': 'Neem oil (5ml/L), release ladybugs',
                'chemical': 'Imidacloprid (0.5ml/L)'
            },
            'caterpillar': {
                'identification': 'Larvae with chewing mouthparts',
                'damage': 'Eat leaves and fruits',
                'organic': 'Bt spray, hand picking',
                'chemical': 'Chlorantraniliprole (0.3ml/L)'
            },
            'whitefly': {
                'identification': 'Tiny white flying insects',
                'damage': 'Suck sap, cause sooty mold',
                'organic': 'Yellow sticky traps, neem spray',
                'chemical': 'Thiamethoxam (0.3g/L)'
            }
        }

        message_lower = message.lower()
        found_pest = None
        for pest in pests:
            if pest in message_lower:
                found_pest = pest
                break

        if found_pest:
            info = pests[found_pest]
            response += f"**{found_pest.title()} Control:**\n\n"
            response += f"🔍 **Identification:** {info['identification']}\n"
            response += f"⚠️ **Damage:** {info['damage']}\n"
            response += f"🌿 **Organic Control:** {info['organic']}\n"
            response += f"💊 **Chemical Control:** {info['chemical']}\n\n"
            response += "**Prevention Tips:**\n"
            response += "• Regular monitoring of crops\n"
            response += "• Maintain field hygiene\n"
            response += "• Use resistant varieties\n"
        else:
            response += "Common pests and quick solutions:\n\n"
            response += "🐛 **Aphids:** Neem oil spray (5ml/L)\n"
            response += "🦋 **Caterpillars:** Bt spray or hand picking\n"
            response += "🪰 **Whiteflies:** Yellow sticky traps\n"
            response += "🕷️ **Mites:** Increase humidity, apply miticide\n\n"
            response += "Tell me which pest you're dealing with for specific advice!"

        return response

    def _handle_irrigation(self, message: str) -> str:
        """Handle irrigation queries"""
        response = "💧 **Irrigation Guidance:**\n\n"

        crop = self._extract_crop(message)

        water_needs = {
            'rice': ('High', '1200-1400mm', 'Standing water for most of growth'),
            'wheat': ('Medium', '450-650mm', '4-6 irrigations at critical stages'),
            'maize': ('Medium', '500-800mm', 'Critical at tasseling and grain filling'),
            'cotton': ('Medium-High', '700-1200mm', 'Avoid water stress at flowering'),
            'tomato': ('Medium', '400-600mm', 'Regular watering, avoid waterlogging'),
            'potato': ('Medium', '500-700mm', 'Keep soil consistently moist')
        }

        if crop and crop in water_needs:
            need, amount, tip = water_needs[crop]
            response += f"**{crop.title()} Water Requirements:**\n"
            response += f"• Water Need: {need}\n"
            response += f"• Total Requirement: {amount}\n"
            response += f"• Tip: {tip}\n\n"

        response += "**Irrigation Methods Comparison:**\n\n"
        response += "🚿 **Drip Irrigation:**\n"
        response += "• Water saving: 30-50%\n"
        response += "• Best for: Vegetables, fruits, cotton\n\n"

        response += "💦 **Sprinkler:**\n"
        response += "• Water saving: 20-30%\n"
        response += "• Best for: Field crops, lawns\n\n"

        response += "🌊 **Flood Irrigation:**\n"
        response += "• Efficiency: 40-50%\n"
        response += "• Best for: Rice, sugarcane\n\n"

        response += "💡 **Tip:** Use our Smart Irrigation tool for real-time recommendations!"

        return response

    def _handle_weather(self, message: str) -> str:
        """Handle weather-related queries"""
        response = "🌤️ **Weather Advisory:**\n\n"

        message_lower = message.lower()

        if 'rain' in message_lower or 'monsoon' in message_lower:
            response += "**Rainy Season Tips:**\n"
            response += "• Ensure proper field drainage\n"
            response += "• Apply fungicide preventively\n"
            response += "• Stake tall plants\n"
            response += "• Harvest mature crops before heavy rain\n\n"

        if 'heat' in message_lower or 'hot' in message_lower:
            response += "**Heat Wave Protection:**\n"
            response += "• Increase irrigation frequency\n"
            response += "• Apply mulch (5-7cm layer)\n"
            response += "• Use shade nets for sensitive crops\n"
            response += "• Irrigate during cooler hours\n\n"

        if 'frost' in message_lower or 'cold' in message_lower:
            response += "**Frost Protection:**\n"
            response += "• Cover plants with cloth/plastic\n"
            response += "• Irrigate before frost (releases heat)\n"
            response += "• Use windbreaks\n"
            response += "• Harvest sensitive crops\n\n"

        if len(response) < 100:
            response += "Weather affects farming in many ways. What specific weather concern do you have?\n"
            response += "• Heavy rain / monsoon\n"
            response += "• Heat wave / drought\n"
            response += "• Frost / cold\n"
            response += "• Wind / storms"

        return response

    def _handle_help(self) -> str:
        """Show available commands"""
        return """🤖 **AgriBot Help Menu:**

I can assist you with:

🌾 **Crop Information**
Ask: "How to grow wheat?" or "Tell me about rice cultivation"

🔬 **Disease Identification**
Ask: "My tomato leaves have spots" or "Yellow leaves on my crop"

🧪 **Fertilizer Guidance**
Ask: "What fertilizer for wheat?" or "Nitrogen deficiency symptoms"

🐛 **Pest Control**
Ask: "How to control aphids?" or "Caterpillar in my field"

💧 **Irrigation**
Ask: "Water requirement for rice" or "Best irrigation method"

🌤️ **Weather Advice**
Ask: "How to protect from frost?" or "Monsoon farming tips"

📊 **Market Prices**
Ask: "Wheat price today" or "Best time to sell rice"

💡 **Tips:**
• Be specific about your crop
• Describe symptoms clearly
• Mention your region if relevant

Type your question to get started!"""

    def _handle_thanks(self) -> str:
        """Handle thank you messages"""
        responses = [
            "You're welcome! Feel free to ask if you have more questions. Happy farming! 🌾",
            "Glad I could help! Best wishes for a great harvest! 🚜",
            "My pleasure! Don't hesitate to return for more agricultural guidance. 🌱"
        ]
        import random
        return random.choice(responses)

    def _handle_goodbye(self) -> str:
        """Handle goodbye messages"""
        responses = [
            "Goodbye! Wishing you a bountiful harvest! 🌾",
            "Take care! Visit again for agricultural advice. Happy farming! 🚜",
            "See you soon! May your fields flourish! 🌻"
        ]
        import random
        return random.choice(responses)

    def _handle_general(self, message: str) -> str:
        """Handle general queries"""
        return f"""I understand you're asking about: "{message}"

I'm specialized in agricultural topics. I can help with:

• 🌾 Crop cultivation and care
• 🔬 Disease identification and treatment
• 🧪 Fertilizer recommendations
• 🐛 Pest control
• 💧 Irrigation guidance
• 🌤️ Weather advisories
• 📊 Market information

Could you rephrase your question or ask about one of these topics?

Type "help" to see all my capabilities!"""

    def chat(self, message: str) -> Dict[str, Any]:
        """Process a chat message and return response"""

        # Store user message
        self.conversation_history.append(ChatMessage(role='user', content=message))

        # Detect intent
        intent, confidence = self._detect_intent(message)

        # Generate response based on intent
        intent_handlers = {
            'greeting': self._handle_greeting,
            'crop_info': lambda: self._handle_crop_info(message),
            'disease': lambda: self._handle_disease(message),
            'fertilizer': lambda: self._handle_fertilizer(message),
            'pest': lambda: self._handle_pest(message),
            'irrigation': lambda: self._handle_irrigation(message),
            'weather': lambda: self._handle_weather(message),
            'help': self._handle_help,
            'thanks': self._handle_thanks,
            'goodbye': self._handle_goodbye,
            'general': lambda: self._handle_general(message)
        }

        handler = intent_handlers.get(intent, intent_handlers['general'])
        if callable(handler) and intent in ['greeting', 'help', 'thanks', 'goodbye']:
            response_text = handler()
        else:
            response_text = handler()

        # Store assistant response
        self.conversation_history.append(ChatMessage(
            role='assistant',
            content=response_text,
            metadata={'intent': intent, 'confidence': confidence}
        ))

        return {
            'response': response_text,
            'intent': intent,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }

    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp
            }
            for msg in self.conversation_history
        ]

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# Global chatbot instance
chatbot = AgriChatbot()

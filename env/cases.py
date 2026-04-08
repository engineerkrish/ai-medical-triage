CASES = {
    "easy": [
        {
            "id": "headache_easy",
            "difficulty": "easy",
            "initial": "I have a headache for two days.",
            "hidden_info": {
                "fever": "No fever",
                "vision": "No blurred vision"
            },
            "expected": {
                "triage": "non-emergency",
                "condition": "tension headache",
                "advice": "rest and hydration"
            },
            "critical_symptoms": ["fever", "vision"]
        }
    ],

    "medium": [
        {
            "id": "chest_pain_medium",
            "difficulty": "medium",
            "initial": "I have chest pain and feel uneasy.",
            "hidden_info": {
                "breathing": "Yes, I feel shortness of breath."
            },
            "expected": {
                "triage": "emergency",
                "condition": "possible heart attack",
                "advice": "seek immediate medical help"
            },
            "critical_symptoms": ["chest pain", "breathing"]
        }
    ],

    "hard": [
        {
            "id": "ambiguous_chest_pain",
            "difficulty": "hard",
            "initial": "I have mild chest pain for 3 hours.",
            "hidden_info": {
                "breathing": "Mild shortness of breath",
                "fever": "No fever"
            },
            "expected": {
                "triage": "emergency",
                "condition": "possible cardiac issue",
                "advice": "visit hospital immediately"
            },
            "critical_symptoms": ["chest pain", "breathing"]
        }
    ]
}
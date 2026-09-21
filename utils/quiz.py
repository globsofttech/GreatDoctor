"""Short review questions for daily lesson emails."""

QUIZ_BANK = {
    "Rheumatoid Arthritis": {
        "question": "Which antibody is most specific for Rheumatoid Arthritis?",
        "options": [
            "Rheumatoid factor",
            "Anti-cyclic citrullinated peptide (anti-CCP) antibody",
            "Antinuclear antibody (ANA)",
            "Anti-double-stranded DNA antibody",
        ],
        "answer": "B",
        "explanation": "Anti-CCP antibodies are more specific for Rheumatoid Arthritis than rheumatoid factor.",
    },
}


def get_quiz(topic):
    """Return a quiz for a topic, with a simple fallback for new topics."""
    name = topic.get("name", "today's topic")
    return QUIZ_BANK.get(name, {
        "question": f"Which condition is today's lesson about?",
        "options": [name, "A bacterial infection", "A fracture", "A normal finding"],
        "answer": "A",
        "explanation": f"Today's lesson is about {name}.",
    })

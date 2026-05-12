def detect_priority(report_text):

    report_text = report_text.lower()

    emergency_keywords = [
        "heart attack",
        "stroke",
        "severe bleeding",
        "difficulty breathing"
    ]

    high_keywords = [
        "chest pain",
        "high fever",
        "hypertension",
        "diabetes"
    ]

    medium_keywords = [
        "fever",
        "infection",
        "headache"
    ]

    for word in emergency_keywords:
        if word in report_text:
            return "Emergency"

    for word in high_keywords:
        if word in report_text:
            return "High"

    for word in medium_keywords:
        if word in report_text:
            return "Medium"

    return "Low"
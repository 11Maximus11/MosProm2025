class AnalyzerAgent:
    def analyze(self, text: str, image_data=None) -> dict:
        return {"full_text": text, "entities": {}}
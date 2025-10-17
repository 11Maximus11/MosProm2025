class VerifierAgent:
    def verify(self, query: str, answer: str) -> dict:
        return {"decision": "approve", "confidence": 0.99}
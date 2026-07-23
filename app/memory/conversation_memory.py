class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, question: str):
        self.history.append(question)

    def get_context(self, last_n: int = 5):
        return self.history[-last_n:]

    def clear(self):
        self.history.clear()
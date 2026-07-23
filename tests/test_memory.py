from app.memory.conversation_memory import ConversationMemory


def test_add_question():
    memory = ConversationMemory()

    memory.add("What is Python?")

    assert memory.history == ["What is Python?"]


def test_get_context_default():
    memory = ConversationMemory()

    memory.add("Q1")
    memory.add("Q2")
    memory.add("Q3")

    assert memory.get_context() == ["Q1", "Q2", "Q3"]


def test_get_context_last_n():
    memory = ConversationMemory()

    for i in range(1, 8):
        memory.add(f"Q{i}")

    assert memory.get_context(3) == ["Q5", "Q6", "Q7"]


def test_clear():
    memory = ConversationMemory()

    memory.add("Q1")
    memory.add("Q2")

    memory.clear()

    assert memory.history == []
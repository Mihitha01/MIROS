from miros.core.models import IntentCategory
from miros.processing.intent_classifier import IntentClassifier


def test_classifies_system_open_app() -> None:
    classifier = IntentClassifier()
    intent = classifier.classify("open notepad")

    assert intent.category == IntentCategory.SYSTEM
    assert intent.action == "open_app"
    assert intent.entities["app"] == "notepad"


def test_classifies_web_search() -> None:
    classifier = IntentClassifier()
    intent = classifier.classify("search web for event driven architecture")

    assert intent.category == IntentCategory.WEB
    assert intent.action == "web_search"
    assert "event driven architecture" in intent.entities["query"]


def test_falls_back_to_conversation() -> None:
    classifier = IntentClassifier()
    intent = classifier.classify("tell me a story about software reliability")

    assert intent.category == IntentCategory.CONVERSATION
    assert intent.action == "chat"

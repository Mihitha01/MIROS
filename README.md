# MIROS: Modular Intelligent Runtime Operating System

MIROS is a production-style intelligent assistant architecture built as a layered, extensible Python system. It is designed as an AI operating layer, not a single-script demo assistant.

## 1. System Architecture Overview

MIROS is structured as a pipeline of decoupled layers:

1. Interaction Layer
   - Captures input via voice (speech-to-text) or text fallback.
   - Delivers responses via console and optional text-to-speech.

2. Intelligent Processing Layer
   - Performs intent classification with rule-based NLU.
   - Routes intents into execution domains: system, web, API, conversation.

3. Action/Execution Layer
   - Uses a plugin registry and dispatcher.
   - Plugins handle domain-specific actions with a shared execution context.

4. AI Integration Layer
   - Defines LLM provider abstractions.
   - Ships with a mock LLM provider while keeping the interface pluggable.

5. Memory Layer
   - Persists interactions in SQLite.
   - Exposes recent context for conversational continuity.

### Why this architecture

- Separation of concerns: each layer has a focused responsibility.
- Extensibility: new commands and capabilities are added as plugins and adapters.
- Testability: components are independently testable (classifier, memory, registry).
- Operability: structured logging, bounded filesystem access, and explicit error handling.

### Component communication model

1. Multimodal interface captures user input.
2. Intent classifier returns structured intent.
3. Intent router tags execution domain.
4. Command registry dispatches intent to matching plugin.
5. Plugin uses shared context services (system executor, web executor, LLM, API adapter, memory).
6. Result is persisted to memory and returned via output channels.

### Scaling path

- Replace rule-based classifier with transformer-based NLU while preserving Intent model.
- Swap mock LLM provider with OpenAI/Azure/local models behind LLMProvider interface.
- Add GUI/websocket clients on top of service layer.
- Add IoT/device plugins without touching existing domains.
- Add autonomous planning agents as another plugin domain.

## 2. Project Structure

```text
MIROS/
  miros/
    __init__.py
    main.py
    core/
      config.py
      logging_config.py
      models.py
    interaction/
      input_providers.py
      output_providers.py
      interface.py
    processing/
      intent_classifier.py
      intent_router.py
    execution/
      context.py
      system_actions.py
      web_actions.py
      registry.py
      plugins/
        base.py
        system_plugin.py
        web_plugin.py
        api_plugin.py
        conversation_plugin.py
    integration/
      external_api.py
      llm/
        base.py
        mock_provider.py
    memory/
      store.py
    services/
      assistant.py
  tests/
    test_intent_classifier.py
    test_registry.py
    test_memory_store.py
  .env.example
  requirements.txt
  run.py
```

## 3. Module-by-Module Explanation

- miros/core/config.py
  - Centralized environment-driven configuration.
  - Defines runtime knobs for input mode, TTS/STT, logging, memory path, provider selection.

- miros/core/models.py
  - Shared domain objects: Intent, IntentCategory, CommandResult.
  - Keeps contracts stable across layers.

- miros/interaction/*
  - Input providers: text and speech recognition with safe fallback.
  - Output providers: console plus optional pyttsx3 speech synthesis.
  - Interface facade exposes listen/respond methods.

- miros/processing/*
  - Rule-based intent classification with confidence and entities extraction.
  - Router maps intents to execution domains for policy and observability.

- miros/execution/*
  - Registry implements plugin dispatch pattern.
  - System actions: app launch and guarded workspace file operations.
  - Web actions: URL open and search endpoint integration.
  - Plugins isolate command families and business logic.

- miros/integration/*
  - LLMProvider abstraction defines clean API for model integration.
  - MockLLMProvider supports local development.
  - External API adapter uses mock implementation with normalized responses.

- miros/memory/store.py
  - SQLite-backed persistent interaction storage.
  - Provides context retrieval for conversational plugins.

- miros/services/assistant.py
  - Composition root for all layers.
  - Runtime loop, orchestration, persistence, and response lifecycle.

## 4. Full Implementation (File-by-File)

All source files listed in the project structure are fully implemented in this repository, including runtime modules, plugin architecture, memory persistence, and tests.

## 5. requirements.txt

Dependencies are provided in requirements.txt and include:

- SpeechRecognition for STT
- pyttsx3 for TTS
- python-dotenv for environment config
- requests for future API integrations
- pytest for tests

## 6. Run Instructions

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Optional: copy .env.example to .env and adjust settings.

4. Start MIROS (interactive)

```powershell
python run.py
```

5. Start MIROS in text mode (recommended if microphone support is not installed)

```powershell
python run.py --mode text
```

6. Run single command and exit

```powershell
python run.py --once "search web for distributed systems patterns"
```

7. Run tests

```powershell
pytest
```

## Notes on Voice Dependencies

- SpeechRecognition microphone input usually requires PyAudio.
- If PyAudio is not present, MIROS gracefully falls back to text input.

## Future Extensions

- GUI client (desktop/web) as another interaction adapter.
- IoT plugin pack with device command adapters.
- Planner/agent plugin that chains multiple actions autonomously.
- Production LLM provider adapters with auth, retries, and telemetry.

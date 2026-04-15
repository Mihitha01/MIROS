from miros.interaction import output_providers


class _FailingPyttsx3:
    @staticmethod
    def init():
        raise RuntimeError("sapi init failed")


def test_output_manager_disables_tts_when_init_fails(monkeypatch) -> None:
    monkeypatch.setattr(output_providers, "pyttsx3", _FailingPyttsx3)

    manager = output_providers.OutputManager(enable_tts=True)

    assert manager.enable_tts is False
    assert manager.tts is None
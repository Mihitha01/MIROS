"""CLI entrypoint for MIROS."""

from __future__ import annotations

import argparse
from pathlib import Path

from miros.core.config import MirosConfig
from miros.core.logging_config import configure_logging
from miros.services.assistant import MirosAssistantService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MIROS - Modular Intelligent Runtime OS")
    parser.add_argument(
        "--mode",
        choices=["auto", "voice", "text"],
        help="Interaction mode override",
    )
    parser.add_argument(
        "--no-tts",
        action="store_true",
        help="Disable text-to-speech output",
    )
    parser.add_argument(
        "--once",
        type=str,
        help="Run a single prompt and exit",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    workspace_root = Path(__file__).resolve().parent.parent
    config = MirosConfig.from_env(workspace_root=workspace_root)

    if args.mode:
        config.input_mode = args.mode
    if args.no_tts:
        config.enable_tts = False

    configure_logging(config.log_level, logs_dir=config.data_dir / "logs")
    assistant = MirosAssistantService(config)

    if args.once:
        assistant.run_once(args.once)
        return

    assistant.run_forever()


if __name__ == "__main__":
    main()

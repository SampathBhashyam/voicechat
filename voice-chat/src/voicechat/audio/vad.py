from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VADGate:
    """Simple energy gate placeholder for v1 mock orchestration tests."""

    energy_threshold: float = 0.02

    def is_speech(self, pcm_float32: list[float]) -> bool:
        if not pcm_float32:
            return False
        avg = sum(abs(s) for s in pcm_float32) / len(pcm_float32)
        return avg >= self.energy_threshold

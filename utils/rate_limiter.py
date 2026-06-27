import time
import threading
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clients: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            timestamps = self._clients[client_id]
            timestamps[:] = [t for t in timestamps if t > cutoff]

            if len(timestamps) >= self.max_requests:
                return False

            timestamps.append(now)
            return True

    def get_remaining(self, client_id: str) -> int:
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            timestamps = self._clients[client_id]
            timestamps[:] = [t for t in timestamps if t > cutoff]
            remaining = self.max_requests - len(timestamps)

        return max(remaining, 0)

    def get_reset_time(self, client_id: str) -> float:
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            timestamps = self._clients[client_id]
            timestamps[:] = [t for t in timestamps if t > cutoff]

            if not timestamps:
                return 0

            oldest = min(timestamps)
            reset_in = self.window_seconds - (now - oldest)

        return max(reset_in, 0)

    def reset(self, client_id: str | None = None) -> None:
        with self._lock:
            if client_id:
                self._clients.pop(client_id, None)
            else:
                self._clients.clear()

    def cleanup(self) -> None:
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            expired = [
                cid
                for cid, timestamps in self._clients.items()
                if all(t <= cutoff for t in timestamps)
            ]
            for cid in expired:
                del self._clients[cid]

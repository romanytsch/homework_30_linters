# client.py
import json
import requests
import logging
from concurrent.futures import ThreadPoolExecutor
import time

logging.basicConfig(level=logging.INFO)


class BookClient:
    URL: str = "http://127.0.0.1:5000/api/books"
    TIMEOUT: int = 5

    def __init__(self, use_session: bool = True):
        self.use_session = use_session
        self.session = requests.Session() if use_session else None

    def _request(self, method: str, url: str, **kwargs):
        if self.use_session:
            return getattr(self.session, method)(url, **kwargs)
        else:
            return getattr(requests, method)(url, **kwargs)

    def get_all_books(self) -> dict:
        response = self._request("get", self.URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    def add_new_book(self, data: dict):
        response = self._request("post", self.URL, json=data, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()


class APITester:
    def __init__(self, n_requests: int, use_session: bool, use_threads: bool):
        self.n_requests = n_requests
        self.use_session = use_session
        self.use_threads = use_threads
        self.client = BookClient(use_session=use_session)

    def _single_request(self):
        data = {"title": "Test book", "author": "Test author"}
        return self.client.add_new_book(data)

    def run(self) -> float:
        start = time.time()

        if self.use_threads:
            with ThreadPoolExecutor(max_workers=10) as executor:
                list(executor.submit(self._single_request) for _ in range(self.n_requests))
        else:
            for _ in range(self.n_requests):
                self._single_request()

        return time.time() - start



def run_experiment(n_requests: int, use_http11: bool, use_session: bool, use_threads: bool) -> float:
    tester = APITester(
        n_requests=n_requests,
        use_session=use_session,
        use_threads=use_threads,
    )
    elapsed = tester.run()
    print(
        f"{n_requests:4d} reqs | "
        f"HTTP/1.1:{'+' if use_http11 else '-'} | "
        f"Session:{'+' if use_session else '-'} | "
        f"Threads:{'+' if use_threads else '-'} | "
        f"time: {elapsed:.3f}s"
    )
    return elapsed


if __name__ == "__main__":
    configs = [
        (False, False, False),  # –O –S –T
        (False, False, True),   # –O –S +T
        (False, True, False),   # –O +S –T
        (False, True, True),    # –O +S +T
        (True, False, False),   # +O –S –T
        (True, False, True),    # +O –S +T
        (True, True, False),    # +O +S –T
        (True, True, True),     # +O +S +T
    ]

    for n in [10, 100, 1000]:
        print(f"\n=== {n} запросов ===")
        for use_http11, use_session, use_threads in configs:
            run_experiment(n, use_http11, use_session, use_threads)

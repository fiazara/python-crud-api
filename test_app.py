
import unittest
import json
import threading
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer

import app


class TestCRUDAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        app.DATA_FILE = Path(cls.temp_dir.name) / "messages.json"

        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            app.APIHandler
        )

        cls.port = cls.server.server_address[1]

        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.thread.start()

        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.temp_dir.cleanup()

    def request_api(self, method, path, payload=None):
        data = None

        headers = {}

        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(
            self.base_url + path,
            data=data,
            headers=headers,
            method=method
        )

        try:
            response = urlopen(request)
        except HTTPError as error:
            response = error

        body = json.loads(response.read().decode("utf-8"))

        return response.code, body

    def test_health_check(self):
        status, body = self.request_api("GET", "/health")

        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "active")

    def test_post_valid_message(self):
        status, body = self.request_api(
            "POST",
            "/messages",
            {"message": "Automated test message"}
        )

        self.assertEqual(status, 201)
        self.assertEqual(body["status"], "created")

    def test_post_empty_message(self):
        status, body = self.request_api(
            "POST",
            "/messages",
            {"message": "   "}
        )

        self.assertEqual(status, 400)
        self.assertEqual(
            body["error"],
            "message must not be empty"
        )

    def test_post_message_over_500_characters(self):
        status, body = self.request_api(
            "POST",
            "/messages",
            {"message": "A" * 501}
        )

        self.assertEqual(status, 400)
        self.assertEqual(
            body["error"],
            "message must be 500 characters or fewer"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

import json
import time
import unittest
from typing import Any
from unittest.mock import patch

import requests
import responses

from pyensemblrest import (
    EnsemblRest,
    EnsemblRestBadRequestError,
    EnsemblRestError,
    EnsemblRestNotFoundError,
    EnsemblRestRateLimitError,
    EnsemblRestServiceUnavailable,
)
from pyensemblrest.ensembl_config import (
    ensembl_api_table,
    ensembl_default_url,
    ensembl_user_agent,
)


class TestEnsemblRestUnit(unittest.TestCase):
    """Offline unit tests for EnsemblRest client with 100% mocked network calls."""

    def setUp(self) -> None:
        self.ens = EnsemblRest()

    def tearDown(self) -> None:
        self.ens.close()

    # 1. Initialization and Session Management
    def test_init_defaults(self) -> None:
        """Test client initialization with default configuration."""
        client = EnsemblRest()
        self.assertEqual(client.base_url, ensembl_default_url)
        self.assertEqual(client.timeout, 60)
        self.assertEqual(client.max_attempts, 5)
        self.assertEqual(client.reqs_per_sec, 15)
        self.assertEqual(client.wall_time, 1.0)
        self.assertEqual(client.session.headers.get("User-Agent"), ensembl_user_agent)
        self.assertEqual(client.session.headers.get("Content-Type"), "application/json")
        self.assertEqual(client.get_user_agent(), ensembl_user_agent)
        client.close()

    def test_init_custom_args(self) -> None:
        """Test client initialization with custom parameters."""
        custom_headers = {"User-Agent": "CustomApp/1.0", "X-Custom": "Test"}
        client = EnsemblRest(
            base_url="https://custom.rest.org/",
            timeout=30,
            max_attempts=3,
            reqs_per_sec=10,
            wall_time=2.0,
            headers=custom_headers,
        )
        self.assertEqual(client.base_url, "https://custom.rest.org/")
        self.assertEqual(client.timeout, 30)
        self.assertEqual(client.max_attempts, 3)
        self.assertEqual(client.reqs_per_sec, 10)
        self.assertEqual(client.wall_time, 2.0)
        self.assertEqual(client.session.headers.get("User-Agent"), "CustomApp/1.0")
        self.assertEqual(client.session.headers.get("X-Custom"), "Test")
        client.close()

    def test_context_manager(self) -> None:
        """Test context manager __enter__ and __exit__ behavior."""
        with EnsemblRest() as client:
            self.assertIsInstance(client, EnsemblRest)
            self.assertIsNotNone(client.session)

    def test_dynamic_methods_registration(self) -> None:
        """Test that all 106 API methods are registered and listed in dir()."""
        dir_methods = dir(self.ens)
        for method_name in ensembl_api_table:
            self.assertTrue(
                hasattr(self.ens, method_name), f"Missing method: {method_name}"
            )
            self.assertIn(method_name, dir_methods)
            method = getattr(self.ens, method_name)
            self.assertTrue(callable(method))
            self.assertEqual(method.__name__, method_name)

    def test_getattr_fallback(self) -> None:
        """Test __getattr__ fallback for non-existent attributes."""
        with self.assertRaises(AttributeError):
            _ = self.ens.non_existent_method_xyz

    # 2. Parameter Validation and URL Resolution
    def test_missing_mandatory_parameter(self) -> None:
        """Test that missing mandatory URL parameters raise ValueError."""
        with self.assertRaisesRegex(Exception, "mandatory param 'id' not specified"):
            self.ens.getArchiveById()

    def test_mandatory_parameter_with_digit_zero(self) -> None:
        """Test regex handles parameters containing digit 0."""
        custom_table = {
            "testMethod": {
                "url": "/test/{{id0}}/{{param_0}}",
                "method": "GET",
                "content_type": "application/json",
            }
        }
        client = EnsemblRest(api_table=custom_table)
        with self.assertRaisesRegex(Exception, "mandatory param 'id0' not specified"):
            client.testMethod(param_0="val0")
        client.close()

    def test_url_path_quoting(self) -> None:
        """Test URL path interpolation properly quotes characters while preserving colons."""
        resolved = self.ens._resolve_url(
            "/sequence/region/{{species}}/{{region}}",
            {"species": "homo sapiens", "region": "X:1000..2000:1"},
        )
        self.assertEqual(
            resolved,
            f"{ensembl_default_url}/sequence/region/homo%20sapiens/X:1000..2000:1",
        )

    def test_base_url_slash_handling(self) -> None:
        """Test that trailing slashes on base_url do not produce double slashes."""
        client = EnsemblRest(base_url="https://rest.ensembl.org/")
        resolved = client._resolve_url("/archive/id/{{id}}", {"id": "ENSG001"})
        self.assertEqual(resolved, "https://rest.ensembl.org/archive/id/ENSG001")
        client.close()

    # 3. HTTP Methods, Payload and Query Parameters
    @responses.activate
    def test_get_request_json(self) -> None:
        """Test successful GET request parsing JSON response."""
        url = f"{ensembl_default_url}/archive/id/ENSG00000157764"
        responses.add(
            responses.GET,
            url,
            json={"id": "ENSG00000157764", "latest": "ENSG00000157764.14"},
            status=200,
            content_type="application/json",
        )

        res = self.ens.getArchiveById(id="ENSG00000157764")
        self.assertEqual(res["id"], "ENSG00000157764")
        self.assertEqual(res["latest"], "ENSG00000157764.14")

    @responses.activate
    def test_get_request_plain_text(self) -> None:
        """Test GET request with non-JSON content type returns raw string."""
        url = f"{ensembl_default_url}/sequence/id/ENSG00000157764"
        responses.add(
            responses.GET,
            url,
            body=">ENSG00000157764\nATGCATGC",
            status=200,
            content_type="text/x-fasta",
        )

        res = self.ens.getSequenceById(
            id="ENSG00000157764", content_type="text/x-fasta"
        )
        self.assertEqual(res, ">ENSG00000157764\nATGCATGC")

    @responses.activate
    def test_post_request_with_body_and_params(self) -> None:
        """Test POST request separates post_parameters into JSON body and other kwargs into query params."""
        url = f"{ensembl_default_url}/lookup/id"
        responses.add(
            responses.POST,
            url,
            json={
                "ENSG00000157764": {"id": "ENSG00000157764"},
                "ENSG00000248378": {"id": "ENSG00000248378"},
            },
            status=200,
            content_type="application/json",
        )

        res = self.ens.getLookupByMultipleIds(
            ids=["ENSG00000157764", "ENSG00000248378"], expand=1
        )
        self.assertIn("ENSG00000157764", res)

        # Inspect request
        self.assertEqual(len(responses.calls), 1)
        req = responses.calls[0].request
        self.assertEqual(
            json.loads(req.body), {"ids": ["ENSG00000157764", "ENSG00000248378"]}
        )
        self.assertIn("expand=1", req.url)

    # 4. Rate Limiting Logic
    def test_sliding_window_rate_limiter(self) -> None:
        """Test that rate limiter records request timestamps and purges expired ones."""
        client = EnsemblRest(reqs_per_sec=5, wall_time=0.1)

        # Simulate 5 fast calls
        for _ in range(5):
            client._wait_for_rate_limit()

        self.assertEqual(len(client._request_timestamps), 5)
        self.assertEqual(client.req_count, 5)

        # Wait for window to expire
        time.sleep(0.12)
        client._wait_for_rate_limit()
        # Old timestamps purged, now should only have 1 active timestamp
        self.assertEqual(len(client._request_timestamps), 1)
        client.close()

    # 5. Header Parsing and Rate Limit Metadata
    @responses.activate
    def test_rate_limit_headers_extraction(self) -> None:
        """Test extraction of X-RateLimit-* and Retry-After headers."""
        url = f"{ensembl_default_url}/info/ping"
        headers = {
            "X-RateLimit-Reset": "45",
            "X-RateLimit-Period": "3600",
            "X-RateLimit-Limit": "55000",
            "X-RateLimit-Remaining": "54990",
            "Retry-After": "12.5",
        }
        responses.add(
            responses.GET,
            url,
            json={"ping": 1},
            status=200,
            headers=headers,
        )

        res = self.ens.getInfoPing()
        self.assertEqual(res, {"ping": 1})
        self.assertEqual(self.ens.rate_reset, 45)
        self.assertEqual(self.ens.rate_period, 3600)
        self.assertEqual(self.ens.rate_limit, 55000)
        self.assertEqual(self.ens.rate_remaining, 54990)
        self.assertEqual(self.ens.retry_after, 12.5)

    # 6. Error Handling and Exceptions
    @responses.activate
    def test_bad_request_json_error(self) -> None:
        """Test HTTP 400 with JSON error message raises EnsemblRestBadRequestError."""
        url = f"{ensembl_default_url}/archive/id/INVALID_ID"
        responses.add(
            responses.GET,
            url,
            json={"error": "ID 'INVALID_ID' not found"},
            status=400,
        )

        with self.assertRaises(EnsemblRestBadRequestError) as ctx:
            self.ens.getArchiveById(id="INVALID_ID")

        self.assertIn("400 (Bad Request)", str(ctx.exception))
        self.assertIn("ID 'INVALID_ID' not found", str(ctx.exception))
        self.assertEqual(ctx.exception.error_code, 400)
        self.assertEqual(ctx.exception.msg, ctx.exception.args[0])

    @responses.activate
    def test_bad_request_html_error_safe_json(self) -> None:
        """Test HTTP 400 with HTML/plain-text error safely raises without JSONDecodeError."""
        url = f"{ensembl_default_url}/archive/id/INVALID_ID"
        responses.add(
            responses.GET,
            url,
            body="<html><body>Bad Request</body></html>",
            status=400,
        )

        with self.assertRaises(EnsemblRestBadRequestError) as ctx:
            self.ens.getArchiveById(id="INVALID_ID")

        self.assertIn("400 (Bad Request)", str(ctx.exception))
        self.assertEqual(ctx.exception.error_code, 400)

    @responses.activate
    def test_not_found_error(self) -> None:
        """Test HTTP 404 raises EnsemblRestNotFoundError."""
        url = f"{ensembl_default_url}/archive/id/NOT_FOUND"
        responses.add(
            responses.GET,
            url,
            status=404,
        )

        with self.assertRaises(EnsemblRestNotFoundError) as ctx:
            self.ens.getArchiveById(id="NOT_FOUND")

        self.assertIn("404 (Not Found)", str(ctx.exception))
        self.assertEqual(ctx.exception.error_code, 404)

    @responses.activate
    def test_rate_limit_error_int_and_float_retry_after(self) -> None:
        """Test HTTP 429 raises EnsemblRestRateLimitError with formatted retry seconds."""
        url = f"{ensembl_default_url}/info/ping"
        responses.add(
            responses.GET,
            url,
            status=429,
            headers={"Retry-After": "40"},
        )

        with self.assertRaises(EnsemblRestRateLimitError) as ctx:
            self.ens.getInfoPing()

        self.assertIn("429 (Too Many Requests)", str(ctx.exception))
        self.assertIn("Retry after 40 seconds", str(ctx.exception))
        self.assertEqual(ctx.exception.retry_after, 40.0)

    @responses.activate
    def test_service_unavailable_error(self) -> None:
        """Test HTTP 503 raises EnsemblRestServiceUnavailable."""
        url = f"{ensembl_default_url}/info/ping"
        responses.add(
            responses.GET,
            url,
            status=503,
        )

        with self.assertRaises(EnsemblRestServiceUnavailable) as ctx:
            self.ens.getInfoPing()

        self.assertIn("503 (Service Unavailable)", str(ctx.exception))
        self.assertEqual(ctx.exception.error_code, 503)

    @responses.activate
    def test_connection_error_raises_service_unavailable(self) -> None:
        """Test network connection error raises EnsemblRestServiceUnavailable."""
        url = f"{ensembl_default_url}/info/ping"
        responses.add_callback(
            responses.GET,
            url,
            callback=lambda req: (_ for _ in ()).throw(
                requests.ConnectionError("Failed to connect")
            ),
        )

        with self.assertRaises(EnsemblRestServiceUnavailable):
            self.ens.getInfoPing()

    @responses.activate
    @patch("time.sleep", return_value=None)
    def test_retry_on_500_success(self, mock_sleep: Any) -> None:
        """Test automatic retry on transient HTTP 500 error succeeding on 2nd attempt."""
        url = f"{ensembl_default_url}/archive/id/ENSG00000157764"
        responses.add(responses.GET, url, status=500)
        responses.add(
            responses.GET,
            url,
            json={"id": "ENSG00000157764", "latest": "ENSG00000157764.14"},
            status=200,
        )

        res = self.ens.getArchiveById(id="ENSG00000157764")
        self.assertEqual(res["id"], "ENSG00000157764")
        self.assertEqual(len(responses.calls), 2)
        mock_sleep.assert_called_once()

    @responses.activate
    @patch("time.sleep", return_value=None)
    def test_retry_max_attempts_exceeded(self, mock_sleep: Any) -> None:
        """Test persistent HTTP 500 error raises EnsemblRestError after max retries."""
        self.ens.max_attempts = 2
        url = f"{ensembl_default_url}/archive/id/ENSG00000157764"
        for _ in range(3):
            responses.add(responses.GET, url, status=500)

        with self.assertRaisesRegex(
            EnsemblRestError, "Max number of retries attempts reached"
        ):
            self.ens.getArchiveById(id="ENSG00000157764")

        self.assertEqual(len(responses.calls), 3)

    @responses.activate
    @patch("time.sleep", return_value=None)
    def test_known_error_retry(self, mock_sleep: Any) -> None:
        """Test automatic retry on Ensembl known error strings in HTTP 400."""
        url = f"{ensembl_default_url}/archive/id/ENSG00000157764"
        responses.add(
            responses.GET,
            url,
            json={"error": "something bad has happened"},
            status=400,
        )
        responses.add(
            responses.GET,
            url,
            json={"id": "ENSG00000157764", "latest": "ENSG00000157764.14"},
            status=200,
        )

        res = self.ens.getArchiveById(id="ENSG00000157764")
        self.assertEqual(res["id"], "ENSG00000157764")
        self.assertEqual(len(responses.calls), 2)

    def test_fake_response_object(self) -> None:
        """Test FakeResponse object creation and properties."""
        from pyensemblrest.ensemblrest import FakeResponse

        fake = FakeResponse(headers={"X-Test": "1"}, status_code=400, text="error")
        self.assertEqual(fake.status_code, 400)
        self.assertEqual(fake.text, "error")
        self.assertEqual(fake.headers["X-Test"], "1")

    def test_getattr_dynamic_resolution(self) -> None:
        """Test resolving an API method dynamically through __getattr__."""
        client = EnsemblRest()
        # Remove getArchiveById from __dict__ to force __getattr__ resolution
        client.__dict__.pop("getArchiveById", None)
        method = client.getArchiveById
        self.assertTrue(callable(method))
        self.assertEqual(method.__name__, "getArchiveById")
        client.close()

    @patch("requests.Session.get", side_effect=requests.Timeout("Connection timed out"))
    @patch("time.sleep", return_value=None)
    def test_timeout_retry_and_error(self, mock_sleep: Any, mock_get: Any) -> None:
        """Test that requests.Timeout is handled, retried, and raises EnsemblRestError."""
        client = EnsemblRest(max_attempts=2)
        with self.assertRaisesRegex(
            EnsemblRestError, "Max number of retries attempts reached.*timeout"
        ):
            client.getArchiveById(id="ENSG00000157764")
        client.close()


if __name__ == "__main__":
    unittest.main()

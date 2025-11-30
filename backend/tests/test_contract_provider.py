from pathlib import Path
from pact import Verifier
import unittest


class TestProviderPacts(unittest.TestCase):
    def test_provider_against_consumer_contracts(self):
        pact_file = str(Path(__file__).parent.parent.parent / "pacts" / "frontend-backend.json")
        verifier = (
            Verifier("backend")
            .add_source(pact_file)
            .add_transport(url="http://localhost:8080")
        )
        verifier.verify()
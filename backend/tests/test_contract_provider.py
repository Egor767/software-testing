from pact import Verifier
import unittest


class TestProviderPacts(unittest.TestCase):
    def test_provider_against_consumer_contracts(self):
        verifier = (
            Verifier("my-provider")
            .add_source("./pacts/")
            .add_transport(url="http://localhost:8080")
        )

        verifier.verify()

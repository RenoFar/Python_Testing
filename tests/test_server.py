import server
import pytest


class TestEmail:
    """
        Entering a unknown email crashes the app
    """
    @classmethod
    def setup_class(cls):
        """
             setup variable of the class
        """
        cls.client_test = server.app.test_client()
        cls.clubs_test = server.clubs

    def test_known_email(self):
        """
            testing a known email
        """
        result = self.client_test.post(
            '/showSummary', data={'email': "kate@shelifts.co.uk"}
        )
        assert result.status_code in [200]
        assert self.clubs_test[2]['email'] == "kate@shelifts.co.uk"

    def test_unknown_email(self):
        """
            testing a unknown email
        """
        result = self.client_test.post(
            '/showSummary', data={'email': "john@doe.com"}
        )
        assert result.status_code in [403]
        assert self.clubs_test.get("john@doe.com")

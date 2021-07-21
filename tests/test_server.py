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


class TestPoints:
    """
        Clubs should not be able to use more than their points allowed
    """

    @classmethod
    def setup_class(cls):
        """
             setup variable of the class
        """
        cls.client_test = server.app.test_client()
        cls.clubs_test = server.clubs
        cls.competitions_test = server.competitions

    def test_enough_point(self):
        """
            testing club using its points allowed
        """
        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": int(self.clubs_test[0]["points"]) - 1,
                "club": self.clubs_test[0]["name"],
                "competition": self.competitions_test[0]["name"]}
        )
        assert result.status_code in [200]

    def test_not_enough_point(self):
        """
            testing club using not allowed points
        """
        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": int(self.clubs_test[0]["points"]) + 1,
                "club": self.clubs_test[0]["name"],
                "competition": self.competitions_test[0]["name"]}
        )
        assert result.status_code in [403]


class TestPlacesNumber:
    """
        Clubs shouldn't be able to book more than 12 places per competition
    """

    @classmethod
    def setup_class(cls):
        """
             setup variable of the class
        """
        cls.client_test = server.app.test_client()
        cls.clubs_test = server.clubs
        cls.competitions_test = server.competitions

    def test_book_twelve(self):
        """
            testing to book 12 places per competition
        """
        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": 12,
                "club": self.clubs_test[2]["name"],
                "competition": self.competitions_test[0]["name"]}
        )
        assert result.status_code in [200]

    def test_more_than_twelve(self):
        """
            testing to book more than 12 places per competition
        """
        # reinitialisation of  the value
        self.clubs_test[2]["points"] = server.clubs[2]["points"]

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": 13,
                "club": self.clubs_test[2]["name"],
                "competition": self.competitions_test[0]["name"]}
        )
        assert result.status_code in [403]


class TestPastCompetition:
    """
        Clubs shouldn't be able to Booking places in past competitions
    """

    @classmethod
    def setup_class(cls):
        """
             setup variable of the class
        """
        cls.client_test = server.app.test_client()
        cls.clubs_test = server.clubs
        cls.competitions_test = server.competitions
        # adding a future competition test
        cls.competitions_test.append(
            {"name": "Test competition",
             "date": "2024-07-21 09:00:00",
             "numberOfPlaces": 21,
             }
        )

    def test_past_competition(self):
        """
            testing to book a past competition
        """
        result = self.client_test.get(
            "/book/" + self.competitions_test[0]['name']
            + "/" + self.clubs_test[0]['name']
        )
        assert result.status_code in [302]

    def test_future_competition(self):
        """
            testing to book a future competition
        """
        result = self.client_test.get(
            "/book/" + self.competitions_test[2]['name']
            + "/" + self.clubs_test[0]['name']
        )
        assert result.status_code in [200]

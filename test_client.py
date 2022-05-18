from pytest import raises
import client_tunnel as ct


class TestClient(object):
    def test_sanity(self):
        assert 0 == 0

    def test_constructor_correct(self):
        assert ct.Client(ct.Host("", 1), ct.Host("", 2))


class TestHost(object):
    def test_sanity(self):
        assert True

    def test_constructor_port_exceptions(self):
        with raises(ct.PortNumberException):
            ct.Host("some IP", "some port")
        with raises(Exception):
            ct.Host(30, [111, 122])
        with raises(ct.PortNumberException):
            ct.Host("some IP", "69000")

    def test_constractor_correct(self):
        assert ct.Host("some IP", "5000")

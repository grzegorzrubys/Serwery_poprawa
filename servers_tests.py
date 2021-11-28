import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)

class ProductTest(unittest.TestCase):

    def test_wrong_name(self):
        with self.assertRaises(ValueError):
            products = [Product('P', 4), Product('123', 2), Product('PP132', 9), Product('PP321', 5)]


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P7', 1), Product('PP234', 2), Product('P', 1), Product('PPP345', 4)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_exceptions_was_raised(self):
        products = [Product('PP12', 8), Product('PP123', 3), Product('PP132', 9), Product('PP321', 5)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(2)



class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3), Product('PPP345', 4)]
        products2 = [Product('P234', 2), Product('P235', 3), Product('PPP345', 4)]
        for server_type in server_types:
            server = server_type(products)
            server2 = server_type(products2)
            client = Client(server)
            client2 = Client(server2)
            self.assertEqual(5, client.get_total_price(2))
            self.assertEqual(0, client2.get_total_price(2))


if __name__ == '__main__':
    unittest.main()
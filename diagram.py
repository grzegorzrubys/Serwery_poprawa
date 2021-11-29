#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import re


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float) -> None:
        name_pattern = re.compile("^[a-zA-Z]{1,}\\d{1,}$")
        if name_pattern.match(name) and price >= 0:
            self.name = name
            self.price = price
        else:
            raise ValueError('The product\'s name or price is incorrect')

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.price == other.price  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    def __init__(self, msg=None) -> None:
        if msg is None:
            msg = 'Too many products found.'
        super().__init__(msg)
        self.msg = msg


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania
class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        pattern = '^[a-zA-Z]{{{n_letters}}}\\d{{2,3}}$'.format(n_letters=n_letters)
        entries = [p for p in self.get_all_products()
                   if re.match(pattern, p.name)]
        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(entries, key=lambda entr: entr.price)

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        raise NotImplementedError


class ListServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products = products

    def get_all_products(self) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: Dict[str, Product] = {i.name: i for i in products}

    def get_all_products(self) -> List[Product]:
        return list(self.products.values())


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server) -> None:
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            res = self.server.get_entries(n_letters)
            total_price = 0
            if res is not None:
                for i in res:
                    total_price += i.price
                return total_price
            else:
                return None
        except TooManyProductsFoundError:
            return None


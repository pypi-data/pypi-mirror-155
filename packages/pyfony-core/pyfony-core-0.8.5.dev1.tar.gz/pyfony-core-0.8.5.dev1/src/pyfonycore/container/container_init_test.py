import unittest
from injecta.mocks.Bar import Bar
from injecta.mocks.Foo import Foo
from pyfonycore.bootstrap import bootstrapped_container


class container_init_test(unittest.TestCase):  # noqa: N801
    def test_basic(self):
        container = bootstrapped_container.init("test")

        foo = container.get(Foo)
        bar = container.get("injecta.mocks.Bar")

        self.assertIsInstance(foo, Foo)
        self.assertIsInstance(bar, Bar)


if __name__ == "__main__":
    unittest.main()

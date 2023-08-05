import unittest
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.mocks.Bar import Bar
from injecta.mocks.Foo import Foo
from injecta.package.path_resolver import resolve_path
from pyfonycore.Kernel import Kernel


class KernelTest(unittest.TestCase):
    def test_basic(self):
        kernel = Kernel("test", resolve_path("pyfonycore") + "/_config", YamlConfigReader())

        container = kernel.init_container()

        foo = container.get(Foo)
        bar = container.get("injecta.mocks.Bar")

        self.assertIsInstance(foo, Foo)
        self.assertIsInstance(bar, Bar)


if __name__ == "__main__":
    unittest.main()

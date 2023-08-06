import pytest_spec2md.plugin


class A1:
    class B1:
        def func(self):
            pass


class A2:
    def func(self):
        pass


class TestGetParent:

    def test_function_with_class_returns_class(self):
        f = A2.func

        p = pytest_spec2md.plugin.get_parent(f)
        assert p == A2

    def test_two_layers_can_be_walked(self):
        f = A1.B1.func

        p = pytest_spec2md.plugin.get_parent(
            pytest_spec2md.plugin.get_parent(f)
        )
        assert p == A1

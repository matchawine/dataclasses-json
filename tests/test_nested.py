from tests.entities import (DataClassWithDataClass,
                            DataClassWithList,
                            DataClassX,
                            DataClassXs)


class TestEncoder:
    def test_nested_dataclass(self):
        assert (DataClassWithDataClass(DataClassWithList([1])).to_json() ==
                '{"dc_with_list": {"xs": [1]}}')

    def test_nested_list_of_dataclasses(self):
        assert (DataClassXs([DataClassX(0), DataClassX(1)]).to_json() ==
                '{"xs": [{"x": 0}, {"x": 1}]}')


class TestDecoder:
    def test_nested_dataclass(self):
        assert (DataClassWithDataClass.from_json(
            '{"dc_with_list": {"xs": [1]}}') ==
                DataClassWithDataClass(DataClassWithList([1])))

    def test_nested_list_of_dataclasses(self):
        assert (DataClassXs.from_json('{"xs": [{"x": 0}, {"x": 1}]}') ==
                DataClassXs([DataClassX(0), DataClassX(1)]))

    def test_wrong_nested_list_of_dataclasses(self):
        try:
            _ = DataClassX.from_json('{"a": "incorrect_field"}')
            x_error = None
        except Exception as e:
            x_error = e
        assert x_error is not None

        try:
            _ = DataClassXs.from_json('{"xs": [{"a": "incorrect_field"}]}')
            xs_error = None
        except Exception as e:
            xs_error = e
        assert xs_error is not None
        assert x_error.__class__ == xs_error.__class__
        assert x_error.args == xs_error.args

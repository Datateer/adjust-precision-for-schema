from decimal import Decimal
import decimal
from jsonschema import Draft4Validator
import pytest

from adjust_precision_for_schema import adjust_decimal_precision_for_schema, calc_digits


def test_precision_failure():
    """This test reproduces what happens inside of jsonschema's Draft4Validator when
    precision is high, like from PostgresSQL or MongoDB"""
    d1 = Decimal("1.0")
    d2 = Decimal("1E-34")

    # assert the exception is raised
    with pytest.raises(decimal.DecimalException) as ex:
        d1 % d2
    assert isinstance(ex.value, decimal.DecimalException)
    digits = calc_digits(d2)
    assert digits == 34
    assert decimal.getcontext().prec < digits


def test_changes_decimal_context_to_handle_high_precision():
    precision_under_test = 1e-34
    assert decimal.getcontext().prec < calc_digits(precision_under_test)
    schema = {
        "type": "object",
        "properties": {
            "_id": {"type": "string"},
            "bathrooms": {"type": "number", "multipleOf": precision_under_test},
        },
    }

    with decimal.localcontext() as ctx:
        adjust_decimal_precision_for_schema(schema, context=ctx)
        assert ctx.prec == calc_digits(precision_under_test)


def test_validates_after_walking_schema():
    precision_under_test = 1e-34
    assert decimal.getcontext().prec < calc_digits(precision_under_test)
    schema = {
        "type": "object",
        "properties": {
            "_id": {"type": "string"},
            "bathrooms": {"type": "number", "multipleOf": precision_under_test},
        },
    }

    record = {"_id": "asdf", "bathrooms": 1.0}
    with decimal.localcontext() as ctx:
        adjust_decimal_precision_for_schema(schema, ctx)
        validator = Draft4Validator(schema)
        validator.validate(record)

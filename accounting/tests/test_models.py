import pytest
from accounting.models import Price


@pytest.mark.django_db(reset_sequences=True)
def test_accounting_model():
    """test that the accounting model records the product information in the database"""
    price = Price.objects.create(
               session_type="session test",
               price=45)
    expected_value = "session test"
    assert str(price) == expected_value

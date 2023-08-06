from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.exceptions import ResourceNotFound
from odoo_somconnexio_python_client.resources.contract import Contract


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the API-KEY request header with "DUMMY" in cassettes
        "filter_headers": [("API-KEY", "DUMMY")],
    }


class ContractTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search_resource_not_found(self):
        self.assertRaises(ResourceNotFound,
                          Contract.search_by_customer_vat,
                          vat="ES3208282S")

    @pytest.mark.vcr()
    def test_search_contract_by_vat(self):
        contracts = Contract.search_by_customer_vat(vat="ES55642302N")
        first_contract = contracts[0]
        second_contract = contracts[1]

        assert first_contract.code == "34636"
        assert first_contract.customer_vat == "ES55642302N"
        assert first_contract.phone_number == "879786754"
        assert first_contract.current_tariff_product == "SE_SC_REC_BA_F_100"

        assert second_contract.code == "78979"
        assert second_contract.customer_vat == "ES55642302N"
        assert second_contract.phone_number == "676858494"
        assert second_contract.current_tariff_product == "SE_SC_REC_MOBILE_T_150_1024"

    @pytest.mark.vcr()
    def test_search_contract_by_phone_number(self):
        contracts = Contract.search_by_phone_number(phone_number="676858494")
        contract = contracts[0]

        assert contract.code == "78979"
        assert contract.customer_vat == "ES55642302N"
        assert contract.phone_number == "676858494"
        assert contract.current_tariff_product == "SE_SC_REC_MOBILE_T_150_1024"

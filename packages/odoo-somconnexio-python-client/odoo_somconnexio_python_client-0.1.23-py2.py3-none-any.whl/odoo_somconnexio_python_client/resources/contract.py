from odoo_somconnexio_python_client.client import Client

from ..exceptions import ResourceNotFound


class Contract:
    _url_path = "/contract"

    # TODO: Add all the needed fields in the future...
    def __init__(
        self,
        id,
        code,
        customer_firstname,
        customer_lastname,
        customer_ref,
        customer_vat,
        phone_number,
        current_tariff_product,
        technology,
        supplier,
        iban,
        ticket_number,
        date_start,
        date_end,
        is_terminated,
        **kwargs
    ):
        self.id = id
        self.code = code
        self.customer_firstname = customer_firstname
        self.customer_lastname = customer_lastname
        self.customer_ref = customer_ref
        self.customer_vat = customer_vat
        self.phone_number = phone_number
        self.current_tariff_product = current_tariff_product
        self.technology = technology
        self.supplier = supplier
        self.iban = iban
        self.ticket_number = ticket_number
        self.date_start = date_start
        self.date_end = date_end
        self.is_terminated = is_terminated

    @classmethod
    def search_by_customer_vat(cls, vat):
        """
        Search Contract in Odoo by partner's vat.

        :return: Contract object if exists
        """
        return cls._get(
            params={
                "partner_vat": vat,
            }
        )

    @classmethod
    def search_by_phone_number(cls, phone_number):
        """
        Search Contract in Odoo by phone number.

        :return: Contract object if exists
        """
        return cls._get(
            params={
                "phone_number": phone_number,
            }
        )

    @classmethod
    def _get(cls, id=None, params={}):
        if id:
            url = "{}/{}".format(cls._url_path, id)
        else:
            url = cls._url_path

        response_data = Client().get(
            url,
            params=params,
        )
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter=params)

        return [cls(**contract_found) for contract_found in response_data]

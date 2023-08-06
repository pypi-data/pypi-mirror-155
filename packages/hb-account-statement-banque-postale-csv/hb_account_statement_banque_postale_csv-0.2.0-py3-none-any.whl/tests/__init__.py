try:
    from trytond.modules.hb_account_statement_banque_postale_csv.tests.test_hb_account_statement_banque_postale_csv import suite  # noqa: E501
except ImportError:
    from .test_hb_account_statement_banque_postale_csv import suite

__all__ = ['suite']

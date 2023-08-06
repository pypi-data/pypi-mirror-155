import unittest
import doctest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import doctest_teardown
from trytond.tests.test_tryton import doctest_checker


class HbAccountStatementBanquePostaleCsvTestCase(ModuleTestCase):
    'Test Hb Account Statement Banque Postale Csv module'
    module = 'hb_account_statement_banque_postale_csv'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            HbAccountStatementBanquePostaleCsvTestCase))

    suite.addTests(doctest.DocFileSuite(
            'scenario_account_statement_banque_postale_csv.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite

from trytond.pool import Pool

__all__ = ['register']


from . import account
from . import configuration


def register():
    Pool.register(
        account.StatementImportStart,
        configuration.Configuration,
        configuration.ConfigurationStatemenJournal,
        module='hb_account_statement_banque_postale_csv', type_='model')
    Pool.register(
        account.StatementImport,
        module='hb_account_statement_banque_postale_csv', type_='wizard')
    Pool.register(
        module='hb_account_statement_banque_postale_csv', type_='report')

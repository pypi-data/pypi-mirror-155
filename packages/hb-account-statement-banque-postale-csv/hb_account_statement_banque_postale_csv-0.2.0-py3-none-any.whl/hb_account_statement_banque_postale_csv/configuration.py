from trytond.pool import PoolMeta, Pool
from trytond.model import fields, ModelSQL
from trytond.pyson import Eval
from trytond.modules.company.model import CompanyValueMixin


class Configuration(metaclass=PoolMeta):
    'Statement import for : Banque Postale CSV'
    __name__ = 'account.configuration'

    default_statement_journal_for_bp_csv = fields.MultiValue(fields.Many2One(
        'account.statement.journal',
        "Default journal for the statement of the banque postale",
        domain=[('company', '=', Eval('context', {}).get('company', -1))]))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'default_statement_journal_for_bp_csv':
            return pool.get(
                'account.configuration.default_statement_bp')

        return super(Configuration, cls).multivalue_model(field)


class ConfigurationStatemenJournal(ModelSQL, CompanyValueMixin):
    "Account Configuration Default statement journal for Banque postale"
    __name__ = 'account.configuration.default_statement_bp'
    default_statement_journal_for_bp_csv = fields.Many2One(
        'account.statement.journal',
        "Default journal for the statement of the banque postale",
        domain=[('company', '=', Eval('company', -1))],
        depends=['company'])

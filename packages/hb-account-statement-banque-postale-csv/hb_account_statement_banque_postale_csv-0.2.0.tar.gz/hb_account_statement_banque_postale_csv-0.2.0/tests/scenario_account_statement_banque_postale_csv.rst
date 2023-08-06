=============================================
Account Statement Banque postale CSV Scenario
=============================================

Imports::

    >>> import datetime
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.tools import file_open
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts

Activate modules::

    >>> config = activate_modules('hb_account_statement_banque_postale_csv')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> cash = accounts['cash']

Create parties::

    >>> Party = Model.get('party.party')
    >>> bank_party = Party(name='Bank')
    >>> bank_party.save()

Create Bank Account::

    >>> Bank = Model.get('bank')
    >>> BankAccount = Model.get('bank.account')
    >>> bank = Bank()
    >>> bank.party = bank_party
    >>> bank.save()
    >>> bank_account = BankAccount()
    >>> bank_account.bank = bank
    >>> bank_account.owners.append(Party(company.party.id))
    >>> bank_account.currency = company.currency
    >>> bank_account_number = bank_account.numbers.new()
    >>> bank_account_number.type = 'iban'
    >>> bank_account_number.number = 'ES0600815398730001414452'
    >>> bank_account.save()

Create Account Journal::

    >>> Sequence = Model.get('ir.sequence')
    >>> SequenceType = Model.get('ir.sequence.type')
    >>> AccountJournal = Model.get('account.journal')

    >>> sequence_type, = SequenceType.find([('name', '=', "Account Journal")])
    >>> sequence = Sequence(name='Satement',
    ...     sequence_type=sequence_type,
    ...     company=company,
    ...     )
    >>> sequence.save()
    >>> account_journal = AccountJournal(name='Statement',
    ...     type='statement',
    ...     sequence=sequence,
    ...     )
    >>> account_journal.save()

Create a statement::

    >>> StatementJournal = Model.get('account.statement.journal')
    >>> journal = StatementJournal(name='Number',
    ...     journal=account_journal,
    ...     validation='number_of_lines',
    ...     account=cash,
    ...     bank_account=bank_account,
    ...     )
    >>> journal.save()

Add default journal::

    >>> Configuration = Model.get('account.configuration')
    >>> conf = Configuration(
    ...     default_statement_journal_for_bp_csv=journal,
    ... )
    >>> conf.save()

Import a file::

    >>> Statement = Model.get('account.statement')
    >>> with file_open(
    ...         'hb_account_statement_banque_postale_csv/tests/01.csv',
    ...         mode='rb') as fp:
    ...     csv_file = fp.read()
    >>> wbanquepostale = Wizard('account.statement.import')
    >>> wbanquepostale.form.file_format = 'banque_postale_csv'
    >>> wbanquepostale.form.file_ = csv_file
    >>> wbanquepostale.execute('import_')

Check Statement::

    >>> Statement = Model.get('account.statement')
    >>> statement, = Statement.find([])
    >>> statement.journal == journal
    True
    >>> statement.number_of_lines
    10
    >>> statement.total_amount
    Decimal('-48906.00')
    >>> statement.start_balance
    Decimal('12394584.39')
    >>> statement.end_balance
    Decimal('12345678.39')
    >>> line = statement.lines[0]
    >>> line.date == datetime.date(2021, 1, 29)
    True
    >>> line.amount
    Decimal('-5432.00')

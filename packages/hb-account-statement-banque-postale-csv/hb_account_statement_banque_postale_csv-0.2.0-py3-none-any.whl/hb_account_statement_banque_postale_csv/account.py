from io import BytesIO, TextIOWrapper
import csv
import calendar

from datetime import datetime
from decimal import Decimal as D

from trytond.pool import PoolMeta, Pool


class StatementImportStart(metaclass=PoolMeta):
    __name__ = 'account.statement.import.start'

    @classmethod
    def __setup__(cls):
        super(StatementImportStart, cls).__setup__()
        cls.file_format.selection.append(
            ('banque_postale_csv', "Banque Postale (CSV)"))


class StatementImport(metaclass=PoolMeta):
    __name__ = 'account.statement.import'

    def parse_banque_postale_csv(self, encoding='utf8'):
        with TextIOWrapper(BytesIO(self.start.file_),
                           encoding=encoding) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            bank_statement = {'lines': []}
            row = next(reader)
            while row != []:
                bank_statement[row[0].strip()] = row[1]
                row = next(reader)
            header = next(reader)

            for row in reader:
                bank_statement['lines'].append(dict(zip(header, row)))

        return [self.cast_to_tryton_statement(bank_statement)]

    def cast_to_tryton_statement(self, bank_statement):
        pool = Pool()
        Statement = pool.get('account.statement')
        Configuration = pool.get('account.configuration')

        statement = Statement()

        statement.name = bank_statement['Numéro Compte']
        statement.company = self.start.company

        statement.journal = Configuration(
            1).default_statement_journal_for_bp_csv

        bank_stmt_lines = self.cast_to_tryton_statement_lines(
            statement, bank_statement['lines'])

        bkstmt_date = max([l.date for l in bank_stmt_lines])
        _, last_day = calendar.monthrange(bkstmt_date.year, bkstmt_date.month)
        bkstmt_date = bkstmt_date.replace(day=last_day)
        statement.date = bkstmt_date

        statement.end_balance = bank_statement['Solde (EUROS)'].replace(
            ',', '.')
        statement.start_balance = (
            D(statement.end_balance) - sum(
                [D(l.amount) for l in bank_stmt_lines])
        )
        statement.number_of_lines = len(bank_stmt_lines)
        statement.total_amount = sum([D(l.amount) for l in bank_stmt_lines])
        statement.lines = bank_stmt_lines
        return statement

    def cast_to_tryton_statement_lines(self, statement, stmt_lines):
        return [self.cast_to_tryton_statement_line(statement, stmt_line)
                for stmt_line in stmt_lines]

    def cast_to_tryton_statement_line(self, statement, stmt_line):
        pool = Pool()
        Line = pool.get('account.statement.line')

        line = Line()
        line.number = stmt_line['Libellé']
        line.amount = stmt_line['Montant(EUROS)'].replace(',', '.')
        line.date = datetime.strptime(stmt_line['Date'], '%d/%m/%Y').date()

        if hasattr(line, 'set_account_and_party_from_ml'):
            line.set_account_and_party_from_ml()

        if not hasattr(line, 'account'):
            line.account = statement.journal.account

        return line

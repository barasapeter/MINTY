import string
import users
from typing import Union, Tuple
import database
from custom_modules import customlib
import exceptions
import random

# I did one CRUD here. Apologies
import queries


UserType = Union[users.PayBillServiceMerchant,
                 users.Agent,
                 users.Business,
                 users.PochiLaBiashara,
                 users.Person]


class Transaction:
    def __init__(self, sender: UserType, receiver: UserType,
                 amount: Union[int, float], password: str) -> None:
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.transaction_type = self.get_transaction_type()
        self.transaction_code = self.get_transaction_code()
        self.transaction_cost = self.get_transaction_charge(
            transaction_type=self.transaction_type, amount=self.amount
        )
        self.date_of_transaction = customlib.date_today()
        self.time_of_transaction = customlib.time_now()
        self.password = password

        if self.transaction_cost is None or isinstance(self.transaction_cost, str):
            raise exceptions.TransactionAmountNotWithinRange(
                "TRANSACTION FAILED! Make sure the transaction amount you have entered is within daily allowed range."
            )
        if not self.verify_password():
            raise exceptions.WrongPassword(
                "FAILED! You have entered the wrong password."
            )

    def get_transaction_type(self) -> str:
        """Transaction type is determined by the receiver type"""
        if isinstance(self.receiver, users.Person) and isinstance(self.sender, users.Agent):
            return "DEPOSIT FROM AGENT"

        if isinstance(self.receiver, users.PochiLaBiashara) or isinstance(self.receiver, users.Business) or isinstance(self.receiver, users.PayBillServiceMerchant):
            return "TRANSFER TO M-PESA USERS, POCHI LA BIASHARA AND BUSINESS TILL TO CUSTOMER"

        if isinstance(self.receiver, users.Person):
            return "TRANSFER TO OTHER REGISTERED MOBILE MONEY USERS"

        if isinstance(self.receiver, users.Agent):
            return "WITHDRAWAL FROM M-PESA AGENTS"

        if isinstance(self.receiver, users.Agent):
            return "WITHDRAWAL FROM M-PESA AGENTS"

        raise exceptions.TransactionUndefinedError(
            "The transaction is not defined"
        )

    def get_transaction_charge(self, transaction_type, amount):
        data = {
            "TRANSACTION RANGE (KSHS)": [
                (1, 49), (50, 100), (101, 500), (501, 1000), (1001, 1500),
                (1501, 2500), (2501, 3500), (3501, 5000), (5001, 7500),
                (7501, 10000), (10001, 15000), (15001, 20000), (20001, 35000),
                (35001, 50000), (50001, 150000)
            ],
            "TRANSFER TO M-PESA USERS, POCHI LA BIASHARA AND BUSINESS TILL TO CUSTOMER": [
                (0, 0), (0, 0), (7, 7), (13, 13), (23, 23),
                (33, 33), (53, 53), (57, 57), (78, 78), (90, 90),
                (100, 100), (105, 105), (108, 108), (108, 108), (108, 108)
            ],
            "TRANSFER TO OTHER REGISTERED MOBILE MONEY USERS": [
                (0, 0), (0, 0), (7, 7), (13, 13), (23, 23),
                (33, 33), (53, 53), (57, 57), (78, 78), (90, 90),
                (100, 100), (105, 105), (108, 108), (108, 108), (108, 108)
            ],
            "TRANSFER TO UNREGISTERED USERS": [
                ("N/A", "N/A"), ("N/A", "N/A"), (47, 47), (51, 51), (61, 61),
                (76, 76), (115, 115), (139, 139), (171, 171), (211, 211),
                (273, 273), (296, 296), (318, 318), (318, 318), (318, 318)
            ],
            "WITHDRAWAL FROM M-PESA AGENTS": [
                ("N/A", "N/A"), (11, 11), (29, 29), (29, 29), (29, 29),
                (29, 29), (52, 52), (69, 69), (87, 87), (115, 115),
                (167, 167), (185, 185), (197, 197), (278, 278), (309, 309)
            ]
        }
        if transaction_type == "DEPOSIT FROM AGENT":
            return 0

        for i in range(len(data[transaction_type])):
            range_min, range_max = data["TRANSACTION RANGE (KSHS)"][i]
            if range_min <= amount <= range_max:
                charge = data[transaction_type][i]
                if isinstance(charge, tuple):
                    return charge[0]
                else:
                    return charge
        return None

    def get_transaction_code(self) -> str:
        characters = string.ascii_uppercase + string.ascii_lowercase+string.digits
        return "".join(random.choice(characters) for i in range(50))

    def commit(self) -> None:
        sender_account_balance = self.sender.float_balance if isinstance(
            self.sender, users.Agent) else self.sender.account_balance
        receiver_account_balance = self.receiver.float_balance if isinstance(
            self.receiver, users.Agent) else self.receiver.account_balance
        if sender_account_balance >= self.amount + self.transaction_cost:
            if self.verify_password():
                sender_account_balance -= (self.amount + self.transaction_cost)
                receiver_account_balance += self.amount
                user_type_mapping = {
                    users.Person: {
                        "table": "users",
                        "column": "account_balance",
                        "primary_key": "phone_number"
                    },
                    users.Agent: {
                        "table": "agents",
                        "column": "float_balance",
                        "primary_key": "agent_number"
                    },
                    users.Business: {
                        "table": "businesses",
                        "column": "account_balance",
                        "primary_key": "till_number"
                    },
                    users.PayBillServiceMerchant: {
                        "table": "pay_bill_merchants",
                        "column": "account_balance",
                        "primary_key": "business_number"
                    },
                    users.PochiLaBiashara: {
                        "table": "pochi_la_biashara",
                        "column": "account_balance",
                        "primary_key": "registered_user_phone_number"
                    }
                }
                sender_type_info = user_type_mapping.get(type(self.sender))
                if sender_type_info:
                    senders_table = sender_type_info["table"]
                    senders_column_to_alter = sender_type_info["column"]
                    senders_primary_key_column = sender_type_info["primary_key"]
                    senders_id = getattr(
                        self.sender, senders_primary_key_column)

                receiver_type_info = user_type_mapping.get(type(self.receiver))
                if receiver_type_info:
                    receiver_table = receiver_type_info["table"]
                    receiver_column_to_alter = receiver_type_info["column"]
                    receiver_primary_key_column = receiver_type_info["primary_key"]
                    receiver_id = getattr(
                        self.receiver, receiver_primary_key_column)

                if senders_id == receiver_id:
                    raise exceptions.CrossTransactionError(
                        "This transaction has FAILED. Please send to a second party, cross transaction is not allowed."
                    )
                database.update(senders_table, senders_column_to_alter,
                                sender_account_balance, senders_primary_key_column, senders_id)
                database.update(receiver_table, receiver_column_to_alter,
                                receiver_account_balance, receiver_primary_key_column, receiver_id)

                balance = database.fetch_business("X").account_balance
                balance += self.transaction_cost
                database.update("businesses", "account_balance",
                                balance, "till_number", "X")

                # I had to do a CRUD here to avoid the cross import. Sorry :)
                database.cursor.execute(
                    queries.INSERT_INTO_TRANSACTIONS_QUERY, (self.transaction_code, self.transaction_type, self.amount, self.transaction_cost, self.date_of_transaction, self.time_of_transaction))
                database.cursor.execute(
                    'SELECT transaction_id FROM transactions WHERE transaction_code = "%s"' % self.transaction_code)
                transaction_id = database.cursor.fetchone()[0]
                database.cursor.execute(
                    'INSERT INTO transaction_record VALUES(%s, %s, %s)', (transaction_id, senders_id, receiver_id,))

                # Handle a pay bill service
                if isinstance(self.receiver, users.PayBillServiceMerchant):
                    database.create_new_pay_bill_transaction(
                        users.PayBillAPIDatabase(
                            self.transaction_code, receiver_id, senders_id, self.amount
                        ))
                database.cnx.commit()

            return
        raise exceptions.InsufficientFundsToCompleteTransaction(
            "Transaction has FAILED. You have insufficient funds to complete this transaction. You must "
            "have enough funds as well as transaction cost to perform this transaction. "
            "Your account balance is KSHS%s. Sorry!" % sender_account_balance
        )

    def verify_password(self) -> bool:

        if isinstance(self.sender, users.Person):
            return self.sender.check_password(self.password)

        if isinstance(self.sender, users.Agent):
            return database.fetch_user(self.sender.registered_user).check_password(self.password)

        # Bugs might be below this comment. Take a keen look and fix them
        if isinstance(self.sender, users.Business):
            return database.fetch_user(self.sender.business_owner).check_password(self.password)

        if isinstance(self.sender, users.PayBillServiceMerchant):
            return self.sender.access_Person_attributes.check_password(self.password)


if __name__ == '__main__':
    # try:
    transaction = Transaction(
        sender=database.fetch_agent("00000000"),
        receiver=database.fetch_user('0145543776'),
        amount=10,
        password="@StrongTestPassword123",
    )
    transaction.commit()
    database.cnx.close()
    # except Exception as e:
    #     print(e)

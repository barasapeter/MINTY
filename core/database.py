"""This script is responsible for all users C.R.U.D operations"""
import mysql.connector

import queries as queries
import users

# Establish a database connection
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='quantumsoft'
)

cursor = cnx.cursor()


def configure_database() -> None:
    """Could have as well not wrapped up this piece of code in a function 
    Done this to reuse the functionality in transactionqueries.py"""
    for query in queries.SETUP_QUERIES:
        cursor.execute(query)
        cnx.commit()


configure_database()


# C: Create (C.r.u.d) starts here...
def create_new_agent(agent: users.Agent):
    data = agent.__dict__
    if data['registered_user'] is not None:
        data['registered_user'] = data['registered_user'].phone_number
    else:
        data['registered_user'] = users.SUPERUSER.phone_number
    row = tuple(data.values())
    cursor.execute(queries.INSERT_AGENT_QUERY, row)
    cnx.commit()
    return


def create_new_user(user: users.Person) -> None:
    dictdata = user.__dict__
    dictdata.pop('_salt')
    row = tuple(dictdata.values())
    cursor.execute(queries.INSERT_USER_QUERY, row)
    cnx.commit()
    return


def create_new_business(business: users.Business) -> None:
    data = business.__dict__
    data['business_owner'] = data['business_owner'].phone_number
    row = tuple(data.values())
    cursor.execute(queries.INSERT_NEW_BUSINESS_QUERY, row)
    cnx.commit()
    return


def opt_in_pochi_la_biahara(pochi: users.PochiLaBiashara) -> None:
    row = tuple(pochi.__dict__.values())
    cursor.execute(queries.INSERT_POCHI_LA_BIASHARA_QUERY, row)
    cnx.commit()


def create_new_pay_bill_merchant(pay_bill_merchant: users.PayBillServiceMerchant) -> None:
    # Eliminate the class Person
    row = tuple(list(pay_bill_merchant.__dict__.values())[:-1])
    cursor.execute(queries.INSERT_PAY_BILL_SERVICE_MERCHANTS_QUERY, row)
    cnx.commit()
    return


def create_new_pay_bill_transaction(api_body: users.PayBillAPIDatabase) -> None:
    row = tuple(list(api_body.__dict__.values()))
    cursor.execute(queries.INSERT_PAY_BILL_API_QUERY, row)
    cnx.commit()
# C: Create (C.r.u.d) ends here...


# R: Read (c.R.u.d) starts here...
def fetch_user(phone_number: str) -> users.Person:
    # cursor.execute(queries.FETCH_USER_QUERY, (phone_number,))
    ufetch_q = 'SELECT * FROM users WHERE phone_number = "%s"' % phone_number
    cursor.execute(
        # WARNING: Prone to injection attacks. This is a temporary fix, consider fixing this later
        ufetch_q
    )
    user_data = cursor.fetchone()
    import exceptions
    if not user_data:
        raise exceptions.EmptyQueryResultError(
            "the query '%s' returned nothing" % ufetch_q
        )
    person = users.Person(*user_data, salt=False)
    return person


def fetch_agent(agent_number: str) -> users.Agent:
    # Execute as a tuple to block SQL injection attempts
    cursor.execute(queries.FETCH_AGENT_QUERY, (agent_number,))
    agent_data = cursor.fetchone()
    agent = users.Agent(*agent_data)
    return agent


def fetch_business(till_number: str) -> users.Business:
    # Execute as a tuple to block SQL injection attempts
    cursor.execute(queries.FETCH_BUSINESS_QUERY, (till_number,))
    data = cursor.fetchone()
    return users.Business(*data)


def fetch_pochi_la_biashara(merchant_phone_number: str) -> users.PochiLaBiashara:
    cursor.execute(queries.FETCH_POCHI_LA_BIASHARA_QUERY,
                   (merchant_phone_number,))
    data = cursor.fetchone()
    return users.PochiLaBiashara(*data)


def fetch_pay_bill_merchant(business_number: str) -> users.PayBillServiceMerchant:
    cursor.execute(queries.FETCH_PAY_BILL_SERVICE_MERCHANT_QUERY,
                   (business_number,))
    data = cursor.fetchone()
    return users.PayBillServiceMerchant(*data)


def fetch_pay_bill_api_transaction(transaction_code: str) -> users.PayBillAPIDatabase:
    cursor.execute(queries.FETCH_PAY_BILL_API_QUERY, (transaction_code,))
    data = cursor.fetchone()
    return users.PayBillAPIDatabase(*data)
# R: Read (c.R.u.d) ends here...


# U: Update (c.r.U.d) starts here...
def update(table_name, column_to_alter, new_value, primary_key_column, condition) -> None:
    cursor.execute(
        f"UPDATE `{table_name}` SET `{column_to_alter}` = '{new_value}' WHERE `{primary_key_column}` = '{condition}'"
    )
    cnx.commit()
# U: Update (c.r.U.d) ends here...


# Create superuser and superagents
try:
    create_new_user(users.SUPERUSER)
    create_new_agent(users.SUPERAGENT)
except mysql.connector.errors.IntegrityError:
    pass

if __name__ == '__main__':
    person = fetch_user('test_pass_phone_numbery')
    print(person.__dict__)

cnx.commit()

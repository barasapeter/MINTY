from custom_modules import customlib
from typing import Union
from dataclasses import dataclass
import bcrypt
import re
import exceptions


class Person:
    def __init__(
            self, username: str,
            phone_number: str,
            account_balance: Union[int, float],
            password: str,
            national_identification_number: str,
            address: str,
            date_of_registration: str,
            time_of_registration: str,
            agent_number_of_agent_who_registered: str,
            salt: bool = True) -> None:
        """NOTE: When creating a new user and saving in database set salt=True. When fetching rows and recreating the class object set salt=False"""

        self.username: str = username
        self.phone_number: str = phone_number
        self.account_balance: Union[int, float] = account_balance
        self.password: str = password
        self.national_identification_number: str = national_identification_number
        self.address: str = address
        self.date_of_registration: str = date_of_registration
        self.time_of_registration: str = time_of_registration
        self.agent_number_of_agent_who_registered: str = agent_number_of_agent_who_registered
        self._salt = salt
        if not self.is_strong_password(self.password):
            raise exceptions.WeakPasswordEntered(
                "The password you have entered is too weak. A strong password should contain at least "
                "an uppercase letter, a lowercase letter, a number, a special character and have at least "
                "eight characters long. Please try creating a strong password for security reasons."
            )
        self.set_password(password=password)

    def set_password(self, password: str) -> str:
        """Returns: a hashed password (to be used elsewhere)"""
        if self._salt:
            if self.is_strong_password(password):
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                self.password = hashed_password.decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def is_strong_password(self, password: str) -> bool:
        """At least 8 characters long, contains uppercase, lowercase, and a number"""
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        return bool(re.match(regex, password))

    def change_password(self, initial_password: str, new_password: str) -> bool:
        if self.check_password(initial_password):
            self.set_password(new_password)
            return True
        return False

    def update_account_balance(self, new_balance: Union[int, float]):
        self.account_balance = new_balance


@dataclass
class PochiLaBiashara:
    registered_user_phone_number: str
    account_balance: Union[int, float]


class Agent:
    def __init__(
            self, agent_number: str,
            registered_user: Person,
            agent_name: str,
            float_balance: Union[int, float],
            date_of_creation: str,
            time_of_registration: str,
            agent_number_of_superagent_who_registered: str,
            agent_location: str) -> None:

        self.agent_number = agent_number
        self.registered_user = registered_user
        self.agent_name = agent_name
        self.float_balance = float_balance
        self.date_of_creation = date_of_creation
        self.time_of_registration: str = time_of_registration
        self.agent_number_of_superagent_who_registered: str = agent_number_of_superagent_who_registered
        self.agent_location = agent_location


class Business:
    def __init__(self, till_number: str,
                 business_name: str,
                 business_owner: Person,
                 business_account_balance: Union[int, float],
                 date_of_registration: str,
                 time_of_registration: str,
                 agent_number_of_agent_who_registered: str) -> None:

        self.till_number: str = till_number
        self.business_name: str = business_name
        self.business_owner = business_owner
        self.account_balance: Union[int, float] = business_account_balance
        self.date_of_registration: str = date_of_registration
        self.time_of_registration: str = time_of_registration
        self.agent_number_of_superagent_who_registered: str = agent_number_of_agent_who_registered


class PayBillServiceMerchant:
    def __init__(self, service_name: str,
                 business_number: str,
                 admin_passkey: str,
                 account_balance: Union[int, float]) -> None:
        """
        Since the resulting password is encrypted, we will validate the entered passkey using this method:
        - PayBillService(...).access_Person_attributes.check_password(...)
        """

        self.service_name: str = service_name
        self.business_number: str = business_number
        self.admin_passkey: str = admin_passkey
        self.account_balance: Union[int, float] = account_balance

        # Validate the passkey
        self.access_Person_attributes = Person(password=self.admin_passkey, username=None, phone_number=None, account_balance=None,
                                               national_identification_number=None, address=None, date_of_registration=None, time_of_registration=None, agent_number_of_agent_who_registered=None)
        self.admin_passkey = self.access_Person_attributes.password


@dataclass
class PayBillAPIDatabase:
    transaction_code: str
    business_number: str
    account_number: str
    amount: Union[float, int]


SUPERAGENT = Agent(
    registered_user=None,
    agent_number="00000000",
    agent_name="first_degree_superagent",
    float_balance=0,
    date_of_creation=customlib.date_today(),
    time_of_registration=customlib.time_now(),
    agent_number_of_superagent_who_registered=None,
    agent_location="Eldoret-Kitale Road, Nangili KE"
)


SUPERUSER = Person(
    username="superuser",
    phone_number="0100000000",
    account_balance=0,
    password="@StrongTestPassword123",
    national_identification_number="000000",
    address=None,
    date_of_registration=customlib.date_today(),
    time_of_registration=customlib.time_now(),
    agent_number_of_agent_who_registered=SUPERAGENT.agent_number,
    salt=True
)

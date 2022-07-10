from src.repo.users import User
from src.repo.administrators import Administrator
from src.repo.customers import Customer
from src.repo.flights import Flight
from src.repo.tickets import Ticket
from src.repo.airline_companies import AirlineCompany
from src.repo.countries import Country
from src.my_config import log, engine, Session
from random import randint as rnd


class Repository:

    def __init__(self):
        self.session = Session()

    def get_by_id(self, kind: object, _id: int) -> object:
        """Finds the id given ,in a table."""
        try:
            obj = self.session.query(kind).get(_id)
            if obj:
                log.info(f"get_by_id() -> Finds object in {kind.__name__} table")
                return obj
            else:
                log.info(f"get_by_id() -> cant find id: {_id} in {kind.__name__} table")
                # print(f"ID: {_id} does not exist in {kind.__name__} table ")
        except Exception as e:
            log.info(f"get_by_id() -> Failed, make sure: {kind} object is an existing table.")
            log.error(f"get_by_id() -> {e}")

    def get_all(self, kind: object) -> list:
        """get all rows of a selected table into a list of obj"""
        try:
            table = self.session.query(kind).all()
            log.info(f"get_all() -> created a list of all {kind.__name__}")
            return table
        except Exception as e:
            log.info(f"get_all() -> Failed and didn't find the table: {kind}")
            log.error(f"get_all() -> {e}")

    def add(self, kind: object):
        """Add an object to a selected table"""
        try:
            self.session.add(kind)
            self.session.commit()
            log.info(f"add() -> Added a {kind}")
        except Exception as e:
            log.info(f"add() -> failed to add: {kind}")
            log.error(f"add() -> {e}")

    def update(self, new_obj, kind, _id):  ## TODO after add
        obj = self.get_by_id(kind, _id)
        self.add()
        # no use for update because it's not a real database for now
        pass

    def add_all(self, object_list: object):
        """ Uses add() func on a list of objects."""
        count = 0
        for obj in object_list:
            try:
                self.session.add(obj)
                self.session.commit()
                count += 1
            except Exception as e:
                log.info(f"add_all() -> failed to add: {obj} objects to the database")
                log.error(f"add_all() -> {e}")
            finally:
                self.session.close()
        log.info(f"add_all() -> added {count} objects to the database")

    def remove(self, obj: object):
        """Removes an object from our dictionary"""
        try:
            self.session.delete(obj)
            log.info("remove() -> object deleted")
            self.session.commit()
        except Exception as e:
            log.info(f"remove() -> this object doesn't exist in database \n{e}")
            log.error(f"remove() -> {e}")


    def get_airlines_by_country(self, country_id):
        pass

    def get_flights_by_origin_country_id(self, country_id):
        pass

    def get_flights_by_destination_country_id(self, country_id):
        pass

    def get_flights_by_departure_date(self, date):
        pass

    def get_flights_by_landing_date(self, country_id):
        pass


# if __name__ == '__main__':
#     # logging
#     user = Users('Shy', "32144661", 'shy@gmail.com', 1)
#     repo.add(Users('Wizz', "3213215", 'Wizz@gmail.com', 2))
#     repo.add(Countries('Greece'))
#     # repo.add(AirlineCompanies('Wizz', "Greece", repo.get_all()[Users][-1].user_id))
#     wizz = repo.get_by_id(AirlineCompanies, 11111)
#     # if wizz:
#     #     print(wizz.name)
#     # repo.remove(wizz)
#     # # repo.remove(user)
#     #
#     # wizz = repo.get_by_id(AirlineCompanies, 11111)
#
#     print("\n", repo.get_all())

if __name__ == '__main__':
    repo = Repository()

    # user_list = []
    # for i in range(10, 15):
    #     user_list += [User('Inbal_' + str(rnd(0, 99)), str(rnd(111111, 999999)), 'ILOVELeg' + str(i) + '@gmail.com', 1)]
    #     repo.add(user_list[0])
    # repo.add_all(user_list)
    # print(repo.get_all(Repository))

    # inbal1 = repo.get_by_id(User, '0')
    # print(inbal1)
    # print(f"{inbal1._id}: {inbal1.username}: {inbal1.email}")
    # inbal1.email = "ILoveArk15@gmail.com"
    # inbal1.username = "ARkbal"
    # print(f"{inbal1.username}: {inbal1.email}")
    # repo.add(inbal1)
    # print(user_list[0])
    # print(inbal6)

    # repo.remove(inbal6)
    # user_table = repo.get_all(Users)
    # print(user_table[0].username)
    # print(new_user.id)

    pass

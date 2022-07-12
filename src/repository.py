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
        self.tables_d = {
            User.__tablename__: User,
            Administrator.__tablename__: Administrator,
            Customer.__tablename__: Customer,
            Flight.__tablename__: Flight,
            Ticket.__tablename__: Ticket,
            AirlineCompany.__tablename__: AirlineCompany,
            Country.__tablename__: Country
        }

    def get_by_id(self, table_name: str, _id: int) -> object:
        """Finds the id given ,in a table."""
        table_name = '_'.join([w.capitalize() for w in table_name.split("_")])
        if table_name in self.tables_d.keys():
            table = self.tables_d[table_name]
            obj = self.session.query(table).get(_id)
            if obj:
                log.info(f"get_by_id() -> Finds object in {table_name} table")
                return obj
            else:
                log.info(f"get_by_id() -> cant find id: {_id} in {table_name} table")
        else:
            log.info(f"get_by_id() -> Failed, make sure: {table_name} is an existing table.")

    def get_all(self, kind: object) -> list:  ##TODO fix kind to table name
        """get all rows of a selected table into a list of obj"""
        try:
            table = self.session.query(kind).all()
            log.info(f"get_all() -> created a list of all {kind.__name__}")
            return table
        except Exception as e:
            log.info(f"get_all() -> Failed and didn't find the table: {kind}")
            log.error(f"get_all() -> {e}")

    def add(self, kind: object):  ##TODO fix kind to table name
        """Add an object to a selected table"""
        try:
            self.session.add(kind)
            self.session.commit()
            log.info(f"add() -> Added a {kind}")
        except Exception as e:
            log.info(f"add() -> failed to add: {kind}")
            log.error(f"add() -> {e}")

    def update(self, col: str, obj: object, val: str):  ## TODO after add
        if type(obj) not in self.tables_d.values():
            # print(type(obj))
            # print(self.tables_d["Users"])
            log.info(f"update() -> Make sure ur parameters are as it should be")
            return None

        attr = list(obj.__dict__.keys())[1:]
        if col in attr:
            try:
                setattr(obj, col, val)
                self.session.commit()
                log.info(f"update() -> updated {obj.__tablename__} in column {col} id:{obj._id} ")
            except Exception as e:
                log.info(f"update() -> failed to update to: {val} \n\
                make sure you know the constraints of this table")
                log.error(f"update() -> {e}")
        else:
            log.info(f"update() -> Failed make sure that the column exist in table")

        # no use for update because it's not a real database for now

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
        if obj:
            try:
                self.session.delete(obj)
                log.info("remove() -> object deleted")
                self.session.commit()
            except Exception as e:
                log.info(f"remove() -> Failed this object doesn't exist in database \n{e}")
                log.error(f"remove() -> {e}")
        else:
            log.info(f"remove() -> Failed 'obj' Must be a table object ")

    def get_airlines_by_country(self, country: str) -> list:
        airlines = self.session.query(AirlineCompany).\
                filter(AirlineCompany.country.ilike(f"%{country}%"))
        if airlines:
            log.info(f"get_airlines_by_country() -> Found {len(list(airlines))} airlines in {country}")
            return airlines
        else:
            log.info(f"get_airlines_by_country() -> Failed this 'country' parm doesnt exist in the database")

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
    repo.get_airlines_by_country("sdadsa22")
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

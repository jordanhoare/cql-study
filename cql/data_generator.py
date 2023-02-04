import datetime
import random
import string

from faker import Faker
from faker_vehicle import VehicleProvider


class DataGenerator(object):
    def __init__(self):
        """Initialise with the Faker library for Vehicles"""
        self.fake = Faker()
        self.fake.add_provider(VehicleProvider)

    @staticmethod
    def generate_mobile_number():
        """Generate a mobile number beginning with '04'"""
        return "0" + "4" + "".join(str(random.randint(0, 9)) for i in range(8))

    @staticmethod
    def generate_license_number():
        """Generate a license number beginning with 2 letters"""
        letters = string.ascii_uppercase
        return "".join(random.choice(letters) for i in range(2)) + "".join(
            str(random.randint(0, 9)) for i in range(6)
        )

    @staticmethod
    def generate_random_datetimes():
        """
        Generate random rental out and in datetimes
        Time out > time in by atleast 1 day
        """
        now = datetime.datetime.now()
        random_start_day = random.randint(1, 28)
        random_end_day = random.randint(random_start_day + 1, 29)
        random_start_hour = random.randint(8, 17)
        random_end_hour = random.randint(8, 17)
        end_date = now - datetime.timedelta(days=random_start_day, hours=random_start_hour)
        start_date = now - datetime.timedelta(days=random_end_day, hours=random_end_hour)
        return (start_date, end_date)

    @staticmethod
    def generate_car(make, model, category, car_year):
        """
        Generate a random set of car propeties
        A random seed is applied to simulate the rental checkin and reuse of the same plate.
        """

        if random.randint(1, 28) % 5 == 0:
            random.seed(make + make + category + str(car_year))

        number_plate = "".join(str(random.randint(0, 9)) for i in range(3))
        number_plate += "".join(
            random.choice(string.ascii_uppercase + string.digits) for i in range(5)
        )

        return make, model, category, car_year, number_plate

    def generate_records(self, num_records):

        rented = {}
        records = []

        for i in range(num_records):

            make, model, category, car_year, number_plate = DataGenerator.generate_car(
                self.fake.vehicle_make(),
                self.fake.vehicle_model(),
                self.fake.vehicle_category(),
                self.fake.vehicle_year(),
            )
            start, end = DataGenerator.generate_random_datetimes()

            # Check if the number plate is already rented
            if number_plate not in rented or rented[number_plate] <= start:
                rented[number_plate] = end
                records.append(
                    (
                        make,
                        model,
                        start,
                        end,
                        category,
                        int(car_year),
                        number_plate,
                        self.fake.first_name(),
                        self.fake.last_name(),
                        DataGenerator.generate_mobile_number(),
                    )
                )

        return records

import pandas as pd
import random
from datetime import datetime, timedelta

class FakeData:

    @staticmethod
    def generate_data(start_year:int = datetime.now().year - 2, end_year:int = datetime.now().year) -> pd.DataFrame:   
        """
        Generates a sample DataFrame for sales items, cities, costs, and revenues.

        Args:
            start_year: The starting year for the data.
            end_year: The ending year for the data.

        Returns:
            A pandas DataFrame.
        """

        items = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch']
        cities = ['New York', 'London', 'Tokyo', 'Paris', 'Sydney']

        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        date_range = pd.date_range(start_date, end_date, freq='MS')  # Month start frequency

        data = []
        for date in date_range:
            for item in items:
                for city in cities:
                    cost = random.randint(100, 1000)
                    revenue = cost * (1 + random.uniform(0.2, 1.5))  # Revenue is cost + random profit
                    data.append({
                        'Date': date,
                        'Item': item,
                        'City': city,
                        'Cost': cost,
                        'Revenue': revenue
                    })

        df = pd.DataFrame(data)
        return df
    

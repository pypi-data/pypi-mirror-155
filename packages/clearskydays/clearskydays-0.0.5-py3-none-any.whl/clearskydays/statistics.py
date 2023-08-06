import numpy as np
import pandas as pd

class Data(object):
    """
    This class determines the first value, the maximum value,
    the last value and the total number of measurements of the solar irradiance time series
    and divides the series into two parts at the maximum value.

    Then it calculates the sky clearness of the day, the state of the sky in the morning
    and in the afternoon,
    the sunlight time, and verifies that the proportion of the first series
    is at least 70% of the second series and vice versa.

    This simple method identifies the clear sky day,
    assuming that the graph of the temporal distribution of the data
    takes the shape of a bell.
    """
    def __init__(self, date):
        self.date = date
        self.first_value = self.date[self.date > 0].dropna().index[0]
        self.last_value = self.date[self.date > 0].dropna().index[-1]
        self.max_value = np.argmax(self.date[self.first_value:self.last_value])
        self.data = self.date[self.first_value:self.last_value]
        self.part1 = self.data[:self.data.index[self.max_value]]
        self.part2 = self.data[self.data.index[self.max_value + 1]:]
        self.number_measurements = self.part1.size + self.part2.size

    def get_clearness_percentage(self):
        """
        Returns sky clearness (%).
        """
        diff1 = self.part1.diff() >= 0
        diff2 = self.part2.diff() <= 0
        differences = diff1.sum() + diff2.sum() + 2
        percentage = (differences / self.number_measurements) * 100
        return percentage

    def clear_sky_morning(self):
        """
        Returns True if the sky is clear in the morning.
        """
        diff1 = self.part1.diff() >= 0
        difference1 = diff1.sum() + 1
        percentage = (difference1 / diff1.size) * 100
        return percentage >= 90

    def clear_sky_afternoon(self):
        """
        Returns True if the sky is clear in the afternoon.
        """
        diff2 = self.part2.diff() <= 0
        difference2 = diff2.sum() + 1
        percentage = (difference2 / diff2.size) * 100
        return percentage >= 90

    def calculate_sunlight_time(self):
        """
        Returns the sunlight time in hours.
        """
        time = self.last_value - self.first_value
        time = time / np.timedelta64(1, 'h')
        return time

    def check_size(self):
        """
        Returns True if the extent of the data from the start of the measurements
        to the maximum value is at least 70% of the data measured after solar noon,
        and vice versa.
		"""
        if (self.part1.size >= 0.7 * self.part2.size) and (self.part2.size >= 0.7 * self.part1.size):
            return True
        else:
            return False

class Statistics(Data):
    """
    This class performs statistics on the input data and identifies
    clear sky days and cloudy days.
    """
    def __init__(self, dataset):
        self.dataset = dataset
        self.dates = self.dataset.resample('D').max().dropna()
        self.dates = pd.to_datetime(self.dates.index.date).date

    def get_statistics(self):
        """
        Returns a dataframe that contains the sky clearness percentage of the day,
        the sunlight time, the number of measurements, the state of the sky in the morning
        and in the afternoon, and verifies that the proportion
        of the first series (from the start of the measurements to the maximum value)
        is at least 70% of the second series (from the maximum value to the last measured value)
        and vice versa.
        """
        date_list = []
        clearness_list = []
        sunlight_list = []
        values_list = []
        morning_list = []
        afternoon_list = []
        proportionality_list = []

        for date in self.dates:
            try:
                day = date
                clearness = Data(self.dataset.loc[str(date)]).get_clearness_percentage().item()
                sunlight = Data(self.dataset.loc[str(date)]).calculate_sunlight_time()
                values = Data(self.dataset.loc[str(date)]).number_measurements
                morning = Data(self.dataset.loc[str(date)]).clear_sky_morning().item()
                afternoon = Data(self.dataset.loc[str(date)]).clear_sky_afternoon().item()
                data_proportionality = Data(self.dataset.loc[str(date)]).check_size()

            except Exception:
                pass

            else:
                date_list.append(day)
                clearness_list.append(clearness)
                sunlight_list.append(sunlight)
                values_list.append(values)
                morning_list.append(morning)
                afternoon_list.append(afternoon)
                proportionality_list.append(data_proportionality)

        data_dict = {'date': date_list,
                    'clearness': clearness_list,
                    'sunlight': sunlight_list,
                    'measurements': values_list,
                    'clear_sky_morning': morning_list,
                    'clear_sky_afternoon': afternoon_list,
                    'proportionality': proportionality_list}
        statistics_df = pd.DataFrame(data_dict)
        statistics_df = statistics_df[statistics_df['sunlight'] <= 12]

        return statistics_df

    def get_clear_sky_days(self):
        """
        Returns a dataframe containing the selected clear sky days
        based on whether the sky is clear in the morning and in the afternoon,
        and the proportion of the first series (from the start of the measurements
        to the maximum value) is at least 70% of the second series
        (from the maximum value to the last measured value) and vice versa.
        """
        statistics_df = self.get_statistics()
        clear_sky_days_df = statistics_df[(statistics_df.clearness >= 90) &
        (statistics_df['clear_sky_morning'] == True) &
        (statistics_df['clear_sky_afternoon'] == True) &
        (statistics_df['proportionality'] == True)]

        return clear_sky_days_df

    def get_cloudy_days(self):
        """
        Returns a dataframe containing cloudy days. This dataframe contains data
        from days other than the selected clear sky days. See the get_clear_sky_days method.
        """
        statistics_df = self.get_statistics()
        cloudy_days_df = statistics_df[statistics_df['date'].isin(self.get_clear_sky_days()['date']) == False]

        return cloudy_days_df

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

months_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                'november', 'december']


def valid_city(city):
    city = city.lower()
    return city == 'chicago' or city == 'new york city' or city == 'washington'


def valid_month(month):
    month = month.lower()
    return months_names.count(month) > 0 or month == 'all'


def valid_day(day):
    day = day.lower()
    return DAYS.count(day) > 0 or day == 'all'


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid_city inputs
    city = ''
    while not valid_city(city):
        city = input("Enter the city you want statistics for: chicago or new york city or washington ")
        city = city.lower()
        if valid_city(city):
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while not valid_month(month):
        month = input('Enter a month you want statistics for: (all, january, february, ... , june)')
        month = month.lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while not valid_day(day):
        day = input('Enter a day you want statistics for: (all, monday, tuesday, ... sunday)')
        day = day.lower()
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Time Hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1  # because the index of the array starts from 0
        df = df[df['month'] == month]
        print(df['month'].head())

    if day != 'all':
        df = df[df['day_of_week'] == DAYS.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if df['month'].size > 0:
        print('The most common month is:', months_names[df['month'].mode()[0]])
    else:
        print('There is not any common month in the given time intervals')
    # TO DO: display the most common day of week
    if df['day_of_week'].size > 0:
        print('The most common day of week : ', DAYS[df['day_of_week'].mode()[0]])
    else:
        print('There is not any common day in the given time intervals')

    # TO DO: display the most common start hour
    if df['day_of_week'].size > 0:
        print('The most common hour is: ', df['Start Time Hour'].mode()[0])
    else:
        print('There is not any common hour in the given time intervals')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    if 'Start Station' in df and df['Start Station'].size > 0:
        print('The most common start station is: ', df['Start Station'].mode()[0])
    else:
        print('Start Station is not present in this dataset')
    # TO DO: display most commonly used end station
    if 'End Station' in df and df['End Station'].size > 0:
        print('The most common end station is: ', df['End Station'].mode()[0])
    else:
        print('End Station is not present in this dataset')

    # TO DO: display most frequent combination of start station and end station trip
    if 'End Station' in df and 'Start Station' in df and df['End Station'].size > 0 and df['Start Station'].size > 0:
        print('The combination of start station and end station trip is: ',
              df.groupby(['Start Station', 'End Station']).size().idxmax())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time', df['Trip Duration'].sum())
    # TO DO: display mean travel time
    print('Mean Travel Time', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Count of user types: ', df['User Type'].value_counts())
    # TO DO: Display counts of gender
    if 'Gender' in df:
        print('Counts of gender: ', df['Gender'].value_counts())
    else:
        print('Gender is not present in this dataset')
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Most recent year of birth: ', df['Birth Year'].max())

    if 'Birth Year' in df:
        print('Most common year of birth: ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        cnt = 0
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        repeat = 'yes'
        while repeat == 'yes' and cnt+5 < df.size:
            repeat = input('\nWould like to get the next 5 rows ?\n')
            repeat = repeat.lower()
            if repeat == 'yes':
                print(df[cnt:cnt + 5])
                cnt += 5
        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

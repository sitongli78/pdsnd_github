import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        try:
            city = input('Please specify city: Chicago, New York or Washington?\n')
            assert(city in ['Chicago', 'New York', 'Washington'])
            break
        except:
            print('Incorrect city')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Please specify month: Jan, Feb, Mar, Apr, May, Jun or all?\n')
            assert(month in ['all', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
            break
        except:
            print('Incorrect month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Please specify day of week: Monday, Tuesday, Wednesday, Thursday, Friday, Satuday, Sunday or all?\n')
            assert(day in ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Satuday', 'Sunday'])
            break
        except:
            print('Incorrect day of wekk')


    print('-'*40)
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

    month_dict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun'}
    weekday_dict = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Sauturday', 6:'Sunday'}
    
    if city == 'Chicago':
        df = pd.read_csv(CITY_DATA['chicago'])
    elif city == 'New York':
        df = pd.read_csv(CITY_DATA['new york city'])
    elif city == 'Washington':
        df = pd.read_csv(CITY_DATA['washington'])

    
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.weekday # Numerical month
    df['day_of_week'] = df['day_of_week'].apply(lambda x: weekday_dict[x]) # Convert numerical month to string

    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['month'] = df['month'].apply(lambda x: month_dict[x])

    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    df['travel_time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    if month != "all":
        # df = df[df.start_time.str.startswith(month_dict[month])]
        df = df[df.month == month]

    if day != 'all':
        df = df[df.day_of_week == day]

    return df

def most_common(ps):
    value_count = ps.value_counts()
    return value_count.idxmax(), value_count.max()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is %s. Count %i" % most_common(df.month))

    # display the most common day of week
    print("The most common day of week is %s. Count %i" % most_common(df.day_of_week))

    # display the most common start hour
    print("The most common hour is %s. Count %i" % most_common(df.hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is %s. Count %i' % most_common(df['Start Station']))

    # display most commonly used end station
    print('The most commonly used end station is %s. Count %i' % most_common(df['End Station']))

    # display most frequent combination of start station and end station trip
    start_end_most_common, count = most_common(df['Start Station'] + '@' + df['End Station'])
    print('The most frequent combination of start station and end station trip is %s (start) and %s (end). Count %i' % tuple(start_end_most_common.split('@') + [count]) )    

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is %.2f minutes' % (df.travel_time.sum().total_seconds()/60) )

    # display mean travel time
    print('Mean travel time is %.2f minutes' % (df.travel_time.mean().total_seconds()/60) )


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user types: Subscriber %i, Customer %i' % ((df['User Type']=='Subscriber').sum(), (df['User Type']=='Customer').sum()) )

    # Display counts of gender
    if 'Gender' in df.columns.values:
        print('Count of gender: Male %i, Female %i' % ((df.Gender=='Male').sum(), (df.Gender=='Female').sum()) )
    else:
        print('Gender is unavailable for Washintgon')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns.values:
        print('Year of birth: earliest is %i, most recent is %i. Most common is %i. Count %i' % \
            (df['Birth Year'].min(), df['Birth Year'].max(), most_common(df['Birth Year'])[0], most_common(df['Birth Year'])[1] ))
    else:
        print('Birth Year is unavailable for Washintgon')        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        view_idx = 0
        while True:
            view_data = input('\nWould you like to view 5 lines of raw data? Enter yes or no.\n')
            if view_data.lower() == 'yes':
                [print(df.iloc[i, :]) for i in range(view_idx, view_idx+5)]
                view_idx += 5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

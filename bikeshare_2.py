import time
import pandas as pd
import numpy as np

#DEBUG = False

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS_DATA = ("all", "january", "february", "march", "april", "may", "june")
DAYS_DATA = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_city()
    month = get_month()
    day = get_day()

    print('-'*40)
    return city, month, day

def get_city():
    """ return user input for city (chicago, new york city, washington) """
    while True:
        i = 1
        city_txt = "\nCity? "
        for k in CITY_DATA.keys():
            city_txt += "{}.{} ".format(i, k.title())
            i += 1
        city_txt += "\n"

        city = input(city_txt).lower()

        if city in ("1", "chi"):
            city = "chicago"
        elif city in ("2", "nyc"):
            city = "new york city"
        elif city in ("3", "wash"):
            city = "washington"

        if city in CITY_DATA:
            break

        print("\nIncorrect CITY option specified...Please retry.]\n")

    return city

def get_month():
    """ return user input for month (all, january, february, ... june) """
    while True:
        mnth_str = "\nMonth? "
        for i, v in enumerate(MONTHS_DATA):
            mnth_str += "{}.{} ".format(i, v.title())
        mnth_str += "\n"

        month = input(mnth_str).lower()

        if month in ("1", "jan"):
            month = "january"
        elif month in ("2", "feb"):
            month = "february"
        elif month in ("3", "mar"):
            month = "march"
        elif month in ("4", "apr"):
            month = "april"
        elif month in ("5", "may"):
            month = "may"
        elif month in ("6", "jun"):
            month = "june"
        elif month in ("0", "all"):
            month = "all"
            break

        if month in MONTHS_DATA:
            break

        print("\nIncorrect MONTH option specified...Please retry.]\n")

    return month

def get_day():
    """ return user input for day of week (all, monday, tuesday, ... sunday) """
    while True:
        day_str = "\nDay? "
        for i, v in enumerate(DAYS_DATA):
            day_str += "{}.{} ".format(i, v.title())
        day_str += "\n"

        day = input(day_str).lower()

        if day in ("1", "mon"):
            day = "monday"
        elif day in ("2", "tue"):
            day = "tuesday"
        elif day in ("3", "wed"):
            day = "wednesday"
        elif day in ("4", "thu"):
            day = "thursday"
        elif day in ("5", "fri"):
            day = "friday"
        elif day in ("6", "sat"):
            day = "saturday"
        elif day in ("7", "sun"):
            day = "sunday"
        elif day in ("0", "all"):
            day = "all"
            break

        if day in DAYS_DATA:
            break

        print("\nIncorrect DAY option specified...Please retry.]\n")

    return day

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
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour

    month_idx = MONTHS_DATA.index(month)

    if month_idx > 0:
        df = df[df['Month'] == month_idx]

    day_idx = DAYS_DATA.index(day)

    if day_idx > 0:
        df = df[df['Day'] == day_idx - 1]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    c_month = df['Month'].value_counts().idxmax()
    print("\tMost common Month is: ({}) {}".format(c_month, MONTHS_DATA[c_month].title()))

    # display the most common day of week
    c_day = df['Day'].value_counts().idxmax() + 1
    print("\tMost common Day is: ({}) {}".format(c_day, DAYS_DATA[c_day].title()))

    # display the most common start hour
    c_hour = df['Hour'].value_counts().idxmax()
    if c_hour == 0:
        c_hour_text = "Midnight"
    elif c_hour >= 1 and c_hour <= 11:
        c_hour_text = str(c_hour) + " am"
    elif c_hour == 12:
        c_hour_text = "Noon"
    else:
        c_hour_text = str(c_hour - 12) + " pm"

    print("\tMost common Hour is: ({}) {}".format(c_hour, c_hour_text))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    if show_raw():
        print("{}\n".format(df.head().filter(["Start Time", "Month", "Day", "Hour"])))

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    s_station = df['Start Station'].value_counts().idxmax()
    txt = "\tMost Common Start is: {} with {} departures."
    print(txt.format(s_station, df['Start Station'].value_counts().max()))

    # display most commonly used end station
    e_station = df['End Station'].value_counts().idxmax()
    txt = "\tMost Common Destination is: {} with {} arrivals."
    print(txt.format(e_station, df['End Station'].value_counts().max()))

    # display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + " -> " + df['End Station']
    station_combo = df['Station Combo'].value_counts().idxmax()
    txt = "\tMost Common Trip is: {} with {} trips."
    print(txt.format(station_combo, df['Station Combo'].value_counts().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    if show_raw():
        print("{}\n".format(df.head().filter(["Start Station", "End Station"])))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tt = df['Trip Duration'].sum()
    th = int(tt/(60*60))
    th_r = tt%(60*60)
    tm = int(th_r/60)
    ts = int(th_r%60)
    print("\tTotal travel time in seconds: {}.".format(tt))
    print("\t... {} hours, {} minutes, {} seconds.".format(th, tm, ts))

    # display mean travel time
    tt = df['Trip Duration'].mean()
    th = int(tt/(60*60))
    th_r = tt%(60*60)
    tm = int(th_r/60)
    ts = int(th_r%60)
    print("\tAverage travel time in seconds: {}.".format(tt))
    print("\t... {} hours, {} minutes, {} seconds.".format(th, tm, ts))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    if show_raw():
        print("{}\n".format(df.head().filter(["Trip Duration"])))

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("--- User Types ---")
    u_counts = dict(df['User Type'].value_counts())
    for k, v in u_counts.items():
        print("\t{}: {}".format(k, v))

    # Display counts of gender
    print("\n--- User Genders ---")
    try:
        u_gens = dict(df['Gender'].value_counts())
        for k, v in u_gens.items():
            print("\t{}: {}".format(k, v))

    except:
        print("\tGender information is not available")

    print("\n--- Birth Year data ---")
    try:
        # Display earliest, most recent, and most common year of birth
        print("\tEarliest Birth Year: {}".format(int(df['Birth Year'].min())))
        print("\tMost Recent Birth Year: {}".format(int(df['Birth Year'].max())))
        print("\tMost Common Birth Year: {}".format(int(df['Birth Year'].value_counts().idxmax())))

    except:
        print("\tBirth Year information is not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    if show_raw():
        print("{}\n".format(df.head().filter(["User Type", "Gender", "Birth Year"])))

def show_raw(txt="Display Raw Data?"):
    rsp = input(txt + " (y)es or (N)o?\n").lower()
    return rsp[:1] == "y"

def main():
    """ mainline processing """

    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

#        if DEBUG:
#            print(city, month, day)
#            print(df.info())
#            print(df.describe())
#            print(df.shape)
#            print(df.head())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or No.\n')

        if restart.lower() != 'yes' and restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()

# Import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
import pandas as pd
import pathlib
from datetime import timedelta
import random


# load min_val and max_val to normalize data & load latent dimension
ORG = pathlib.Path(__file__).parents[1]
LOC_VARS = str(ORG) + "/Data/important_variables/"
NAME_MAX_VAL = "max_val.npy"
NAME_MIN_VAL = "min_val.npy"
ENCODER_LOCATION = "encoder"

min_val = np.load(LOC_VARS + NAME_MIN_VAL)
max_val = np.load(LOC_VARS + NAME_MAX_VAL)
LATENT_DIM = int(open(LOC_VARS + "/latent_dim.txt", "r").read())


## Normalize data
def normalize(data):
    # Normalize data
    return (data - min_val) / (max_val - min_val)


## Convert a row to a np.datetime64 object
def check_validity_date_elements(date):
    # make sure that the year contains 4 digits and add 0's if necessary
    date[0] = "%04d" %date[0]
    # make sure that the months, days, hours, minutes and seconds contain 2 digits and add 0's if necessary
    date[1:] = ["%02d" %x for x in date[1:]]
    return date

def create_np_datetime_from_date(date):
    # create a numpy datetime64 object from a row in the generated data
    date = date[:6].tolist()
    date = check_validity_date_elements(date)
    result = "-".join(date[:3])
    result += "T"
    result += ":".join(date[3:])
    return np.datetime64(result)


## Vectorize an incoming timestep
def days_per_month(month_number, is_leap_year):
    # February
    if month_number == 2:
        if is_leap_year:
            return 29
        else:
            return 28
    # based on the Knuckle mnemonic
    elif month_number <= 7:
        if month_number % 2 != 0:
            return 31
        else:
            return 30
    else:
        if month_number % 2 == 0:
            return 31
        else:
            return 30

def extract_features_date(date):
    # extract the features of the date
    years = date.astype(object).year
    months = date.astype(object).month
    days = date.astype(object).day
    hours = date.astype(object).hour
    minutes= date.astype(object).minute
    seconds = date.astype(object).second
    day_of_week = date.astype(datetime).isoweekday()
    millennium = round(np.floor(years / 1000))
    century = round(np.floor(years / 100))
    decade = round(np.floor(years / 10))
    last_digit_year = years % 10
    is_leap_year = years % 4 == 0
    # 0 because Sunday is 0
    is_business_day = day_of_week <= 5 
    quarter = round(np.ceil(months / 3))
    days_in_month = days_per_month(months, is_leap_year)
    day_of_year = date.astype(object).timetuple().tm_yday
    is_month_start = days == 1
    is_quarter_start = days == 1 and months % 3 == 0
    is_year_start = days == 1 and months == 1
    is_year_end = days == 31 and months == 12
    # end of the year is the end of the last quarter, 31 March, 30 June, 30 September
    is_quarter_end = is_year_end or (months == 3 and days == 31) or ((months == 6 or 9) and days == 30)
    is_month_end = days == days_in_month
    
    encoding = [years, months, days, hours, minutes, seconds, day_of_week, millennium, century, decade, last_digit_year, is_leap_year, is_business_day, quarter, days_in_month, day_of_year, is_month_start,
            is_quarter_start, is_year_start, is_year_end, is_quarter_end, is_month_end]
    
    return encoding


def date_to_features(date):
    # make a np.datetime64 of the date (in the shape YYYY-MM-DD HH:MM:SS)
    date = np.datetime64(date)
    date = date.astype('datetime64[ms]')
    # obtain features
    features = extract_features_date(date)
    # return all features, except the datetime object
    return features


def get_latent_vars(dates, model):
    # make strings of the dates
    dates = [str(date) for date in dates]
    # obtain the latent vectors
    dates_latent_vec = model(dates)
    return dates_latent_vec


def sample_date(start, end):
    # create datetime objects for start and end to sample
    start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    # calculate the difference between the 2 dates
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    # randomly select the number of seconds to add to the start date
    random_second = random.randrange(int_delta)
    # add the random to the start date and return
    return start + timedelta(seconds=random_second)


def validate_sample(sample, interest, start):
    # check whether the sampled date is a valid date (only if the interest is fixed)
    start_date = np.datetime64(start)
    try:
        if interest == "Y":
            sample = sample.replace(year=start_date.astype(object).year)
        elif interest == "M":
            sample = sample.replace(month=start_date.astype(object).month)
        elif interest == "D":
            sample = sample.replace(day=start_date.astype(object).day)
        elif interest == "h":
            sample = sample.replace(hour=start_date.astype(object).hour)
        elif interest == "m":
            sample = sample.replace(minute=start_date.astype(object).minute)
        elif interest == "s":
            sample = sample.replace(second=start_date.astype(object).second)
        else:
            print("Invalid interest type")
            return None
        return True
    except ValueError:
        return False


def sample_and_vectorize_timestamps(start, end, interest, n_samples, single_interst=False):
    """"
    Obtain samples from start to end
    The interest is used for plotting (and possibly the sampling process)
    When single_interst = True, the samples will get the same value as start for a specific interest
    start = start date
    end = end date
    interest = Y:Year, M:Month, D:Day, h:hour, m:minute, s:seconds
    n_samples = the number of samples
    """
    # sample dates between start and end, while keep the interest time component the same
    result = []
    for _ in range(n_samples):
        start_date = np.datetime64(start)
        sample = sample_date(start, end)
        if single_interst:
            while not validate_sample(sample, interest, start):
                sample = sample_date(start, end)
            if interest == "Y":
                sample = sample.replace(year=start_date.astype(object).year)
            elif interest == "M":
                sample = sample.replace(month=start_date.astype(object).month)
            elif interest == "D":
                sample = sample.replace(day=start_date.astype(object).day)
            elif interest == "h":
                sample = sample.replace(hour=start_date.astype(object).hour)
            elif interest == "m":
                sample = sample.replace(minute=start_date.astype(object).minute)
            elif interest == "s":
                sample = sample.replace(second=start_date.astype(object).second)
            else:
                print("Invalid interest type")
                return None
        sample = np.datetime64(sample)
        result.append(sample)
    result = np.array(result)
    return result


def preprocess_and_obtain_latent_variables(start, end, interest, interval, model):
    """"
    Obtain the latent variables of the dates from start till end, using a certain interval (interest)
    start = start date
    end = end date
    interest = Y:Year, M:Month, D:Day, h:hour, m:minute, s:seconds
    """
    # get the dates from <start> to <end> with interval <interest> 
    dates = obtain_date_range(start, end, interest, interval)
    # obtain the labels for plotting
    labels = obtain_labels_date_range(dates, interest)
    # change type to strings
    dates = [str(date) for date in dates]
    # get latent vectors
    dates_latent_vec = model(dates)

    return dates_latent_vec, labels


### Visualization of the latent space
def label_point(x, y, val, ax, diff):
    x, y, val = pd.Series(x), pd.Series(y), pd.Series(val)
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for _, point in a.iterrows():
        ax.text(point['x']+diff, point['y'], str(point['val']))


def plot_latent_with_label(latent_vector, latent_dim, labels, interest):
    """"
    Plot the latent variable with dimension <latent_dim> with corresponding labels 
    """
    ax = sns.scatterplot(labels, latent_vector[:, latent_dim])
    plt.title('Example Plot')
    # Set x-axis label
    plt.xlabel(interest)
    # Set y-axis label
    plt.ylabel('Latent variable')
    label_point(labels, latent_vector[:, latent_dim], labels, plt.gca(), .0002)


def plot_latent_with_label_2dim(latent_vec, latent_dim1, latent_dim2, labels, interest):
    """"
    Plot the latent variable with dimension <latent_dim> with corresponding labels 
    """
    ax = sns.scatterplot(latent_vec[:, latent_dim1], latent_vec[:, latent_dim2])
    plt.title('Example Plot')
    # Set x-axis label
    plt.xlabel(interest)
    # Set y-axis label
    plt.ylabel('Latent variable')
    label_point(latent_vec[:, latent_dim1], latent_vec[:, latent_dim2], labels, plt.gca(), .0002)


def create_plot_range_2dim(start, end, interest, interval, latent_dim1, latent_dim2, model):
    """"
    Create plots from start till end, using a certain interval (interval)
    start = start date
    end = end date
    interest = Y:Year, M:Month, D:Day, h:hour, m:minute, s:seconds
    """

    # get latent vector and labels
    dates_latent_vec, labels = preprocess_and_obtain_latent_variables(start, end, interest, interval, model)
    # call plot_latent_with_label 
    plot_latent_with_label_2dim(dates_latent_vec, latent_dim1, latent_dim2, labels, interest)


def create_plot_range_all_latent_dim(start, end, interest, interval, model):
    """"
    Create plots from start till end, using a certain interval (interval), for all latent dimensions
    start = start date
    end = end date
    interest = Y:Year, M:Month, D:Day, h:hour, m:minute, s:seconds
    """
    # get latent vector and labels
    dates_latent_vec, labels = preprocess_and_obtain_latent_variables(start, end, interest, interval, model)
    # call plot_all_latent_dim
    plot_all_latent_dim(start, end, dates_latent_vec, labels, interest, interval)


def flatten(t):
    return [item for sublist in t for item in sublist]


def plot_all_latent_dim(start, end, dates_latent_vec, labels, interest, interval):
    fig, axs = plt.subplots(2, 4, figsize=(LATENT_DIM * 4, LATENT_DIM * 2 + 4))
    dim = 1
    for i in range(2):
        for j in range(4):
            axs[i, j].scatter(labels, dates_latent_vec[:, (i*2 + j*1)])
            axs[i, j].set_title("Latent dimension: " + str(dim))
            axs[i, j].set(xlabel=interest, ylabel='Latent dimension')
            label_point(labels, dates_latent_vec[:, (i*2 + j*1)], labels, axs[i, j], .001)
            dim += 1

    fig.suptitle('All single latent dimensions from ' + str(start) + " till " + str(end) + " with an interval of " + str(interval) + interest, y=0.93, fontsize="xx-large", fontweight="bold")

def obtain_date_range(start, end, interest, interval):
    """"
    Obtain the needed date range, with corresponding interval for the create_plot_range function
    interest = Y:Year, M:Month, D:Day, h:hour, m:minute, s:seconds
    """
    if interest == "Y":
        dates = np.arange(start, end, interval, dtype='datetime64[' + interest + ']')
        return dates
    if interest == "M":
        dates = np.arange(start, end, interval, dtype='datetime64[' + interest + ']')
        return dates
    if interest == "D":
        dates = np.arange(start, end, interval, dtype='datetime64[' + interest + ']')
        return dates
    if interest == "h":
        dates = np.arange(start, end, interval, dtype='datetime64[' + interest + ']')
        return dates
    if interest == "m":
        dates = np.arange(start, end, interval, dtype='datetime64[' + interest + ']')
        return dates
    if interest == "s":
        dates = np.arange(start, end, interval, dtype='datetime64[' + interest + ']')
        return dates
    else:
        print("Invalid interest type")
        return None


def obtain_labels_date_range(dates, interest):
    """"
    Obtain the needed labels for the create_plot_range function
        Year = 0
        Month = 1
        Day = 2
        Hour = 3
        Minute = 4
        Second = 5
    """
    if interest == "Y":
        return [date.astype(object).year for date in dates]
    if interest == "M":
        return [date.astype(object).month for date in dates]
    if interest == "D":
        return [date.astype(object).day for date in dates]
    if interest == "h":
        return [date.astype(object).hour for date in dates]
    if interest == "m":
        return [date.astype(object).minute for date in dates]
    if interest == "s":
        return [date.astype(object).second for date in dates]
    else:
        print("Invalid interest type")
        return None

def create_plot_range(start, end, interest, interval, latent_dim, model):
    """"
    Create plot from start till end, using a certain interval (interest), of latent dim <latent_dim>
    start = start date
    end = end date
    interest = Y:Year, M:Month, D:Day, h:hour, m:minute, s:seconds
    """

    # get latent vector and labels
    dates_latent_vec, labels = preprocess_and_obtain_latent_variables(start, end, interest, interval, model)
    # call plot_latent_with_label 
    plot_latent_with_label(dates_latent_vec, latent_dim, labels, interest)


### Visualization of time dataset
def visualize_distribution(data):
    # Visualize the years
    sns.displot(data[:,0])
    plt.xlabel("Years")
    plt.show()
    # Visualize the months
    sns.displot(data[:,1])
    plt.xlabel("Months")
    plt.show()
    # Visualize the days
    sns.displot(data[:,2])
    plt.xlabel("Days")
    plt.show()
    # Visualize the hours
    sns.displot(data[:,3])
    plt.xlabel("Hours")
    plt.show()
    # Visualize the minutes
    sns.displot(data[:,4])
    plt.xlabel("Minutes")
    plt.show()
    # Visualize the seconds
    sns.displot(data[:,5])
    plt.xlabel("Seconds")
    plt.show()
    # Visualize the day of week
    sns.displot(data[:,6])
    plt.xlabel("Day of week")
    plt.show()
    # Visualize the day of week
    sns.displot(data[:,7])
    plt.xlabel("Millenium")
    plt.show()
    # Visualize the century
    sns.displot(data[:,8])
    plt.xlabel("Century")
    plt.show()
    # Visualize the decade
    sns.displot(data[:,9])
    plt.xlabel("Decade")
    plt.show()


### Visualization of the error between reconstructed and input data
def plot_error_timestep(input, reconstruction):
    plt.scatter(range(len(input)), input, color='blue')
    plt.scatter(range(len(reconstruction)), reconstruction, color='red')
    plt.fill_between(np.arange(20), input, reconstruction, color='lightcoral')
    plt.legend(labels=["Input", "Reconstruction", "Error"])
    plt.show()

def plot_error_timesteps(input, reconstructed, n):
    for i in range(n):
        plot_error_timestep(input[i], reconstructed[i])
    

import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    #Group sex when male with age, find the avearge/mean and round to 1 decimal place.
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    #To find percentage of bachelors out of total education. Get the lenght (basically a count) of how many have a bachelor and divide it by total number of people in the dataset.
    percentage_bachelors = round(len(df[df['education'] == 'Bachelors']) / len(df['education']) *100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])] #The '~' sign (tilde), acts as a lot and means "not". So first we get find who has the higher education and then uses the symbol to find all that do not conform. 
  # Instead of using isin, it's also possible to simply make a new df with the ones you one and as for the lower education simply drop the 3 higher levels of education.

    # percentage with salary >50K
    #The process is similar to how we found the % of how many people had a bachelor. Simply replicat the filter while only looking at people above 50k.
    higher_education_rich = round(len(higher_education[higher_education['salary'] == '>50K']) / len(higher_education) * 100, 1)
    lower_education_rich = round(len(lower_education[lower_education['salary'] == '>50K']) / len(lower_education) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    bigsal = df['salary'] == '>50K' #Easier to work sometime if you create subsets of your dataframe.
    num_min_workers = df['hours-per-week'] == min_work_hours

    rich_percentage = round((num_min_workers & bigsal).sum() / num_min_workers.sum() * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    #Create a function that returns the country with the highest earnings in a descending fashion if shown
    c_count = df['native-country'].value_counts()
    c_rich = df[df['salary'] == '>50K']['native-country'].value_counts()
  
    highest_earning_country = (c_rich / c_count *100).idxmax() #idxmax returns first occurency of maximum
    highest_earning_country_percentage = round((c_rich / c_count * 100).max(), 1)
  
    # Identify the most popular occupation for those who earn >50K in India.
    indian_pop_rich = df[(df['salary'] == '>50K') & (df['native-country'] == 'India')]
    top_IN_occupation = indian_pop_rich['occupation'].value_counts().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men, "years old")
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

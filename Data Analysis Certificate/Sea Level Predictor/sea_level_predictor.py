import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')
    x = df['Year'] #Found looking at the CSV file
    y = df['CSIRO Adjusted Sea Level'] #Found looking at the CSV file

    # Create scatter plot
    fig, ax = plt.subplots()
    plt.scatter(x,y)

    # Create first line of best fit
    line = linregress(x,y) #line is an object -> Linregress calculates a linear least-squares regression for the two measurements, x and y.
    x_pred = pd.Series([i for i in range (1880,2051)]) #The years ->If we only put till 2050 we do not have similar size arrays, admittedly as we only go up until but not including 2050 unless we write 2051
    y_pred = line.slope*x_pred + line.intercept #intercept is our B
    plt.plot(x_pred, y_pred, 'r')

    # Create second line of best fit
    new_df = df.loc[df['Year'] >= 2000]
    new_x = new_df['Year']
    new_y = new_df['CSIRO Adjusted Sea Level']
    line2 = linregress(new_x,new_y) #line is an object
    x_pred2 = pd.Series([i for i in range (2000,2051)]) #The years
    y_pred2 = line2.slope*x_pred2 + line2.intercept #intercept is our B
    plt.plot(x_pred2, y_pred2, 'green')

    # Add labels and title
    ax.set_title('Rise in Sea Level') 
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')
  
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
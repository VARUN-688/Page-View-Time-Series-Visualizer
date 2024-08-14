import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(r'/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv')
df['date']=pd.to_datetime(df['date'])
df=df.set_index('date')
# Clean data
df = df.loc[(df['value']>=df.value.quantile(0.025))&(df['value']<=df.value.quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig,ax=plt.subplots(1,1,figsize=(10,4))
    ax.plot(df.index,df['value'],color='r')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar=df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.strftime('%B')
    
    df_grp=df_bar.groupby(by=['year','month'],as_index=False).agg('mean')
    df_grp.sort_values(by=['year','month'])
    months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    df_grp['month'] = pd.Categorical(df_grp['month'], categories=months, ordered=True)
    all_combinations = pd.MultiIndex.from_product(
            [df_grp['year'].unique(), months],
            names=['year', 'month']
        ).to_frame(index=False)
    
    df_complete = pd.merge(all_combinations, df_grp, on=['year', 'month'], how='left').fillna(0)
    
    df_complete = df_complete.sort_values(by=['year', 'month'])

    num_months = len(months)

    years = df_complete['year'].unique()
    num_years = len(years)
    indices = np.arange(num_years)

    # Bar width
    bar_width = 0.8 / num_months

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Loop through each month and plot the bar
    for i, month in enumerate(months):
        month_data = df_complete[df_complete['month'] == month]
        
        # Ensure data is properly aligned with x-axis
        x = indices + i * bar_width
        if len(x) != len(month_data):
            print(f"Warning: Length mismatch in x-coordinates for month '{month}' - expected {len(month_data)}, got {len(x)}")
            continue

        ax.bar(x, month_data['value'], bar_width, label=month, edgecolor='black')

    # Set the x-axis ticks to the middle of the grouped bars
    ax.set_xticks(indices + bar_width * (num_months - 1) / 2)
    ax.set_xticklabels(years)
    plt.xticks(rotation=90)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='month')
    # Draw bar plot





    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    
    # Ensure that the 'value' column is of type float

    # Sort months to ensure correct order in the plot
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Create figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

    # Boxplot by year using Seaborn
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_xticklabels(sorted(df_box['year'].unique()))

    # Boxplot by month using Seaborn
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=month_order)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    plt.suptitle('')  # Remove the default title to avoid overlap
    plt.tight_layout()


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

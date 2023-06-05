import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('./medical_examination.csv', sep=',')

maxDiff = None

# Add 'overweight' column
overweight = []
for row in (df['weight'] / (df['height'] / 100) ** 2):
    if row <= 25:
        overweight.append(0)
    else:
        overweight.append(1)

df['overweight'] = overweight

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
chol = []
gluc = []
for ch in (df['cholesterol']):
    if ch == 1:
        chol.append(0)
    else:
        chol.append(1)
df['cholesterol'] = chol

for glu in (df['gluc']):
    if glu == 1:
        gluc.append(0)
    else:
        gluc.append(1)

df['gluc'] = gluc

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt(id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active','overweight']).sort_values(by='variable')

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.

    # Draw the catplot with 'sns.catplot()'
    plot = sns.catplot(data=df_cat, kind='count', x='variable', hue='value', col='cardio')
    plot.set_axis_labels("variable", "total")

    # Get the figure for the output
    fig = plot.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[ (df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & 
                 (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) &
                  (df['weight'] <= df['weight'].quantile(0.975)) ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    #corr = round(df_heat.corr(), 1)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True, square=True, linewidths=1, linecolor='white', cbar_kws={'shrink': 0.7}, fmt='.1f')


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
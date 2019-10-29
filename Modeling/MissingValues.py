# Number of missing values in each column
Df.isnull().sum()

# Percentage of missing values in each column
Df.isnull().sum() * 100 / len(Df)

# Missing count, Missing Percentage for each column as a dataset - Sorted by count or %
# index consists of variable names
MissingCount = Df.isnull().sum().sort_values(ascending=False)
MissingPercent = (Df.isnull().sum()/X_train.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([MissingCount, MissingPercent], axis=1, keys=['MissingCount', 'MissingPercent'])
missing_data.reset_index(inplace=True)

# Plot Percentages of missing values
f, ax = plt.subplots(figsize=(15, 6))
plt.xticks(rotation='90')
sns.barplot(x=missing_data['index'], y=missing_data['MissingPercent'])
plt.xlabel('Features', fontsize=15)
plt.ylabel('Percent of missing values', fontsize=15)
plt.title('Percent missing data by feature', fontsize=15)

# Calculate skewness
Df['Var'].skew()

# Soft Probability Imputation
valueCounts = {}
def CountAll():
    global all_columns, nanCounts, valueCounts
    all_columns = list(df)
    nanCounts = df.isnull().sum()
    for x in all_columns:
        valueCounts[x] = df[x].value_counts()

"""Random but proportional replacement(RBPR) of numeric"""
def Fill_NaNs_Numeric(col):

    mini = df[col].min()
    maxi = df[col].max()
    """Selecting ONLY non-NaNs."""
    temp = df[df[col].notnull()][col] # type --> pd.Series

    """Any continuous data is 'always' divided into 45 bins (Hard-Coded)."""
    bin_size = 45
    bins = np.linspace(mini, maxi, bin_size)

    """Filling the bins (with non-NaNs) and calculating mean of each bin."""
    non_NaNs_per_bin = []
    mean_of_bins = []

    non_NaNs_per_bin.append(len(temp[(temp <= bins[0])]))
    mean_of_bins.append(temp[(temp <= bins[0])].mean())
    for x in range(1, bin_size):
        non_NaNs_per_bin.append(len(temp[(temp <= bins[x]) & (temp > bins[x-1])]))
        mean_of_bins.append(temp[(temp <= bins[x]) & (temp > bins[x-1])].mean())

    mean_of_bins = pd.Series(mean_of_bins)
    # np.around() on  list 'proportion' may create trouble and we may get a zero-value imputed, hence,
    mean_of_bins.fillna(temp.mean(), inplace= True)
    non_NaNs_per_bin = np.array(non_NaNs_per_bin)

    """Followoing part is SAME as Fill_NaNs_Catigorical()"""

    """Calculating probability and expected value."""
    proportion = np.array(non_NaNs_per_bin) / valueCounts[col].sum() * nanCounts[col]
    proportion = np.around(proportion).astype('int')

    """Adjusting proportion."""
    diff = int(nanCounts[col] - np.sum(proportion))
    if diff > 0:
        for x in range(diff):
            idx = random.randint(0, len(proportion) - 1)
            proportion[idx] =  proportion[idx] + 1
    else:
        diff = -diff
        while(diff != 0):
            idx = random.randint(0, len(proportion) - 1)
            if proportion[idx] > 0:
                proportion[idx] =  proportion[idx] - 1
                diff = diff - 1

    """Filling NaNs."""
    nan_indexes = df[df[col].isnull()].index.tolist()
    for x in range(len(proportion)):
            if proportion[x] > 0:
                random_subset = random.sample(population= nan_indexes, k= proportion[x])
                df.loc[random_subset, col] = mean_of_bins[x] # <--- Replacing with bin mean
                nan_indexes = list(set(nan_indexes) - set(random_subset))

"""-------------------------------------------------------------------------"""






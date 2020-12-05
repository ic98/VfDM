import pandas
csv_data = pandas.read_csv('/Data/rust-answers.csv', usecols=['Body'])
csv_data.to_csv('r-a.csv')

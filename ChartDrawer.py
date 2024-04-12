import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import requests


class Plotter:
    def __init__(self):
        self.plot_dir = 'plots'
        os.makedirs(self.plot_dir, exist_ok=True)
        self.__set_plot_params()

    def __check_url(self, url):
        try:
            response = requests.head(url, timeout=5)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to connect to URL: {e}")
            return False

    def draw_plots(self, file_path):
        if not self.__check_url(file_path):
            print("URL is not accessible")
            return []

        try:
            df = pd.read_json(file_path)
        except ValueError as e:
            print(f'Failed to read JSON: {e}')
            return []
        except Exception as e:
            print(f'An error occurred: {e}')
            return []

        plot_paths = []
        try:
            plot_paths.append(self.draw_scatterplot(df, 'gt_corners', 'rb_corners', True))
            plot_paths.append(self.draw_scatterplot(df, 'floor_mean', 'ceiling_mean'))
            plot_paths.append(self.draw_histogram(df, 'mean'))
            plot_paths.append(self.draw_histogram(df, 'floor_mean'))
            plot_paths.append(self.draw_histogram(df, 'ceiling_mean'))
            plot_paths.append(self.draw_boxplots(df, ['mean', 'floor_mean', 'ceiling_mean'], 'means'))
            plot_paths.append(self.draw_boxplots(df, ['min', 'mean', 'max'], 'stats'))
            plot_paths.append(self.draw_top_bottom_data(df, 'mean', 10))
            plot_paths.append(self.draw_top_bottom_data(df, 'mean', 10, False))
        except KeyError as e:
            print(f'Failed to draw plot: {e}')
        return plot_paths

    def __set_plot_params(self):
        plt.rcParams['axes.titlesize'] = 18
        plt.rcParams['axes.titlepad'] = 20
        sns.set_style('whitegrid')
        plt.rcParams['figure.figsize'] = (10, 6)

    def __save_plot_to_file(self, filename):
        filepath = f'{os.path.join(self.plot_dir, filename)}.png'
        plt.savefig(filepath, dpi=300)
        return filepath

    def __show_and_close_plot(self):
        plt.show()
        plt.close()

    def __plot_setup(self, title, xlabel, ylabel):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    def draw_scatterplot(self, data, x, y, add_line=False):
        plt.figure()
        title = f'Scatter plot {x} vs {y}'
        if add_line:
            max_limit = max(data[x].max(), data[y].max()) * 1.1
            min_limit = min(data[x].min(), data[y].min()) * 0.9
            plt.plot([min_limit, max_limit], [min_limit, max_limit], 'r--', linewidth=1, zorder=1)
        self.__plot_setup(title, x, y)
        sns.scatterplot(x=x, y=y, data=data, zorder=2)
        path = self.__save_plot_to_file(title)
        self.__show_and_close_plot()
        return path

    def draw_histogram(self, data, column, bins='auto'):
        plt.figure()
        sns.histplot(data[column], label=column, bins=bins)
        title = f'Histogram for {column}'
        self.__plot_setup(title, 'Degrees', 'Frequency')
        path = self.__save_plot_to_file(title)
        self.__show_and_close_plot()
        return path

    def draw_boxplots(self, data, columns, title):
        plt.figure()
        sns.boxplot(x='variable', y='value', data=pd.melt(data[columns]))
        title = f'Boxplots for {title}'
        self.__plot_setup(title, '', 'Degrees')
        path = self.__save_plot_to_file(title)
        self.__show_and_close_plot()
        return path

    def draw_top_bottom_data(self, data, column, cnt=5, top=True):
        plt.figure()
        values = data.sort_values(by=column, ascending=top).head(cnt)
        sns.barplot(x=column, y='name', data=values)
        order = 'best' if top else 'worst'
        title = f'Top {cnt} {order} results for {column}'
        self.__plot_setup(title, 'Degrees', '')
        path = self.__save_plot_to_file(title)
        self.__show_and_close_plot()
        return path
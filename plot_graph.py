import matplotlib.pyplot as plt
import pandas as pd


def plot_csv(file_path, x_column, y_column, x_label, y_label, output_file=None):
    """
    繪製 CSV 檔案中的數據圖表，並根據指定的參數設置圖表屬性。

    :param file_path: CSV 檔案的路徑
    :param x_column: 作為 x 軸的列名
    :param y_column: 作為 y 軸的列名
    :param x_label: x 軸標籤
    :param y_label: y 軸標籤
    :param output_file: 圖片輸出的檔案路徑（可選）
    """
    try:
        # 讀取 CSV 檔案
        data = pd.read_csv(file_path)

        # 檢查列是否存在
        if x_column not in data.columns or y_column not in data.columns:
            raise KeyError(f"One of the columns ({x_column}, {y_column}) does not exist in the file.")

        # 繪製圖表
        plt.figure(figsize=(10, 6))
        plt.plot(data[x_column], data[y_column], marker='o', label=f'{y_column} vs {x_column}')
        plt.title(f"{y_label} over {x_label}")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.legend()

        # 保存或顯示圖表
        if output_file:
            plt.savefig(output_file)
            print(f"Graph saved as {output_file}")
        else:
            plt.show()

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
le.")

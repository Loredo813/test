import matplotlib.pyplot as plt
import pandas as pd

def plot_csv(file_path, x_column, y_column, mode, x_label, y_label, output_file=None):
    """
    繪製 CSV 檔案數據的圖表，根據 mode 設置動態標題。
    
    :param file_path: CSV 檔案的路徑
    :param x_column: 作為 x 軸的列名
    :param y_column: 作為 y 軸的列名
    :param mode: 模式 (1: default, 2: adjust)
    :param x_label: x 軸標籤
    :param y_label: y 軸標籤
    :param output_file: 圖片輸出的檔案路徑（可選）
    """
    try:
        # 讀取 CSV 檔案
        data = pd.read_csv(file_path)

        # 設定標題根據 mode
        title = f"{y_column} Over {x_column} ({'Default' if mode == 1 else 'Adjust'})"

        # 繪製圖表
        plt.figure(figsize=(10, 6))
        plt.plot(data[x_column], data[y_column], marker='o', label=f'{y_column} over {x_column}')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.legend()

        # 如果指定了輸出檔案，保存圖表
        if output_file:
            plt.savefig(output_file)
            print(f"Graph saved as {output_file}")
        else:
            # 顯示圖表
            plt.show()

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except KeyError:
        print(f"Error: One of the columns ({x_column}, {y_column}) does not exist in the file.")

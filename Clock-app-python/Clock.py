import tkinter as tk
from time import strftime
import requests
import sys

n = 0

# 日付の上表を取得
def day():
    today = strftime('%Y-%m-%d (%A)')
    canvas.itemconfig(day_text, text=today)

# 時間の情報を取得
def time():
    string = strftime('%H:%M:%S')  
    canvas.itemconfig(clock_text, text=string)
    root.after(1000, time)

# 背景の画像を変更    
def show_image():
    global n, img

    # 次の画像番号に進める
    n += 1

    # 最後まで行ったら最初に戻る
    if n >= len(image_list):
        n = 0

    # 画像を読み込み直す
    img = tk.PhotoImage(file=image_list[n])

    # キャンバス上の画像を変更する
    canvas.itemconfig(image_on_canvas, image=img)

    # 20秒後にまた実行
    root.after(20000, show_image)

# 天気の情報を取得

def weather_kanazawa():
    # 金沢市の予報区コード（気象庁API）
    # 石川県加賀地方: 170000
    JSON_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/170000.json"
    jma_json = requests.get(JSON_URL).json()
    try:
        response = requests.get(JSON_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 今日と明日のデータを取得
        jma_area = jma_json[0]["timeSeries"][0]["areas"][0]["area"]["name"]
        jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        
        weather = f'{jma_area}の天気：{jma_weather}'
        canvas.itemconfig(weather_text, text=weather)
        
    except requests.exceptions.RequestException as e:
        print(f"HTTPエラー: {e}")
        sys.exit(1)
    except (KeyError, IndexError, ValueError) as e:
        print(f"データ解析エラー: {e}")
        sys.exit(1)  
  
root = tk.Tk()
root.title('デジタル時計')
root.geometry('700x350')
root.resizable(width=False,height=False) #ウィンドウの大きさを固定

# キャンバス作成
canvas = tk.Canvas(root, height=350, width=700)
canvas.pack() 

# 画像読込
image_list = ['WPIMGL2778_TP_V4.png','mountain_00002.png','japanese-style_00024.png','tree-woods_00049.png','japanese-style_00014.png']
img = tk.PhotoImage(file=image_list[n])

# 画像を表示
image_on_canvas = canvas.create_image(0, 0, image=img, anchor="nw")

# 日付テキストを表示
day_text = canvas.create_text(
    200, 80,
    text ="",
    fill="lime",
    font=("Helvetica", 24, "bold")
)

# 時計テキストを表示
clock_text = canvas.create_text(
    350, 175,
    text="",
    fill="lime",
    font=("Helvetica", 96, "bold")
)

# 天候テキストを表示
weather_text = canvas.create_text(
    350, 270,
    text ="",
    fill="lime",
    font=("Helvetica", 18, "bold")
)

day()
time()
weather_kanazawa()
show_image()
root.mainloop()
import tkinter as tk
from tkinter import messagebox
import csv
import os

FILE_NAME = "records.csv"


# ==================================
# 勉強記録を保存する
# ==================================
def save_record():

    subject = subject_entry.get()
    time = time_entry.get()

    # 科目が空欄かチェック
    if subject == "":
        messagebox.showwarning("入力エラー", "科目を入力してください。")
        return

    # 勉強時間が数字かチェック
    if not time.isdigit():
        messagebox.showwarning("入力エラー", "勉強時間は数字で入力してください。")
        return

    # CSVに保存
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([subject, time])

    messagebox.showinfo("保存完了", "勉強記録を保存しました！")

    # 入力欄を空にする
    subject_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

    # 表示を更新
    show_records()
    show_totals()


# ==================================
# 過去の勉強記録を表示する
# ==================================
def show_records():

    # 一度表示内容を削除
    records_text.delete("1.0", tk.END)

    if not os.path.exists(FILE_NAME):
        records_text.insert(tk.END, "まだ記録がありません。")
        return

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        records_exist = False

        for row in reader:

            if len(row) >= 2:
                records_text.insert(
                    tk.END,
                    f"{row[0]}：{row[1]}分\n"
                )

                records_exist = True

        if not records_exist:
            records_text.insert(
                tk.END,
                "まだ記録がありません。"
            )


# ==================================
# 科目別の合計勉強時間を表示する
# ==================================
def show_totals():

    # 一度表示内容を削除
    totals_text.delete("1.0", tk.END)

    if not os.path.exists(FILE_NAME):
        totals_text.insert(tk.END, "まだ記録がありません。")
        return

    totals = {}

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:

            if len(row) >= 2 and row[1].isdigit():

                subject = row[0]
                time = int(row[1])

                if subject in totals:
                    totals[subject] += time

                else:
                    totals[subject] = time

    if not totals:
        totals_text.insert(
            tk.END,
            "まだ記録がありません。"
        )
        return

    for subject, total_time in totals.items():

        totals_text.insert(
            tk.END,
            f"{subject}：{total_time}分\n"
        )


# ==================================
# メイン画面
# ==================================

root = tk.Tk()

root.title("Study Tracker")
root.geometry("600x650")


# タイトル
title_label = tk.Label(
    root,
    text="Study Tracker",
    font=("Arial", 20)
)

title_label.pack(pady=15)


# ==================================
# 科目入力
# ==================================

subject_label = tk.Label(
    root,
    text="科目"
)

subject_label.pack()

subject_entry = tk.Entry(
    root,
    width=30
)

subject_entry.pack(pady=5)


# ==================================
# 勉強時間入力
# ==================================

time_label = tk.Label(
    root,
    text="勉強時間（分）"
)

time_label.pack()

time_entry = tk.Entry(
    root,
    width=30
)

time_entry.pack(pady=5)


# ==================================
# 保存ボタン
# ==================================

save_button = tk.Button(
    root,
    text="記録する",
    command=save_record
)

save_button.pack(pady=10)


# ==================================
# 過去の記録
# ==================================

records_label = tk.Label(
    root,
    text="過去の勉強記録",
    font=("Arial", 14)
)

records_label.pack(pady=(15, 5))

records_text = tk.Text(
    root,
    width=50,
    height=10
)

records_text.pack()


# ==================================
# 科目別合計
# ==================================

totals_label = tk.Label(
    root,
    text="科目別 合計勉強時間",
    font=("Arial", 14)
)

totals_label.pack(pady=(15, 5))

totals_text = tk.Text(
    root,
    width=50,
    height=8
)

totals_text.pack()


# ==================================
# 起動時に記録を表示
# ==================================

show_records()
show_totals()


# ==================================
# アプリを起動
# ==================================

root.mainloop()
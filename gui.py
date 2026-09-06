import tkinter as tk
from tkinter import messagebox
import csv
import os

FILE_NAME = "records.csv"


# ==================================
# CSVから記録を読み込む
# ==================================
def load_records():

    if not os.path.exists(FILE_NAME):
        return []

    records = []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) >= 2:
                records.append([row[0], row[1]])

    return records


# ==================================
# CSVへ記録をすべて保存する
# ==================================
def save_all_records(records):

    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(records)


# ==================================
# 入力内容をチェックする
# ==================================
def validate_input(subject, time):

    # 前後の空白を削除
    subject = subject.strip()
    time = time.strip()

    # 学習内容が空欄
    if subject == "":
        messagebox.showwarning(
            "入力エラー",
            "学習内容を入力してください。"
        )
        return None

    # 数字ではない
    if not time.isdigit():
        messagebox.showwarning(
            "入力エラー",
            "勉強時間は1分以上の数字で入力してください。"
        )
        return None

    # 0分
    if int(time) <= 0:
        messagebox.showwarning(
            "入力エラー",
            "勉強時間は1分以上で入力してください。"
        )
        return None

    return subject, time


# ==================================
# 新しい勉強記録を保存する
# ==================================
def save_record():

    subject = subject_entry.get()
    time = time_entry.get()

    result = validate_input(subject, time)

    if result is None:
        return

    subject, time = result

    # CSVへ追加保存
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([subject, time])

    messagebox.showinfo(
        "保存完了",
        "勉強記録を保存しました！"
    )

    # 入力欄を空にする
    subject_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

    # 表示更新
    show_records()
    show_totals()


# ==================================
# 過去の勉強記録を表示する
# ==================================
def show_records():

    records_listbox.delete(0, tk.END)

    records = load_records()

    if not records:
        records_listbox.insert(
            tk.END,
            "まだ記録がありません。"
        )
        return

    # 最新の記録を上に表示
    for subject, time in reversed(records):
        records_listbox.insert(
            tk.END,
            f"{subject}：{time}分"
        )


# ==================================
# 科目別の合計時間を表示する
# ==================================
def show_totals():

    totals_text.delete("1.0", tk.END)

    records = load_records()

    if not records:
        totals_text.insert(
            tk.END,
            "まだ記録がありません。"
        )
        return

    totals = {}
    display_names = {}

    for subject, time in records:

        if not time.isdigit():
            continue

        # 大文字・小文字を区別しないためのキー
        key = subject.strip().casefold()

        if key == "":
            continue

        if key not in totals:
            totals[key] = 0

            # 最初に登録された表記を表示用として使用
            display_names[key] = subject.strip()

        totals[key] += int(time)

    if not totals:
        totals_text.insert(
            tk.END,
            "まだ記録がありません。"
        )
        return

    for key, total_time in totals.items():

        subject_name = display_names[key]

        totals_text.insert(
            tk.END,
            f"{subject_name}：{total_time}分\n"
        )


# ==================================
# 選択された記録のCSV上の位置を取得する
# ==================================
def get_selected_record_index():

    records = load_records()

    if not records:
        return None

    selected = records_listbox.curselection()

    if not selected:
        return None

    # Listboxは新しい順
    display_index = selected[0]

    # CSVは古い順なので位置を変換
    csv_index = len(records) - 1 - display_index

    return csv_index


# ==================================
# 記録を削除する
# ==================================
def delete_record():

    record_index = get_selected_record_index()

    if record_index is None:
        messagebox.showwarning(
            "選択エラー",
            "削除する記録を選択してください。"
        )
        return

    answer = messagebox.askyesno(
        "削除確認",
        "この記録を削除しますか？"
    )

    if not answer:
        return

    records = load_records()

    # 選択された1件だけ削除
    del records[record_index]

    save_all_records(records)

    messagebox.showinfo(
        "削除完了",
        "記録を削除しました。"
    )

    show_records()
    show_totals()


# ==================================
# 記録を編集する
# ==================================
def edit_record():

    record_index = get_selected_record_index()

    if record_index is None:
        messagebox.showwarning(
            "選択エラー",
            "編集する記録を選択してください。"
        )
        return

    records = load_records()

    subject, time = records[record_index]

    # 編集用ウィンドウ
    edit_window = tk.Toplevel(root)

    edit_window.title("記録を編集")
    edit_window.geometry("350x250")
    edit_window.resizable(False, False)

    title = tk.Label(
        edit_window,
        text="記録を編集",
        font=("Arial", 16)
    )
    title.pack(pady=15)

    subject_label = tk.Label(
        edit_window,
        text="学習内容"
    )
    subject_label.pack()

    edit_subject_entry = tk.Entry(
        edit_window,
        width=30
    )
    edit_subject_entry.pack(pady=5)

    edit_subject_entry.insert(
        0,
        subject
    )

    time_label = tk.Label(
        edit_window,
        text="勉強時間（分）"
    )
    time_label.pack()

    edit_time_entry = tk.Entry(
        edit_window,
        width=30
    )
    edit_time_entry.pack(pady=5)

    edit_time_entry.insert(
        0,
        time
    )

    # ==================================
    # 編集内容を保存する
    # ==================================
    def update_record():

        new_subject = edit_subject_entry.get()
        new_time = edit_time_entry.get()

        result = validate_input(
            new_subject,
            new_time
        )

        if result is None:
            return

        new_subject, new_time = result

        records = load_records()

        # 選択した記録だけ変更
        records[record_index] = [
            new_subject,
            new_time
        ]

        save_all_records(records)

        messagebox.showinfo(
            "更新完了",
            "記録を更新しました。"
        )

        edit_window.destroy()

        show_records()
        show_totals()

    update_button = tk.Button(
        edit_window,
        text="保存",
        command=update_record,
        width=12
    )

    update_button.pack(pady=15)


# ==================================
# メイン画面
# ==================================

root = tk.Tk()

root.title("Study Tracker")
root.geometry("600x720")


# ==================================
# タイトル
# ==================================

title_label = tk.Label(
    root,
    text="Study Tracker",
    font=("Arial", 20)
)

title_label.pack(pady=15)


# ==================================
# 学習内容入力
# ==================================

subject_label = tk.Label(
    root,
    text="学習内容"
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
# 記録ボタン
# ==================================

save_button = tk.Button(
    root,
    text="記録する",
    command=save_record,
    width=15
)

save_button.pack(pady=10)


# ==================================
# 過去の勉強記録
# ==================================

records_label = tk.Label(
    root,
    text="過去の勉強記録",
    font=("Arial", 14)
)

records_label.pack(pady=(15, 5))


records_listbox = tk.Listbox(
    root,
    width=50,
    height=10
)

records_listbox.pack()


# ==================================
# 編集・削除ボタン
# ==================================

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


edit_button = tk.Button(
    button_frame,
    text="編集",
    command=edit_record,
    width=10
)

edit_button.pack(
    side=tk.LEFT,
    padx=10
)


delete_button = tk.Button(
    button_frame,
    text="削除",
    command=delete_record,
    width=10
)

delete_button.pack(
    side=tk.LEFT,
    padx=10
)


# ==================================
# 科目別合計時間
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
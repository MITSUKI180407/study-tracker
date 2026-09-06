import csv
import os

# 勉強記録を保存するCSVファイル
FILE_NAME = "records.csv"


# ==============================
# 勉強記録を追加する処理
# ==============================
def add_record():

    subject = input("科目を入力してください：")
    time = input("勉強時間を入力してください（分）：")

    # 勉強時間が数字かチェックする
    if not time.isdigit():
        print("勉強時間は数字で入力してください。")
        return

    # 科目と勉強時間を1つの記録としてまとめる
    record = [subject, time]

    # CSVファイルに記録を追加する
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(record)

    print(f"{subject}を{time}分勉強した記録を保存しました！")


# ==============================
# 過去の勉強記録を表示する処理
# ==============================
def show_records():

    print("\n--- 過去の勉強記録 ---")

    # CSVファイルがまだ存在しない場合
    if not os.path.exists(FILE_NAME):
        print("まだ記録がありません。")
        return

    # CSVファイルを読み込む
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        records_exist = False

        # CSVから1行ずつ記録を取り出す
        for row in reader:

            if len(row) >= 2:
                print(f"{row[0]}：{row[1]}分")
                records_exist = True

        if not records_exist:
            print("まだ記録がありません。")


# ==============================
# 科目ごとの合計勉強時間を表示する処理
# ==============================
def show_totals():

    print("\n--- 科目別 合計勉強時間 ---")

    # CSVファイルがまだ存在しない場合
    if not os.path.exists(FILE_NAME):
        print("まだ記録がありません。")
        return

    # 科目ごとの合計時間を保存する辞書
    totals = {}

    # CSVファイルを読み込む
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        # 記録を1行ずつ確認する
        for row in reader:

            if len(row) >= 2 and row[1].isdigit():

                subject = row[0]

                # CSVから読み込んだ文字列を整数に変換
                time = int(row[1])

                # すでに同じ科目があれば時間を追加
                if subject in totals:
                    totals[subject] += time

                # 初めての科目なら新しく登録
                else:
                    totals[subject] = time

    if not totals:
        print("まだ記録がありません。")
        return

    # 科目と合計時間を順番に表示する
    for subject, total_time in totals.items():
        print(f"{subject}：{total_time}分")


# ==============================
# メインメニュー
# ==============================
def main():

    # 終了が選択されるまで繰り返す
    while True:

        print("\n===== Study Tracker =====")
        print("1. 勉強を記録する")
        print("2. 過去の記録を見る")
        print("3. 科目別の合計時間を見る")
        print("4. 終了")

        choice = input("選択してください：")

        # 選択された番号によって処理を変更する
        if choice == "1":
            add_record()

        elif choice == "2":
            show_records()

        elif choice == "3":
            show_totals()

        elif choice == "4":
            print("Study Trackerを終了します。")
            break

        else:
            print("1〜4の数字を入力してください。")


# ==============================
# プログラムを開始する
# ==============================
if __name__ == "__main__":
    main()
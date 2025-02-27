import tkinter as tk
import random

def snake_game():
    root = tk.Tk()
    root.title("破解密码")
    root.geometry("400x200")
    root.resizable(False, False)
    root.configure(bg="white")

    # 单词列表
    words = [
        "python", "algorithm", "computer", "programming", "software", 
        "hardware", "network", "database", "internet", "security", 
        "encryption", "decryption", "firewall", "malware", "phishing", 
        "ransomware", "spyware", "trojan", "virus", "worm"
    ]
    word = random.choice(words)
    guessed_word = ["_" for _ in word]
    attempts = 0  # 破解次数

    def check_letter():
        nonlocal word, guessed_word, attempts
        letter = entry.get().lower()
        if letter in word:
            for i, char in enumerate(word):
                if char == letter:
                    guessed_word[i] = letter
            output_label.config(text=" ".join(guessed_word))
            if "_" not in guessed_word:
                attempts += 1
                if attempts < 4:
                    entry.delete(0, tk.END)
                    entry.insert(0, "破解未完全完成")
                    entry.config(state='disabled')
                    root.update()
                    root.after(2000)  # 等待两秒
                    entry.config(state='normal')
                    entry.delete(0, tk.END)
                    word = random.choice(words)
                    guessed_word = ["_" for _ in word]
                    output_label.config(text=" ".join(guessed_word))
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, "密码破解！")
                    entry.config(state='disabled')
        else:
            output_label.config(text="错误的字母。")
        entry.delete(0, tk.END)

    # 输入框
    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(pady=10)

    # 检查按钮
    check_button = tk.Button(root, text="检查", command=check_letter, font=("Arial", 14))
    check_button.pack(pady=10)

    # 输出框
    output_label = tk.Label(root, text=" ".join(guessed_word), font=("Arial", 14), bg="white")
    output_label.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    snake_game()

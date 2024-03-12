import tkinter as tk
from tkinter import ttk
from openai import OpenAI
import os
import threading
import time

class AgentCatApp:
    def __init__(self):
        self.window = tk.Tk()
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        self.history = [
            {"role": "system", "content": "You are AgentCat, an autonomous AI that is a foundational private AGI. You are assembled, configured, and deployed autonomously at agents in your browser."},
            {"role": "user", "content": "Hello AgentCat, please introduce yourself to someone opening this program for the first time. Be concise."},
        ]
        self.initialize_ui()

    def initialize_ui(self):
        self.window.title("AgentCat")
        self.window.geometry("1200x800")
        self.window.resizable(False, False)
        self.window.configure(bg="#1E1E1E")

        chat_frame = ttk.Frame(self.window, padding="10")
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_history = tk.Text(chat_frame, wrap=tk.WORD, state='disabled', bg="#1E1E1E", fg="#D4D4D4", font=("Consolas", 12))
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        self.chat_history.tag_configure('user', foreground="#9CDCFE")
        self.chat_history.tag_configure('assistant', foreground="#CE9178")

        scrollbar = ttk.Scrollbar(chat_frame, command=self.chat_history.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_history['yscrollcommand'] = scrollbar.set

        style = ttk.Style()
        style.configure("Custom.TFrame", background="#252526")
        style.configure("Custom.TEntry", fieldbackground="#1E1E1E", foreground="#D4D4D4")

        input_frame = ttk.Frame(self.window, padding="10", style="Custom.TFrame")
        input_frame.pack(fill=tk.X)

        self.user_input = ttk.Entry(input_frame, font=("Consolas", 12), style="Custom.TEntry")
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", lambda event: self.send_message())

        style.configure("Custom.TButton", background="#007ACC", foreground="white")

        send_button = ttk.Button(input_frame, text="Deploy Agent", command=self.send_message, style="Custom.TButton")
        send_button.pack(side=tk.RIGHT)

        title_label = tk.Label(self.window, text="AgentCat", font=("Consolas", 24, "bold"), bg="#1E1E1E", fg="#4EC9B0")
        title_label.pack(pady=10)

        subtitle_label = tk.Label(self.window, text="Deploy AI Agents", font=("Consolas", 16), bg="#1E1E1E", fg="#9CDCFE")
        subtitle_label.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_message(self):
        user_message = self.user_input.get()
        if user_message:
            self.chat_history.configure(state='normal')
            self.chat_history.insert(tk.END, f"You: {user_message}\n", 'user')
            self.user_input.delete(0, tk.END)
            self.history.append({"role": "user", "content": user_message})

            completion = self.client.chat.completions.create(
                model="local-model",
                messages=self.history,
                temperature=0.7,
                stream=True,
            )

            new_message = {"role": "assistant", "content": ""}

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    self.chat_history.insert(tk.END, chunk.choices[0].delta.content, 'assistant')
                    new_message["content"] += chunk.choices[0].delta.content
                    self.chat_history.see(tk.END)
                    self.window.update()

            self.history.append(new_message)
            self.chat_history.configure(state='disabled')

    def on_close(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AgentCatApp()
    app.run()

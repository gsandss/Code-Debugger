import subprocess
import requests
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from tkinter import ttk
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token

# LM Studio API URL
LM_STUDIO_API = "http://127.0.0.1:5000/v1/completions"

def apply_syntax_highlighting(event):
    code = code_input.get("1.0", "end-1c")
    code_input.mark_set("range_start", "1.0")
    for token, content in lex(code, PythonLexer()):
        code_input.mark_set("range_end", f"range_start + {len(content)}c")
        if token in Token.Keyword:
            code_input.tag_add("keyword", "range_start", "range_end")
        elif token in Token.Literal.String:
            code_input.tag_add("string", "range_start", "range_end")
        elif token in Token.Comment:
            code_input.tag_add("comment", "range_start", "range_end")
        code_input.mark_set("range_start", "range_end")

def query_lm_studio(prompt):
    payload = {
        "prompt": prompt,
        "max_new_tokens": 150,
        "temperature": 0.7
    }
    response = requests.post(LM_STUDIO_API, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        raise Exception(f"Error querying LM Studio: {response.status_code} - {response.text}")

def analyze_error(error_message):
    prompt = (
        "You are a programming assistant. Explain the following Python error message in simple terms "
        "and provide suggestions to fix it:\n\n"
        f"Error Message:\n{error_message}\n\n"
        "Explanation and Suggestions:"
    )
    return query_lm_studio(prompt)

def run_code(code, output_box):
    try:
        temp_file = "temp_code.py"
        with open(temp_file, "w") as file:
            file.write(code)
        result = subprocess.run(["python", temp_file], capture_output=True, text=True)
        if result.returncode != 0:
            error_message = result.stderr
            explanation = analyze_error(error_message)
            output_box.config(state="normal")
            output_box.insert(tk.END, f"Error:\n{error_message}\n\nAI Suggestions:\n{explanation}\n")
            output_box.config(state="disabled")
        else:
            output_box.config(state="normal")
            output_box.insert(tk.END, f"Success:\n{result.stdout}\n")
            output_box.config(state="disabled")
    except Exception as e:
        output_box.config(state="normal")
        output_box.insert(tk.END, f"Unexpected Error: {e}\n")
        output_box.config(state="disabled")

def ask_chatbot(code, question):
    prompt = (
        f"You are a programming assistant. Answer the following question about this Python code:\n\n"
        f"Code:\n{code}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    return query_lm_studio(prompt)

def display_in_gui():
    def toggle_dark_mode():
        if root.tk.call("ttk::style", "theme", "use") == "default":
            # Switch to dark mode
            root.tk.call("ttk::style", "theme", "use", "alt")
            root.configure(bg="#1e1e1e")
            main_frame.configure(style="Dark.TFrame")
            code_input.config(bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff")
            output_box.config(bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff")
            header_label.config(bg="#1e1e1e", fg="#ffffff")
            code_input_label.config(bg="#1e1e1e", fg="#ffffff")
            output_box_label.config(bg="#1e1e1e", fg="#ffffff")
            question_label.config(bg="#1e1e1e", fg="#ffffff")
        else:
            # Switch to light mode
            root.tk.call("ttk::style", "theme", "use", "default")
            root.configure(bg="#f0f0f0")
            main_frame.configure(style="TFrame")
            code_input.config(bg="#ffffff", fg="#000000", insertbackground="#000000")
            output_box.config(bg="#ffffff", fg="#000000", insertbackground="#000000")
            header_label.config(bg="#333333", fg="#ffffff")
            code_input_label.config(bg="#f5f5f5", fg="#333333")
            output_box_label.config(bg="#f5f5f5", fg="#333333")
            question_label.config(bg="#f5f5f5", fg="#333333")

        # Update button styles
        style = ttk.Style()
        if root.tk.call("ttk::style", "theme", "use") == "alt":
            style.configure("TButton", background="#2d2d2d", foreground="#ffffff")
            style.map("TButton", background=[("active", "#3d3d3d")])
        else:
            style.configure("TButton", background="#f0f0f0", foreground="#000000")
            style.map("TButton", background=[("active", "#e0e0e0")])

    def debug_code():
        code = code_input.get("1.0", tk.END).strip()
        if code:
            output_box.config(state="normal")
            output_box.insert(tk.END, "Running Code...\n\n")
            output_box.config(state="disabled")
            run_code(code, output_box)

    def save_session():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("# Code:\n")
                file.write(code_input.get("1.0", tk.END))
                file.write("\n# Output:\n")
                file.write(output_box.get("1.0", tk.END))

    def load_code():
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            code_input.delete("1.0", tk.END)
            code_input.insert("1.0", code)

    root = tk.Tk()
    root.title("Code Debugger")
    root.geometry("900x700")
    font_family = "Figtree"

    style = ttk.Style()
    style.configure("Dark.TFrame", background="#1e1e1e")

    header_label = tk.Label(
        root, text="Code Debugger", font=(font_family, 18, "bold"),
        fg="#ffffff", bg="#333333", padx=10, pady=10
    )
    header_label.pack(fill=tk.X)

    main_frame = ttk.Frame(root, padding="10", style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    code_input_label = tk.Label(
        main_frame, text="Enter Code to Debug:", font=(font_family, 12, "bold"),
        fg="#333333", bg="#f5f5f5"
    )
    code_input_label.pack(anchor="w", pady=5)

    global code_input
    code_input = scrolledtext.ScrolledText(
        main_frame, wrap=tk.WORD, height=10, font=(font_family, 12),
        bg="#f5f5f5", fg="#333333", bd=2, relief=tk.SUNKEN
    )
    code_input.pack(fill=tk.BOTH, expand=True, pady=5)
    code_input.bind("<KeyRelease>", apply_syntax_highlighting)
    code_input.tag_configure("keyword", foreground="blue")
    code_input.tag_configure("string", foreground="green")
    code_input.tag_configure("comment", foreground="gray")

    output_box_label = tk.Label(
        main_frame, text="Debugger Output:", font=(font_family, 12, "bold"),
        fg="#333333", bg="#f5f5f5"
    )
    output_box_label.pack(anchor="w", pady=5)

    global output_box
    output_box = scrolledtext.ScrolledText(
        main_frame, wrap=tk.WORD, height=15, font=(font_family, 12),
        bg="#f5f5f5", fg="#333333", bd=2, relief=tk.SUNKEN, state="normal"
    )
    output_box.pack(fill=tk.BOTH, expand=True, pady=5)

    question_frame = ttk.Frame(main_frame)
    question_frame.pack(fill=tk.X, pady=5)

    question_label = tk.Label(
        question_frame, text="Ask a question about the code:", 
        font=(font_family, 12, "bold"), fg="#333333", bg="#f5f5f5"
    )
    question_label.pack(side=tk.LEFT, padx=5)

    question_entry = ttk.Entry(question_frame, width=50, font=(font_family, 12))
    question_entry.pack(side=tk.LEFT, padx=5)

    def ask_question():
        code = code_input.get("1.0", tk.END).strip()
        question = question_entry.get().strip()
        if code and question:
            output_box.config(state="normal")
            output_box.insert(tk.END, f"\nQuestion: {question}\n")
            answer = ask_chatbot(code, question)
            output_box.insert(tk.END, f"Answer: {answer}\n\n")
            output_box.config(state="disabled")
            output_box.see(tk.END)

    ask_button = ttk.Button(
        question_frame, text="Ask", command=ask_question
    )
    ask_button.pack(side=tk.LEFT, padx=5)

    button_frame = ttk.Frame(root, padding="10")
    button_frame.pack(fill=tk.X)

    debug_button = ttk.Button(
        button_frame, text="Run Debugger", command=debug_code
    )
    debug_button.pack(side=tk.LEFT, padx=10, pady=5)

    save_button = ttk.Button(
        button_frame, text="Save Session", command=save_session
    )
    save_button.pack(side=tk.LEFT, padx=10, pady=5)

    load_button = ttk.Button(
        button_frame, text="Load Code", command=load_code
    )
    load_button.pack(side=tk.LEFT, padx=10, pady=5)

    dark_mode_button = ttk.Button(
        button_frame, text="Toggle Dark Mode", command=toggle_dark_mode
    )
    dark_mode_button.pack(side=tk.LEFT, padx=10, pady=5)

    close_button = ttk.Button(
        button_frame, text="Close", command=root.destroy
    )
    close_button.pack(side=tk.RIGHT, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    display_in_gui()

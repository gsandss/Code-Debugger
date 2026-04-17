const codeInput = document.getElementById("code-input");
const outputBox = document.getElementById("output-area");
const questionInput = document.getElementById("question-input");
const runButton = document.getElementById("run-code");
const clearButton = document.getElementById("clear-code");
const askButton = document.getElementById("ask-question");

const API_BASE = "http://127.0.0.1:5000";

runButton.addEventListener("click", runCode);
clearButton.addEventListener("click", clearAll);
askButton.addEventListener("click", askAI);

async function runCode() {
    const code = codeInput.value.trim();

    if (!code) {
        outputBox.textContent = "Please enter some code to run.";
        return;
    }

    outputBox.textContent = "Running code...";

    try {
        const response = await fetch(`${API_BASE}/run`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code })
        });

        const data = await response.json();

        if (data.success) {
            outputBox.textContent = `Output:\n\n${data.output || "(No output)"}`;
        } else {
            outputBox.textContent =
                `Error:\n\n${data.error || "Unknown error"}\n\nAI Explanation:\n\n${data.ai_explanation || "No AI explanation available."}`;
        }
    } catch (error) {
        outputBox.textContent = `Could not connect to the server.\n\n${error}`;
    }
}

async function askAI() {
    const code = codeInput.value.trim();
    const question = questionInput.value.trim();

    if (!code || !question) {
        outputBox.textContent = "Please give both code and a question.";
        return;
    }

    outputBox.textContent = "Thinking...";

    try {
        const response = await fetch(`${API_BASE}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code, question })
        });

        const data = await response.json();

        if (data.success) {
            outputBox.textContent = `AI Answer:\n\n${data.answer}`;
        } else {
            outputBox.textContent = data.error || "Something went wrong.";
        }
    } catch (error) {
        outputBox.textContent = `Could not connect to the server.\n\n${error}`;
    }
}

function clearAll() {
    codeInput.value = "";
    questionInput.value = "";
    outputBox.textContent = "Output and debugging information will appear here...";
}
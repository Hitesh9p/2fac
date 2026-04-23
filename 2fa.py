from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pyotp

app = FastAPI(title="2FA Code Generator")

class SecretInput(BaseModel):
    secret: str

@app.get("/", response_class=HTMLResponse)
async def ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>2FA Code Generator</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                width: 90%;
                max-width: 400px;
            }
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
                font-size: 24px;
            }
            .input-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 500;
            }
            input[type="text"] {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            button:active {
                transform: translateY(0);
            }
            .code-display {
                margin-top: 30px;
                text-align: center;
                display: none;
            }
            .code-display.active {
                display: block;
            }
            .code {
                font-size: 48px;
                font-weight: bold;
                color: #667eea;
                letter-spacing: 8px;
                margin: 20px 0;
                font-family: 'Courier New', monospace;
            }
            .timer {
                font-size: 14px;
                color: #888;
            }
            .timer-bar {
                width: 100%;
                height: 4px;
                background: #e0e0e0;
                border-radius: 2px;
                margin-top: 10px;
                overflow: hidden;
            }
            .timer-progress {
                height: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                transition: width 1s linear;
            }
            .error {
                color: #e74c3c;
                text-align: center;
                margin-top: 10px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 2FA Code Generator</h1>
            <div class="input-group">
                <label for="secret">Secret Key (Base32)</label>
                <input type="text" id="secret" placeholder="Enter your secret key">
            </div>
            <button onclick="generateCode()">Generate Code</button>
            <div class="error" id="error"></div>
            <div class="code-display" id="codeDisplay">
                <div class="code" id="code">------</div>
                <div class="timer">Refreshes in <span id="timerText">30</span>s</div>
                <div class="timer-bar">
                    <div class="timer-progress" id="timerBar"></div>
                </div>
            </div>
        </div>

        <script>
            let timerInterval;
            let countdownInterval;

            async function generateCode() {
                const secret = document.getElementById('secret').value.trim();
                if (!secret) {
                    showError('Please enter a secret key');
                    return;
                }

                try {
                    const response = await fetch('/code', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ secret: secret })
                    });

                    if (!response.ok) throw new Error('Invalid secret');

                    const data = await response.json();
                    displayCode(data.code);
                    hideError();
                } catch (err) {
                    showError('Invalid secret key. Please check and try again.');
                }
            }

            function displayCode(code) {
                document.getElementById('code').textContent = code;
                document.getElementById('codeDisplay').classList.add('active');
                startTimer();
            }

            function startTimer() {
                let timeLeft = 30;
                updateTimerDisplay(timeLeft);

                if (timerInterval) clearInterval(timerInterval);
                if (countdownInterval) clearInterval(countdownInterval);

                timerInterval = setInterval(async () => {
                    try {
                        const secret = document.getElementById('secret').value.trim();
                        const response = await fetch('/code', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ secret: secret })
                        });
                        const data = await response.json();
                        document.getElementById('code').textContent = data.code;
                        timeLeft = 30;
                    } catch (err) {
                        console.error('Error refreshing code:', err);
                    }
                }, 30000);

                countdownInterval = setInterval(() => {
                    timeLeft--;
                    updateTimerDisplay(timeLeft);
                    if (timeLeft <= 0) timeLeft = 30;
                }, 1000);
            }

            function updateTimerDisplay(seconds) {
                document.getElementById('timerText').textContent = seconds;
                const percentage = (seconds / 30) * 100;
                document.getElementById('timerBar').style.width = percentage + '%';
            }

            function showError(msg) {
                const errorEl = document.getElementById('error');
                errorEl.textContent = msg;
                errorEl.style.display = 'block';
            }

            function hideError() {
                document.getElementById('error').style.display = 'none';
            }

            // Allow Enter key to generate code
            document.getElementById('secret').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') generateCode();
            });
        </script>
    </body>
    </html>
    """

@app.post("/code")
async def get_code(data: SecretInput):
    # Remove spaces and dashes from secret (accepts both formats)
    cleaned_secret = data.secret.replace(" ", "").replace("-", "").upper()
    totp = pyotp.TOTP(cleaned_secret)
    code = totp.now()
    return {"code": code}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

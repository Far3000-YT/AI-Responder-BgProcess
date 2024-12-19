# Online Quizz Responder using AI API (Gemini experimental model)

## Limits

*   **50 requests a day** (so 25 usages daily for each API key with the default settings)
*   A website could in theory detect what commands you are doing (if they record all the inputs).
*   You need to paste somewhere to get the response, so you need to find where.

## Usage

1. **Get an API Key:**
    *   Go to [https://ai.google.dev/aistudio](https://ai.google.dev/aistudio) and get an API key (keep it later for the environment variable).
    *   (Optional) Get a second API key with a second Google account to enable the double requests method for more uses (100 requests daily).

2. **Configure `config.yaml`:**
    *   Open the `config.yaml` file.
    *   **`model_name`:** Set this to the latest experimental model on Gemini for best results. You can find the latest models here: [https://ai.google.dev/gemini-api/docs/models/experimental-models](https://ai.google.dev/gemini-api/docs/models/experimental-models)
    *   **`base_prompt`:** This is crucial! Customize this prompt based on the subject of your quizzes. Experiment and refine it to get the best results.
    *   **`short_response`:**  (Recommended: `True`) If enabled, the script will attempt to extract only the essential answer from Gemini's output. If disabled, you will receive the entire output as a prompt.
    *   **`max_output_tokens`:** Do not change unless you encounter an error message.
    *   **`top_k`:** Refer to the Gemini documentation for details. The maximum value for Gemini 2.0 models is 40.
    *   **`double_requests`:** Set to `True` to use two API keys, alternating between them. This allows for 100 requests per day and 4 per minute. If enabled, you **must** set the environment variables `API_KEY_GEMINI` and `API_KEY_GEMINI2`. They reset at 9:00 AM France timezone.
    *   **`screenshot_cmd`:** Define the keyboard shortcut for taking a screenshot (here it is `shift+alt+ç`). You will then select two points on the screen to define the screenshot area.
    *   **`point_select`:** Define the key used to select the two points for the screenshot (e.g., `ctrl`) (you need to press `ctrl` once for the first point, release it and press it another time at the second point of the screenshot).
    *   **`ctrl_c`:** If `True` (recommended), pressing Ctrl+C will instantly send the currently copied text to Gemini and provide a response.
    *   **`promptf`:** **Do not modify this unless you understand its function.** It's crucial for the short response extraction.

3. **Set Environment Variables:**
    *   **`API_KEY_GEMINI`:** Set this environment variable to your first Gemini API key.
    *   **(Optional) `API_KEY_GEMINI2`:** If you enabled `double_requests`, set this environment variable to your second Gemini API key.

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    You need to create a file `requirements.txt` with the following content:

    ```
    pyautogui
    pyperclip
    keyboard
    pycaw
    Pillow
    google-generativeai
    comtypes
    pyyaml
    ```
   
5. **Run the script:**
   ```bash
   python bg-process-main.py
   ```

6. **How to use:**
   *   When the script is running in the background, put the command you set in `config.yaml` or just use the `ctrl+c` command when you need it. Wait a bit and you will be able to paste the response correctly. To know when the AI is loading, you can check the sound on your PC taskbar (it will blink from mute to unmute at sound level 0)
   *   I will give the ability soon in the `config.yaml` file to remove the sound blink functionality in case you don't need it / if it annoys you (if you hear music etc)

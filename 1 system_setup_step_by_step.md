# System Setup Guide — Step by Step

A simple checklist based on the class transcript. Follow the steps in order. You do **not** need to install every optional tool.

## What you will set up

1. Python — runs your Python code.
2. Visual Studio Code (VS Code) — where you write code.
3. Python and Jupyter extensions in VS Code — help VS Code run Python and notebooks.
4. A project folder — keeps your class files organized.
5. Claude Code for VS Code — lets you use Claude as a coding assistant and choose a model.
6. OBS Studio — records your screen, voice, and optional camera for assignments.
7. YouTube — uploads assignment videos so you can share the link.
8. Atrium/course dashboard — where tasks, deadlines, submissions, and feedback are managed.
9. GitHub — creates an account for future code/project work.
10. Professional/social accounts — especially LinkedIn and YouTube, as recommended by the trainer.
11. Optional AI productivity tools — ChatGPT, Gemini, Gamma, and Epic Pen, depending on your needs.

> **Recommended for beginners:** Start with Python + VS Code. Cursor and Google Antigravity are optional alternatives, not required to begin.

---

## Step 1 — Install Python

**What it does:** Python is the programming language you will learn. Your computer needs Python installed to run Python programs.

1. Open your browser.
2. Visit the official Python website: https://www.python.org/downloads/
3. Download the version for your operating system (Windows, macOS, or Linux).
4. Open the downloaded installer.
5. Follow the installation instructions.
6. Finish the installation.

### Check that Python is installed (Windows)

1. Open the **Start** menu.
2. Search for **Command Prompt** or **Terminal** and open it.
3. Type this command and press **Enter**:

```bash
python --version
```

If that does not work, try:

```bash
py --version
```

You should see a Python version number. If neither command works, revisit the installation steps.

---

## Step 2 — Install Visual Studio Code (VS Code)

**What it does:** VS Code is the editor you will use to create and manage your code files.

1. Visit the official VS Code website: https://code.visualstudio.com/
2. Download VS Code for your operating system.
3. Open the downloaded installer.
4. Follow the installation instructions.
5. Open **Visual Studio Code** after installation.

The trainer said they would use VS Code during the classes. Use it as your main editor to keep your setup simple.

---

## Step 3 — Install the Python extension in VS Code

**What it does:** The extension helps VS Code understand and run Python code.

1. Open VS Code.
2. Click the **Extensions** icon on the left.
   - Shortcut on Windows: `Ctrl + Shift + X`
3. Search for **Python**.
4. Choose the Python extension published by **Microsoft**.
5. Click **Install**.
6. Wait for installation to finish.

**Important:** Check that the publisher is Microsoft before installing.

---

## Step 4 — Install the Jupyter extension in VS Code

**What it does:** Jupyter notebooks let you write and run code in separate cells. Notebook files usually end in `.ipynb`.

1. In VS Code, open the **Extensions** panel.
2. Search for **Jupyter**.
3. Choose the Jupyter extension published by **Microsoft**.
4. Click **Install**.
5. Wait for installation to finish.

---

## Step 5 — Create a folder for your class projects

**What it does:** A project folder keeps your code and other files together.

1. Open File Explorer (Windows) or Finder (Mac).
2. Choose a location that is easy to find, such as Documents.
3. Create a new folder named:

```text
Python-Learning
```

4. Open VS Code.
5. Click **File → Open Folder**.
6. Select the `Python-Learning` folder.
7. Click **Select Folder** or **Open**.

From now on, save your class files inside this folder. You can create a separate folder for each project later.

---

## Step 6 — Test Python in two ways

The trainer showed two ways to check that Python is working: a Jupyter notebook and a regular `.py` Python file.

### A. Test with a Jupyter notebook

1. In VS Code, open the `Python-Learning` folder.
2. Create a new file and name it:

```text
test.ipynb
```

3. Open the notebook.
4. If asked to select a **kernel**, choose an available Python environment.
   - A kernel connects the notebook to Python so it can run code.
5. Create a code cell and enter:

```python
1 + 1
```

6. Click the **Run** button for that cell.

**Expected result:**

```text
2
```

If you see `2`, the notebook is running successfully.

### B. Test with a regular Python file

1. In VS Code, create a new file named `test.py`.
2. Enter this code (you can use your own name):

   ```python
   print("My name is Alex")
   ```

3. Save the file with `Ctrl + S`.
4. Open **Terminal → New Terminal**. The trainer also demonstrated `Ctrl + `` (the backtick key) as a terminal shortcut.
5. Run:

   ```bash
   python test.py
   ```

   If your system uses the Windows Python launcher, try:

   ```bash
   py test.py
   ```

6. You should see the text printed in the terminal.

If both the notebook test and the `.py` file test work, your basic Python setup is ready.

### If the notebook does not run

- Make sure Python is installed.
- Make sure the Microsoft Python and Jupyter extensions are installed.
- Click **Select Kernel** and choose a Python environment.
- If no Python environment appears, close and reopen VS Code. If the issue continues, check the Python installation.

---

## Step 7 — Optional: Try another AI coding editor

The trainer mentioned these alternatives:

- **Cursor:** https://www.cursor.com/
- **Google Antigravity:** https://antigravity.google/
- **Windsurf:** https://windsurf.com/

They provide AI-assisted coding-editor experiences. The trainer said Python and the Python/Jupyter extensions can be set up in these editors in a similar way to VS Code.

**You do not need to install all of them.** The trainer said they would use VS Code for class. Start there and try an alternative later only if you want to.

---

## Step 8 — Install Claude Code and choose a model

The trainer demonstrates **Claude Code for VS Code by Anthropic**. This is the Claude coding assistant extension, not just the regular Claude chat website.

### A. Install the Claude Code extension

1. Open **Visual Studio Code**.
2. Click the **Extensions** icon on the left. On Windows, you can also press `Ctrl + Shift + X`.
3. Search for:

   ```text
   Claude Code
   ```

4. Find **Claude Code for VS Code** published by **Anthropic**. Check the publisher so you install the official extension.
5. Click **Install** and wait for it to finish.

### B. Open Claude Code in the terminal

1. Open your project folder in VS Code.
2. Open the built-in terminal using **Terminal → New Terminal**.
3. Type this command and press **Enter**:

   ```bash
   claude
   ```

4. Claude Code should open in the terminal. If the command is not recognized, check that the extension/setup completed and follow any installation instructions shown by VS Code or Claude Code.

### C. Log in to Claude

1. In Claude Code, type:

   ```text
   /login
   ```

2. Press **Enter**.
3. Follow the prompt. It should open a browser window or provide a sign-in flow.
4. Sign in to your Anthropic account and approve the requested connection.
5. Return to VS Code and wait for Claude Code to confirm that you are signed in.

The trainer explains that first-time users need to log in through the browser. Your account must have access to Claude Code; if a plan or payment screen appears, review the options shown to you before choosing one.

### D. Select or change the model

1. In Claude Code, type:

   ```text
   /model
   ```

2. Press **Enter**.
3. Review the models offered in the menu.
4. Select the model you want to use and confirm the selection if prompted.

The trainer demonstrates changing the selected model with `/model`. The transcript's automatic captions appear to say **Opus, “Fable,” “Sonet,” and Haiku**; some model names may have been misheard by the automatic transcription. Do not rely on those captions as an exact current model list. Choose from the names actually displayed in your own model menu.

**Simple way to remember:**

- `/login` — sign in to your Claude account.
- `/model` — see the available models and switch the model.
- `claude` — open Claude Code from the VS Code terminal, as demonstrated in the class.

> **Note:** Some Claude Code features and models depend on your account, plan, and current availability. You do not need to buy multiple AI subscriptions just to follow the basic Python setup.

---

## Step 9 — Install OBS Studio for assignment recordings

**What it does:** OBS Studio records your screen and can also record your microphone and camera. The trainer used it to make videos for class tasks.

1. Visit the official OBS website: https://obsproject.com/
2. Download OBS Studio for your operating system.
3. Install it.
4. Open OBS Studio.

### Add your screen

1. Find the **Sources** section.
2. Click the **+** button.
3. Choose **Display Capture** (the name may vary slightly by system).
4. Select your main display/monitor.
5. Click **OK**.
6. If the screen does not fit the preview, right-click the source and choose **Transform → Fit to Screen**.

### Add your microphone

1. In **Sources**, click **+**.
2. Choose **Audio Input Capture**.
3. Select your microphone.
4. Click **OK**.
5. Speak and check that the audio meter moves.

### Add your camera (if you have one)

1. In **Sources**, click **+**.
2. Choose **Video Capture Device**.
3. Select your webcam.
4. Click **OK**.
5. Resize and move the camera preview to a suitable corner of the screen.

### Make a short test recording

1. Check that the screen is visible.
2. Check that the microphone meter responds when you speak.
3. Check that the camera is visible if you added one.
4. Click **Start Recording**.
5. Say a few words and open a page or file on your screen.
6. Click **Stop Recording**.
7. Play the recorded video and check the screen and sound.

**Before recording an assignment:** Close private tabs and notifications. Make sure the correct screen, microphone, and camera are selected.

*Optional later:* The trainer also mentioned vertical-video layouts/plugins for formats such as Reels. You can ignore these until you need them.

---

## Step 10 — Create or sign in to YouTube

The trainer said assignment videos should be uploaded to YouTube and the video link submitted.

1. Visit YouTube: https://www.youtube.com/
2. Sign in with your Google account, or create an account if needed.
3. Record your assignment using OBS.
4. Upload the finished video to YouTube.
5. Choose the visibility setting required by your course.

### Which visibility setting should you use?

- **Unlisted:** Anyone with the link can watch; it generally does not appear in public search results. This is often useful for sharing a submission link.
- **Private:** Only specifically permitted viewers can watch. Your trainer may not be able to view it unless access is granted.
- **Public:** Anyone can find and watch it.

Follow the course instructions. If the trainer asks for a link that they can open, make sure the visibility setting allows them to view it.

6. Copy the video link.
7. Paste the link into the required class submission area.

---

## Step 11 — Find the course submission area (Atrium)

The transcript mentions **Atrium** as part of the task/submission workflow, but it does not provide a confirmed website address or enough detail to describe every click.

1. Open your training/course dashboard.
2. Look for the Atrium or task-submission area mentioned by your trainer.
3. Open the relevant task.
4. Follow the instructions shown there.
5. Submit the requested item, such as your YouTube video link, if that is what the task asks for.

Use the exact link provided by your course dashboard or trainer. Do not guess the website address.

---

## Step 12 — Create a GitHub account

**What it does:** GitHub is used to store and share code projects. The trainer said GitHub would be covered in a later class, but suggested creating an account.

1. Visit the official GitHub website: https://github.com/
2. Click **Sign up** if you do not have an account.
3. Follow the sign-up steps, or sign in if you already have an account.
4. Keep your login details safe.
5. You can learn how to use repositories and GitHub workflows during the GitHub lessons.

---

## Step 13 — Set up professional/social accounts

The trainer mentioned these platforms:

- LinkedIn: https://www.linkedin.com/
- X (formerly Twitter): https://x.com/
- YouTube: https://www.youtube.com/
- Instagram: https://www.instagram.com/
- Facebook: https://www.facebook.com/

Start with the platforms your course specifically requires. The transcript emphasizes building a professional presence and sharing learning/task videos, but you do not need to post on every platform immediately.

### Simple professional profile checklist

- Use a clear, professional profile photo if you are comfortable doing so.
- Add a short, accurate description of your skills and learning goals.
- Keep posts relevant and professional.
- Follow your trainer's instructions about what to post and where to submit it.
- Do not share passwords, private information, or confidential work in a public post.

---

## Step 14 — AI tools mentioned in class (optional)

The trainer mentioned using AI assistants to help with learning and coding:

- ChatGPT: https://chatgpt.com/
- Claude: https://claude.ai/
- Gemini: https://gemini.google.com/

You can start with an AI tool you already have access to. A paid subscription is **not required just to complete the basic setup** described here. The trainer specifically said you do not need to pay for several tools at once.

Use AI to explain errors, clarify concepts, and review your understanding. Read and test any code before relying on it.

---

## Step 15 — Optional AI tools the trainer demonstrated

These are useful extras, not required for the first Python lesson.

### A. ChatGPT, Claude, and Gemini

The trainer showed AI assistants being used to create prompts, explain ideas, and help prepare content. You can start with an account you already have:

- ChatGPT: https://chatgpt.com/
- Claude: https://claude.ai/
- Gemini: https://gemini.google.com/

**Simple workflow:** Explain your goal to the AI assistant, ask it to draft a prompt or plan, review the answer, and verify the result before using it. Do not assume AI output is always correct.

### B. Gamma — create a presentation from a prompt

The trainer demonstrated using ChatGPT to draft a detailed prompt, then pasting that prompt into Gamma to generate a presentation.

1. Visit Gamma: https://gamma.app/
2. Sign in if required.
3. Ask an AI assistant to draft a presentation prompt that includes your topic, audience, purpose, key points, project flow, architecture, and preferred slide count.
4. Review the prompt and correct any missing or incorrect details.
5. Paste it into Gamma and generate the presentation.
6. Review every slide, verify facts, and edit the result before sharing it.

Gamma may have free and paid limits. The trainer discussed subscriptions generally but did **not** say every student must buy Gamma or another AI subscription.

### D. Subscription note from the transcript

Around **00:57:12–00:57:35**, the trainer talks about paid subscriptions used by their team, including a **$20 Gemini subscription available through their Google Workspace/G Suite arrangement**, plus other paid tools. The transcript does **not** clearly say that the $20 subscription is Claude Pro or GitHub Copilot. Do not treat the trainer's team's subscriptions as a requirement for students; check the current plan and price directly before paying.

### C. Other tools mentioned (optional)

- **Eraser:** https://www.eraser.io/ — mentioned as another tool in the AI-tool discussion.
- **Vmake:** https://vmake.ai/ — mentioned in the context of content/video tools.
- **Epic Pen:** https://epicpen.com/ — a screen-annotation tool the trainer described as free. It can help you draw or write over your screen while explaining something in a recording.

Install these only if you have a real use for them. They are not prerequisites for learning Python.

---

## Step 16 — Improve task submissions and your professional presence

The trainer emphasized consistency and submitting every assigned task.

1. Check the course dashboard for the task and its deadline.
2. Complete the task.
3. Record a clear explanation or walkthrough with OBS.
4. Upload the video to YouTube.
5. Submit the video link in the course/Atrium task area, following the exact instructions.
6. Read the feedback you receive and apply it to the next task.
7. Ask for help in your class group if you are stuck, and help classmates when you can.

### YouTube privacy: public vs. unlisted

The trainer recommends building a visible portfolio, but also explicitly says you do **not** have to make every task video public. An **unlisted** video can be shared with the trainer using its link and generally will not appear in public search. Use the visibility setting required by the course and make sure the trainer can access the video.

### LinkedIn and YouTube first

The trainer's strongest recommendation was to have at least **LinkedIn and YouTube**. X/Twitter and Instagram were discussed, but are not presented as essential for the immediate setup.

The trainer also suggested sharing useful learning updates on LinkedIn regularly (they mentioned once or twice per day). Treat that as advice, not a requirement; prioritize accurate, professional posts and follow any specific course instructions.

---

## What the transcript does not fully specify

- It mentions **Atrium**, but does not give a confirmed website address or a complete click-by-click submission process. Use the link in your course dashboard or from your trainer.
- It mentions several AI tools and paid plans, but does not establish that every student must purchase a subscription. Do not buy a plan unless you know which tool you need and what access your course requires.
- The trainer briefly mentions recording vertical videos/Reels and camera/light equipment, but these are optional presentation improvements, not necessary to get the coding environment working.

---

## Final checklist

Tick each item when it is complete.

- [ ] Python installed
- [ ] VS Code installed
- [ ] Microsoft Python extension installed
- [ ] Microsoft Jupyter extension installed
- [ ] `Python-Learning` folder created and opened in VS Code
- [ ] `test.ipynb` created
- [ ] Selected a Python kernel
- [ ] Ran `1 + 1` in a notebook and saw `2`
- [ ] Created and ran a simple `test.py` file
- [ ] Claude Code for VS Code installed (if using Claude Code)
- [ ] Logged in using `/login` (if using Claude Code)
- [ ] Selected a model using `/model` (if using Claude Code)
- [ ] OBS installed
- [ ] Tested screen recording and microphone audio
- [ ] YouTube account ready
- [ ] Know where to submit the task in the course dashboard/Atrium
- [ ] GitHub account created or signed in
- [ ] LinkedIn and YouTube accounts ready
- [ ] Know how to check task deadlines and apply feedback
- [ ] Optional tools (Gamma/Epic Pen/etc.) installed only if needed

## Recommended order for your first day

If you want to get started quickly, do only these first:

1. Install Python.
2. Install VS Code.
3. Install the Microsoft Python extension.
4. Install the Microsoft Jupyter extension.
5. Create and open your project folder.
6. Run `1 + 1` in a notebook and confirm the result is `2`.

After your coding setup works, configure OBS and YouTube for assignment submissions. Cursor and Google Antigravity are optional.

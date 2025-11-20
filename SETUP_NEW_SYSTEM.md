# Setup Guide for New System

This guide covers how to clone the repository and cherry-pick specific changes on a new machine.

---

## 🚀 Quick Start: Automated Setup (Recommended)

### Step-by-Step Execution:

#### **Step 1: Open Terminal**
- On Mac: Press `Cmd + Space`, type "Terminal", press Enter
- On Linux: Press `Ctrl + Alt + T`
- On Windows: Use Git Bash or WSL

#### **Step 2: Navigate to Your Projects Directory**
```bash
# Example: Go to your projects folder
cd ~/Projects

# Or create one if it doesn't exist
mkdir -p ~/Projects && cd ~/Projects
```

#### **Step 3: Clone the Repository**
```bash
git clone https://github.com/vishalbtathe-ux/AILegacy.git
```
**Expected output:**
```
Cloning into 'AILegacy'...
remote: Enumerating objects: 50, done.
remote: Counting objects: 100% (50/50), done.
...
```

#### **Step 4: Enter the Directory**
```bash
cd AILegacy
```

#### **Step 5: Run the Automated Setup Script**
```bash
# Make the script executable (if not already)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

**Expected output:**
```
🚀 Starting AILegacy setup...
✅ Already in AILegacy directory
🐍 Creating virtual environment...
⚡ Activating virtual environment...
📚 Installing dependencies...
...
✨ Setup complete!
```

#### **Step 6: Start Ollama (in a separate terminal)**
```bash
# Open a new terminal window/tab
ollama serve
```

#### **Step 7: Run the Application**
```bash
# Back in your original terminal
# Make sure virtual environment is activated
source venv/bin/activate

# Run the Streamlit app
streamlit run app/app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.11:8501
```

#### **Step 8: Open in Browser**
- Your browser should automatically open
- If not, go to: `http://localhost:8501`

---

## 📋 Manual Setup (Alternative Method)

If you prefer to do it step-by-step manually:

## Option 1: Clone Entire Repository (Recommended)

### Step 1: Clone the Repository
```bash
# Navigate to where you want the project
cd ~/Projects  # or your preferred location

# Clone the repository
git clone https://github.com/vishalbtathe-ux/AILegacy.git

# Enter the directory
cd AILegacy
```

### Step 2: Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
# Create .env file
touch .env

# Edit .env and add:
# OLLAMA_BASE_URL=http://localhost:11434/v1
# OLLAMA_MODEL=llama3.2:1b
```

### Step 4: Install Ollama
```bash
# Download from https://ollama.com
# Or on Mac with Homebrew:
brew install ollama

# Pull the model
ollama pull llama3.2:1b
```

### Step 5: Run the Application
```bash
# Start Ollama (if not running)
ollama serve  # In a separate terminal

# Run the Streamlit app
streamlit run app/app.py
```

---

## Option 2: Cherry-Pick Specific Commits

If you already have the repository and want to apply specific changes:

### Step 1: View Commit History
```bash
# See recent commits
git log --oneline -10

# Or view specific commits with details
git log --oneline --graph --all
```

### Step 2: Identify Commit Hash
From our recent commits:
- `83aa6e1` - Optimize performance and improve UX
- `fb903c3` - Switch from OpenAI to Ollama

### Step 3: Cherry-Pick a Specific Commit
```bash
# Cherry-pick a single commit
git cherry-pick 83aa6e1

# If there are conflicts, resolve them and continue
git cherry-pick --continue

# Or abort if needed
git cherry-pick --abort
```

### Step 4: Cherry-Pick Multiple Commits
```bash
# Cherry-pick a range of commits
git cherry-pick fb903c3..83aa6e1

# Cherry-pick specific commits (not in sequence)
git cherry-pick fb903c3 83aa6e1
```

### Step 5: Cherry-Pick from Remote
```bash
# If you're on a different branch or fresh clone
# First, fetch the latest changes
git fetch origin

# Cherry-pick from remote branch
git cherry-pick origin/main~2  # 2 commits back from main
```

---

## Option 3: Apply Specific File Changes Only

If you only want changes from specific files:

### Method A: Checkout Specific Files
```bash
# Checkout a specific file from a commit
git checkout 83aa6e1 -- agents/rag_agent.py

# Checkout multiple files
git checkout 83aa6e1 -- agents/rag_agent.py app/app.py
```

### Method B: Show and Apply Patches
```bash
# View changes in a specific commit
git show 83aa6e1

# Create a patch file
git show 83aa6e1 > changes.patch

# Apply the patch
git apply changes.patch
```

---

## Quick Reference: Our Recent Commits

### Commit: `83aa6e1`
**Message:** "Optimize performance and improve UX"
**Files Changed:**
- `agents/rag_agent.py` - Performance optimizations
- `app/app.py` - Removed feedback, added loading spinner
- `PERFORMANCE.md` - New file
- `TESTING.md` - New file
- `sample_docs/` - New sample documents

**Cherry-pick command:**
```bash
git cherry-pick 83aa6e1
```

### Commit: `fb903c3`
**Message:** "Switch from OpenAI to Ollama"
**Files Changed:**
- `agents/rag_agent.py` - Updated to use Ollama
- `requirements.txt` - Dependencies
- `verify_ollama.py` - New verification script

**Cherry-pick command:**
```bash
git cherry-pick fb903c3
```

---

## Troubleshooting

### Conflict During Cherry-Pick
```bash
# View conflicted files
git status

# Edit files to resolve conflicts (look for <<<<<<< markers)
# After resolving:
git add <resolved-files>
git cherry-pick --continue
```

### Skip a Commit
```bash
git cherry-pick --skip
```

### Undo Cherry-Pick
```bash
# If you haven't committed yet
git cherry-pick --abort

# If already committed
git reset --hard HEAD~1
```

---

## Complete Setup Script

Here's a complete script to set up on a new system:

```bash
#!/bin/bash

# Clone repository
git clone https://github.com/vishalbtathe-ux/AILegacy.git
cd AILegacy

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2:1b
EOF

# Install Ollama (Mac)
brew install ollama

# Pull model
ollama pull llama3.2:1b

# Run the app
echo "Setup complete! Run: streamlit run app/app.py"
```

Save this as `setup.sh`, make it executable with `chmod +x setup.sh`, and run with `./setup.sh`.

---

## 🎯 Common Execution Scenarios

### Scenario 1: Fresh Setup on New Mac
```bash
# Step 1: Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Step 2: Install Git (if not installed)
brew install git

# Step 3: Clone and setup
cd ~/Desktop
git clone https://github.com/vishalbtathe-ux/AILegacy.git
cd AILegacy
./setup.sh

# Step 4: Run the app
source venv/bin/activate
streamlit run app/app.py
```

### Scenario 2: Update Existing Installation
```bash
# Navigate to project
cd ~/Projects/AILegacy

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt --upgrade

# Run the app
streamlit run app/app.py
```

### Scenario 3: Cherry-Pick Only Performance Improvements
```bash
# Navigate to your existing project
cd ~/Projects/AILegacy

# Fetch latest commits
git fetch origin

# Cherry-pick only the performance commit
git cherry-pick 83aa6e1

# If conflicts occur, resolve them
# Edit conflicted files, then:
git add .
git cherry-pick --continue

# Test the changes
source venv/bin/activate
streamlit run app/app.py
```

### Scenario 4: Get Only Specific Files
```bash
# Get only the optimized RAG agent
git checkout 83aa6e1 -- agents/rag_agent.py

# Get only the improved UI
git checkout 83aa6e1 -- app/app.py

# Commit the changes
git add agents/rag_agent.py app/app.py
git commit -m "Applied performance optimizations"
```

---

## 📅 Daily Usage Commands

### Starting the Application
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run the app
cd ~/Projects/AILegacy
source venv/bin/activate
streamlit run app/app.py
```

### Running Tests
```bash
cd ~/Projects/AILegacy
source venv/bin/activate
PYTHONPATH=. python3 tests/test_cli.py
```

### Checking Status
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check available models
ollama list

# Check git status
git status
```

---

## 🔧 Environment Configuration

### Edit .env File
```bash
# Open .env in your editor
nano .env
# or
code .env  # if using VS Code
```

### Recommended .env Settings
```bash
# For fastest performance
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2:1b

# For better quality (slower)
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3

# For balanced performance
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=phi3:mini
```

---

## 🆘 Quick Troubleshooting

### Problem: "Command not found: ollama"
```bash
# Install Ollama
brew install ollama
# or download from https://ollama.com
```

### Problem: "Connection refused" when running app
```bash
# Start Ollama in a separate terminal
ollama serve

# Then run the app again
streamlit run app/app.py
```

### Problem: "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Slow responses
```bash
# Switch to faster model
ollama pull llama3.2:1b

# Update .env
echo "OLLAMA_MODEL=llama3.2:1b" >> .env
```

### Problem: Port already in use
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or use a different port
streamlit run app/app.py --server.port 8502
```

---

## 📝 Summary Cheat Sheet

```bash
# SETUP (one-time)
git clone https://github.com/vishalbtathe-ux/AILegacy.git
cd AILegacy
./setup.sh

# DAILY USE
ollama serve                    # Terminal 1
source venv/bin/activate        # Terminal 2
streamlit run app/app.py        # Terminal 2

# UPDATE
git pull origin main
pip install -r requirements.txt --upgrade

# CHERRY-PICK
git cherry-pick 83aa6e1

# TEST
PYTHONPATH=. python3 tests/test_cli.py
```

---

**Need help?** Check the other documentation files:
- `PERFORMANCE.md` - Performance optimization tips
- `TESTING.md` - Testing guide
- `README.md` - Project overview


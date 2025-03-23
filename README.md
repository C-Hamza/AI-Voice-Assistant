# 🎤 AI Voice Assistant  
A Python-based voice-controlled assistant with wake word detection, speech recognition, and system integration.

**Features:**  
- 🛎️ Wake word detection using Picovoice Porcupine  
- 🗣️ Speech-to-text via OpenAI Whisper  
- 🔊 Natural-sounding TTS with ElevenLabs  
- 💻 System control (apps, media, files)  
- 📅 Basic query handling (time/date/weather)  

**Tech Stack:**  
- Python  
- OpenAI Whisper  
- ElevenLabs API  
- Picovoice Porcupine  
- SoundDevice/SoundFile  

### **Installation Notes for AI Voice Agent**  

#### **1️⃣ Install System Dependencies**  
- **Windows:**  
  - Install FFmpeg using Chocolatey:  
    ```bash
    choco install ffmpeg
    ```
  - Or manually download **FFmpeg** and add it to **PATH**.  

---

#### **2️⃣ Install PyTorch with GPU Support** *(For NVIDIA GPU users only)*  
- First, uninstall existing **torch** and **torchaudio**:  
  ```bash
  pip uninstall torch torchaudio -y
  ```
- Then, install the CUDA-enabled version:  
  ```bash
  pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

---

#### **3️⃣ Fix Errors with PvPorcupine** *(Wake Word Detection Library)*  
- If you face issues, upgrade it:  
  ```bash
  pip install --upgrade pvporcupine
  ```

---

#### **4️⃣ Setup ElevenLabs for TTS (Optional)**  
- **Get an API Key** from [ElevenLabs](https://elevenlabs.io/)  
- Add it to the **`.env`** file:  
  ```env
  ELEVENLABS_API_KEY="your-api-key"
  PICOVOICE_ACCESS_KEY="your-picovoice-key"
  ```


## 🚀 Quick Start  
1. Clone the repo:  
   `git clone https://github.com/C-Hamza/AI-Voice-Assistant.git`  
2. Install dependencies:  
   `pip install -r requirements.txt`  
3. Add API keys to `.env` file  
4. Run:  
   `python assistant.py`  

## 📂 Project Structure  

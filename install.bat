@echo off
REM Create a virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install Python packages
pip install pvporcupine==3.0.2 sounddevice==0.4.6 soundfile==0.12.1 openai-whisper==20231117 torch==2.1.0 torchaudio==2.1.0 elevenlabs==0.2.28 gtts==2.4.0 rasa==3.6.15 python-dotenv==1.0.0 requests==2.31.0 numpy==1.24.4 scipy==1.10.1

REM Install PyTorch with CPU support (if no GPU)
pip uninstall torch torchaudio -y
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

echo Installation complete! Don't forget to add FFmpeg to your PATH.
pause
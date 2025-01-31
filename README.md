# TARS - ChatGPT-4 Powered Voice Assistant #

🚀 A voice-controlled AI assistant powered by OpenAI's GPT-4.  

   -----## ⚠️ Important ⚠️ ##----
**YOU NEED YOUR OWN API KEY FROM OPENAI**  
      https://platform.openai.com

---

## 📌 Setup  

### 1. Install Dependencies  
Run the following command to install the required libraries:  
```sh
pip install openai pyttsx3 SpeechRecognition
```
*(DO AT YOUR OWN RISK. I AM NOT RESPONSIBLE FOR ANY DAMAGE DONE TO YOUR COMPUTER.)*  

### 2. Running the Assistant  
Navigate to the file location:  
```sh
cd /Path/to/File/location
```
Run the script:  
```sh
python3 tars.py
```

---

## 📝 Notes  
- Ensure your OpenAI API key is set correctly in the script or as an environment variable.  
- The voice index for `pyttsx3` may need to be adjusted depending on your system.  

---

## 🔧 Troubleshooting  
If you face issues with **speech recognition**, install PortAudio:  

**For macOS:**  
```sh
brew install portaudio
```
```sh
pip install pyaudio
```



---

Enjoy using TARS! 🚀  

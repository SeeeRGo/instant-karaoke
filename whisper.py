import whisper

model = whisper.load_model("base")
result = model.transcribe("01 - Bela Kiss.mp3")
print(result["text"])
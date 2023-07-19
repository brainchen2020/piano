import uvicorn
from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
import base64
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#挂在目录
app.mount("/media", StaticFiles(directory="./media"), name="media")
app.mount("/min", StaticFiles(directory="./min"), name="min")
app.mount("/inc", StaticFiles(directory="./inc"), name="inc")
app.mount("/soundfont", StaticFiles(directory="./soundfont"), name="soundfont")

#将文件转换成base64编码
def write_midi_file(filename, data):
    midi_file = open(filename, "wb")
    decodestring = base64.b64decode(data)
    midi_file.write(decodestring)
    midi_file.close()
#读取midi文件编码base64数据
def read_midi_file(filename):
    midi_file1 = open(filename, "rb")
    midi_data = midi_file1.read()
    midi_file1.close()
    midi_base64 = base64.b64encode(midi_data)
    return str(midi_base64, encoding='utf-8')

@app.get('/', response_class=HTMLResponse)
async def root():
    index_html = open("index.html", 'r').read()
    return index_html


midi_dir = "midi/"
@app.get("/piano/midi-to-text")
async def midi_to_json(query: Optional[str] = Query('')):
    print(midi_dir+query)
    try:
        midi_data = read_midi_file(midi_dir+query)
    except Exception as e:
        print(e)
        midi_data = ""
    response = f"""Piano.loadExternalMIDICallback('data:audio/midi;base64,{midi_data}')"""

    return Response(content= response, media_type= "text/plain")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
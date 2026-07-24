from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Annotated
from reserachagent import ResearchAgent
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

research_agent = None


class UserQuery(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Welcome to the Research Agent API!"}


@app.post("/uploadfile/")
async def upload_files(
    files: Annotated[List[UploadFile], File(description="Multiple PDF files")]
):
    global research_agent

    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No PDF files uploaded.")

    pdf_paths = []

    try:
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)

            content = await file.read()

            with open(file_path, "wb") as f:
                f.write(content)

            pdf_paths.append(file_path)

        research_agent = ResearchAgent(pdf_paths)
        research_agent.create_embeddings()
        research_agent.build_chain()

        return {
            "message": "Files uploaded and processed successfully."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(query: UserQuery):

    global research_agent

    if research_agent is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload PDFs first."
        )

    answer = research_agent.ask(query.question)

    return {"answer": answer}

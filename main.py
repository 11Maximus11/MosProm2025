from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from utils.logging_config import setup_logging

# Импортируем всех агентов
from agents.retriever import RetrieverAgent
from agents.generator import GeneratorAgent
from agents.analyzer import AnalyzerAgent
from agents.classifier import ClassifierAgent
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
from agents.personalizer import PersonalizerAgent
from agents.orchestrator import OrchestratorAgent # Импортируем нового оркестратора

# --- Настройка ---
setup_logging()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Модели данных API ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    action: dict | None = None

# --- Инициализация Агентов ---
# Создаем одного агента-оркестратора, который будет управлять остальными
orchestrator = OrchestratorAgent()
print("\n--- СЕРВЕР ГОТОВ К РАБОТЕ ---\n")

# --- Логика Оркестратора ---
async def process_ticket_logic(user_query: str) -> str:
    """
    Основная логика обработки запроса. Вызывает агентов в нужной последовательности.
    """
    # Теперь вся логика инкапсулирована в оркестраторе
    final_answer = await orchestrator.process_query(user_query)
    return final_answer

# --- Эндпоинты ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Отдает главную HTML-страницу."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat/")
async def process_chat_api(request: Request):
    """Принимает JSON-запрос от UI, обрабатывает его и возвращает JSON-ответ."""
    try:
        # Получаем данные напрямую из запроса
        data = await request.json()
        message = data.get("message", "")
        
        # Обрабатываем сообщение
        answer_text = await process_ticket_logic(message)
        
        # Возвращаем ответ
        return {"response": answer_text, "action": None}
    except Exception as e:
        print(f"Error processing request: {e}")
        return {"response": f"Произошла ошибка при обработке запроса: {str(e)}", "action": None}
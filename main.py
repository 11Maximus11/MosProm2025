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

# --- Настройка ---
setup_logging()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Модели данных API ---
class TicketRequest(BaseModel): text: str
class TicketResponse(BaseModel): answer: str

# --- Инициализация Агентов ---
retriever = RetrieverAgent()
generator = GeneratorAgent()
analyzer = AnalyzerAgent()
classifier = ClassifierAgent()
planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()
personalizer = PersonalizerAgent()
print("\n--- СЕРВЕР ГОТОВ К РАБОТЕ ---\n")

# --- Логика Оркестратора ---
def process_ticket_logic(user_query: str) -> str:
    # MVP-цепочка: Используем только retriever и generator
    # Остальные агенты вызываются, но их результат (заглушка) не используется
    
    classification = classifier.classify(user_query)
    analysis = analyzer.analyze(user_query)
    
    # 1. Поиск релевантной информации (реальный шаг MVP)
    context = retriever.retrieve_documents(analysis['full_text'])
    
    plan = planner.plan_actions(analysis['full_text'], context)
    execution_report = executor.execute_plan(plan)

    # 2. Генерация ответа (реальный шаг MVP)
    draft_answer = generator.generate_final_answer(user_query, context, execution_report)
    
    verification = verifier.verify(user_query, draft_answer)
    if verification['decision'] != 'approve':
        return "Ответ системы не прошел внутреннюю проверку. Обращение передано оператору."

    final_answer = personalizer.personalize(draft_answer, {})
    return final_answer

# --- Эндпоинты ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request): return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/process_ticket", response_model=TicketResponse)
async def process_ticket_api(ticket: TicketRequest):
    answer_text = process_ticket_logic(ticket.text)
    return TicketResponse(answer=answer_text)
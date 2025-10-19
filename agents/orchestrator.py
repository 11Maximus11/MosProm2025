import asyncio
from agents.retriever import RetrieverAgent
from agents.generator import GeneratorAgent
from agents.analyzer import AnalyzerAgent
from agents.classifier import ClassifierAgent
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
from agents.personalizer import PersonalizerAgent

class OrchestratorAgent:
    """
    Главный агент, который управляет всем процессом обработки запроса.
    Он вызывает других агентов асинхронно, где это возможно, чтобы ускорить ответ.
    """
    def __init__(self):
        # Инициализируем всех дочерних агентов один раз
        self.retriever = RetrieverAgent()
        self.generator = GeneratorAgent()
        self.analyzer = AnalyzerAgent()
        self.classifier = ClassifierAgent()
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.verifier = VerifierAgent()
        self.personalizer = PersonalizerAgent()

    async def process_query(self, user_query: str) -> str:
        """
        Обрабатывает запрос пользователя, координируя работу других агентов.
        """
        # Шаг 1: Параллельный запуск анализа и классификации
        # Эти агенты не зависят друг от друга и могут работать одновременно
        analysis_task = asyncio.create_task(self.analyzer.analyze_async(user_query))
        classification_task = asyncio.create_task(self.classifier.classify_async(user_query))
        
        analysis, classification = await asyncio.gather(analysis_task, classification_task)

        # Шаг 2: Поиск релевантной информации (зависит от анализа)
        context = await self.retriever.retrieve_documents_async(analysis['full_text'])

        # Шаг 3: Планирование и выполнение (зависят от предыдущих шагов)
        plan = await self.planner.plan_actions_async(analysis['full_text'], context)
        execution_report = await self.executor.execute_plan_async(plan)

        # Шаг 4: Генерация ответа (зависит от всех предыдущих данных)
        draft_answer = await self.generator.generate_final_answer_async(user_query, context, execution_report)

        # Шаг 5: Проверка и персонализация
        # Эти шаги выполняем асинхронно
        verification = await self.verifier.verify_async(user_query, draft_answer)
        if verification['decision'] != 'approve':
            return "Ответ системы не прошел внутреннюю проверку. Обращение передано оператору."

        # Передаем пустой словарь в качестве профиля пользователя
        user_profile = {}
        final_answer = await self.personalizer.personalize_async(draft_answer, user_profile)
        return final_answer

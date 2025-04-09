from database.models_db import QuestionAndAnswerModel
from typing import Optional
from admin_folder.admin_verification import get_current_admin
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Form, HTTPException, Depends

templates = Jinja2Templates(directory="templates/admin_pages")
router = APIRouter()

@router.get("/admin/questions", response_class=HTMLResponse, tags=["questions_admin"])
async def admin_questions(request: Request,
                          username: str = Depends(get_current_admin)):
    """ Страница с вопросами и ответами """
    questions = await QuestionAndAnswerModel.all()
    return templates.TemplateResponse('admin_questions.html', {"request": request,
                                                               'questions': questions})


@router.get("/admin/add_question", response_class=HTMLResponse, tags=["questions_admin"])
async def admin_add_questions(request: Request,
                              username: str = Depends(get_current_admin)):
    """ Отправление формы с добавлением вопроса """
    return templates.TemplateResponse('add_question.html', {"request": request})


@router.post("/admin/save_add_question", tags=["questions_admin"])
async def admin_save_add_questions(question: str = Form(),
                                   answer: str = Form(),
                                   article: Optional[str] = Form(None),
                                   username: str = Depends(get_current_admin)):
    """ Сохранение формы с добавлением вопроса """
    question = question.strip()
    answer = answer.strip()
    article = article.strip() if article else None
    print(f"Received: question={question}, answer={answer}, article={article}")
    await QuestionAndAnswerModel.create(question=question,
                                        answer=answer,
                                        article=article)

    return RedirectResponse(url='/admin/questions', status_code=303)


@router.get("/admin/edit_question/{question_id}", tags=["questions_admin"])
async def admin_edit_questions(request: Request, question_id: int, username: str = Depends(get_current_admin)):
    """" Редактирование вопросов-ответов"""
    question = await QuestionAndAnswerModel.get(id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    return templates.TemplateResponse("edit_question.html", {"request": request, "question": question})


@router.post("/admin/save_edit_question/{question_id}", tags=["questions_admin"])
async def admin_save_edit_questions(question_id: int,
                          question: str = Form(),
                          answer: str = Form(),
                          article: str = Form(),
                          username: str = Depends(get_current_admin)):
    """ Сохранение формы с редактированием вопроса """
    question_and_answer = await QuestionAndAnswerModel.get(id=question_id)
    question_and_answer.question = question.strip()
    question_and_answer.answer = answer.strip()
    question_and_answer.article = article.strip() if article else None
    print(f"Received: question={question}, answer={answer}, article={article}")
    await question_and_answer.save()

    return RedirectResponse('/admin/questions', status_code=303)

@router.post("/admin/delete_question/{question_id}", tags=["questions"])
async def admin_delete_question(question_id: int, username: str = Depends(get_current_admin)):
    """ Удаление данных """
    try:
        question = await QuestionAndAnswerModel.get(id=question_id)
        print(f'question: {question}')
        if question:
            await question.delete()
            return RedirectResponse(url='/admin/questions', status_code=303)
        return {"error": "Вопрос не найден"}
    except Exception as e:
        return {"error": f"Произошла ошибка удаления вопроса: {e}"}
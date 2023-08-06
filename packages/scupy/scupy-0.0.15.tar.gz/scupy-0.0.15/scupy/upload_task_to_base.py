# Это программа для разработки, если вы случайно тут, то выйдите, пожалуйста, и ничего не ломайте
# ID меняется вручную, молю всех не продолбить это (я перед экзом поревьюю, но не обещаю)
# если вы не уверены в задаче, но хотите ее добавить в базу, пишите тем, кто знает тервер чтобы проверили
# если вы считаете, что это говнокод и соберете лучше -- пишите свою либу и шерьте со всеми
# если вы пришли с фичреквестом -- пишите dashkaz или rozyev23

import json
import pathlib

my_own_task = {
    "id" : 1,
    "unit": "test",
    "task_text": "сложите два числа",
    "task_solution_code_analytics":
        """
a = 1
b = 5
print(a + b)
        """,
    "task_solution_code":
        """
a = 1
b = 5
print(sum(a, b))
        """
}
new_task = json.dumps(my_own_task, ensure_ascii=False)
with open(pathlib.Path(pathlib.Path(pathlib.Path.cwd(), "task_struct", "tasks_base.json")), "a", encoding="UTF8") as f:
    f.write(new_task)

# NLP4Code / LLM as coding assistant

## Навигация
сделаю потом

## Введение
Прикладная цель проекта - добиться высоких результатов на лидерборде swebench 
- Идея (1) - LLM RAG с примерами кодинга и коррекцией кода

## Описание данных/модели/инструментов/подходов
поскольку swebench содержит 300 issues (на разных языках), причем достаточно сложных и с наличием связанных компонентов, то сначала хотелось бы опробовать подход на данных более простой структуры (см ссылку python-errors)

Модель : Codestral API

## Процесс интеракции с моделью
Flask:
 

## Результаты
Идея - добавить собственную метрику (для swebench она может быть прокси-метрикой), которая будет работать следующим образом:
1) выполняем аутпут модели (где инпут - рабочий фрагмент кода)
2) если изначальный код падал с ошибкой, а исправленный моделью код отрабатывает без ошибки, то ставим "1", и "0" - иначе.
3) стоит помнить, что в таком случае может нарушаться логический замысел кода, т.е. не факт, что аутпут модели возвращает именно то, что хотел юзер, даже если код не падает в ошибку
4) но он является своеобразным показателям качества "обращения" к модели
5) вряд ли модель будет "хакать" код, где просто закомментит все и не будет ошибок, но тоже можно поресерчить

## Метрики

| **Evaluation Criterion**       | **Description**                                                                         | **Common Benchmarks/Tools**         | **Value**|
|---------------------------------|----------------------------------------------------------------------------------------|-------------------------------------|-----|
| Functional Correctness          | Measures whether generated code passes all unit tests or solves the given problem.     | HumanEval, MBPP, DS-1000, APPS      | -   |
| Syntactic Closeness             | Assesses similarity to reference code using metrics like BLEU, CodeBLEU, or ROUGE.     | CodeXGLUE, NaturalCC Toolkit        | -   |
| Semantic Accuracy               | Evaluates whether the code's logic aligns with the problem requirements.               | APPS, CoderEval                     | -   |
| Completion Rate                 | Proportion of tasks successfully completed by the model.                               | MathQA-Python, EvoCodeBench         | -   |
| Execution Accuracy              | Checks if the code runs without errors and provides correct outputs.                   | JuICe, Exec-CSN                     | -   |
| Efficiency Metrics              | Considers the computational complexity or runtime efficiency of generated code.        | Multipl-E                           | -   |
| Natural Language Understanding  | Assesses how well the model interprets problem descriptions and maps them to code.     | ClassEval, CodeSearch               | -   |
| Generalization to New Domains   | Evaluates the model’s performance on unseen or diverse datasets.                       | HumanEval+, Multipl-E               | -   |
| Explainability                  | Ability to generate readable, maintainable, and well-commented code.                   | None explicitly                     | -   |
| Learning and Adaptation         | Measures how effectively a model can fine-tune or adapt to new coding styles or tasks. | APPS, HumanEval                     | -   |


## Ссылки

- [swebench-lite](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Lite)
- [huggingface dataset python-errors](https://huggingface.co/datasets/TacoPrime/errored_python)

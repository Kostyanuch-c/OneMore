import { Card, CardBody } from "@heroui/card";

export default function LessonsPage() {
  return (
    <section className="py-8 md:py-10">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
        <header className="space-y-4">
          <h1 className="text-3xl font-bold md:text-4xl">
            Как проходят занятия
          </h1>
          <p className="text-default-600">
            Занятия проходят индивидуально с преподавателем и подстраиваются под
            цель ученика: разобрать сложную тему, подготовиться к контрольной,
            закрыть пробелы или системно готовиться к экзамену.
          </p>
          <p className="text-default-600">
            Обычно занятия проходят онлайн и длятся около 1,5 часов.
            Преподаватель использует презентации, задачи, схемы, разборы решений
            и дополнительные материалы, чтобы тема была не просто пройдена, а
            действительно понята.
          </p>
          <p className="text-default-600">
            Формат может отличаться у разных преподавателей, потому что у
            каждого есть свой опыт, подход и сильные стороны. Общая идея
            остается одной: сначала понять текущий уровень ученика, затем
            разобрать слабые места и постепенно выстроить понятный маршрут
            обучения.
          </p>
          <p className="text-default-600">
            Можно заниматься регулярно по плану или обратиться разово, например
            перед контрольной, проверочной работой, экзаменом или для разбора
            конкретной темы.
          </p>
        </header>

        <div className="space-y-4">
          <h2 className="text-2xl font-bold">Два основных формата занятий</h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <Card className="border border-primary/20 bg-linear-to-r from-primary/10 to-primary/5">
              <CardBody className="space-y-4">
                <div className="space-y-1">
                  <h3 className="text-xl font-semibold text-foreground">
                    Классический формат
                  </h3>
                  <p className="text-default-600">
                    Длительная и системная подготовка заранее для максимально
                    высокого результата.
                  </p>
                </div>
                <div className="space-y-2">
                  <p className="text-sm font-medium text-foreground">Плюсы</p>
                  <ul className="list-disc space-y-1 pl-5 text-default-600">
                    <li>Материал усваивается постепенно и устойчиво.</li>
                    <li>Есть время закрыть базу и отработать сложные темы.</li>
                    <li>Проще держать стабильный прогресс без перегруза.</li>
                    <li>Выше потенциал по итоговому баллу на экзамене.</li>
                  </ul>
                </div>
                <div className="space-y-2">
                  <p className="text-sm font-medium text-foreground">
                    Ограничения
                  </p>
                  <ul className="list-disc space-y-1 pl-5 text-default-600">
                    <li>Требует больше времени и регулярности.</li>
                    <li>Нужно начинать заранее и соблюдать план.</li>
                  </ul>
                </div>
              </CardBody>
            </Card>

            <Card className="border border-primary/20 bg-linear-to-r from-primary/10 to-primary/5">
              <CardBody className="space-y-4">
                <div className="space-y-1">
                  <h3 className="text-xl font-semibold">Экспресс-формат</h3>
                  <p className="text-default-600">
                    Интенсивная подготовка за короткий срок, когда до экзамена
                    остается мало времени.
                  </p>
                </div>
                <div className="space-y-2">
                  <p className="text-sm font-medium text-foreground">Плюсы</p>
                  <ul className="list-disc space-y-1 pl-5 text-default-600">
                    <li>Быстрый фокус на ключевых темах и типовых задачах.</li>
                    <li>Часто позволяет за короткий срок пройти порог.</li>
                    <li>
                      Реалистичная цель в таком формате обычно 60-70 баллов.
                    </li>
                  </ul>
                </div>
                <div className="space-y-2">
                  <p className="text-sm font-medium text-foreground">
                    Ограничения
                  </p>
                  <ul className="list-disc space-y-1 pl-5 text-default-600">
                    <li>Высокая нагрузка и плотный темп.</li>
                    <li>
                      Без прочной базы сложнее выйти на заметно более высокий
                      результат.
                    </li>
                  </ul>
                </div>
              </CardBody>
            </Card>
          </div>
          <p className="text-default-600">
            Форматы можно комбинировать: например, начать с экспресс-подготовки,
            чтобы быстро закрыть ближайшую цель, а затем перейти в классический
            ритм для более глубокого результата. План занятий всегда
            подстраивается под уровень ученика, сроки, учебную нагрузку и
            конкретный запрос, и мы готовы гибко идти навстречу в этом выборе.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <Card className="border border-default-200/70">
            <CardBody className="space-y-3">
              <h2 className="text-xl font-semibold">Кому подойдут занятия</h2>
              <ul className="list-disc space-y-2 pl-5 text-default-600">
                <li>Если сложно разобраться в теме самостоятельно.</li>
                <li>Если скоро контрольная или экзамен.</li>
                <li>Если есть пробелы за прошлые классы.</li>
                <li>Если хочется больше практики по задачам.</li>
                <li>
                  Если нужен преподаватель, который объяснит спокойно и понятно.
                </li>
              </ul>
            </CardBody>
          </Card>

          <Card className="border border-default-200/70">
            <CardBody className="space-y-3">
              <h2 className="text-xl font-semibold">
                Что может быть на занятии
              </h2>
              <ul className="list-disc space-y-2 pl-5 text-default-600">
                <li>Объяснение темы и ключевых принципов.</li>
                <li>Разбор задач разного уровня сложности.</li>
                <li>Работа с ошибками и сложными моментами.</li>
                <li>Подготовка к контрольной, проверочной или экзамену.</li>
                <li>Домашнее задание для закрепления.</li>
                <li>Рекомендации, что повторить и потренировать дальше.</li>
              </ul>
            </CardBody>
          </Card>
        </div>
      </div>
    </section>
  );
}

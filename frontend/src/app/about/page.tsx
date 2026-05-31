import { Card, CardBody } from "@heroui/card";

export default function AboutPage() {
  return (
    <section className="py-8 md:py-10">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-8">
        <header className="space-y-4">
          <h1 className="text-3xl font-bold md:text-4xl">О проекте</h1>
          <p className="text-default-600">
            Наш проект объединяет задания, решения и преподавателей по разным
            предметам. Здесь можно самостоятельно тренироваться, разбирать
            сложные темы и находить репетитора, если нужна индивидуальная
            помощь, в том числе для подготовки к вступительным испытаниям и
            экзаменам в вузе.
          </p>
          <p className="text-default-600">
            Мы хотим сделать обучение понятнее и спокойнее: не просто показать
            правильный ответ, а объяснить ход решения, логику рассуждений и
            помочь закрыть пробелы в знаниях.
          </p>
        </header>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <Card className="border border-default-200/70">
            <CardBody className="space-y-3">
              <h2 className="text-xl font-semibold">Кому полезен сайт</h2>
              <ul className="list-disc space-y-2 pl-5 text-default-600">
                <li>
                  Школьникам, которые готовятся к контрольным и проверочным.
                </li>
                <li>Тем, кто готовится к ОГЭ и ЕГЭ по предмету.</li>
                <li>
                  Выпускникам, которым нужна помощь с подготовкой к
                  вступительным экзаменам.
                </li>
                <li>
                  Студентам, которым нужна поддержка при подготовке к экзаменам
                  в вузе.
                </li>
                <li>Тем, кто хочет увереннее разбираться в сложных темах.</li>
                <li>Тем, кому нужно закрыть отдельные пробелы в знаниях.</li>
              </ul>
            </CardBody>
          </Card>

          <Card className="border border-default-200/70">
            <CardBody className="space-y-3">
              <h2 className="text-xl font-semibold">
                Что можно делать на сайте
              </h2>
              <ul className="list-disc space-y-2 pl-5 text-default-600">
                <li>
                  Тренироваться на заданиях и сверяться с разбором решения.
                </li>
                <li>
                  Разбирать логику решения шаг за шагом, а не только ответ.
                </li>
                <li>Использовать материалы для самостоятельной подготовки.</li>
                <li>
                  При необходимости обратиться к преподавателю за консультацией
                  или регулярными занятиями.
                </li>
              </ul>
            </CardBody>
          </Card>

          <Card className="border border-primary/20 bg-linear-to-r from-primary/10 to-primary/5 md:col-span-2">
            <CardBody className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">
                Почему проекту можно доверять
              </h2>
              <p className="text-default-600">
                В материалах делаем акцент на понятных объяснениях и
                последовательном ходе решения. Цель проекта не в том, чтобы дать
                шаблонный ответ, а помочь разобраться в теме и применять знания
                в похожих задачах.
              </p>
              <p className="text-default-600">
                В проекте постепенно появляются новые предметы, задания, решения
                и преподаватели. Наша цель — собрать удобное место, где ученик
                может найти и практику, и понятное объяснение, и живую помощь от
                репетитора.
              </p>
            </CardBody>
          </Card>
        </div>
      </div>
    </section>
  );
}

import { Card, CardBody } from "@heroui/card";
import { Chip } from "@heroui/chip";

export default function HowItWorks() {
  const steps = [
    "Выберите предмет в меню «Задачи»",
    "Подберите задачи по разделу и теме",
    "Разберите решение шаг за шагом",
  ];

  return (
    <Card className="w-full max-w-6xl mb-12">
      <CardBody>
        <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
          <div className="shrink-0">
            <h2 className="text-xl font-bold">Как начать</h2>
            <p className="text-default-600">
              Быстрый путь к нужной задаче на платформе.
            </p>
          </div>

          <div className="grid flex-1 grid-cols-1 gap-4 md:grid-cols-3 md:pl-8">
            {steps.map((step, index) => (
              <div key={step} className="flex items-center gap-3">
                <Chip color="primary" radius="full" size="sm" variant="flat">
                  {index + 1}
                </Chip>

                <span className="text-default-700">{step}</span>
              </div>
            ))}
          </div>
        </div>
      </CardBody>
    </Card>
  );
}

"use client";

import { Card, CardBody } from "@heroui/card";

function LessonAccessInfo() {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Материалы и личный кабинет</h2>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card className="border border-default-200/70">
          <CardBody className="space-y-3">
            <h3 className="text-xl font-semibold">Для учеников</h3>
            <p className="text-default-600">
              После записи на занятия открывается личный кабинет с расписанием,
              материалами уроков и презентациями, подготовленными под обучение.
            </p>
            <p className="text-default-600">
              Это помогает держать все материалы в одном месте и возвращаться к
              ним после занятия для повторения.
            </p>
          </CardBody>
        </Card>

        <Card className="border border-default-200/70">
          <CardBody className="space-y-3">
            <h3 className="text-xl font-semibold">Для преподавателей</h3>
            <p className="text-default-600">
              Презентации можно приобрести отдельно без занятий — как готовые
              материалы для объяснения тем и проведения уроков.
            </p>
            <p className="text-default-600">
              Такой вариант подойдет преподавателям, которым нужны аккуратно
              оформленные учебные материалы для собственных занятий.
            </p>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
export default LessonAccessInfo;

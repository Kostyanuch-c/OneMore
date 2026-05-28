import { Button } from "@heroui/button";
import { Card, CardBody } from "@heroui/card";
import { Chip } from "@heroui/chip";
import { Image } from "@heroui/image";
import { Link } from "@heroui/link";

import { siteConfig } from "@/config/site";
import { teachers } from "@/features/teachers/teachers";

export default function TeachersPage() {
  return (
    <section className="py-8 md:py-10">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-6">
        <header className="space-y-3">
          <h1 className="text-3xl font-bold md:text-4xl">Преподаватели</h1>
          <p className="text-default-600">
            Выберите преподавателя под ваш предмет и цель: от регулярной
            системной подготовки до точечной помощи перед контрольной или
            экзаменом.
          </p>
        </header>

        <div className="flex flex-col gap-5">
          {teachers.map((teacher) => (
            <Card key={teacher.id} className="border border-default-200/70">
              <CardBody className="p-5 md:p-6">
                <div className="flex flex-col gap-5 md:flex-row">
                  <Image
                    alt={teacher.name}
                    className="h-56 w-full object-cover md:h-64 md:w-56"
                    radius="md"
                    src={teacher.imageUrl ?? "/teachers/anna-smirnova.png"}
                  />

                  <div className="flex flex-1 flex-col gap-4">
                    <div className="space-y-2">
                      <div className="flex flex-wrap items-center gap-2">
                        <h2 className="text-2xl font-semibold">
                          {teacher.name}
                        </h2>
                        <Chip color="primary" size="sm" variant="flat">
                          {teacher.subject}
                        </Chip>
                      </div>
                      <p className="text-default-600">{teacher.description}</p>
                    </div>

                    <div className="space-y-1 text-sm text-default-600">
                      <p>
                        <span className="font-medium text-foreground">
                          Опыт:
                        </span>{" "}
                        {teacher.experience}
                      </p>
                      <p>
                        <span className="font-medium text-foreground">
                          Образование:
                        </span>{" "}
                        {teacher.education}
                      </p>
                    </div>

                    <div className="space-y-2">
                      <p className="text-sm font-medium text-foreground">
                        Сильные стороны
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {teacher.achievements.map((achievement) => (
                          <Chip key={achievement} size="sm" variant="bordered">
                            {achievement}
                          </Chip>
                        ))}
                      </div>
                    </div>

                    <div className="space-y-2">
                      <p className="text-sm font-medium text-foreground">
                        Формат занятий
                      </p>
                      <ul className="list-disc space-y-1 pl-5 text-default-600">
                        {teacher.lessonFormat.map((formatItem) => (
                          <li key={formatItem}>{formatItem}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="mt-1 flex flex-col gap-2 sm:flex-row">
                      <Button
                        as={Link}
                        color="primary"
                        href={`/teachers/${teacher.slug}`}
                        variant="flat"
                      >
                        Подробнее
                      </Button>
                      <Button
                        as={Link}
                        color="primary"
                        href={siteConfig.contacts.telegram}
                        target="_blank"
                      >
                        Записаться
                      </Button>
                    </div>
                  </div>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

import { Card, CardBody, CardFooter, CardHeader } from "@heroui/card";
import { Chip } from "@heroui/chip";
import { Link } from "@heroui/link";
import { Button } from "@heroui/button";

import { problemsData } from "@/lib/data/problemsData";
import { title } from "@/components/primitives";

export default function Home() {
  const recentProblems = [...problemsData]
    .sort(
      (a, b) =>
        new Date(b.publishedDate).getTime() -
        new Date(a.publishedDate).getTime(),
    )
    .slice(0, 6);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "легкая":
        return "success";
      case "средняя":
        return "warning";
      case "сложная":
        return "danger";
      default:
        return "default";
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);

    return date.toLocaleDateString("ru-RU", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  };

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      {/* Hero Section */}
      <div className="inline-block max-w-4xl text-center justify-center mb-8">
        <h1 className="text-4xl lg:text-5xl font-bold mb-4 ">
          Добро пожаловать на платформу{" "}
          <span className={title({ color: "blue" })}>ХимРепетитор</span>
        </h1>
        <p className="text-lg text-default-600">
          Подробные разборы задач по химии с пошаговыми решениями и понятными
          объяснениями
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl mb-12">
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl font-bold text-primary mb-2">5</div>
            <div className="text-default-600">Задач с решениями</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl font-bold text-primary mb-2">5</div>
            <div className="text-default-600">Тематических разделов</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl font-bold text-primary mb-2">100%</div>
            <div className="text-default-600">Проверенных решений</div>
          </CardBody>
        </Card>
      </div>
      {/* Recent Problems */}
      <div className="w-full max-w-6xl">
        <div className="flex items-center gap-2 mb-6">
          <span className="text-2xl">📈</span>
          <h2 className="text-2xl font-bold">Последние задачи</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {recentProblems.map((problem) => (
            <Card
              key={problem.id}
              isPressable
              as={Link}
              href={`/problems/${problem.id}`}
            >
              <CardHeader className="flex-col items-start gap-2">
                <div className="flex justify-between w-full items-center">
                  <Chip
                    color={getDifficultyColor(problem.difficulty) as any}
                    size="sm"
                    variant="flat"
                  >
                    {problem.difficulty}
                  </Chip>
                  <span className="text-xs text-default-500">
                    📅 {formatDate(problem.publishedDate)}
                  </span>
                </div>
                <h4 className="text-lg font-semibold">{problem.title}</h4>
              </CardHeader>
              <CardBody className="pt-0">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-sm">🏷️</span>
                  <span className="text-sm text-default-600">
                    {problem.topic}
                  </span>
                </div>
                <p className="text-sm text-default-500 line-clamp-3">
                  {problem.problem}
                </p>
              </CardBody>
              <CardFooter>
                <Button className="w-full" color="primary" variant="flat">
                  Посмотреть решение
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

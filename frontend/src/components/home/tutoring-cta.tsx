"use client";

import { Button } from "@heroui/button";
import { Card, CardBody } from "@heroui/card";
import { Link } from "@heroui/link";
import NextLink from "next/link";

import { siteConfig } from "@/config/site";

function TutoringCTA() {
  return (
    <Card className="border border-primary/20 bg-linear-to-r from-primary/10 to-primary/5">
      <CardBody className="p-6 text-center md:p-8">
        <h2 className="text-2xl font-semibold text-foreground md:text-3xl">
          Нужна помощь с учебой?
        </h2>

        <p className="mx-auto mt-4 max-w-3xl text-default-600">
          Разберём сложные темы, подготовимся к контрольной, проверочной или
          экзамену и поможем закрыть пробелы в понимании. Можно заниматься
          регулярно или обратиться за разовой консультацией по конкретной теме и
          заданиям.
        </p>

        <div className="mt-6 flex flex-col items-stretch justify-center gap-3 sm:flex-row sm:items-center">
          <Button
            as={Link}
            color="primary"
            href={siteConfig.contacts.telegram}
            rel="noopener noreferrer"
            size="lg"
            target="_blank"
          >
            Написать в Telegram
          </Button>

          <Button
            as={NextLink}
            color="primary"
            href="/lessons"
            size="lg"
            variant="flat"
          >
            Подробнее о занятиях
          </Button>
        </div>

        <p className="mt-4 text-sm text-default-500">
          Также можно связаться через{" "}
          <Link
            className="text-default-500"
            href={siteConfig.contacts.discord}
            rel="noopener noreferrer"
            target="_blank"
          >
            Discord
          </Link>{" "}
          или{" "}
          <Link
            className="text-default-500"
            href={siteConfig.contacts.max}
            rel="noopener noreferrer"
            target="_blank"
          >
            MAX
          </Link>
          .
        </p>
      </CardBody>
    </Card>
  );
}

export default TutoringCTA;

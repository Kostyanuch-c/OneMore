"use client";

import { useEffect } from "react";
import { Card, CardBody } from "@heroui/card";
import { Button } from "@heroui/button";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    /* eslint-disable no-console */
    console.error(error);
  }, [error]);

  return (
    <main className="flex min-h-[60vh] items-center justify-center px-4">
      <Card className="max-w-lg w-full">
        <CardBody className="gap-4 text-center">
          <h1 className="text-2xl font-bold">Что-то пошло не так</h1>

          <p className="text-default-500">
            Не удалось загрузить данные. Попробуйте обновить страницу или
            повторить попытку чуть позже.
          </p>

          <Button color="primary" onPress={reset}>
            Попробовать снова
          </Button>
        </CardBody>
      </Card>
    </main>
  );
}

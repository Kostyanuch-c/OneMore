import { Button } from "@heroui/button";
import Link from "next/link";

import { subtitle, title } from "@/components/primitives";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <h1 className={title({ color: "blue" })}>404</h1>
      <h2 className={subtitle()}>Страница не найдена</h2>
      <p className="text-default-600 mb-8">
        Извините, страница которую вы ищете не существует.
      </p>
      <Button as={Link} color="primary" href="/" size="lg">
        Вернуться на главную
      </Button>
    </div>
  );
}

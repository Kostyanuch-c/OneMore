import { Card, CardBody } from "@heroui/card";
import { Skeleton } from "@heroui/skeleton";

const SKELETON_ITEMS_COUNT = 10;

export default function Loading() {
  return (
    <section className="mx-auto w-full max-w-5xl py-8">
      <Skeleton className="mb-6 h-10 w-64 rounded-lg" />

      <div className="flex flex-col gap-4">
        {Array.from({ length: SKELETON_ITEMS_COUNT }).map((_, index) => (
          <Card key={index}>
            <CardBody className="gap-3">
              <Skeleton className="h-6 w-2/3 rounded-lg" />
              <Skeleton className="h-4 w-full rounded-lg" />
              <Skeleton className="h-4 w-5/6 rounded-lg" />
            </CardBody>
          </Card>
        ))}
      </div>
    </section>
  );
}

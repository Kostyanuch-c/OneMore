import { subtitle, title } from "@/components/primitives";

function HomeHero() {
  return (
    <div className="inline-block max-w-4xl text-center justify-center mb-8">
      <h1 className="text-4xl lg:text-5xl font-bold mb-4">
        Добро пожаловать на платформу{" "}
        <span className={title({ color: "blue" })}>ХимРепетитор</span>
      </h1>
      <p className={subtitle()}>
        Подробные разборы задач по химии с пошаговыми решениями и понятными
        объяснениями
      </p>
    </div>
  );
}

export default HomeHero;

import { Link } from "@heroui/link";
import { Divider } from "@heroui/divider";

export const Footer = () => {
  return (
    <footer className="w-full border-t border-divider">
      <div className="mx-auto max-w-7xl px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* О сайте */}
          <div>
            <h3 className="text-lg font-semibold mb-3">О сайте</h3>
            <p className="text-sm text-default-500">
              Платформа для изучения химии с подробными разборами задач и
              индивидуальным подходом к каждому ученику.
            </p>
          </div>

          {/* Контакты */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Контакты</h3>
            <div className="space-y-2 text-sm text-default-500">
              <div className="flex items-center gap-2">
                <span>📧</span>
                <span>info@chemtutor.ru</span>
              </div>
              <div className="flex items-center gap-2">
                <span>📞</span>
                <span>+7 (999) 123-45-67</span>
              </div>
              <div className="flex items-center gap-2">
                <span>🕐</span>
                <span>Пн-Пт: 10:00 - 20:00</span>
              </div>
            </div>
          </div>

          {/* Информация */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Информация</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link className="text-default-500" href="#">
                  Правила пользования
                </Link>
              </li>
              <li>
                <Link className="text-default-500" href="#">
                  Политика конфиденциальности
                </Link>
              </li>
              <li>
                <Link className="text-default-500" href="#">
                  Методика обучения
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <Divider className="my-8" />

        <div className="text-center text-sm text-default-500">
          <p>© 2024 ХимРепетитор. Все права защищены.</p>
        </div>
      </div>
    </footer>
  );
};

export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "ХимРепетитор",
  description: "Платформа для изучения химии с подробными разборами задач",
  navItems: [
    {
      label: "Главная",
      href: "/",
    },
    {
      label: "Занятия",
      href: "/lessons",
    },
    {
      label: "Преподаватели",
      href: "/teachers",
    },
    {
      label: "О проекте",
      href: "/about",
    },
  ],
  navMenuItems: [
    {
      label: "Главная",
      href: "/",
    },
    {
      label: "Занятия",
      href: "/lessons",
    },
    {
      label: "Преподаватели",
      href: "/teachers",
    },
    {
      label: "О проекте",
      href: "/about",
    },
  ],
  contacts: {
    telegram: "https://t.me/your_username",
    discord: "https://t.me/your_username",
    max: "https://t.me/your_username",
  },
};

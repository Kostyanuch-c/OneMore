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
      label: "Все задачи",
      href: "/about",
    },
    {
      label: "Наборы задач",
      href: "/problem-sets",
    },
  ],
  navMenuItems: [
    {
      label: "Главная",
      href: "/",
    },
    {
      label: "Все задачи",
      href: "/problems",
    },
    {
      label: "Наборы задач",
      href: "/problem-sets",
    },
  ],
  links: {
    github: "https://github.com",
    twitter: "https://twitter.com",
    discord: "https://discord.gg",
  },
};

"use client";

import type { CurrentUser } from "@/features/auth/api/auth";
import type { Subject } from "@/features/subjects/api/subjects";

import {
  Navbar as HeroUINavbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  NavbarMenu,
  NavbarMenuItem,
  NavbarMenuToggle,
} from "@heroui/navbar";
import { Button } from "@heroui/button";
import { Link } from "@heroui/link";
import {
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
} from "@heroui/dropdown";
import { link as linkStyles } from "@heroui/theme";
import NextLink from "next/link";
import clsx from "clsx";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";

import { ThemeSwitch } from "@/components/theme-switch";
import { BeakerIcon } from "@/components/icons";

type NavbarProps = {
  subjects: Subject[];
  currentUser?: CurrentUser | null;
};

export const Navbar = ({ subjects, currentUser = null }: NavbarProps) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  const isSubjectPage = pathname.endsWith("/problems");
  const authHref = currentUser ? "/profile" : "/login";
  const authLabel = currentUser ? "Профиль" : "Войти";

  return (
    <HeroUINavbar
      isMenuOpen={isMenuOpen}
      maxWidth="xl"
      position="sticky"
      onMenuOpenChange={setIsMenuOpen}
    >
      <NavbarContent justify="start">
        <NavbarBrand as="li" className="gap-3 max-w-fit">
          <NextLink className="flex items-center gap-2" href="/">
            <BeakerIcon className="text-primary" size={32} />
            <p className="font-bold text-inherit text-xl">ХимРепетитор</p>
          </NextLink>
        </NavbarBrand>
      </NavbarContent>
      <NavbarContent className="basis-1/5 sm:basis-full" justify="center">
        <ul className="hidden md:flex gap-4 justify-start ml-2 items-center">
          <NavbarItem>
            <NextLink
              className={clsx(
                linkStyles({ color: "foreground" }),
                "data-[active=true]:text-primary data-[active=true]:font-medium",
              )}
              data-active={pathname === "/"}
              href="/"
            >
              Главная
            </NextLink>
          </NavbarItem>

          <NavbarItem>
            <Dropdown>
              <DropdownTrigger>
                <Button
                  disableAnimation
                  disableRipple
                  className={clsx(
                    "px-0 data-[active=true]:text-primary data-[active=true]:font-medium",
                    linkStyles({ color: "foreground" }),
                  )}
                  data-active={isSubjectPage}
                  radius="none"
                  variant="light"
                >
                  Задачи
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                aria-label="Список предметов"
                disabledKeys={subjects.length === 0 ? ["empty"] : []}
                onAction={(key) => {
                  setIsMenuOpen(false);
                  router.push(`/${String(key)}/problems`);
                }}
              >
                {subjects.length === 0 ? (
                  <DropdownItem key="empty">Пока нет предметов</DropdownItem>
                ) : (
                  subjects.map((subject) => (
                    <DropdownItem key={subject.slug}>
                      {subject.name}
                    </DropdownItem>
                  ))
                )}
              </DropdownMenu>
            </Dropdown>
          </NavbarItem>

          <NavbarItem>
            <NextLink
              className={clsx(
                linkStyles({ color: "foreground" }),
                "data-[active=true]:text-primary data-[active=true]:font-medium",
              )}
              data-active={pathname === "/about"}
              href="/about"
            >
              О сайте
            </NextLink>
          </NavbarItem>

          <NavbarItem>
            <NextLink
              className={clsx(
                linkStyles({ color: "foreground" }),
                "data-[active=true]:text-primary data-[active=true]:font-medium",
              )}
              data-active={pathname === "/teachers"}
              href="/teachers"
            >
              Учителя
            </NextLink>
          </NavbarItem>

          <NavbarItem>
            <span
              className={clsx(
                linkStyles({ color: "foreground" }),
                "opacity-50 cursor-not-allowed",
              )}
            >
              Презентации
            </span>
          </NavbarItem>
        </ul>
      </NavbarContent>

      <NavbarContent
        className="hidden md:flex basis-1/5 md:basis-full"
        justify="end"
      >
        <NavbarItem className="flex gap-2">
          <div className="w-6 h-6">
            <ThemeSwitch />
          </div>
        </NavbarItem>
        <NavbarItem className="hidden md:flex">
          <Button
            as={Link}
            className="text-sm font-normal"
            color="primary"
            href={authHref}
            variant="flat"
          >
            {authLabel}
          </Button>
        </NavbarItem>
      </NavbarContent>

      <NavbarContent className="md:hidden basis-1 pl-4" justify="end">
        <div className="w-6 h-6">
          <ThemeSwitch />
        </div>
        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Close menu" : "Open menu"}
        />
      </NavbarContent>

      <NavbarMenu>
        <div className="mx-4 mt-2 flex flex-col gap-2">
          <NavbarMenuItem>
            <Link
              color="foreground"
              href="/"
              size="lg"
              onPress={() => setIsMenuOpen(false)}
            >
              Главная
            </Link>
          </NavbarMenuItem>
          <NavbarMenuItem>
            <p className="text-default-500 text-sm px-1">Задачи</p>
          </NavbarMenuItem>
          {subjects.map((subject) => (
            <NavbarMenuItem key={subject.slug}>
              <NextLink
                className={clsx(linkStyles({ color: "foreground" }), "pl-4")}
                href={`/${subject.slug}/problems`}
                onClick={() => setIsMenuOpen(false)}
              >
                {subject.name}
              </NextLink>
            </NavbarMenuItem>
          ))}
          <NavbarMenuItem>
            <Link
              color="foreground"
              href="/about"
              size="lg"
              onPress={() => setIsMenuOpen(false)}
            >
              О сайте
            </Link>
          </NavbarMenuItem>
          <NavbarMenuItem>
            <Link
              color="foreground"
              href="/teachers"
              size="lg"
              onPress={() => setIsMenuOpen(false)}
            >
              Учителя
            </Link>
          </NavbarMenuItem>
          <NavbarMenuItem>
            <Link isDisabled color="foreground" size="lg">
              Презентации (soon)
            </Link>
          </NavbarMenuItem>
          <NavbarMenuItem>
            <Button
              as={Link}
              className="w-full"
              color="primary"
              href={authHref}
              variant="flat"
              onPress={() => setIsMenuOpen(false)}
            >
              {authLabel}
            </Button>
          </NavbarMenuItem>
        </div>
      </NavbarMenu>
    </HeroUINavbar>
  );
};

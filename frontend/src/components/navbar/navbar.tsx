"use client";

import type { CurrentUser } from "@/features/auth/api/auth";
import type { Subject } from "@/features/subjects/api/subjects";
import type {
  MobileProblemsMenuListProps,
  NavItemConfig,
  ProblemsDropdownProps,
} from "@/shared/types/navbar";

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
import { siteConfig } from "@/config/site";

interface NavbarProps {
  subjects: Subject[];
  currentUser?: CurrentUser | null;
  isLoading?: boolean;
}

const ProblemsDropdown = ({
  subjects,
  isProblemsPage,
  onSelectProblemSubject,
  isLoading,
}: ProblemsDropdownProps & { isLoading?: boolean }) => (
  <Dropdown>
    <DropdownTrigger>
      <Button
        disableAnimation
        disableRipple
        className={clsx(
          "px-0 data-[active=true]:text-primary data-[active=true]:font-medium",
          linkStyles({ color: "foreground" }),
        )}
        data-active={isProblemsPage}
        radius="none"
        variant="light"
      >
        Задачи
      </Button>
    </DropdownTrigger>
    <DropdownMenu
      aria-label="Список предметов"
      disabledKeys={subjects.length === 0 || isLoading ? ["empty"] : []}
      onAction={(key) => onSelectProblemSubject(String(key))}
    >
      {isLoading ? (
        <DropdownItem key="empty">Загрузка...</DropdownItem>
      ) : subjects.length === 0 ? (
        <DropdownItem key="empty">Пока нет предметов</DropdownItem>
      ) : (
        subjects.map((subject) => (
          <DropdownItem key={subject.slug}>{subject.name}</DropdownItem>
        ))
      )}
    </DropdownMenu>
  </Dropdown>
);

const MobileProblemsMenuList = ({
  subjects,
  onCloseMenu,
  isLoading,
}: MobileProblemsMenuListProps & { isLoading?: boolean }) => (
  <>
    <NavbarMenuItem>
      <p className="text-default-500 text-sm px-1">Задачи</p>
    </NavbarMenuItem>
    {isLoading ? (
      <NavbarMenuItem>
        <span className="pl-4 text-default-400">Загрузка...</span>
      </NavbarMenuItem>
    ) : subjects.length === 0 ? (
      <NavbarMenuItem>
        <span className="pl-4 text-default-400">Пока нет предметов</span>
      </NavbarMenuItem>
    ) : (
      subjects.map((subject) => (
        <NavbarMenuItem key={subject.slug}>
          <NextLink
            className={clsx(linkStyles({ color: "foreground" }), "pl-4")}
            href={`/${subject.slug}/problems`}
            onClick={onCloseMenu}
          >
            {subject.name}
          </NextLink>
        </NavbarMenuItem>
      ))
    )}
  </>
);

export const Navbar = ({
  subjects,
  currentUser = null,
  isLoading = false,
}: NavbarProps) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  const isProblemsPage = pathname.endsWith("/problems");
  const authHref = currentUser ? "/profile" : "/login";
  const authLabel = isLoading
    ? "Загрузка..."
    : currentUser
      ? "Профиль"
      : "Войти";
  const navLinkClassName = clsx(
    linkStyles({ color: "foreground" }),
    "data-[active=true]:text-primary data-[active=true]:font-medium",
  );
  const [homeNavItem, ...restNavItems] = siteConfig.navItems;
  const [homeMenuItem, ...restMenuItems] = siteConfig.navMenuItems;
  const closeMenu = () => setIsMenuOpen(false);
  const handleProblemSelect = (subjectSlug: string) => {
    closeMenu();
    router.push(`/${subjectSlug}/problems`);
  };

  const renderDesktopNavLink = (item: NavItemConfig) => (
    <NavbarItem key={item.href}>
      <NextLink
        className={navLinkClassName}
        data-active={pathname === item.href}
        href={item.href}
      >
        {item.label}
      </NextLink>
    </NavbarItem>
  );

  const renderMobileNavLink = (item: NavItemConfig) => (
    <NavbarMenuItem key={item.href}>
      <NextLink
        className={clsx(navLinkClassName, "text-large")}
        data-active={pathname === item.href}
        href={item.href}
        onClick={closeMenu}
      >
        {item.label}
      </NextLink>
    </NavbarMenuItem>
  );

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
          {homeNavItem ? renderDesktopNavLink(homeNavItem) : null}
          <NavbarItem>
            <ProblemsDropdown
              isLoading={isLoading}
              isProblemsPage={isProblemsPage}
              subjects={subjects}
              onSelectProblemSubject={handleProblemSelect}
            />
          </NavbarItem>
          {restNavItems.map(renderDesktopNavLink)}

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
          {homeMenuItem ? renderMobileNavLink(homeMenuItem) : null}
          <MobileProblemsMenuList
            isLoading={isLoading}
            subjects={subjects}
            onCloseMenu={closeMenu}
          />
          {restMenuItems.map(renderMobileNavLink)}
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
              onPress={closeMenu}
            >
              {authLabel}
            </Button>
          </NavbarMenuItem>
        </div>
      </NavbarMenu>
    </HeroUINavbar>
  );
};

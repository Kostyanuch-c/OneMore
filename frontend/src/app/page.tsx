import {
  HomeHero,
  HowItWorks,
  MainStats,
  RecentProblemsSection,
  TutoringCTA,
} from "@/components/home";

export default function Home() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <HomeHero />

      <MainStats />

      <HowItWorks />

      <RecentProblemsSection />

      <div className="w-full max-w-6xl">
        <TutoringCTA />
      </div>
    </section>
  );
}

import { AccessibilityStatement } from "./components/AccessibilityStatement";
import { Components } from "./components/Components";
import { Detects } from "./components/Detects";
import { DesignDocuments, PosterAndPresentations } from "./components/Documents";
import { Hero } from "./components/Hero";
import { HowItWorks } from "./components/HowItWorks";
import { Objectives } from "./components/Objectives";
import { Problem } from "./components/Problem";
import { Progress } from "./components/Progress";
import { ProjectInfo } from "./components/ProjectInfo";
import { SiteFooter } from "./components/SiteFooter";
import { SiteHeader } from "./components/SiteHeader";
import { SiteNav } from "./components/SiteNav";
import { SkipLink } from "./components/SkipLink";
import { SourceCode } from "./components/SourceCode";
import { Team } from "./components/Team";

export function App() {
  return (
    <>
      <SkipLink />
      <SiteHeader />
      <SiteNav />
      <main id="main" tabIndex={-1} className="focus:outline-none">
        <Hero />
        <Problem />
        <HowItWorks />
        <Objectives />
        <Detects />
        <Components />
        <Progress />
        <DesignDocuments />
        <PosterAndPresentations />
        <Team />
        <SourceCode />
        <ProjectInfo />
        <AccessibilityStatement />
      </main>
      <SiteFooter />
    </>
  );
}

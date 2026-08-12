import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import ProblemSection from "@/components/ProblemSection";
import FrameworkSection from "@/components/FrameworkSection";
import PersonaSection from "@/components/PersonaSection";
import MicroLessonDemo from "@/components/MicroLessonDemo";
import SecuritySection from "@/components/SecuritySection";
import WaitlistSection from "@/components/WaitlistSection";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <div className="min-h-screen bg-paper">
      <Navbar />
      <main>
        <Hero />
        <ProblemSection />
        <FrameworkSection />
        <PersonaSection />
        <MicroLessonDemo />
        <SecuritySection />
        <WaitlistSection />
      </main>
      <Footer />
    </div>
  );
}

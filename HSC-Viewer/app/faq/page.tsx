import { Metadata } from "next";
import Link from "next/link";
import { REPO_LINKS, APP_KEYWORDS } from "@/lib/constants";
import { SITE_URL } from "@/lib/og-metadata";

export const metadata: Metadata = {
  title: "FAQ | HSC Math Hub",
  description:
    "Got questions about HSC Math Hub? Find answers about our free Extension 1 & 2 maths booklets, study pathways, LaTeX resources, and how to prepare for NSW HSC Mathematics exams.",
  keywords: [
    ...APP_KEYWORDS,
    "HSC Maths FAQ",
    "Math Hub Help",
    "HSC Mathematics questions",
    "NSW HSC Preparation",
    "Free Math Resources FAQ",
  ],
  openGraph: {
    title: "FAQ | HSC Math Hub",
    description:
      "Got questions about HSC Math Hub? Find answers about our free Extension 1 & 2 maths booklets, study pathways, LaTeX resources, and how to prepare for NSW HSC Mathematics exams.",
    url: `${SITE_URL}/faq`,
    siteName: "HSC Math Hub",
    type: "website",
  },
};

export default function FAQPage() {
  const faqs = [
    {
      q: "Who created this website?",
      a: "Vu Hung Nguyen, an ML/AI engineer and educator passionate about maths.",
    },
    {
      q: "Why did you create this impressive HSC Math Hub?",
      a: '"To keep someone busy and not playing too many video games." To help students in NSW and Australia prepare for their HSC exams and for higher math education. To help you approach maths in a rigorous way, which most math books fail to do.',
    },
    {
      q: "How long have you spent on this math hub?",
      a: '"Haha, let\'s just say it took a fair few cups of coffee and quite a few late nights! I definitely put a lot of work into curating the booklets to make sure they were actually useful, but I try not to count the hours."',
    },
    {
      q: "How can I help?",
      a: (
        <>
          Send me any feedback, suggestions, typos, or grammatical errors. Send me your problems, assessment tasks, and trial papers. Reach me via{" "}
          <a href={REPO_LINKS.github} className="font-semibold text-[var(--color-purple)] hover:underline" target="_blank" rel="noreferrer">GitHub issues</a>{" "}
          or{" "}
          <a href={REPO_LINKS.linkedin} className="font-semibold text-[var(--color-purple)] hover:underline" target="_blank" rel="noreferrer">LinkedIn</a>
          , or comment/DM on{" "}
          <a href={REPO_LINKS.substack} className="font-semibold text-[var(--color-purple)] hover:underline" target="_blank" rel="noreferrer">Substack</a>.
        </>
      ),
      aString: "Send me any feedback, suggestions, typos, or grammatical errors. Send me your problems, assessment tasks, and trial papers. Reach me via GitHub issues or LinkedIn, or comment/DM on Substack.",
    },
    {
      q: "Your LaTeX/TikZ is crazy. Teach me!",
      a: "Yes, you can learn it by reading the LaTeX code on GitHub, or by DMing me.",
    },
    {
      q: "Can I use the booklets for my school?",
      a: "Yes, you can use them for personal use, in your school, and distribute them. As they are under the CC BY 4.0 license, you can use the booklets as long as you adhere to the license.",
    },
    {
      q: "How did you come up with the ideas for creating original problems?",
      a: "Because I love maths! :)",
    },
    {
      q: "Are you available for collaboration, tutoring, and coaching?",
      a: "While my schedule is currently full with my uni work and building this hub, I'm always open to brief collaborations or quick questions via GitHub or LinkedIn!",
    },
    {
      q: "Where should I start my HSC Maths study pathway?",
      a: "In general, start from your pain points and weaknesses. Read the Fundamental Review sections and then attack the easy problems. A tailored assessment or coaching might be needed (and is available).",
    },
    {
      q: '"Damn, what school do you go to?"',
      a: "I am an adult :) I teach ML/AI at a university in NSW.",
    },
    {
      q: 'Why is there so much "enrichment" in your booklets?',
      a: "To help your brain melt! And to help you prepare for maths in university and higher education. I find the maths in most textbooks way too easy.",
    },
  ];

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqs.map((faq) => ({
      "@type": "Question",
      name: faq.q,
      acceptedAnswer: {
        "@type": "Answer",
        text: faq.aString || (typeof faq.a === "string" ? faq.a : ""),
      },
    })),
  };

  return (
    <main className="mx-auto max-w-[800px] px-4 py-12 sm:px-6 lg:px-8">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="mb-8">
        <Link href="/" className="text-sm font-medium text-[var(--color-purple)] hover:underline">
          &larr; Back to Home
        </Link>
      </div>
      <h1 className="mb-8 text-3xl font-bold tracking-tight text-[var(--color-charcoal)]">
        Frequently Asked Questions (FAQ) - HSC Mathematics
      </h1>
      <div className="space-y-8">
        {faqs.map((faq, index) => (
          <div key={index} className="flex flex-col gap-2">
            <h2 className="text-xl font-semibold text-[var(--color-purple)]">
              {faq.q}
            </h2>
            <div className="text-[var(--color-charcoal)] leading-relaxed">
              {faq.a}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}

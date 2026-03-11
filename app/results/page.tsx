"use client"

import { Suspense } from "react"
import { useSearchParams } from "next/navigation"
import Link from "next/link"
import { ArrowLeft, Sparkles, Search, FileText } from "lucide-react"
import { GrantCard, type Grant } from "@/components/grant-card"
import { Button } from "@/components/ui/button"

// Mock data - in production, this would come from your backend API
const MOCK_GRANTS: Grant[] = [
  {
    id: "1",
    title: "Notice of Intent to Publish a Funding Opportunity Announcement for Impact of Technology and Digital Media Exposure Usage on Child and Adolescent Development",
    agency: "NICHD",
    description: "The Eunice Kennedy Shriver National Institute of Child Health and Human Development (NICHD) plans to issue a funding opportunity to support research on the impact of technology and digital media (TDM)—including social media, apps, AI, and video games—on the health and development of children and adolescents. The initiative seeks to address the urgent need to understand how TDM exposure affects cognitive, emotional, social, and physical development across diverse populations.",
    openDate: "06/25/2025",
    closeDate: "N/A",
    awardMin: "N/A",
    awardMax: "N/A",
    grantUrl: "https://grants.nih.gov/grants/guide/notice-files/NOT-HD-25-017.html",
  },
  {
    id: "2",
    title: "Developmental Sciences",
    agency: "NSF",
    description: "This grant supports basic research on human developmental processes across the lifespan, including perceptual, cognitive, social, emotional, linguistic, and motor domains. It funds studies investigating factors like family, culture, genetics, and media, and encourages multidisciplinary, longitudinal, and innovative methodological approaches. Typical projects are three years in duration with budgets appropriate to the scope of the research.",
    openDate: "02/15/2024",
    closeDate: "07/30/2026",
    awardMin: "N/A",
    awardMax: "N/A",
    grantUrl: "https://www.nsf.gov/funding/programs/developmental-sciences",
  },
  {
    id: "3",
    title: "Research on Social Media and Adolescent Mental Health",
    agency: "NIMH",
    description: "This funding opportunity supports research examining the relationship between social media use and mental health outcomes in adolescents. Areas of interest include understanding mechanisms linking social media to depression, anxiety, and self-esteem; developing and testing interventions; and identifying protective factors for at-risk youth populations.",
    openDate: "01/15/2025",
    closeDate: "12/15/2025",
    awardMin: "$250,000",
    awardMax: "$500,000",
    grantUrl: "https://www.nimh.nih.gov/funding",
  },
  {
    id: "4",
    title: "Youth Mental Health Innovation Grant",
    agency: "RWJF",
    description: "Supporting innovative approaches to understanding and improving adolescent mental health in the digital age. This grant focuses on community-based interventions, policy research, and scalable solutions that address the intersection of technology use and youth wellbeing.",
    openDate: "03/01/2025",
    closeDate: "09/30/2025",
    awardMin: "$100,000",
    awardMax: "$300,000",
    grantUrl: "https://www.rwjf.org/en/grants.html",
  },
]

function ResultsContent() {
  const searchParams = useSearchParams()
  const projectTitle = searchParams.get("title") || ""
  const projectDescription = searchParams.get("description") || ""

  // For demo, show description preview
  const descriptionPreview = projectDescription.length > 200 
    ? projectDescription.slice(0, 200) + "..." 
    : projectDescription

  return (
    <main className="min-h-screen bg-background">
      {/* Subtle gradient background */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-accent/20 via-background to-background pointer-events-none" />
      
      <div className="relative">
        {/* Header */}
        <header className="border-b border-border/60 bg-card/50 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-primary shadow-sm group-hover:shadow transition-shadow">
                <Sparkles className="h-4 w-4 text-primary-foreground" />
              </div>
              <span className="text-lg font-semibold tracking-tight text-foreground">MatchMaker</span>
            </Link>
            <Link href="/">
              <Button variant="outline" size="sm" className="border-border/80 text-foreground hover:bg-muted/50 shadow-sm">
                <Search className="mr-2 h-4 w-4" />
                New Search
              </Button>
            </Link>
          </div>
        </header>

        <div className="max-w-4xl mx-auto px-6 py-8">
          {/* Back button */}
          <Link href="/">
            <Button variant="ghost" size="sm" className="mb-8 -ml-3 text-muted-foreground hover:text-foreground hover:bg-transparent">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to search
            </Button>
          </Link>

          {/* Results Header */}
          <div className="mb-10">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
              <span>{MOCK_GRANTS.length} grants found</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground mb-3 text-balance">
              Recommended Grants for "{projectTitle || "Your Project"}"
            </h1>
            <p className="text-muted-foreground text-base">
              Based on your project description, the following grants may be relevant.
            </p>
            
            {projectDescription && (
              <div className="mt-6 p-5 rounded-xl bg-card border border-border/80 shadow-sm">
                <div className="flex items-center gap-2 mb-3">
                  <FileText className="h-4 w-4 text-muted-foreground" />
                  <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Your Project Description</span>
                </div>
                <p className="text-sm text-foreground/80 leading-relaxed">
                  {descriptionPreview}
                </p>
              </div>
            )}
          </div>

          {/* Grant Cards */}
          <div className="space-y-4">
            {MOCK_GRANTS.map((grant) => (
              <GrantCard key={grant.id} grant={grant} />
            ))}
          </div>

          {MOCK_GRANTS.length === 0 && (
            <div className="text-center py-20 px-4">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-muted mb-6">
                <Search className="h-7 w-7 text-muted-foreground" />
              </div>
              <p className="text-xl font-semibold text-foreground mb-2">No matching grants found</p>
              <p className="text-muted-foreground max-w-sm mx-auto">
                Try adjusting your search criteria or project description to find more results.
              </p>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}

export default function ResultsPage() {
  return (
    <Suspense fallback={<ResultsPageSkeleton />}>
      <ResultsContent />
    </Suspense>
  )
}

function ResultsPageSkeleton() {
  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/60 bg-card/50 backdrop-blur-sm px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-muted animate-pulse" />
          <div className="h-5 w-28 rounded-md bg-muted animate-pulse" />
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="h-8 w-32 animate-pulse rounded-md bg-muted mb-8" />
        <div className="h-6 w-24 animate-pulse rounded-full bg-muted mb-4" />
        <div className="h-10 w-3/4 animate-pulse rounded-md bg-muted mb-3" />
        <div className="h-5 w-1/2 animate-pulse rounded-md bg-muted mb-10" />
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-52 animate-pulse rounded-xl bg-muted mb-4" />
        ))}
      </div>
    </main>
  )
}

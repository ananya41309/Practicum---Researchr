"use client"

import { useState, useRef } from "react"
import { useRouter } from "next/navigation"
import { Upload, ChevronDown, ChevronUp, Sparkles, FileText, Search, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import { Checkbox } from "@/components/ui/checkbox"
import { Slider } from "@/components/ui/slider"

export default function HomePage() {
  const router = useRouter()
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  const [projectTitle, setProjectTitle] = useState("")
  const [projectDescription, setProjectDescription] = useState("")
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [sortBy, setSortBy] = useState("relevance")
  const [filtersOpen, setFiltersOpen] = useState(false)
  
  // Filter states
  const [fundingRange, setFundingRange] = useState([0, 1000000])
  const [selectedAgencies, setSelectedAgencies] = useState<string[]>([])
  const [selectedGrantTypes, setSelectedGrantTypes] = useState<string[]>([])

  const handleFileUpload = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadedFile(file)
    }
  }

  const handleSearch = () => {
    if (projectTitle.trim() || projectDescription.trim()) {
      const params = new URLSearchParams()
      if (projectTitle) params.set("title", projectTitle)
      if (projectDescription) params.set("description", projectDescription)
      if (sortBy) params.set("sort", sortBy)
      router.push(`/results?${params.toString()}`)
    }
  }

  const agencies = [
    "National Science Foundation",
    "National Institutes of Health",
    "Department of Energy",
    "NASA",
    "DARPA",
    "Private Foundation",
  ]

  const grantTypes = [
    "Research Grant",
    "Fellowship",
    "Equipment Grant",
    "Travel Grant",
  ]

  return (
    <main className="min-h-screen bg-background">
      {/* Subtle gradient background */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-accent/30 via-background to-background pointer-events-none" />
      
      <div className="relative">
        {/* Header */}
        <header className="border-b border-border/60 bg-card/50 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-3xl mx-auto px-6 py-4 flex items-center gap-3">
            <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-primary shadow-sm">
              <Sparkles className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="text-lg font-semibold tracking-tight text-foreground">MatchMaker</span>
          </div>
        </header>

        {/* Main Content */}
        <div className="max-w-3xl mx-auto px-6 py-12">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-foreground mb-4 text-balance">
              Find Your Perfect Research Grant
            </h1>
            <p className="text-muted-foreground text-base sm:text-lg max-w-xl mx-auto leading-relaxed">
              Describe your research project and we'll match you with relevant funding opportunities from top agencies.
            </p>
          </div>

          {/* Form Card */}
          <div className="rounded-2xl border border-border bg-card shadow-sm">
            <div className="p-6 sm:p-8">
              {/* Project Title */}
              <div className="mb-6">
                <Label htmlFor="project-title" className="text-sm font-medium text-foreground mb-2 block">
                  Project Title
                </Label>
                <Input
                  id="project-title"
                  value={projectTitle}
                  onChange={(e) => setProjectTitle(e.target.value)}
                  className="w-full h-11 bg-background border-border/80 text-foreground placeholder:text-muted-foreground/60 focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all"
                  placeholder="e.g., Impact of Social Media on Adolescent Mental Health"
                />
              </div>

              {/* Project Description */}
              <div className="mb-6">
                <Label htmlFor="project-description" className="text-sm font-medium text-foreground mb-2 block">
                  Project Description
                </Label>
                <Textarea
                  id="project-description"
                  value={projectDescription}
                  onChange={(e) => setProjectDescription(e.target.value)}
                  className="w-full min-h-[160px] resize-y bg-background border-border/80 text-foreground placeholder:text-muted-foreground/60 focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all leading-relaxed"
                  placeholder="Describe your research objectives, methodology, and expected outcomes..."
                />
              </div>

              {/* Upload Documents */}
              <div className="mb-6">
                <Label className="text-sm font-medium text-foreground mb-2 block">
                  Upload Documents
                  <span className="text-muted-foreground font-normal ml-1.5">(optional)</span>
                </Label>
                <div
                  onClick={handleFileUpload}
                  className="flex items-center justify-center gap-3 border-2 border-dashed border-border/80 rounded-xl p-8 cursor-pointer hover:border-primary/50 hover:bg-accent/30 transition-all duration-200 group"
                >
                  {uploadedFile ? (
                    <div className="flex items-center gap-3">
                      <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
                        <FileText className="h-5 w-5 text-primary" />
                      </div>
                      <div className="flex flex-col">
                        <span className="text-sm font-medium text-foreground">{uploadedFile.name}</span>
                        <span className="text-xs text-muted-foreground">Click to replace</span>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          setUploadedFile(null)
                        }}
                        className="ml-2 p-1 rounded-md hover:bg-muted transition-colors"
                      >
                        <X className="h-4 w-4 text-muted-foreground" />
                      </button>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center gap-2">
                      <div className="flex items-center justify-center w-12 h-12 rounded-xl bg-muted group-hover:bg-primary/10 transition-colors">
                        <Upload className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
                      </div>
                      <div className="text-center">
                        <span className="text-sm font-medium text-foreground">Drop files here or click to upload</span>
                        <p className="text-xs text-muted-foreground mt-1">PDF, DOCX, CSV, TXT</p>
                      </div>
                    </div>
                  )}
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.docx,.csv,.txt"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </div>

              {/* Filters Collapsible */}
              <Collapsible open={filtersOpen} onOpenChange={setFiltersOpen} className="mb-6">
                <CollapsibleTrigger asChild>
                  <button className="w-full flex items-center justify-between px-4 py-3.5 rounded-xl bg-muted/50 hover:bg-muted transition-colors text-sm font-medium text-foreground border border-transparent hover:border-border/50">
                    <span>Advanced Filters</span>
                    <div className="flex items-center gap-2">
                      {(selectedAgencies.length > 0 || selectedGrantTypes.length > 0) && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-primary/10 text-primary font-medium">
                          {selectedAgencies.length + selectedGrantTypes.length} selected
                        </span>
                      )}
                      {filtersOpen ? (
                        <ChevronUp className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <ChevronDown className="h-4 w-4 text-muted-foreground" />
                      )}
                    </div>
                  </button>
                </CollapsibleTrigger>
                <CollapsibleContent className="pt-4 space-y-4">
                  {/* Funding Range */}
                  <div className="p-5 rounded-xl bg-muted/30 border border-border/50">
                    <Label className="text-sm font-medium text-foreground mb-4 block">
                      Funding Amount Range
                    </Label>
                    <Slider
                      value={fundingRange}
                      onValueChange={setFundingRange}
                      max={1000000}
                      step={10000}
                      className="mb-3"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground">
                      <span className="font-medium">${fundingRange[0].toLocaleString()}</span>
                      <span className="font-medium">${fundingRange[1].toLocaleString()}</span>
                    </div>
                  </div>

                  {/* Agencies */}
                  <div className="p-5 rounded-xl bg-muted/30 border border-border/50">
                    <Label className="text-sm font-medium text-foreground mb-4 block">
                      Funding Agency
                    </Label>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {agencies.map((agency) => (
                        <div key={agency} className="flex items-center gap-3">
                          <Checkbox
                            id={`agency-${agency}`}
                            checked={selectedAgencies.includes(agency)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                setSelectedAgencies([...selectedAgencies, agency])
                              } else {
                                setSelectedAgencies(selectedAgencies.filter((a) => a !== agency))
                              }
                            }}
                            className="border-border data-[state=checked]:bg-primary data-[state=checked]:border-primary"
                          />
                          <label
                            htmlFor={`agency-${agency}`}
                            className="text-sm text-foreground/80 cursor-pointer hover:text-foreground transition-colors"
                          >
                            {agency}
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Grant Types */}
                  <div className="p-5 rounded-xl bg-muted/30 border border-border/50">
                    <Label className="text-sm font-medium text-foreground mb-4 block">
                      Grant Type
                    </Label>
                    <div className="grid grid-cols-2 gap-3">
                      {grantTypes.map((type) => (
                        <div key={type} className="flex items-center gap-3">
                          <Checkbox
                            id={`type-${type}`}
                            checked={selectedGrantTypes.includes(type)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                setSelectedGrantTypes([...selectedGrantTypes, type])
                              } else {
                                setSelectedGrantTypes(selectedGrantTypes.filter((t) => t !== type))
                              }
                            }}
                            className="border-border data-[state=checked]:bg-primary data-[state=checked]:border-primary"
                          />
                          <label
                            htmlFor={`type-${type}`}
                            className="text-sm text-foreground/80 cursor-pointer hover:text-foreground transition-colors"
                          >
                            {type}
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>
                </CollapsibleContent>
              </Collapsible>

              {/* Sort and Search */}
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-2">
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="w-full sm:w-[180px] h-11 bg-background border-border/80 text-foreground">
                    <SelectValue placeholder="Sort by" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="relevance">Sort by: Relevance</SelectItem>
                    <SelectItem value="deadline">Sort by: Deadline</SelectItem>
                    <SelectItem value="amount">Sort by: Amount</SelectItem>
                  </SelectContent>
                </Select>
                <Button
                  onClick={handleSearch}
                  className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground font-medium h-11 shadow-sm hover:shadow transition-all"
                >
                  <Search className="mr-2 h-4 w-4" />
                  Search Grants
                </Button>
              </div>
            </div>
          </div>
          
          {/* Footer hint */}
          <p className="text-center text-xs text-muted-foreground mt-8">
            Powered by AI matching technology
          </p>
        </div>
      </div>
    </main>
  )
}

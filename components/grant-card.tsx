"use client"

import { useState } from "react"
import { ExternalLink, Calendar, DollarSign, ChevronDown, ChevronUp, Building2 } from "lucide-react"
import { Button } from "@/components/ui/button"

export interface Grant {
  id: string
  title: string
  agency: string
  description: string
  openDate: string
  closeDate: string
  awardMin?: string
  awardMax?: string
  grantUrl?: string
}

interface GrantCardProps {
  grant: Grant
}

export function GrantCard({ grant }: GrantCardProps) {
  const [expanded, setExpanded] = useState(false)

  const handleViewDetails = () => {
    if (grant.grantUrl) {
      window.open(grant.grantUrl, "_blank", "noopener,noreferrer")
    }
  }

  return (
    <article className="group rounded-xl border border-border bg-card p-6 hover:border-primary/40 hover:shadow-sm transition-all duration-200">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="flex items-center gap-2">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-primary/10">
            <Building2 className="h-4 w-4 text-primary" />
          </div>
          <span className="text-sm font-medium text-primary">
            {grant.agency}
          </span>
        </div>
      </div>

      {/* Title */}
      <h3 className="text-lg font-semibold text-foreground mb-4 leading-snug text-balance">
        {grant.title}
      </h3>
      
      {/* Meta Info */}
      <div className="flex flex-wrap gap-x-6 gap-y-2 mb-4">
        <div className="flex items-center gap-2 text-sm">
          <Calendar className="h-4 w-4 text-muted-foreground/70" />
          <span className="text-muted-foreground">
            <span className="text-foreground/70 font-medium">Open:</span> {grant.openDate}
          </span>
          <span className="text-muted-foreground/50 mx-1">|</span>
          <span className="text-muted-foreground">
            <span className="text-foreground/70 font-medium">Close:</span> {grant.closeDate}
          </span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <DollarSign className="h-4 w-4 text-muted-foreground/70" />
          <span className="text-muted-foreground">
            <span className="text-foreground/70 font-medium">Award:</span> {grant.awardMin || "N/A"} – {grant.awardMax || "N/A"}
          </span>
        </div>
      </div>

      {/* Description */}
      <p className={`text-sm text-muted-foreground leading-relaxed mb-5 ${!expanded ? "line-clamp-2" : ""}`}>
        {grant.description}
      </p>

      {/* Actions */}
      <div className="flex items-center gap-3 pt-2 border-t border-border/50">
        <Button
          variant="ghost"
          size="sm"
          className="text-muted-foreground hover:text-foreground hover:bg-muted/50 -ml-2"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? (
            <>
              <ChevronUp className="mr-1.5 h-4 w-4" />
              Show less
            </>
          ) : (
            <>
              <ChevronDown className="mr-1.5 h-4 w-4" />
              Read more
            </>
          )}
        </Button>
        <Button
          size="sm"
          className="ml-auto bg-primary hover:bg-primary/90 text-primary-foreground shadow-sm hover:shadow transition-all"
          onClick={handleViewDetails}
        >
          <ExternalLink className="mr-1.5 h-3.5 w-3.5" />
          View Grant Details
        </Button>
      </div>
    </article>
  )
}

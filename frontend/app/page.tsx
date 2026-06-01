"use client";

import { useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  createJob,
  runCareerAgentStream,
  searchDocuments,
  uploadDocument,
  type StreamStep,
} from "../lib/api";

type SearchResult = {
  document_id: number | null;
  chunk_id: string;
  content: string;
  score: number;
  source: string;
  metadata: Record<string, unknown>;
  retrieval_mode: string;
};

type UploadResult = {
  id: number;
  filename: string;
  file_type: string;
  chunk_count: number;
  retrieval_mode: string;
};

type RunStatus = "idle" | "running" | "done" | "error";

const defaultDescription =
  "Requires Python, FastAPI, LLM API integration, prompt engineering, RAG retrieval, agent workflow design, and pytest experience.";
const sampleTitle = "AI Agent Intern";
const sampleCompany = "Demo AI Lab";
const sampleDescription = [
  "Responsibilities: build backend services for an AI career agent, analyze job descriptions, retrieve profile evidence, detect skill gaps, and generate learning plans.",
  "Requirements: Python, FastAPI, SQL, LLM API calls, prompt engineering, RAG document retrieval, SSE streaming, and basic frontend collaboration.",
  "Bonus: agent workflow design, tool calling, pytest automation, Next.js demo pages, and Markdown report generation.",
].join("\n\n");
const sampleGoal =
  "I want to apply for an AI Agent internship and need skill-gap analysis, a learning plan, project ideas, resume bullets, and interview preparation.";

export default function Home() {
  const [title, setTitle] = useState("AI Agent Intern");
  const [company, setCompany] = useState("Demo Company");
  const [description, setDescription] = useState(defaultDescription);
  const [jobId, setJobId] = useState<number | null>(null);
  const [jobMessage, setJobMessage] = useState("");

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);
  const [query, setQuery] = useState("Python FastAPI RAG project experience");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [profileMessage, setProfileMessage] = useState("");

  const [userGoal, setUserGoal] = useState("I want to apply for an AI Agent internship and need a practical gap analysis and project roadmap.");
  const [runStatus, setRunStatus] = useState<RunStatus>("idle");
  const [steps, setSteps] = useState<StreamStep[]>([]);
  const [contentPreview, setContentPreview] = useState<Record<string, string>>({});
  const [markdownReport, setMarkdownReport] = useState("");
  const [analysisId, setAnalysisId] = useState<number | null>(null);
  const [agentMessage, setAgentMessage] = useState("");
  const eventSourceRef = useRef<EventSource | null>(null);

  async function handleCreateJob() {
    setJobMessage("Creating job...");
    try {
      const job = await createJob({ title, company, description });
      setJobId(job.id);
      setJobMessage(`Job created. job_id=${job.id}`);
    } catch (error) {
      setJobMessage(error instanceof Error ? error.message : "Failed to create job");
    }
  }

  function fillSampleJob() {
    setTitle(sampleTitle);
    setCompany(sampleCompany);
    setDescription(sampleDescription);
    setJobMessage("Sample job filled. Click Create job to continue.");
  }

  function fillSampleGoal() {
    setUserGoal(sampleGoal);
    setAgentMessage("Sample goal filled.");
  }

  async function handleUpload() {
    if (!selectedFile) {
      setProfileMessage("Choose a .md or .txt file first.");
      return;
    }
    setProfileMessage("Uploading profile...");
    try {
      const result = await uploadDocument(selectedFile);
      setUploadResult(result);
      setProfileMessage(`Upload complete. Split into ${result.chunk_count} chunks. Retrieval mode: ${retrievalModeLabel(result.retrieval_mode)}.`);
    } catch (error) {
      setProfileMessage(error instanceof Error ? error.message : "Upload failed");
    }
  }

  async function handleSearch() {
    if (!query.trim()) {
      setProfileMessage("Enter a search query.");
      return;
    }
    setProfileMessage("Searching profile evidence...");
    try {
      const response = await searchDocuments(query, 5);
      setSearchResults(response.results);
      setProfileMessage(`Search complete. Mode: ${retrievalModeLabel(response.retrieval_mode)}. Returned ${response.results.length} chunks.`);
    } catch (error) {
      setProfileMessage(error instanceof Error ? error.message : "Search failed");
    }
  }

  function handleRunAgent() {
    if (!jobId) {
      setAgentMessage("Create a job first.");
      setRunStatus("error");
      return;
    }

    if (!userGoal.trim()) {
      setAgentMessage("Enter a goal.");
      setRunStatus("error");
      return;
    }

    eventSourceRef.current?.close();
    setRunStatus("running");
    setSteps([]);
    setContentPreview({});
    setMarkdownReport("");
    setAnalysisId(null);
    setAgentMessage("Career Agent is running...");

    eventSourceRef.current = runCareerAgentStream(jobId, userGoal, {
      onStep: (payload) => {
        setSteps((current) => [...current, payload]);
      },
      onContent: (payload) => {
        setContentPreview((current) => ({
          ...current,
          [payload.section]: payload.content,
        }));
      },
      onFinal: (payload) => {
        setRunStatus("done");
        setAnalysisId(payload.analysis_id);
        setMarkdownReport(payload.markdown_report);
        setAgentMessage(`Analysis complete. analysis_id=${payload.analysis_id}`);
        setSteps((current) => [
          ...current,
          { name: "final", status: "done", message: "Analysis complete" },
        ]);
      },
      onError: (payload) => {
        setRunStatus("error");
        setAgentMessage(payload.message);
      },
    });
  }

  async function handleCopyReport() {
    if (!markdownReport) return;
    await navigator.clipboard.writeText(markdownReport);
    setAgentMessage("Report copied to clipboard.");
  }

  function handleDownloadReport() {
    if (!markdownReport) return;
    const suffix = analysisId ?? Date.now();
    const blob = new Blob([markdownReport], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `ai-career-agent-report-${suffix}.md`;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
    setAgentMessage("Markdown report downloaded.");
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-6 px-5 py-8">
      <header className="rounded-3xl border border-line bg-white/85 p-7 shadow-card backdrop-blur">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-accent">AI Career Agent</p>
        <h1 className="mt-2 text-3xl font-semibold text-ink">AI Career Agent Workspace</h1>
        <p className="mt-3 max-w-3xl text-base text-muted">
          Job analysis / profile retrieval / skill gaps / learning plans / resume bullets
        </p>
      </header>

      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="flex flex-col gap-6">
          <Card title="1. Job Input" description="Create a job to get a job_id. The agent will run against that job.">
            <button className="button-secondary" onClick={fillSampleJob}>
              Fill sample job
            </button>
            <Field label="Job title">
              <input className="input" value={title} onChange={(event) => setTitle(event.target.value)} />
            </Field>
            <Field label="Company">
              <input className="input" value={company} onChange={(event) => setCompany(event.target.value)} />
            </Field>
            <Field label="Job description">
              <textarea
                className="input min-h-36 resize-y"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
              />
            </Field>
            <div className="flex flex-wrap items-center gap-3">
              <button className="button-primary" onClick={handleCreateJob}>
                Create job
              </button>
              <span className="text-sm text-muted">{jobMessage || "No job created yet"}</span>
            </div>
            {jobId ? <Badge>job_id: {jobId}</Badge> : null}
          </Card>

          <Card title="2. Profile Upload" description="Supports .md and .txt files with fallback search or Embedding + JSON VectorStore.">
            <Field label="Choose file">
              <div className="flex flex-wrap items-center gap-3 rounded-xl border border-line bg-white px-3 py-2 text-sm">
                <label className="button-secondary cursor-pointer">
                  Choose file
                  <input
                    className="sr-only"
                    type="file"
                    accept=".md,.txt"
                    onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
                  />
                </label>
                <span className="text-muted">{selectedFile?.name ?? "No file selected"}</span>
              </div>
            </Field>
            <div className="flex flex-wrap items-center gap-3">
              <button className="button-primary" onClick={handleUpload}>
                Upload profile
              </button>
              <span className="text-sm text-muted">{profileMessage || "No profile uploaded yet"}</span>
            </div>
            {uploadResult ? (
              <div className="rounded-xl bg-paper p-3 text-sm text-ink">
                File: {uploadResult.filename}, type: {uploadResult.file_type}, chunks: {uploadResult.chunk_count},
                retrieval mode: {retrievalModeLabel(uploadResult.retrieval_mode)}
              </div>
            ) : null}
            <Field label="Search test query">
              <input className="input" value={query} onChange={(event) => setQuery(event.target.value)} />
            </Field>
            <button className="button-secondary" onClick={handleSearch}>
              Search profile
            </button>
          </Card>

          <Card title="3. Agent Runner" description="Receives stage-level step/content/final events through SSE.">
            <button className="button-secondary" onClick={fillSampleGoal}>
              Fill sample goal
            </button>
            <Field label="user_goal">
              <textarea
                className="input min-h-24 resize-y"
                value={userGoal}
                onChange={(event) => setUserGoal(event.target.value)}
              />
            </Field>
            <div className="flex flex-wrap items-center gap-3">
              <button className="button-primary" disabled={runStatus === "running"} onClick={handleRunAgent}>
                Run Career Agent
              </button>
              <Badge tone={runStatus === "error" ? "danger" : runStatus === "done" ? "success" : "neutral"}>
                {runStatus}
              </Badge>
            </div>
            <p className="text-sm text-muted">{agentMessage || "Waiting to run"}</p>
          </Card>
        </div>

        <div className="flex flex-col gap-6">
          <Card title="Profile Search Results" description="Confirms whether uploaded profile evidence can be retrieved.">
            {searchResults.length === 0 ? (
              <EmptyText>No search results yet</EmptyText>
            ) : (
              <div className="space-y-3">
                {searchResults.map((result) => (
                  <div key={`${result.source}-${result.chunk_id}`} className="rounded-xl border border-line bg-paper p-3">
                    <div className="mb-2 flex items-center justify-between text-xs text-muted">
                      <span>{result.source}</span>
                      <span>{retrievalModeLabel(result.retrieval_mode)} | score {result.score}</span>
                    </div>
                    <p className="text-sm leading-6 text-ink">{result.content}</p>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card title="Step Log" description="Each agent stage writes start and finish events here.">
            {steps.length === 0 ? (
              <EmptyText>No step logs yet</EmptyText>
            ) : (
              <div className="space-y-2">
                {steps.map((step, index) => (
                  <div key={`${step.name}-${step.status}-${index}`} className="grid grid-cols-[7rem_1fr] gap-3 rounded-xl border border-line bg-white p-3">
                    <Badge tone={step.status === "done" ? "success" : step.status === "error" ? "danger" : "neutral"}>
                      {statusLabel(step.status)}
                    </Badge>
                    <div>
                      <p className="text-sm font-semibold text-ink">{step.name}</p>
                      <p className="text-sm text-muted">{step.message}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card title="Stage Content Preview" description="Latest snippets from SSE content events.">
            {Object.keys(contentPreview).length === 0 ? (
              <EmptyText>No stage content yet</EmptyText>
            ) : (
              <div className="space-y-3">
                {Object.entries(contentPreview).map(([section, content]) => (
                  <details key={section} className="rounded-xl border border-line bg-paper p-3">
                    <summary className="cursor-pointer text-sm font-semibold text-ink">{section}</summary>
                    <pre className="mt-3 max-h-48 overflow-auto whitespace-pre-wrap text-xs leading-5 text-muted">{content}</pre>
                  </details>
                ))}
              </div>
            )}
          </Card>

          <Card title="4. Report Viewer" description="Renders the final Markdown report and keeps copy/download actions available.">
            <div className="mb-3 flex justify-end gap-3">
              <button className="button-secondary" disabled={!markdownReport} onClick={handleCopyReport}>
                Copy Markdown
              </button>
              <button className="button-secondary" disabled={!markdownReport} onClick={handleDownloadReport}>
                Download Markdown report
              </button>
            </div>
            {markdownReport ? (
              <article className="markdown-body max-h-[48rem] overflow-auto rounded-2xl border border-line bg-white p-5">
                <ReactMarkdown>{markdownReport}</ReactMarkdown>
              </article>
            ) : (
              <EmptyText>Run Career Agent to display the final Markdown report</EmptyText>
            )}
          </Card>
        </div>
      </section>
    </main>
  );
}

function statusLabel(status: StreamStep["status"]) {
  if (status === "running") return "Running";
  if (status === "done") return "Done";
  return "Error";
}

function retrievalModeLabel(mode: string) {
  if (mode === "fallback") return "fallback keyword search";
  if (mode === "vector") return "Embedding + JSON VectorStore";
  if (mode === "fallback_due_to_vector_error") return "vector retrieval failed; fell back to keyword search";
  return mode || "unknown mode";
}

function Card({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-3xl border border-line bg-white p-5 shadow-card">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-ink">{title}</h2>
        <p className="mt-1 text-sm text-muted">{description}</p>
      </div>
      <div className="space-y-4">{children}</div>
    </section>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium text-ink">{label}</span>
      {children}
    </label>
  );
}

function Badge({
  children,
  tone = "neutral",
}: {
  children: React.ReactNode;
  tone?: "neutral" | "success" | "danger";
}) {
  const color =
    tone === "success"
      ? "bg-emerald-50 text-emerald-700 ring-emerald-200"
      : tone === "danger"
        ? "bg-red-50 text-red-700 ring-red-200"
        : "bg-slate-50 text-slate-700 ring-slate-200";
  return <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ring-1 ${color}`}>{children}</span>;
}

function EmptyText({ children }: { children: React.ReactNode }) {
  return <p className="rounded-xl border border-dashed border-line bg-paper p-4 text-sm text-muted">{children}</p>;
}

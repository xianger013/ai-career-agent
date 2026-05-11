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
  "需要 Python、FastAPI、LLM API、Prompt Engineering、RAG 文档检索、Agent 工作流和 pytest 测试经验。";
const sampleTitle = "AI Agent 实习生";
const sampleCompany = "Demo AI Lab";
const sampleDescription = [
  "岗位职责：参与 AI Agent 应用后端开发，完成岗位 JD 分析、用户资料检索、能力差距分析和学习路线生成。",
  "技术要求：熟悉 Python、FastAPI、SQL、LLM API 调用、Prompt Engineering、RAG 文档检索、SSE 流式输出和基础前端协作。",
  "加分项：了解 Agent 工作流、Tool Calling、pytest 自动化测试、Next.js 展示页和 Markdown 报告生成。",
].join("\n\n");
const sampleGoal =
  "我想申请 AI Agent 实习生岗位，希望知道能力差距、学习路线、项目建议、简历描述和面试准备。";

export default function Home() {
  const [title, setTitle] = useState("AI Agent 实习生");
  const [company, setCompany] = useState("Demo Company");
  const [description, setDescription] = useState(defaultDescription);
  const [jobId, setJobId] = useState<number | null>(null);
  const [jobMessage, setJobMessage] = useState("");

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);
  const [query, setQuery] = useState("Python FastAPI RAG 项目经验");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [profileMessage, setProfileMessage] = useState("");

  const [userGoal, setUserGoal] = useState("我想申请 AI Agent 实习岗位，希望知道差距和项目路线。");
  const [runStatus, setRunStatus] = useState<RunStatus>("idle");
  const [steps, setSteps] = useState<StreamStep[]>([]);
  const [contentPreview, setContentPreview] = useState<Record<string, string>>({});
  const [markdownReport, setMarkdownReport] = useState("");
  const [analysisId, setAnalysisId] = useState<number | null>(null);
  const [agentMessage, setAgentMessage] = useState("");
  const eventSourceRef = useRef<EventSource | null>(null);

  async function handleCreateJob() {
    setJobMessage("正在创建岗位...");
    try {
      const job = await createJob({ title, company, description });
      setJobId(job.id);
      setJobMessage(`岗位已创建，job_id=${job.id}`);
    } catch (error) {
      setJobMessage(error instanceof Error ? error.message : "创建岗位失败");
    }
  }

  function fillSampleJob() {
    setTitle(sampleTitle);
    setCompany(sampleCompany);
    setDescription(sampleDescription);
    setJobMessage("已填充示例岗位，请点击创建岗位。");
  }

  function fillSampleGoal() {
    setUserGoal(sampleGoal);
    setAgentMessage("已填充示例目标。");
  }

  async function handleUpload() {
    if (!selectedFile) {
      setProfileMessage("请先选择 .md 或 .txt 文件。");
      return;
    }
    setProfileMessage("正在上传资料...");
    try {
      const result = await uploadDocument(selectedFile);
      setUploadResult(result);
      setProfileMessage(`上传成功，切分 ${result.chunk_count} 个片段，检索模式：${retrievalModeLabel(result.retrieval_mode)}。`);
    } catch (error) {
      setProfileMessage(error instanceof Error ? error.message : "上传失败");
    }
  }

  async function handleSearch() {
    if (!query.trim()) {
      setProfileMessage("请填写检索 query。");
      return;
    }
    setProfileMessage("正在检索资料...");
    try {
      const response = await searchDocuments(query, 5);
      setSearchResults(response.results);
      setProfileMessage(`检索完成，模式：${retrievalModeLabel(response.retrieval_mode)}，返回 ${response.results.length} 条片段。`);
    } catch (error) {
      setProfileMessage(error instanceof Error ? error.message : "检索失败");
    }
  }

  function handleRunAgent() {
    if (!jobId) {
      setAgentMessage("请先创建岗位。");
      setRunStatus("error");
      return;
    }

    if (!userGoal.trim()) {
      setAgentMessage("请填写目标。");
      setRunStatus("error");
      return;
    }

    eventSourceRef.current?.close();
    setRunStatus("running");
    setSteps([]);
    setContentPreview({});
    setMarkdownReport("");
    setAnalysisId(null);
    setAgentMessage("Career Agent 正在运行...");

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
        setAgentMessage(`分析完成，analysis_id=${payload.analysis_id}`);
        setSteps((current) => [
          ...current,
          { name: "final", status: "done", message: "分析完成" },
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
    setAgentMessage("报告已复制到剪贴板。");
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
    setAgentMessage("Markdown 报告已下载。");
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-6 px-5 py-8">
      <header className="rounded-3xl border border-line bg-white/85 p-7 shadow-card backdrop-blur">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-accent">AI Career Agent</p>
        <h1 className="mt-2 text-3xl font-semibold text-ink">AI Career Agent 工作台</h1>
        <p className="mt-3 max-w-3xl text-base text-muted">
          岗位分析 / 资料检索 / 能力差距 / 学习路线 / 简历描述生成
        </p>
      </header>

      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="flex flex-col gap-6">
          <Card title="1. 岗位输入区" description="创建岗位后会得到 job_id，后续 Agent 基于该岗位运行。">
            <button className="button-secondary" onClick={fillSampleJob}>
              填充示例岗位
            </button>
            <Field label="岗位标题">
              <input className="input" value={title} onChange={(event) => setTitle(event.target.value)} />
            </Field>
            <Field label="公司">
              <input className="input" value={company} onChange={(event) => setCompany(event.target.value)} />
            </Field>
            <Field label="岗位 JD">
              <textarea
                className="input min-h-36 resize-y"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
              />
            </Field>
            <div className="flex flex-wrap items-center gap-3">
              <button className="button-primary" onClick={handleCreateJob}>
                创建岗位
              </button>
              <span className="text-sm text-muted">{jobMessage || "尚未创建岗位"}</span>
            </div>
            {jobId ? <Badge>job_id: {jobId}</Badge> : null}
          </Card>

          <Card title="2. 个人资料上传区" description="当前支持 .md / .txt；可使用 fallback 检索或 Embedding + JSON VectorStore。">
            <Field label="选择文件">
              <input
                className="block w-full rounded-xl border border-line bg-white px-3 py-2 text-sm"
                type="file"
                accept=".md,.txt"
                onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
              />
            </Field>
            <div className="flex flex-wrap items-center gap-3">
              <button className="button-primary" onClick={handleUpload}>
                上传资料
              </button>
              <span className="text-sm text-muted">{profileMessage || "尚未上传资料"}</span>
            </div>
            {uploadResult ? (
              <div className="rounded-xl bg-paper p-3 text-sm text-ink">
                文件：{uploadResult.filename}，类型：{uploadResult.file_type}，片段：{uploadResult.chunk_count}
                ，检索模式：{retrievalModeLabel(uploadResult.retrieval_mode)}
              </div>
            ) : null}
            <Field label="检索测试 query">
              <input className="input" value={query} onChange={(event) => setQuery(event.target.value)} />
            </Field>
            <button className="button-secondary" onClick={handleSearch}>
              检索资料
            </button>
          </Card>

          <Card title="3. Agent 运行区" description="通过 SSE 接收阶段式 step/content/final 事件。">
            <button className="button-secondary" onClick={fillSampleGoal}>
              填充示例目标
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
                运行 Career Agent
              </button>
              <Badge tone={runStatus === "error" ? "danger" : runStatus === "done" ? "success" : "neutral"}>
                {runStatus}
              </Badge>
            </div>
            <p className="text-sm text-muted">{agentMessage || "等待运行"}</p>
          </Card>
        </div>

        <div className="flex flex-col gap-6">
          <Card title="资料检索结果" description="用于确认上传资料是否能被召回。">
            {searchResults.length === 0 ? (
              <EmptyText>暂无检索结果</EmptyText>
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

          <Card title="步骤日志" description="每个 Agent 阶段开始和结束都会写入这里。">
            {steps.length === 0 ? (
              <EmptyText>暂无步骤日志</EmptyText>
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

          <Card title="阶段内容预览" description="SSE content 事件的最新片段。">
            {Object.keys(contentPreview).length === 0 ? (
              <EmptyText>暂无阶段内容</EmptyText>
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

          <Card title="4. 报告展示区" description="渲染最终 Markdown 报告，同时保留复制和下载原文。">
            <div className="mb-3 flex justify-end gap-3">
              <button className="button-secondary" disabled={!markdownReport} onClick={handleCopyReport}>
                复制 Markdown
              </button>
              <button className="button-secondary" disabled={!markdownReport} onClick={handleDownloadReport}>
                下载 Markdown 报告
              </button>
            </div>
            {markdownReport ? (
              <article className="markdown-body max-h-[48rem] overflow-auto rounded-2xl border border-line bg-white p-5">
                <ReactMarkdown>{markdownReport}</ReactMarkdown>
              </article>
            ) : (
              <EmptyText>运行 Career Agent 后显示最终 Markdown 报告</EmptyText>
            )}
          </Card>
        </div>
      </section>
    </main>
  );
}

function statusLabel(status: StreamStep["status"]) {
  if (status === "running") return "进行中";
  if (status === "done") return "已完成";
  return "错误";
}

function retrievalModeLabel(mode: string) {
  if (mode === "fallback") return "fallback keyword search";
  if (mode === "vector") return "Embedding + JSON VectorStore";
  if (mode === "fallback_due_to_vector_error") return "向量检索失败，已回退 fallback";
  return mode || "未知模式";
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

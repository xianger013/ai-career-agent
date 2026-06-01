const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export type JobPayload = {
  title: string;
  company: string;
  description: string;
};

export type StreamStep = {
  name: string;
  status: "running" | "done" | "error";
  message: string;
};

export type StreamContent = {
  section: string;
  content: string;
};

export type StreamFinal = {
  analysis_id: number;
  markdown_report: string;
  report_path?: string;
};

export type StreamHandlers = {
  onStep?: (payload: StreamStep) => void;
  onContent?: (payload: StreamContent) => void;
  onFinal?: (payload: StreamFinal) => void;
  onError?: (payload: { message: string }) => void;
};

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function createJob(payload: JobPayload) {
  const response = await fetch(`${API_BASE_URL}/api/jobs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse<{
    id: number;
    title: string;
    company: string;
    description: string;
    created_at: string;
    updated_at: string;
  }>(response);
}

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
    method: "POST",
    body: formData,
  });
  return parseResponse<{
    id: number;
    document_id: number;
    filename: string;
    file_type: string;
    created_at: string;
    chunk_count: number;
    retrieval_mode: string;
    retrieval_error?: string | null;
  }>(response);
}

export async function searchDocuments(query: string, topK = 5) {
  const response = await fetch(`${API_BASE_URL}/api/documents/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k: topK }),
  });
  return parseResponse<{
    retrieval_mode: string;
    retrieval_error?: string | null;
    results: Array<{
      document_id: number | null;
      chunk_id: string;
      content: string;
      score: number;
      source: string;
      metadata: Record<string, unknown>;
      retrieval_mode: string;
    }>;
  }>(response);
}

export function runCareerAgentStream(jobId: number, userGoal: string, handlers: StreamHandlers) {
  const url = new URL(`${API_BASE_URL}/api/agents/career/analyze/stream`);
  url.searchParams.set("job_id", String(jobId));
  url.searchParams.set("user_goal", userGoal);

  const source = new EventSource(url.toString());

  source.addEventListener("step", (event) => {
    handlers.onStep?.(JSON.parse(event.data) as StreamStep);
  });

  source.addEventListener("content", (event) => {
    handlers.onContent?.(JSON.parse(event.data) as StreamContent);
  });

  source.addEventListener("final", (event) => {
    handlers.onFinal?.(JSON.parse(event.data) as StreamFinal);
    source.close();
  });

  source.addEventListener("error", (event) => {
    if ("data" in event && typeof event.data === "string" && event.data) {
      handlers.onError?.(JSON.parse(event.data) as { message: string });
    } else {
      handlers.onError?.({ message: "Stream connection failed. Check that the backend is running." });
    }
    source.close();
  });

  return source;
}

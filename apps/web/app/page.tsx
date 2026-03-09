"use client";

import { useState } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isValidUrl = (() => {
    try {
      const parsed = new URL(url);
      return parsed.protocol === "http:" || parsed.protocol === "https:";
    } catch {
      return false;
    }
  })();

  const apiUrl =
    process.env.NEXT_PUBLIC_BE_API_URL ?? "http://localhost:8000";

  const handleGenerate = async () => {
    setError(null);
    if (!url.trim()) {
      setError("Please enter a URL.");
      return;
    }
    setIsLoading(true);
    try {
      const response = await fetch(`${apiUrl}/export-content`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const blob = await response.blob();
      const disposition = response.headers.get("Content-Disposition");
      const filenameMatch = disposition?.match(/filename="([^"]+)"/);
      const filename = filenameMatch?.[1] ?? "llms.txt";

      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = objectUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(objectUrl);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans">
      <main className="w-full max-w-xl rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-semibold text-zinc-900">
          Generate `llms.txt`
        </h1>
        <p className="mt-2 text-sm text-zinc-600">
          Enter a URL and download the generated file.
        </p>

        <div className="mt-6 flex flex-col gap-3">
          <input
            type="url"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="h-11 w-full rounded-lg border border-zinc-300 px-3 text-sm text-zinc-900 placeholder:text-zinc-400 outline-none focus:border-zinc-500"
          />
          <button
            onClick={handleGenerate}
            disabled={isLoading || !isValidUrl}
            className="h-11 w-full rounded-lg bg-zinc-900 text-sm font-medium text-white transition disabled:opacity-60"
          >
            {isLoading ? "Generating..." : "Generate File"}
          </button>
          {error ? (
            <p className="text-sm text-red-600">{error}</p>
          ) : null}
        </div>
      </main>
    </div>
  );
}

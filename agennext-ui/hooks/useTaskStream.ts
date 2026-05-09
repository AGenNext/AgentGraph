// hooks/useTaskStream.ts
"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { createTaskStream } from "@/lib/a2a-client";
import type { TaskStreamEvent, TaskState } from "@/types/a2a";

interface StreamState {
  events: TaskStreamEvent[];
  state: TaskState | null;
  statusMessage: string | null;
  isDone: boolean;
  isError: boolean;
  errorMessage: string | null;
}

export function useTaskStream(taskId: string | null) {
  const [stream, setStream] = useState<StreamState>({
    events: [],
    state: null,
    statusMessage: null,
    isDone: false,
    isError: false,
    errorMessage: null,
  });

  const cleanupRef = useRef<(() => void) | null>(null);

  const reset = useCallback(() => {
    setStream({
      events: [],
      state: null,
      statusMessage: null,
      isDone: false,
      isError: false,
      errorMessage: null,
    });
  }, []);

  useEffect(() => {
    if (!taskId) return;

    reset();

    const cleanup = createTaskStream(taskId, {
      onEvent: (event) => {
        setStream((prev) => {
          const newEvents = [...prev.events, event];

          if (event.type === "status" && event.status) {
            const msg =
              event.status.message?.parts
                .filter((p) => p.type === "text")
                .map((p) => (p as { type: "text"; text: string }).text)
                .join("") ?? null;

            return {
              ...prev,
              events: newEvents,
              state: event.status.state,
              statusMessage: msg,
              isDone: event.final ?? false,
            };
          }

          if (event.type === "error") {
            return {
              ...prev,
              events: newEvents,
              isError: true,
              errorMessage: event.error?.message ?? "Unknown error",
              isDone: true,
            };
          }

          return { ...prev, events: newEvents };
        });
      },
      onError: () => {
        setStream((prev) => ({
          ...prev,
          isError: true,
          errorMessage: "Stream connection lost",
          isDone: true,
        }));
      },
      onDone: () => {
        setStream((prev) => ({ ...prev, isDone: true }));
      },
    });

    cleanupRef.current = cleanup;
    return cleanup;
  }, [taskId, reset]);

  return { ...stream, reset };
}

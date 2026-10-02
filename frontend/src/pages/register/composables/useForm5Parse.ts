import { onBeforeUnmount, ref } from "vue";

import { buildParseScript, simulateParseDuration } from "@/domain/mockData";
import type { LogLine } from "@/domain/mockData";
import type { ParsedForm5 } from "@/domain/registration";

/**
 * Drives the simulated parse pass (FR-1): replays `buildParseScript` line by
 * line with its holds, then hands the parsed payload to `onComplete`.
 *
 * A run token plus a timer set guard the async loop — a restart (start over,
 * new file) bumps the token and clears pending timers, so a stale script can
 * never write into the restarted flow or leak timeouts.
 */
export function useForm5Parse(onComplete: (payload: ParsedForm5) => void) {
  const logLines = ref<LogLine[]>([]);
  const isParsing = ref(false);

  // Guards against a stale parse script writing into a restarted flow.
  let runToken = 0;
  const timers = new Set<ReturnType<typeof setTimeout>>();

  function schedule(callback: () => void, delay: number) {
    const handle = setTimeout(() => {
      timers.delete(handle);
      callback();
    }, delay);
    timers.add(handle);
  }

  function cancelRun() {
    runToken += 1;
    for (const handle of timers) clearTimeout(handle);
    timers.clear();
  }

  onBeforeUnmount(cancelRun);

  async function runParse(payload: ParsedForm5) {
    cancelRun();
    const token = runToken;

    logLines.value = [];
    isParsing.value = true;
    const script = buildParseScript(payload, simulateParseDuration());

    for (const line of script) {
      if (token !== runToken) return;
      logLines.value = [...logLines.value, line];
      if (line.hold > 0) {
        await new Promise<void>(resolve =>
          schedule(() => resolve(), line.hold)
        );
      }
    }

    if (token !== runToken) return;
    isParsing.value = false;
    onComplete(payload);
  }

  /** Stops any running script, drops its pending timers and clears the log. */
  function resetParse() {
    cancelRun();
    logLines.value = [];
    isParsing.value = false;
  }

  return { logLines, isParsing, runParse, resetParse };
}

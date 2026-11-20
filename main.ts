// Entry program for make.fun's news-image-20261120 contest.
//
// The repository ships one finished front page, entry.png (drawn by
// draw.py). The grader runs this file twice, offline, and both runs
// must leave identical bytes in the output folder — so the program
// does the simplest possible thing: copy the picture next to it into
// the output directory and report its size. MAKEFUN_OUTPUT_DIR stands
// in for /output when the program runs outside the grader.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");

copyFileSync(new URL("./entry.png", import.meta.url), target);

const { size } = statSync(target);
console.log(`entry.png -> ${target} (${size} bytes)`);

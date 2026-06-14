#!/usr/bin/env node
/**
 * Render a slide HTML file to PNG using the local Chrome install.
 * Usage: node render_slide.js <input.html> <output.png> [width] [height]
 */
const puppeteer = require("puppeteer-core");
const path = require("path");
const fs = require("fs");

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const [, , input, output, w, h] = process.argv;

if (!input || !output) {
  console.error("Usage: node render_slide.js <input.html> <output.png> [width] [height]");
  process.exit(1);
}

const WIDTH  = parseInt(w  || "1280");
const HEIGHT = parseInt(h || "720");

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 2 });
  const html = fs.readFileSync(path.resolve(input), "utf8");
  await page.setContent(html, { waitUntil: "networkidle0" });
  await page.screenshot({ path: path.resolve(output), fullPage: false });
  await browser.close();
  console.log(`Rendered ${WIDTH}×${HEIGHT} → ${output}`);
})();

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import puppeteer from 'puppeteer-core';

const root = process.cwd();
const baseUrl = (process.argv[2] || 'http://127.0.0.1:4173').replace(/\/$/, '');
const chromePath = process.env.CHROME_BIN || '/usr/bin/google-chrome';
const moduleDir = path.join(root, 'modules');
const pages = [
  'index.html',
  ...fs.readdirSync(moduleDir)
    .filter(name => name.endsWith('.html'))
    .sort()
    .map(name => `modules/${name}`),
];
const viewports = [
  { name: 'narrow', width: 360, height: 800 },
  { name: 'standard', width: 390, height: 844 },
];
const artifactDir = path.join(root, 'mobile-readability-artifacts');
fs.mkdirSync(artifactDir, { recursive: true });

if (!fs.existsSync(chromePath)) {
  throw new Error(`Chromium executable not found: ${chromePath}`);
}

const browser = await puppeteer.launch({
  executablePath: chromePath,
  headless: true,
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});

const failures = [];
let checks = 0;

for (const viewport of viewports) {
  for (const rel of pages) {
    const page = await browser.newPage();
    await page.setViewport({
      width: viewport.width,
      height: viewport.height,
      deviceScaleFactor: 1,
      isMobile: true,
      hasTouch: true,
    });

    const url = `${baseUrl}/${rel}`;
    let pageFailures = [];
    try {
      const response = await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
      if (!response || !response.ok()) {
        pageFailures.push(`HTTP load failed (${response?.status() ?? 'no response'})`);
      }

      await page.evaluate(async () => {
        if (document.fonts?.ready) await document.fonts.ready;
      });
      await page.waitForFunction(
        () => !document.querySelector('script[data-site-nav]') || document.documentElement.dataset.siteNavInitialized === '1',
        { timeout: 5000 },
      ).catch(() => {});

      const runtimeFindings = await page.evaluate(async ({ viewportWidth }) => {
        const EPS = 1.5;
        const findings = [];
        const style = el => getComputedStyle(el);
        const rect = el => el.getBoundingClientRect();
        const visible = el => {
          const cs = style(el);
          const r = rect(el);
          return cs.display !== 'none' && cs.visibility !== 'hidden' && Number(cs.opacity || 1) > 0 && r.width > 0 && r.height > 0;
        };
        const scrollableX = el => {
          const cs = style(el);
          return /^(auto|scroll)$/.test(cs.overflowX) && el.scrollWidth > el.clientWidth + EPS;
        };
        const insideIntentionalScroller = el => {
          for (let node = el; node && node !== document.documentElement; node = node.parentElement) {
            if (scrollableX(node)) return true;
          }
          return false;
        };
        const ignoredOffCanvas = el => !!el.closest('.site-sidebar,.page-toc,[aria-hidden="true"]');
        const shortLabel = el => {
          const id = el.id ? `#${el.id}` : '';
          const cls = typeof el.className === 'string' && el.className.trim()
            ? `.${el.className.trim().split(/\s+/).slice(0, 2).join('.')}`
            : '';
          return `${el.tagName.toLowerCase()}${id}${cls}`;
        };

        const docWidth = document.documentElement.scrollWidth;
        if (docWidth > viewportWidth + EPS) {
          findings.push(`document overflow: scrollWidth=${docWidth}px > viewport=${viewportWidth}px`);
          const rogues = [...document.querySelectorAll('body *')]
            .filter(visible)
            .filter(el => !ignoredOffCanvas(el))
            .filter(el => {
              const r = rect(el);
              return (r.left < -EPS || r.right > viewportWidth + EPS) && !insideIntentionalScroller(el);
            })
            .slice(0, 10)
            .map(el => {
              const r = rect(el);
              return `${shortLabel(el)}[${r.left.toFixed(1)},${r.right.toFixed(1)}]`;
            });
          if (rogues.length) findings.push(`overflow candidates: ${rogues.join(', ')}`);
        }

        for (const selector of ['table', '.eq', 'pre']) {
          for (const el of document.querySelectorAll(selector)) {
            if (!visible(el) || el.scrollWidth <= el.clientWidth + EPS) continue;
            if (!insideIntentionalScroller(el)) {
              findings.push(`${shortLabel(el)} has clipped horizontal content without an x-scroll container`);
            }
          }
        }

        for (const el of document.querySelectorAll('figure,figure img,figcaption')) {
          if (!visible(el) || ignoredOffCanvas(el) || insideIntentionalScroller(el)) continue;
          const r = rect(el);
          if (r.left < -EPS || r.right > viewportWidth + EPS || r.width > viewportWidth + EPS) {
            findings.push(`${shortLabel(el)} exceeds the mobile viewport (${r.width.toFixed(1)}px wide)`);
          }
        }

        window.scrollTo(0, Math.min(1200, Math.max(0, document.documentElement.scrollHeight / 3)));
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));

        const top = document.querySelector('.top');
        const mobileToc = document.querySelector('.mobile-toc');
        if (top && mobileToc && visible(top) && visible(mobileToc)) {
          const topRect = rect(top);
          const tocRect = rect(mobileToc);
          if (tocRect.top < topRect.bottom - EPS) {
            findings.push(`sticky overlap: mobile TOC starts at ${tocRect.top.toFixed(1)}px before header ends at ${topRect.bottom.toFixed(1)}px`);
          }
        }

        for (const button of document.querySelectorAll('.nav-drawer-btn')) {
          if (!visible(button)) continue;
          const r = rect(button);
          if (r.width < 40 || r.height < 40) {
            findings.push(`${shortLabel(button)} tap target is ${r.width.toFixed(1)}×${r.height.toFixed(1)}px (<40px)`);
          }
          if (top && visible(top) && r.bottom > rect(top).bottom + EPS) {
            findings.push(`${shortLabel(button)} extends below the sticky header and can cover reading content`);
          }
        }

        if (mobileToc && visible(mobileToc)) {
          const summary = mobileToc.querySelector('summary');
          if (summary && visible(summary) && rect(summary).height < 36) {
            findings.push(`mobile TOC summary tap target is ${rect(summary).height.toFixed(1)}px high (<36px)`);
          }
          for (const link of mobileToc.querySelectorAll('a')) {
            if (visible(link) && rect(link).height < 32) {
              findings.push(`mobile TOC link "${link.textContent.trim()}" is ${rect(link).height.toFixed(1)}px high (<32px)`);
            }
          }
        }

        const anchorHeading = document.querySelector('main h2[id]');
        if (anchorHeading) {
          anchorHeading.scrollIntoView();
          await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
          const stickyBottom = [document.querySelector('.top'), document.querySelector('.mobile-toc')]
            .filter(el => el && visible(el))
            .reduce((m, el) => Math.max(m, rect(el).bottom), 0);
          const headingTop = rect(anchorHeading).top;
          if (headingTop < stickyBottom - EPS) {
            findings.push(`anchor heading is obscured: h2 top=${headingTop.toFixed(1)}px, sticky bottom=${stickyBottom.toFixed(1)}px`);
          }
        }

        return findings;
      }, { viewportWidth: viewport.width });

      pageFailures.push(...runtimeFindings);
    } catch (error) {
      pageFailures.push(`runtime exception: ${error instanceof Error ? error.message : String(error)}`);
    }

    checks += 1;
    if (pageFailures.length) {
      const stem = rel.replace(/[\\/]/g, '__').replace(/\.html$/, '');
      const shot = path.join(artifactDir, `${stem}__${viewport.name}.png`);
      await page.screenshot({ path: shot, fullPage: true }).catch(() => {});
      failures.push({ rel, viewport: viewport.name, messages: pageFailures });
    }
    await page.close();
  }
}

await browser.close();

if (failures.length) {
  console.error(`MOBILE READABILITY SEAL FAIL: ${failures.length}/${checks} page×viewport checks failed`);
  for (const failure of failures) {
    console.error(`\n[${failure.viewport}] ${failure.rel}`);
    for (const message of failure.messages) console.error(` - ${message}`);
  }
  process.exit(1);
}

console.log(
  `MOBILE READABILITY SEAL PASS: ${pages.length} pages × ${viewports.length} mobile viewports; ` +
  'no document-level horizontal overflow; table/equation/pre overflow remains scrollable; figures fit; ' +
  'sticky header/TOC geometry, anchor clearance, drawer buttons, and mobile TOC tap targets validated.',
);

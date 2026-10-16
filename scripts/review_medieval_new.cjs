const { chromium } = require('C:/Users/Pichau/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const numbers = process.argv.slice(2).map(Number).filter(Number.isInteger);
const root = 'http://127.0.0.1:8976/hqs/estradas-do-crepusculo/ler/';
const out = path.join(__dirname, '..', '..', 'arc-audit', 'review-451-502');
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await chromium.launch({headless:true, executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', args:['--no-sandbox']});
  const results = [];
  for (const number of numbers) {
    for (const [mode, width, height] of [['desktop',1440,1100],['mobile',390,844]]) {
      const page = await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
      const response = await page.goto(root + number + '/', {waitUntil:'networkidle'});
      if (response.status() !== 200) throw new Error(`${number} HTTP ${response.status()}`);
      const stage = page.locator('.twilight-page-stage');
      await stage.locator('img').waitFor();
      await stage.screenshot({path:path.join(out,`${number}-${mode}.png`)});
      const balloons = await stage.locator('.twilight-page-speech').evaluateAll(nodes => nodes.map(node => {
        const a = node.getBoundingClientRect(), b = node.parentElement.getBoundingClientRect();
        return {speaker:node.querySelector('strong')?.textContent, x:(a.x-b.x)/b.width*100, y:(a.y-b.y)/b.height*100, w:a.width/b.width*100, h:a.height/b.height*100, target_x:node.dataset.targetX,target_y:node.dataset.targetY, overflow:a.bottom>b.bottom};
      }));
      results.push({number,mode,balloons});
      await page.close();
    }
  }
  fs.writeFileSync(path.join(out,'balloon-boxes.json'),JSON.stringify(results,null,2));
  await browser.close();
  console.log(`${results.length} renders; ${results.reduce((n,p)=>n+p.balloons.filter(b=>b.overflow).length,0)} balloon overflows`);
})().catch(e=>{console.error(e);process.exitCode=1});

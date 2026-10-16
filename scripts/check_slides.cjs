const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('/Users/jmao1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  const page = await browser.newPage({viewport:{width:1440,height:900}});
  const errors=[];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(pathToFileURL(path.join(root,'slides.html')).href);
  await page.waitForFunction(()=>window.Reveal?.isReady());
  await page.waitForTimeout(1200);
  const total = await page.evaluate(()=>Reveal.getTotalSlides());
  fs.mkdirSync(path.join(root,'qa'),{recursive:true});
  const results=[];
  for(let i=0;i<total;i++){
    await page.evaluate(i=>Reveal.slide(i,0,99),i);
    await page.waitForTimeout(900);
    results.push(await page.evaluate(()=>{
      const s=Reveal.getCurrentSlide();
      const r=s.getBoundingClientRect();
      const outside=[...s.querySelectorAll('h1,h2,p,li,table,img,.katex-display')].filter(e=>!e.closest('.notes')&&!e.closest('[aria-hidden="true"]')).map(e=>{
        const b=e.getBoundingClientRect();
        return {tag:e.tagName,text:e.textContent.slice(0,90),left:b.left,right:b.right,bottom:b.bottom,top:b.top};
      }).filter(b=>b.right>r.right+2||b.left<r.left-2||b.bottom>r.bottom+2);
      return {title:s.querySelector('h1,h2')?.textContent,slideHeight:r.height,scrollHeight:s.scrollHeight,clientHeight:s.clientHeight,outside,brokenImages:[...s.querySelectorAll('img')].filter(i=>!i.complete||i.naturalWidth===0).length};
    }));
    await page.screenshot({path:path.join(root,'qa','slide-'+String(i).padStart(2,'0')+'.png')});
  }
  const math = await page.evaluate(()=>({rendered:document.querySelectorAll('.katex').length,errors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent)}));
  fs.writeFileSync(path.join(root,'qa','layout.json'),JSON.stringify({total,errors,math,results},null,2));
  console.log(JSON.stringify({total,errors,math,overflows:results.filter(x=>x.outside.length||x.brokenImages)},null,2));
  await browser.close();
})();

// Run Playwright MCP from the repository root, HTTP :8768.
async (page) => {
  const check=(condition,message)=>{if(!condition)throw new Error(message)};
  const base='http://127.0.0.1:8768/';
  const out='site/screenshots/issue-468/';
  const errors=[]; const onError=e=>errors.push(e.message);
  page.on('pageerror',onError); page.setDefaultTimeout(5000);
  try {
    await page.setViewportSize({width:1440,height:1000});
    await page.goto(base+'#processes',{waitUntil:'domcontentloaded'});
    await page.reload({waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>document.querySelector('[data-site-version]')?.textContent==='v2.8.1');
    const proposal=page.locator('#a-in-proposal'); const summary=proposal.locator('summary');
    check(await proposal.locator('[data-ain-step]').count()===24,'24 steps');
    check(await proposal.locator('button').count()===0,'proposal has no fake copy buttons');
    await summary.focus();await page.keyboard.press('Enter');
    check(await proposal.evaluate(el=>el.open),'Enter opens proposal');
    await page.keyboard.press('Space');
    check(!(await proposal.evaluate(el=>el.open)),'Space closes proposal');
    await page.keyboard.press('Enter');
    const link=proposal.locator('a');
    check((await link.getAttribute('href')).endsWith('/docs/rfc/2026-11-a-in-decomposition.md'),'RFC link');
    await page.evaluate(()=>document.activeElement.blur());
    await page.evaluate(()=>scrollTo(0,0));
    await page.screenshot({path:out+'after-processes-desktop.png',timeout:5000});
    await proposal.screenshot({path:out+'after-route-desktop.png',timeout:5000});
    // Exercise the existing real copy handler without host clipboard permission.
    await page.evaluate(()=>{window.ainCopied=[];Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.ainCopied.push(text)}})});
    const copies=page.locator('#bcreq-testkit-steps .testkit-copy');
    check(await copies.count()===14,'14 existing copy buttons');
    for(let i=0;i<14;i++){
      await copies.nth(i).click();
      await page.waitForFunction(n=>window.ainCopied.length===n,i+1);
    }
    check(await page.evaluate(()=>window.ainCopied.every(t=>t.startsWith('<!-- mango-')&&t.length>500)),'all prompts copied with IDs');
    for(const theme of ['light','dark']){
      await page.setViewportSize({width:390,height:844});
      await page.evaluate(theme=>document.documentElement.dataset.theme=theme,theme);
      check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'no mobile overflow: '+theme);
    }
    await page.waitForFunction(()=>document.querySelector('#toast').dataset.visible!=='true');
    await proposal.screenshot({path:out+'after-route-mobile-dark.png',timeout:5000});
    await page.goto(base+'#standards?section=ttz',{waitUntil:'domcontentloaded'});
    await page.locator('#standard-ttz').waitFor({state:'visible'});
    check(await page.locator('#standards > details.standards-group').count()===3,'three standards groups');
    check(await page.locator('#standard-ttz').evaluate(el=>el.closest('details').open),'TTZ deep link preserved');
    await page.goto(base+'#catalog',{waitUntil:'domcontentloaded'});
    // Catalog data is independently counted to avoid tying the test to card markup.
    const catalog=await page.evaluate(async()=>(await(await fetch('data/prompts.json')).json()).prompts);
    check(catalog.filter(x=>x.classId).length===39,'39 classes');
    check(errors.length===0,'runtime errors: '+errors.join('; '));
    return {proposedSteps:24,copyButtons:14,copiedPrompts:14,standardsGroups:3,themes:2,mobile:'passed',keyboard:'passed',runtimeErrors:errors};
  } finally {page.off('pageerror',onError);}
}

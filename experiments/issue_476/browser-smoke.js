async (page) => {
  const base = 'http://127.0.0.1:8768/';
  const shots = '/tmp/gh-issue-solver-1794171263541/site/screenshots/issue-476/';
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.setViewportSize({width:1280,height:960});
  await page.goto(base+'#processes', {waitUntil:'domcontentloaded'});
  await page.reload({waitUntil:'domcontentloaded'});
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);
  await page.waitForFunction(() => document.querySelectorAll('[data-ain-step]').length === 24);
  const steps = await page.evaluate(async () => (await (await fetch('data/a-in-kit.json')).json()).steps);
  if (await page.locator('.testkit-step-layout').count() !== 35) throw Error('Card form/count changed');
  if (await page.locator('.process-help').count() !== 1) throw Error('Help lost');
  for (const step of steps) {
    const card = page.locator(`[data-ain-step="${step.id}"]`);
    if (await card.locator('.testkit-prompt-text').textContent() !== step.prompt) throw Error('Preview '+step.id);
    const expected = `<!-- mango-bcreq-${step.id.toLowerCase()}-stepwise · ${step.id} ${step.name} -->\n\n${step.prompt}`;
    await card.locator('.testkit-copy').click();
    await page.waitForFunction(async text => await navigator.clipboard.readText() === text, expected);
    if (await card.locator('.testkit-more a[href^="#prompt="]').count()<2) throw Error('Reverse archive links '+step.id);
    if (!await card.locator('.prompt-links a').count()) throw Error('Step links missing '+step.id);
  }
  await page.locator('[data-process-tab="g2"]').click();
  const legacy = page.locator('.testkit-group[data-group="g2"] .testkit-step').first();
  const editions = legacy.locator('[data-testkit-edition]');
  const oldText = await legacy.locator('.testkit-prompt-text').textContent();
  if (await editions.count() !== 2) throw Error('Legacy editions lost');
  await editions.nth(1).click();
  if (await legacy.locator('.testkit-prompt-text').textContent() === oldText) throw Error('Legacy switch failed');
  await legacy.locator('.testkit-copy').click();
  await page.waitForFunction(async text => (await navigator.clipboard.readText()).endsWith(text), await legacy.locator('.testkit-prompt-text').textContent());
  await editions.nth(0).click();
  // Deep links reopen the relevant stage and preserve the ordinary reader.
  for (const id of ['AIN-02','AIN-14','AIN-24']) {
    await page.goto(base+'#processes?ain='+id);
    await page.waitForFunction(id => !document.querySelector(`[data-ain-step="${id}"]`).closest('.testkit-group').hidden,id);
  }
  await page.goto(base+'#processes?ain=AIN-01');
  await page.locator('#theme-toggle').evaluate(button => { if(document.documentElement.dataset.theme!=='light') button.click(); });
  const card = page.locator('[data-ain-step="AIN-01"]');
  const scroll = async () => card.evaluate(el=>window.scrollTo({top:el.getBoundingClientRect().top+scrollY-document.querySelector('.topbar').offsetHeight-16,behavior:'instant'}));
  await scroll();
  await page.waitForFunction(()=>document.querySelector('#toast').dataset.visible!=='true');
  await page.screenshot({path:shots+'after-processes-desktop.png'});
  await page.setViewportSize({width:390,height:844});
  await scroll();
  if (await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)) throw Error('Mobile overflow');
  await card.screenshot({path:shots+'after-processes-mobile.png'});
  await page.locator('#theme-toggle').click();
  await scroll();
  await page.waitForFunction(()=>document.querySelector('#toast').dataset.visible!=='true');
  await card.screenshot({path:shots+'after-processes-dark.png'});
  await page.setViewportSize({width:1280,height:960});
  await page.goto(base+'#catalog');
  await page.locator('#theme-toggle').evaluate(button=>{if(document.documentElement.dataset.theme!=='light')button.click();});
  const select = async token => page.locator('[data-filter-token]').evaluateAll((els,token)=>els.find(e=>e.dataset.filterToken===token).click(),token);
  if(await page.locator('.prompt-card').count()!==39) throw Error('Default catalog');
  await select('family:archive');
  if(await page.locator('.prompt-card').count()!==18) throw Error('Archive catalog');
  await select('process:A-IN · Приём задачи');
  await page.locator('#search-input').fill('2.7.0');
  await page.waitForFunction(()=>document.querySelectorAll('.prompt-card').length===4);
  if(await page.locator('.archive-badge').filter({hasText:'Архивная версия'}).count()!==4) throw Error('Archive label');
  const archives=await page.evaluate(async()=> (await (await fetch('data/prompts.json')).json()).prompts.filter(p=>p.archiveInfo));
  for(const prompt of archives){
    await page.locator(`[data-copy-id="${prompt.id}"]`).first().click();
    await page.waitForFunction(async text=>await navigator.clipboard.readText()===text,`<!-- ${prompt.id} -->\n\n${prompt.body}`);
  }
  await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
  await page.waitForFunction(()=>document.querySelector('#toast').dataset.visible!=='true');
  await page.screenshot({path:shots+'after-archive.png'});
  // A deep link must remain visible even with previous conflicting facets/search.
  await page.locator('#search-input').fill('no-such-id');
  const chosen=archives.find(p=>p.archiveInfo.step==='Ш-А');
  await page.goto(base+'#prompt='+chosen.id);
  await page.waitForFunction(()=>document.querySelectorAll('.prompt-card').length===1);
  if(await page.locator(`[data-copy-id="${chosen.id}"]`).count()!==2) throw Error('Archive deep link');
  for(const section of ['1','2','ttz','9']){
    await page.goto(base+'#standards?section='+section);
    const target=page.locator(section==='ttz'?'#standard-ttz':section==='9'?'#standard-industry':'#standard-'+section);
    if(!await target.isVisible())throw Error('Standard link '+section);
  }
  await page.goto(base+'#standards?section=2');
  if(!await page.locator('[data-ain-guidance="2"]').isVisible()) throw Error('Mirrored guidance');
  await page.screenshot({path:shots+'after-standard-2.png'});
  // Existing failure feedback and normal reload recovery remain functional.
  await page.goto(base+'#processes');
  await page.route('**/data/a-in-kit.json',route=>route.abort());
  await page.reload({waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>document.querySelector('#bcreq-testkit-summary').textContent.includes('Данные не загрузились'));
  await page.unroute('**/data/a-in-kit.json');
  await page.reload({waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>document.querySelectorAll('[data-ain-step]').length===24);
  if(errors.length)throw Error(errors.join('\n'));
  return {cards:35,ainPreviews:24,ainClipboard:24,archiveClipboard:4,archiveSearch:true,deepLinks:true,legacyEditionCopy:true,standards:true,mobileOverflow:false,lightDark:true,errorReload:true,pageErrors:errors};
}

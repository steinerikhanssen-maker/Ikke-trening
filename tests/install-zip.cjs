/* Real WP-admin ZIP upload on an isolated, source-free WordPress at port 8081. */
const {chromium,expect}=require('@playwright/test');
const fs=require('node:fs');const path=require('node:path');
async function main(){
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});const log=[];
 const pass=s=>{log.push('PASS '+s);process.stdout.write('PASS '+s+'\n');fs.writeFileSync('evidence/zip-install.txt',log.join('\n')+'\n');};
 try{
  await page.goto('http://localhost:8081/wp-login.php');await page.locator('#user_login').fill('gnf_test_admin');await page.locator('#user_pass').fill('LocalTestOnly_2026');await page.locator('#wp-submit').click();await page.waitForURL('**/wp-admin/**');
  await page.goto('http://localhost:8081/wp-admin/plugin-install.php?tab=upload');await page.locator('#pluginzip').setInputFiles(path.resolve('dist/gymnotfound-0.1.0-beta.1.zip'));await page.locator('#install-plugin-submit').click();await expect(page.getByText('Plugin installed successfully.',{exact:true})).toBeVisible({timeout:30000});pass('A1 upload built ZIP in WP-admin without Node/Composer');
  await page.getByRole('link',{name:'Activate Plugin',exact:true}).click();await expect(page.getByText('Plugin activated.',{exact:true})).toBeVisible();pass('A2 activate ZIP without fatal');
  await page.goto('http://localhost:8081/wp-admin/edit.php?post_type=page');await expect(page.locator('#the-list .row-title').filter({hasText:'GymNotFound'})).toHaveCount(0);pass('A2 activation creates no app page');
  await page.goto('http://localhost:8081/wp-admin/admin.php?page=gymnotfound');await page.getByRole('button',{name:'Create draft app page',exact:true}).click();await expect(page.getByText('Draft app page ready. Preview it, then publish it when you choose.',{exact:true})).toBeVisible();
  const appId=await page.locator('select[name=gnf_page_id]').inputValue();expect(Number(appId)).toBeGreaterThan(0);pass('A4 explicit creation creates selected draft');
  await page.getByRole('button',{name:'Create draft app page',exact:true}).click();expect(await page.locator('select[name=gnf_page_id]').inputValue()).toBe(appId);pass('A2 repeated explicit creation is idempotent');
  await page.screenshot({path:'screenshots/wordpress-admin.png',fullPage:true});
  const preview=await page.getByRole('link',{name:'Preview app',exact:true}).getAttribute('href');await page.goto(preview);await expect(page.locator('#gnf-try')).toBeVisible();await expect(page.locator('body')).not.toContainText('Deprecated');pass('A3 selected page has standalone shell and a working card');
  await page.goto('http://localhost:8081/wp-admin/plugins.php');await page.locator('#deactivate-gymnotfound').click();await expect(page.getByText('Plugin deactivated.',{exact:true})).toBeVisible();await page.locator('#activate-gymnotfound').click();await expect(page.getByText('Plugin activated.',{exact:true})).toBeVisible();pass('A2 deactivate/reactivate installed ZIP');
  await page.goto('http://localhost:8081/wp-admin/edit.php?post_type=gnf_activity');await expect(page.locator('.tablenav.top .displaying-num')).toContainText('36');pass('A4 36 editable templates, no duplicate seed');
  const first=page.locator('#the-list .row-title').first();await first.click();await expect(page.locator('textarea[name=gnf_nb_title]')).not.toBeEmpty();await expect(page.locator('textarea[name=gnf_en_step]')).not.toBeEmpty();pass('A4 real bilingual template editing fields');
  await page.goto('http://localhost:8081/wp-admin/admin.php?page=gymnotfound');await page.locator('input[name=gnf_hour_cap]').fill('7');await page.getByRole('button',{name:'Save settings',exact:true}).click();await expect(page.locator('input[name=gnf_hour_cap]')).toHaveValue('7');pass('A4 save settings with admin nonce');
  const missing=await page.request.post('http://localhost:8081/wp-admin/admin-post.php',{form:{action:'gnf_settings',gnf_action:'create'}});expect(missing.status()).toBe(403);pass('E4 settings action without nonce is rejected');
  const anonymous=await browser.newContext();const denied=await anonymous.request.post('http://localhost:8081/wp-admin/admin-post.php',{form:{action:'gnf_settings',gnf_action:'create'}});expect(denied.status()).toBe(400);await anonymous.close();pass('E4 anonymous settings action rejected by WordPress (no nopriv handler)');
  fs.writeFileSync('/tmp/gnf-zip-page-id',appId);fs.writeFileSync('evidence/zip-install.txt',log.join('\n')+'\n');
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});

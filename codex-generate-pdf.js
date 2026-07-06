const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const htmlPath = 'file://' + path.resolve(__dirname, 'Codex橙皮书.html');
  const pdfPath = path.resolve(__dirname, 'Codex橙皮书.pdf');

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto(htmlPath, {
    waitUntil: 'networkidle',
    timeout: 60000
  });

  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: false,
    margin: {
      top: '12mm',
      right: '12mm',
      bottom: '12mm',
      left: '12mm'
    }
  });

  await browser.close();
  console.log('PDF generated:', pdfPath);
})();

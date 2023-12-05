const puppeteer = require('puppeteer');
const fs = require('fs');

async function capturePanorama(lat, lng, pan) {
    // Puppeteer 브라우저 실행
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // HTML 파일 경로 설정 (실제 파일 경로로 변경 필요)
    const filePath = 'file:///C:/Users/user/image_download/pano.html';
    await page.goto(filePath);

    // createPanorama 함수 실행 (지정된 좌표 및 pan 값 사용)
    await page.evaluate((lat, lng, pan) => {
        window.createPanorama(lat, lng, pan);
    }, lat, lng, pan);

    // 파노라마 로딩을 위한 대기 (대기 시간 조절 필요)
    await page.waitForTimeout(600);

    // 스크린샷 캡처
    const screenshot = await page.screenshot();

    console.log(`Captured: lat ${lat}, lng ${lng}, pan ${pan}`);

    // 스크린샷을 파일로 저장
    const filename = `download_image/screenshot_lat_${lat}_lng_${lng}_pan_${pan}.png`;
    require('fs').writeFileSync(filename, screenshot);

    console.log(`Captured: ${filename}`);

    // 브라우저 닫기
    await browser.close();
}

const panValues = [-160, -140, -120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180];

// 파일 경로
const filePath = 'C:/Users/user/image_download/pure_lat_lng.txt'; // 실제 파일 경로로 변경해야 합니다.

// 파일에서 좌표 읽기
fs.readFile(filePath, 'utf8', async (err, data) => {
    if (err) {
        console.error('파일을 읽는 도중 오류가 발생했습니다.', err);
        return;
    }

    const lines = data.split('\n');
    for (const line of lines) {
        const [lat, lng] = line.split(' '); // 공백을 기준으로 위도와 경도 분리

        // 위도와 경도를 parseFloat()를 통해 숫자로 변환하여 capturePanorama 함수 호출
        for(const pan of panValues) {
            await capturePanorama(parseFloat(lat), parseFloat(lng), pan); 
        }

    }
});
import puppeteer from 'puppeteer';
import { load } from 'cheerio';

async function fetchPage(url: string): Promise<string | null> {
    let html: string | null = null;
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: 'networkidle2' });
        html = await page.content();
        await browser.close();
    } catch (error) {
        console.error('Error fetching page:', error);
    }
    return html;
}

interface ItemListing {
    itemName: string;
    game: string;
    dailyVolume: string;
    minPrice: string;
    optimalListing: string;
    optimalPurchase: string;
    stablePurchase: string;
    recentTransactions: string;
    tradingPlatform: string;
    steamLink: string;
    updateTime: string;
}

function parseTableRow(html: string | null): void {
    if (!html) {
        console.error('Empty HTML content');
        return;
    }
    const $ = load(html);
    const rows = $('tbody > tr');
    if (rows.length === 0) {
        console.log('No rows found in the table');
        return;
    }
    const row = rows.eq(1);
    const columns = $(row).find('td');
    const itemListing: ItemListing = {
        itemName: $(columns[2]).find('a').text().trim(),
        game: $(columns[3]).find('a > span').text().trim(),
        dailyVolume: $(columns[4]).text().trim(),
        minPrice: $(columns[5]).find('a').text().trim(),
        optimalListing: $(columns[6]).find('a').text().trim(),
        optimalPurchase: $(columns[7]).find('a').text().trim(),
        stablePurchase: $(columns[8]).find('a').text().trim(),
        recentTransactions: $(columns[9]).find('a').text().trim(),
        tradingPlatform: $(columns[10]).find('button > span').text().trim(),
        steamLink: $(columns[11]).find('button > span').text().trim(),
        updateTime: $(columns[12]).find('a').text().trim(),
    };
    console.log(itemListing);
}

async function main() {
    const url = 'https://steam.iflow.work/?page_num=1&platforms=buff&games=csgo-dota2&sort_by=safe_buy&min_price=1&max_price=5000&min_volume=2';
    const html = await fetchPage(url);
    parseTableRow(html);
}

main();

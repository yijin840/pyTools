import puppeteer from 'puppeteer';
import { DOMParser } from 'xmldom';
import xpath from 'xpath';
import fs from 'fs';
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

function parseHTMLWithXPathSync(html: string | null, xpathExpression: string): string | null {
    if (!html) {
        console.error('Empty HTML content');
        return null;
    }
    try {
        console.log("xpathExpression ==> ", xpathExpression);
        const doc = new DOMParser().parseFromString(html);
        const nodes = xpath.select('//tbody/*[2]', doc) as Node[];
        if (nodes.length === 0) {
            console.log('No matching nodes found');
            return null;
        }

        // Construct the HTML content from selected nodes
        let resultHtml = '';
        nodes.forEach((node) => {
            resultHtml += node.toString();
            // console.log(node.toString());
        });

        return resultHtml;

    } catch (error) {
        console.error('Error parsing HTML with XPath:', error);
        return null;
    }
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

function parseTableRow(html: string): void {
    try {
        const doc = new DOMParser().parseFromString(html);
        const trNodes = xpath.select('//tr', doc) as Node[];

        if (!trNodes || trNodes.length === 0) {
            console.error('No <tr> elements found in the HTML');
            return;
        }

        const trNode = trNodes[0] as Element; // Type assertion to Element
        const dataRowKeyAttr = trNode.getAttributeNode('data-row-key');
        const dataRowKey = dataRowKeyAttr ? dataRowKeyAttr.value : '';

        const select = (expression: string, node: Node): string => {
            const result = xpath.select(expression, node) as Node[];
            if (result.length > 0 && 'nodeValue' in result[0] && result[0].nodeValue) {
                return result[0].nodeValue.trim();
            }
            return '';
        };

        const itemListing: ItemListing = {
            itemName: select('td[3]/a/text()', trNode),
            game: select('td[4]/a/span/text()', trNode),
            dailyVolume: select('td[5]/text()', trNode),
            minPrice: select('td[6]/a/text()', trNode),
            optimalListing: select('td[7]/a/text()', trNode),
            optimalPurchase: select('td[8]/a/text()', trNode),
            stablePurchase: select('td[9]/a/text()', trNode),
            recentTransactions: select('td[10]/a/text()', trNode),
            tradingPlatform: select('td[11]/button/span/text()', trNode),
            steamLink: select('td[12]/button/span/text()', trNode),
            updateTime: select('td[13]/a/text()', trNode),
        };

        console.log(itemListing);

    } catch (error) {
        console.error('Error parsing HTML:', error);
    }
}

async function main() {
    const url = 'https://steam.iflow.work/?page_num=1&platforms=buff&games=csgo-dota2&sort_by=safe_buy&min_price=1&max_price=5000&min_volume=2';
    const html = await fetchPage(url);
    const xpathExpression = '/html/body/main/section/div[2]/div/div/div/div/div/div/div[2]/table/tbody';

    const resultHtml = parseHTMLWithXPathSync(html, xpathExpression);
    if (resultHtml != null) {
        parseTableRow(resultHtml);
    }

    // if (html != null) {
    //     saveHTMLToFile(html, 'output.html');
    // }

}

main();

// Legt de architectuurplaat uit de sectie Code vast als beeld voor de pitch (overzicht/ov/pitch/arch.jpg).
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:2,colorScheme:'light'});
await p.goto('file://'+path.resolve(__dirname,'../overzicht/index.html')+'#code');await p.waitForTimeout(1000);
await (await p.$('.arch')).screenshot({path:path.resolve(__dirname,'../overzicht/ov/pitch/arch.jpg'),type:'jpeg',quality:88});await b.close();console.log('ok arch')})();

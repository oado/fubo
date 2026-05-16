const localtunnel = require('localtunnel');

(async () => {
  const tunnel = await localtunnel({ port: 8765 });
  console.log('PUBLIC_URL:' + tunnel.url);
  
  // Keep process alive
  tunnel.on('close', () => {
    console.log('Tunnel closed');
    process.exit(0);
  });
  
  // Write URL to file
  const fs = require('fs');
  fs.writeFileSync('C:\\Users\\Administrator\\WorkBuddy\\2026-05-15-task-1\\public_url.txt', tunnel.url);
})();

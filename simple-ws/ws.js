const WebSocket = require('ws');
const WebSocketServer = WebSocket.WebSocketServer;

// Initialize a WebSocket Server on port 8080
const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', function connection(ws) {
  console.log('A new client connected');

  // Send a message to the client
  ws.send('Welcome to the WebSocket server!');

  // Listen for messages from the client
  ws.on('message', function message(data) {
    console.log(`Received message from client: ${data}`);
  });

  // Handle client disconnection
  ws.on('close', () => {
    console.log('A client disconnected');
  });
});

console.log('WebSocket server is running on ws://localhost:8080');

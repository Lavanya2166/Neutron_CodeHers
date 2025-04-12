// backend/server.js
const express = require('express');
const cors = require('cors');
const firebaseAdmin = require('firebase-admin');
const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

// Initialize Firebase Admin SDK using the service account key
const serviceAccount = require('./firebase-adminsdk.json'); // Make sure the file path is correct

firebaseAdmin.initializeApp({
  credential: firebaseAdmin.credential.cert(serviceAccount),
});

app.get('/', (req, res) => {
  res.send('Hello from Express!');
});

// Handle the /create-collaborator route
app.post('/create-collaborator', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ success: false, error: 'Email and password are required' });
  }

  try {
    // Create a new Firebase user with email and password
    const userRecord = await firebaseAdmin.auth().createUser({
      email: email,
      password: password,
    });

    // Once the user is created, Firebase generates a UID automatically
    const uid = userRecord.uid;

    // Send response with the generated UID
    res.json({ success: true, uid });

  } catch (error) {
    console.error("Error creating user: ", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
// backend/server.js (add this below the existing code)
const WebSocket = require('ws');

// Create a WebSocket server
const wss = new WebSocket.Server({ port: 3000 });

wss.on('connection', (ws) => {
  console.log('Client connected');
  ws.on('message', (message) => {
    console.log('Received: %s', message);
  });

  ws.send('Hello from WebSocket server!');
});

// frontend/src/firebase.js

// Import Firebase core
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCBJTBRNE_FYp5gevHMMdk6TXJYAt28AI4",
  authDomain: "neutron-a3e7c.firebaseapp.com",
  projectId: "neutron-a3e7c",
  storageBucket: "neutron-a3e7c.appspot.com",  // Corrected the storageBucket URL
  messagingSenderId: "570190409552",
  appId: "1:570190409552:web:2936eeee1728e8c6aa8655"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
const auth = getAuth(app);
const db = getFirestore(app);

// Export the services so you can use them in your components
export { app, auth, db };

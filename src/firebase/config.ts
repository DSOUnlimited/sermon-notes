import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getAnalytics } from 'firebase/analytics';
import { getFirestore } from 'firebase/firestore';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDqjSQollQze2v_pnQoQibugXWN3dI8650",
  authDomain: "sermon-notes-7a6d9.firebaseapp.com",
  projectId: "sermon-notes-7a6d9",
  storageBucket: "sermon-notes-7a6d9.firebasestorage.app",
  messagingSenderId: "710630235495",
  appId: "1:710630235495:web:b01bcef03f161b41e0e3c2",
  measurementId: "G-2471ZGTPCC"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const analytics = getAnalytics(app);
const db = getFirestore(app);

export { auth, analytics, db }; 
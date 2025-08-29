// src/firebase.js

import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// ✅ Firebase config from your project
const firebaseConfig = {
    apiKey: "AIzaSyBaiO-l6MyEl1pYuIGg9JJtusHe1ciqTSw",
    authDomain: "what-s-it-cost.firebaseapp.com",
    projectId: "what-s-it-cost",
    storageBucket: "what-s-it-cost.firebasestorage.app",
    messagingSenderId: "814845984017",
    appId: "1:814845984017:web:a84b375d808a590eae20b0",
    measurementId: "G-HFC8B5YJLW"
};

// ✅ Initialize Firebase
const app = initializeApp(firebaseConfig);

// ✅ Initialize Firestore and export
const db = getFirestore(app);
export { db };

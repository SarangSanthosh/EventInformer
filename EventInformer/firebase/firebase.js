// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDpXMm88DR4ghgDQjBZnuEYdCJK_SbsYfg",
  authDomain: "event-chatbot-5b6b4.firebaseapp.com",
  projectId: "event-chatbot-5b6b4",
  storageBucket: "event-chatbot-5b6b4.firebasestorage.app",
  messagingSenderId: "891672388108",
  appId: "1:891672388108:web:4750853352c00bcdf10429",
  measurementId: "G-RSY3BL627T"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
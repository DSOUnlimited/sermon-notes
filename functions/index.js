/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const { onSchedule } = require("firebase-functions/v2/scheduler");

// Create and deploy your first functions
// https://firebase.google.com/docs/functions/get-started

// exports.helloWorld = onRequest((request, response) => {
//   logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

admin.initializeApp();

// exports.deleteOldSermons = onSchedule("every 24 hours", async (event) => {
//   const db = admin.firestore();
//   const now = Date.now();
//   const sevenDays = 7 * 24 * 60 * 60 * 1000;
//
//   const snapshot = await db.collection('sermons')
//     .where('deleted', '==', true)
//     .get();
//
//   const batch = db.batch();
//   snapshot.forEach(doc => {
//     const data = doc.data();
//     if (data.deletedAt && data.deletedAt.toMillis() < now - sevenDays) {
//       batch.delete(doc.ref);
//     }
//   });
//
//   await batch.commit();
//   console.log('Old deleted sermons cleaned up.');
//   return null;
// });

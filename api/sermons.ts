import { VercelRequest, VercelResponse } from '@vercel/node';
import * as admin from 'firebase-admin';
import * as serviceAccount from '../config/serviceAccountKey.json';

// Initialize Firebase Admin
if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount as admin.ServiceAccount)
  });
}

const db = admin.firestore();

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'GET') {
    try {
      const sermonsSnapshot = await db.collection('sermons').get();
      const sermons = sermonsSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      res.status(200).json(sermons);
    } catch (error) {
      console.error('Error fetching sermons:', error);
      res.status(500).json({ error: 'Failed to fetch sermons' });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}

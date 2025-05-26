import { VercelRequest, VercelResponse } from '@vercel/node';
import { db } from '../../src/firebase/config';
import { collection, getDocs } from 'firebase/firestore';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'GET') {
    try {
      const sermonsCollection = collection(db, 'sermons');
      const sermonsSnapshot = await getDocs(sermonsCollection);
      const sermons = sermonsSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      res.status(200).json(sermons);
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch sermons' });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
} 
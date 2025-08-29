const { onRequest } = require("firebase-functions/v2/https");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");
admin.initializeApp();
const db = admin.firestore();

exports.getSeriesData = onRequest(async (req, res) => {
    const seriesId = req.query.seriesId;

    if (!seriesId) {
        logger.warn("Missing seriesId");
        return res.status(400).send("Missing seriesId");
    }

    try {
        const snapshot = await db.collection("seriesData")
            .where("seriesId", "==", seriesId)
            .get();

        const data = snapshot.docs.map(doc => doc.data());
        logger.info(`Fetched ${data.length} records for seriesId: ${seriesId}`);
        return res.status(200).json(data);
    } catch (err) {
        logger.error("Error fetching Firestore data:", err);
        return res.status(500).send("Error retrieving data");
    }
});

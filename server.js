const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cors = require("cors");
const authRoutes = require("./routes/auth");
const path = require("path");

const app = express();
app.use(cors());
const PORT = process.env.PORT || 5000;

// Connect to MongoDB
// NOTE: Ensure MongoDB is running on your system, or replace this with a cloud URI.
mongoose.connect("mongodb://127.0.0.1:27017/slcvet")
    .then(() => console.log("✅ MongoDB Connected Successfully"))
    .catch(err => {
        console.error("❌ MongoDB Connection Error:", err.message);
        console.log("⚠️  Please ensure MongoDB service is running (mongod).");
    });

// Middleware
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));

// API Routes
app.use("/api", authRoutes);

// Fallback for SPA routing if needed
app.use((req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
    console.log(`🔗 Localhost: http://localhost:${PORT}`);
});

const express = require("express");
const router = express.Router();
const User = require("../models/User");

// Middleware to simulate the logic the frontend expects
// ENDPOINTS:
// GET /users/:mobile -> check if user exists
// POST /auth/send-otp -> send OTP
// POST /auth/verify-otp -> verify
// POST /users/signup -> final registration

// 1. Check User Existence
router.get("/users/:mobile", async (req, res) => {
    try {
        const user = await User.findOne({ mobile_number: req.params.mobile });
        if (!user) return res.status(404).json({ detail: "User not found" });
        res.json({
            full_name: user.full_name,
            role: user.role,
            mobile_number: user.mobile_number
        });
    } catch (err) {
        res.status(500).json({ detail: err.message });
    }
});

// 2. Send OTP
router.post("/auth/send-otp", async (req, res) => {
    try {
        const { mobile_number } = req.body;
        const otp = Math.floor(100000 + Math.random() * 900000).toString();

        // For simplicity, we'll store OTP on a temporary record or update user
        let user = await User.findOne({ mobile_number: mobile_number });
        if (!user) {
            // If user doesn't exist, we create a placeholder so we can store the OTP
            user = new User({
                mobile_number: mobile_number,
                full_name: "Pending Verification",
                role: "pending",
                otp: otp
            });
        } else {
            user.otp = otp;
        }
        await user.save();

        console.log(`[SMS] OTP for ${mobile_number}: ${otp}`);
        res.json({ message: "OTP Sent", otp: otp });
    } catch (err) {
        res.status(500).json({ detail: err.message });
    }
});

// 3. Verify OTP
router.post("/auth/verify-otp", async (req, res) => {
    try {
        const { mobile_number, otp } = req.body;
        const user = await User.findOne({ mobile_number, otp });

        if (!user) return res.status(400).json({ detail: "Invalid or expired OTP" });

        user.is_verified = true;
        user.otp = null;
        await user.save();

        res.json({
            message: "OTP verified successfully",
            user_exists: user.role !== "pending",
            mobile_number: user.mobile_number,
            role: user.role,
            access_token: "mock-jwt-token",
            token_type: "bearer"
        });
    } catch (err) {
        res.status(500).json({ detail: err.message });
    }
});

// 4. Final Signup
router.post("/users/signup", async (req, res) => {
    try {
        const { mobile_number, full_name, role, ...extra } = req.body;

        let user = await User.findOne({ mobile_number });
        if (user && user.role !== "pending") {
            return res.status(400).json({ detail: "User already registered" });
        }

        if (!user) {
            user = new User({ mobile_number, full_name, role, ...extra });
        } else {
            user.full_name = full_name;
            user.role = role;
            Object.assign(user, extra);
        }

        await user.save();
        res.json({
            message: "Registration successful",
            user: user,
            access_token: "mock-jwt-token",
            token_type: "bearer"
        });
    } catch (err) {
        res.status(500).json({ detail: err.message });
    }
});

module.exports = router;

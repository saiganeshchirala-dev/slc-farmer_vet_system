const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    full_name: { type: String, required: true },
    mobile_number: { type: String, required: true, unique: true },
    dob: { type: Date },
    role: { type: String, required: true }, // farmer, veterinarian, paravet
    otp: { type: String },
    is_verified: { type: Boolean, default: false },

    // Extension fields from original project
    state: { type: String, default: "N/A" },
    district: { type: String, default: "N/A" },
    mandal: { type: String },
    village: { type: String },
    language: { type: String },
    registration_num: { type: String }, // For Vets
    degree: { type: String },           // For Vets
    email: { type: String },            // For Vets
    hospital_name: { type: String },    // For Vets
    working_area: { type: String },     // For Vets/Paravets

    created_at: { type: Date, default: Date.now }
});

module.exports = mongoose.model("User", userSchema);

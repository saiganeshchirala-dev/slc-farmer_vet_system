// ---------- CONSTANTS ----------
// If on localhost, use the full local URL. If deployed, use relative path.
const API_BASE_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? "http://127.0.0.1:8000/api/v1"
    : "/api/v1";

// ---------- UTILITIES ----------
// Helper to call APIs
async function apiCall(endpoint, method, data) {
    try {
        const token = localStorage.getItem("access_token");
        const options = {
            method: method,
            headers: {
                "Content-Type": "application/json"
            }
        };
        if (token) {
            options.headers["Authorization"] = `Bearer ${token}`;
        }
        if (data && method !== "GET") {
            options.body = JSON.stringify(data);
        }
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.detail || "Something went wrong");
        }
        return result;
    } catch (error) {
        console.error("API Error:", error);
        if (error.name === "TypeError" && error.message.includes("Failed to fetch")) {
            throw new Error("Cannot connect to server. Is the backend running?");
        }
        throw error;
    }
}

// ---------- SIGN IN ----------
async function handleSignin(event) {
    event.preventDefault();

    const mobileInput = document.getElementById("signinMobile");
    const mobile = mobileInput.value.trim();
    const msg = document.getElementById("signinMsg");

    if (mobile.length !== 10) {
        msg.innerText = "Enter valid 10-digit mobile number";
        msg.style.color = "red";
        return;
    }

    try {
        // 1. Check if user exists (Strict Login Flow)
        try {
            await apiCall(`/users/${mobile}`, "GET");
        } catch (checkErr) {
            // If 404/User not found, redirect to Signup
            if (checkErr.message.toLowerCase().includes("not found")) {
                alert("This mobile number is not registered. Redirecting to Sign Up page...");
                window.location.href = "signup.html";
                return;
            }
            throw checkErr; // Other errors
        }

        // 2. Call Backend to Send OTP (Only if user exists)
        const response = await apiCall("/auth/send-otp", "POST", { mobile_number: mobile });

        // Save mobile and OTP to display on next page
        localStorage.setItem("verifyingMobile", mobile);
        localStorage.setItem("generatedOtp", response.otp);

        // ONE-WAY FLOW: Always redirect to otp.html
        alert("OTP Sent! Please check the OTP displayed on the next page.");
        window.location.href = "otp.html";

    } catch (error) {
        msg.innerText = error.message;
        msg.style.color = "red";
    }
}

function showMobileSection() {
    document.getElementById("otpSection").classList.add("hidden");
    document.getElementById("mobileSection").classList.remove("hidden");
    document.getElementById("signinMsg").innerText = "";
}

// Focus Management for OTP
function moveFocus(element, index) {
    if (element.value.length >= 1) {
        const next = element.nextElementSibling;
        if (next) next.focus();
    }
}

function handleBackspace(event, element, index) {
    if (event.key === "Backspace" && element.value === "") {
        const prev = element.previousElementSibling;
        if (prev) prev.focus();
    }
}

async function submitOtp() {
    const inputs = document.querySelectorAll(".otp-box");
    let enteredOtp = "";
    inputs.forEach(input => enteredOtp += input.value);

    if (enteredOtp.length !== 6) {
        const msg = document.getElementById("signinMsg");
        msg.innerText = "Please enter 6-digit OTP";
        msg.style.color = "red";
        return;
    }

    await verifyOtpBackend(enteredOtp);
}

// ---------- OTP SHARED LOGIC ----------
function initOtpPage() {
    console.log("Initializing OTP Page...");
    const mobile = localStorage.getItem("verifyingMobile");
    const otp = localStorage.getItem("generatedOtp");
    const displayEl = document.getElementById("displayMobile");
    const otpDisplayEl = document.getElementById("otpDisplay");
    const generatedOtpEl = document.getElementById("generatedOtp");

    if (mobile && displayEl) {
        displayEl.innerText = "+91 " + mobile;
    } else if (!mobile) {
        console.warn("No mobile number found in localStorage, redirecting to login.");
        window.location.href = "index.html";
        return;
    }

    // Display the OTP on the page
    if (otp && otpDisplayEl && generatedOtpEl) {
        generatedOtpEl.innerText = otp;
        otpDisplayEl.style.display = "block";
    }

    startTimer();
}

function startTimer() {
    const timerVal = document.getElementById("timer");
    const timerText = document.getElementById("timer-text");
    const resendLink = document.getElementById("resend-link");

    if (!timerVal || !timerText || !resendLink) {
        console.warn("Timer elements not found");
        return;
    }

    let timeLeft = 30;
    resendLink.style.display = "none";
    timerText.style.display = "inline";
    timerVal.innerText = timeLeft;

    if (window.timerInterval) clearInterval(window.timerInterval);

    window.timerInterval = setInterval(() => {
        timeLeft--;
        timerVal.innerText = timeLeft;
        if (timeLeft <= 0) {
            clearInterval(window.timerInterval);
            timerText.style.display = "none";
            resendLink.style.display = "inline";
        }
    }, 1000);
}

async function handleResend() {
    const success = await resendOtp();
    if (success) {
        startTimer();
        // Clear inputs
        document.querySelectorAll(".otp-box").forEach(input => input.value = "");
        const firstInput = document.querySelectorAll(".otp-box")[0];
        if (firstInput) firstInput.focus();
    }
}

function changeNumber() {
    localStorage.removeItem("verifyingMobile");
    window.location.href = "index.html";
}

// ---------- SIGN UP ----------
const roleRadios = document.querySelectorAll('input[name="role"]');
const roleSections = document.querySelectorAll('.role-fields');

function updateRoleFields() {
    // 1. Hide all sections and disable their inputs
    roleSections.forEach(section => {
        section.classList.add("hidden");
        const inputs = section.querySelectorAll('input, select, textarea');
        inputs.forEach(input => input.disabled = true);
    });

    // 2. Find selected role
    const selectedRadio = document.querySelector('input[name="role"]:checked');
    if (selectedRadio) {
        const roleValue = selectedRadio.value;
        const selectedSection = document.getElementById(roleValue);

        if (selectedSection) {
            selectedSection.classList.remove("hidden");
            const inputs = selectedSection.querySelectorAll('input, select, textarea');
            inputs.forEach(input => input.disabled = false);
        }
    }
}

// Initialize logic only if we are on the signup page
if (roleRadios.length > 0) {
    roleRadios.forEach(radio => {
        radio.addEventListener("change", updateRoleFields);
    });
    // Initial call to set correct state on page load
    updateRoleFields();
}

async function registerUser(event) {
    event.preventDefault();

    const nameInput = document.getElementById("signupName");
    const mobileInput = document.getElementById("signupMobile");
    const selectedRole = document.querySelector('input[name="role"]:checked').value;

    // Base Data
    const userData = {
        full_name: nameInput.value.trim(),
        mobile_number: mobileInput.value.trim(),
        role: selectedRole
    };

    // Get additional details based on role
    const visibleSection = document.getElementById(selectedRole);
    if (visibleSection) {
        const inputs = visibleSection.querySelectorAll('input');
        inputs.forEach(input => {
            const val = input.value.trim();
            const ph = input.placeholder ? input.placeholder.toLowerCase() : "";

            if (input.type === 'date') {
                const dobVal = val;
                if (!dobVal) throw new Error("Date of Birth is required");

                // Age Validation (> 18)
                const dobDate = new Date(dobVal);
                const today = new Date();
                let age = today.getFullYear() - dobDate.getFullYear();
                const m = today.getMonth() - dobDate.getMonth();
                if (m < 0 || (m === 0 && today.getDate() < dobDate.getDate())) {
                    age--;
                }

                if (age < 18) {
                    throw new Error("You must be at least 18 years old to register.");
                }

                userData.dob = dobVal;
            }
            else if (ph === "village") userData.village = val;
            else if (ph === "mandal") userData.mandal = val;
            else if (ph === "district") userData.district = val;
            else if (ph === "state") userData.state = val;
            else if (ph.includes("language")) userData.language = val;
            else if (ph.includes("vci") || ph.includes("reg")) userData.registration_num = val;
            else if (ph.includes("degree")) userData.degree = val;
            else if (ph.includes("email")) userData.email = val;
            else if (ph.includes("clinical") || ph.includes("hospital")) userData.hospital_name = val;
            else if (ph.includes("working area")) userData.working_area = val;
            else if (ph.includes("qualification")) userData.qualification = val;
        });
    }

    // Defaults for required fields in schema
    if (!userData.state) userData.state = "N/A";
    if (!userData.district) userData.district = "N/A";

    try {
        await apiCall("/users/signup", "POST", userData);
        alert("Registration successful! Please Login.");
        // Clear verifyingMobile after successful signup
        localStorage.removeItem("verifyingMobile");
        window.location.href = "index.html";
    } catch (error) {
        alert("Registration Failed: " + error.message);
    }
}

// Pre-fill Mobile in Signup if exists
// Pre-fill Mobile in Signup if exists
function initSignup() {
    const prefillMobile = localStorage.getItem("verifyingMobile");
    const mobileInput = document.getElementById("signupMobile");
    if (prefillMobile && mobileInput) {
        mobileInput.value = prefillMobile;
        // Optionally make it read-only if we want to enforce verified number
        // mobileInput.readOnly = true;
    }
}

if (window.location.pathname.includes("signup.html")) {
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSignup);
    } else {
        initSignup();
    }
}

// ---------- USER PROFILE LOADING ----------
async function loadUserProfile() {
    const userStr = localStorage.getItem("loggedInUser");
    if (!userStr) return;

    try {
        const loggedInUser = JSON.parse(userStr);
        const mobile = loggedInUser.mobile;

        // Fetch full profile from backend
        const user = await apiCall(`/users/${mobile}`, "GET");

        // Update Name/Profile displays if they exist
        const nameDisplays = document.querySelectorAll(".user-name-display");
        nameDisplays.forEach(el => el.innerText = user.full_name);

        const mobileDisplays = document.querySelectorAll(".user-mobile-display");
        mobileDisplays.forEach(el => el.innerText = user.mobile_number);

        // Update title if we are on dashboard
        if (document.querySelector(".header h1")) {
            // For example "SLC farmer - [Name]"
            // document.querySelector(".header h1").innerText += ` - ${user.full_name}`;
        }

    } catch (error) {
        console.error("Failed to load user profile:", error);
    }
}

// ---------- OTP VERIFICATION (Function used by otp.html) ----------
// Note: otp.html has its own inline script as well. 
// We should ideally consolidate. But let's support global function if called.

// This function is likely called by the inline script in otp.html or we can replace the inline script logic.
// However, otp.html was manually updated earlier to inline logic. 
// Ideally we should have one place. Let's make a function that can be called.

async function verifyOtpBackend(enteredOtp) {
    const mobile = localStorage.getItem("verifyingMobile");
    const msg = document.getElementById("otpMsg");

    if (!mobile) {
        alert("No mobile number found. Please login again.");
        window.location.href = "index.html";
        return;
    }

    try {
        const response = await apiCall("/auth/verify-otp", "POST", {
            mobile_number: mobile,
            otp: enteredOtp
        });

        // Store JWT and session info
        localStorage.setItem("access_token", response.access_token);
        localStorage.setItem("loggedInUser", JSON.stringify({
            mobile: response.mobile_number,
            role: response.role
        }));

        alert(response.message);

        // Redirect based on user state
        if (response.user_exists) {
            window.location.href = `dashboard_${response.role}.html`;
        } else {
            alert("Verification successful. Please complete your registration.");
            window.location.href = "signup.html";
        }

    } catch (error) {
        if (msg) {
            msg.innerText = error.message;
            msg.style.color = "red";
        } else {
            alert(error.message);
        }
    }
}

// ---------- RESEND OTP ----------
async function resendOtp() {
    const mobile = localStorage.getItem("verifyingMobile");
    const msg = document.getElementById("otpMsg");

    if (!mobile) {
        alert("No mobile number found. Please login again.");
        window.location.href = "index.html";
        return false;
    }

    try {
        const response = await apiCall("/auth/send-otp", "POST", { mobile_number: mobile });

        // Store and display the new OTP
        localStorage.setItem("generatedOtp", response.otp);
        const otpDisplayEl = document.getElementById("otpDisplay");
        const generatedOtpEl = document.getElementById("generatedOtp");
        if (otpDisplayEl && generatedOtpEl) {
            generatedOtpEl.innerText = response.otp;
            otpDisplayEl.style.display = "block";
        }

        alert("A new OTP has been sent: " + response.otp);
        if (msg) msg.innerText = "";
        return true;
    } catch (error) {
        if (msg) {
            msg.innerText = error.message;
            msg.style.color = "red";
        } else {
            alert(error.message);
        }
        return false;
    }
}

// ---------- LOGOUT ----------
function logoutFunction() {
    if (confirm("Are you sure you want to log out?")) {
        localStorage.removeItem("loggedInUser");
        localStorage.removeItem("verifyingMobile");
        localStorage.removeItem("generatedOtp");
        window.location.href = "index.html";
    }
}


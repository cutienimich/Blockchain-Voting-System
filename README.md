# Blockchain-Voting-System
A voting system that uses blockchain for school organization electoral processes in Colegio de Montalban
📘 Blockchain-Based E-Voting System with AI Integration
(For School Organization Electoral Process)
1. 📌 Introduction

The proposed system is a secure, transparent, and efficient electronic voting platform designed for school organization elections. It integrates:

Blockchain technology to ensure vote immutability and transparency
Artificial Intelligence (AI) for identity verification and fraud detection
Multi-platform architecture (Mobile for users, Desktop for admin)

The goal is to eliminate traditional voting issues such as fraud, duplication, and lack of transparency.

2. 🎯 Objectives
General Objective

To develop a secure blockchain-based e-voting system enhanced with AI for school elections.

Specific Objectives
Ensure one person, one vote
Provide transparent and tamper-proof voting records
Implement AI-based facial verification
Detect fraudulent voting behavior using AI
Develop admin and user platforms
3. 🧩 System Overview

The system consists of:

📱 Mobile Application (Students / Voters)
💻 Desktop Application (Admin Panel)
⚙️ Backend API
🧠 AI Module
🧱 Blockchain Network
🗄️ Database System
4. 🛠️ Technology Stack
Frontend
Mobile App: React Native
Admin Desktop App: Electron
Backend
API Framework: FastAPI
Blockchain
Platform: Ethereum or Polygon
Smart Contracts: Solidity
Database
PostgreSQL
AI & Machine Learning
OpenCV
face_recognition
Scikit-learn
Authentication
JWT
5. 📱 System Features
5.1 User Mobile Application
Authentication
Login / Registration
Student ID verification
Voting
View elections
View candidates
Cast vote
Confirm vote
Transparency
View election results
View vote status
Profile
User information
Verification status
5.2 Admin Desktop Application
Election Management
Create elections
Set positions
Define voting schedule
Candidate Management
Approve/reject applications
Assign candidates
Voter Management
Upload student list
Verify users
Monitoring
Real-time voting activity
Fraud alerts
Reports
Export results
Audit logs
6. 🗄️ Database and Blockchain Design
6.1 Blockchain (On-chain)

Used for:

Vote storage
Smart contract execution
Ensuring immutability

Each vote includes:

Voter hash
Candidate ID
Timestamp
6.2 Database (Off-chain)

Used for:

User accounts
Candidate information
Election data
AI results (fraud flags, verification status)
6.3 System Interaction
Mobile App → Backend → Blockchain
                     ↓
                 Database
7. 🤖 Artificial Intelligence Integration
7.1 AI Module Overview

The system integrates AI for:

Identity verification
Fraud detection
7.2 Face Verification System
Purpose

To ensure that each registered user is a real and verified student.

Process
User uploads school ID
User captures live selfie
AI compares both images
System verifies identity
Output
Verified
Rejected
Needs manual review
Security Enhancements
Liveness Detection

Prevents fake inputs such as:

Printed photos
Screenshots

Example actions:

Blink detection
Head movement
Data Handling
Store face embeddings instead of raw images
Encrypt sensitive data
7.3 Fraud Detection System
Purpose

To detect abnormal or suspicious voting behavior.

Data Used
IP address
Device information
Login patterns
Voting timing
AI Model
Anomaly Detection using:
Scikit-learn (Isolation Forest)
Example Detection
Multiple votes from same IP
Rapid voting behavior
Repeated login attempts
Output
Low risk
Medium risk
High risk (flagged for admin review)
8. 🔐 Security Measures
Authentication
JWT-based session management
Multi-factor authentication (optional)
Data Security
HTTPS encryption
Password hashing (bcrypt)
Blockchain Security
Immutable vote records
Smart contract validation
Access Control
Role-based access (Admin / User)
9. 🔗 System Integration Architecture
[ Mobile App ]        [ Admin Desktop ]
        ↓                     ↓
        └──────→ [ Backend API ] ←──────┘
                         ↓
                 ┌───────────────┐
                 │   AI Module   │
                 │ Face Verify   │
                 │ Fraud Detect  │
                 └───────────────┘
                         ↓
                  [ Blockchain ]
                         ↓
                   [ Database ]
10. 🗳️ Candidate Application Process
Recommended Approach: Hybrid System
User submits candidacy via mobile app
Admin reviews application
Admin approves or rejects
Advantages
Scalable
Controlled
Transparent
11. ⚖️ Ethical and Privacy Considerations
Obtain user consent for facial data
Limit access to sensitive information
Encrypt biometric data
Use AI strictly for:
Verification
Security
Statement for Documentation

“The system utilizes facial recognition solely for identity verification and employs anomaly detection for fraud prevention, ensuring that all biometric and behavioral data are securely processed and protected.”

12. 🏁 Conclusion

The proposed system combines:

Blockchain → ensures transparency and immutability
AI → enhances security and intelligence
Modern applications → improve accessibility and usability

This integration results in a secure, efficient, and trustworthy voting system suitable for academic institutions.

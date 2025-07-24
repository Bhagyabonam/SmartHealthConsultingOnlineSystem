# 🏥 Smart Health Consulting Online System

A blockchain-powered web platform for secure health data management, appointment booking, and prescription handling for hospitals, doctors, and patients.

---

## 📦 Project Structure

```
walmart Project/
│
├── Blockchain/
│   ├── SmartHealth/
│   │   ├── manage.py
│   │   ├── db.sqlite3
│   │   ├── SmartHealth/
│   │   │   └── ... Django project files ...
│   │   ├── SmartHealthApp/
│   │   │   └── ... Django app files ...
│   ├── SmartHealth.sol
│   ├── SmartHealth.json
│   ├── instructions.txt
│   ├── node-v12.13.1-x64.msi
│   ├── hello-eth/
│   ├── SCREENS.docx
│
├── 2.Smart Health Consulting Online System/
│   └── Smart Health Consulting Online System doc.docx
```

---

## 🚀 Features

- **Blockchain Security:** Health data stored on Ethereum blockchain.
- **Role-Based Access:** Admin, Doctor, and Patient portals.
- **Appointment & Prescription Management:** Book appointments, view reports, manage prescriptions.
- **Disease & Doctor Search:** Find doctors and medicines by symptoms.
- **Modern UI:** Responsive templates and easy navigation.

---

## 🛠️ Installation & Requirements

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/walmart-Project.git
cd "walmart Project/Blockchain/SmartHealth"
```

### 2. Install Node.js

Run the installer from the project:

```
Blockchain/node-v12.13.1-x64.msi
```

### 3. Install Python Dependencies

```sh
pip install numpy==1.19.2 pandas==0.25.3 web3==4.7.2 Django==2.1.7
```

### 4. Deploy the Smart Contract

- Compile and deploy `SmartHealth.sol` using Ganache/Truffle or your preferred Ethereum environment.
- Update the contract address in Django settings or `views.py`.

### 5. Run the Django Server

```sh
python manage.py runserver
```

---

## 👨‍💻 Usage

- Visit `http://127.0.0.1:8000/`
- Register as a patient, doctor, or admin
- Book appointments, add/view health reports, and manage prescriptions
- All actions are securely logged on the blockchain

---

## 📸 Screenshots

See [[SCREENS.docx](https://docs.google.com/document/d/1L5GrNx-Qo-uXQQukx9diIKDj9Wcl9Q1q/edit?usp=sharing&ouid=100390410469731224803&rtpof=true&sd=true)] for UI and workflow examples.

---

## 📜 Documentation

- [[Smart Health Consulting Online System doc.docx](https://docs.google.com/document/d/1APEQWesnIcjuwq0VjkdX8OAMLVGEfOxy/edit?usp=sharing&ouid=100390410469731224803&rtpof=true&sd=true)]

---

## 🤝 Author

**Bonam Bhagya Sri Lakshmi**  
GitHub: [@BhagyaBonam](https://github.com/BhagyaBonam)

---

## ⭐️ Support

If you like this project, please star it on GitHub!

---

_This project uses Django, Web3.py, and Ethereum smart contracts for secure

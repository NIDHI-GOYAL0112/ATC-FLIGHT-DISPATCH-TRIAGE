# ATC-FLIGHT-DISPATCH-TRIAGE
AI-based Expert System for Air Traffic Control (ATC) flight dispatch using Python and Experta. The system analyzes aircraft type, weather, fuel, visibility, and wind conditions through rule-based inference to generate intelligent decisions such as landing clearance, holding patterns, and emergency diversion.
# ✈️ ATC Flight Dispatch Triage Expert System

An AI-based Expert System for Air Traffic Control (ATC) Flight Dispatch Decision Support built using Python and the `Experta` rule engine.

The system simulates intelligent flight dispatch operations by evaluating aircraft telemetry and environmental conditions, then using rule-based inference to generate operational recommendations such as landing clearance, holding patterns, or emergency diversion.

---

## 📌 Project Overview

This project implements a **knowledge-based expert system** that mimics decision-making used in aviation dispatch and air traffic management.

The system analyzes:

* Aircraft category
* Weather conditions
* Wind speed
* Visibility
* Fuel availability

Using inference rules and fact chaining, it determines the safest operational action.

---

## 🚀 Features

✅ Rule-based AI using the Experta inference engine
✅ Dynamic weather safety evaluation
✅ Aircraft-specific operating limits
✅ Fuel reserve analysis
✅ Weather hazard detection
✅ Military aircraft priority handling
✅ Automatic dispatch recommendations
✅ Input validation and error handling
✅ Command Line Interface (CLI)

---

## 🧠 Expert System Architecture

The project follows a classic Expert System design:

### Knowledge Base

Stores facts and decision rules:

* Flight data
* Weather status
* Fuel status
* Aircraft priority

### Inference Engine

Uses forward chaining to derive conclusions from facts.

### User Interface

Command-line interface for entering telemetry data.

---

## 📋 Rules Implemented

### Weather Rules

* Thunderstorms automatically trigger unsafe conditions
* Fog with low visibility is considered hazardous
* Snow/Ice reduces runway friction
* Heavy weather reduces allowable wind limits

### Fuel Rules

* Fuel < 45 minutes → Critical fuel reserve
* Fuel ≥ 45 minutes → Healthy fuel reserve

### Aircraft Rules

Different aircraft classes have different wind tolerance:

| Aircraft Type | Maximum Wind |
| ------------- | ------------ |
| Small         | 20 knots     |
| Medium        | 30 knots     |
| Large         | 40 knots     |
| Industrial    | 40 knots     |
| Army          | 40 knots     |

### Final Decision Rules

| Weather | Fuel     | Action              |
| ------- | -------- | ------------------- |
| Severe  | Healthy  | Holding Pattern     |
| Severe  | Critical | Emergency Diversion |
| Clear   | Any      | Cleared for Landing |

---

## 🛠️ Technologies Used

* Python 3
* Experta
* Rule-Based Artificial Intelligence
* Forward Chaining Inference

---

## 📂 Project Structure

```bash
project/
│
├── evaluator.py        # Main Expert System implementation
├── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ATC-Flight-Dispatch-Expert-System.git
```

Move into the project directory:

```bash
cd ATC-Flight-Dispatch-Expert-System
```

Install required dependencies:

```bash
pip install experta
```

---

## ▶️ Run the Project

Execute:

```bash
python evaluator.py
```

---

## 💻 Example Execution

```bash
Select Aircraft Class:
[1] Small
[2] Medium
[3] Large
[4] Industrial
[5] Army

Enter choice: 3

Select Current Destination Weather:
[1] Clear / Normal
[2] Light Rain
[3] Heavy Rain
[4] Snow / Ice
[5] Thunderstorm
[6] Fog

Enter choice: 5

Fuel Remaining: 60
Visibility: 2
Wind Speed: 35
```

Output:

```bash
⚡ WARNING: Thunderstorm cell detected.
🌩️ HAZARD: Weather exceeds safe operating limits.
⛽ FUEL: Sufficient holding fuel available.
✈️ FINAL ACTION: INITIATE HOLDING PATTERN.
```

---

## 🎯 Future Improvements

* Add graphical user interface (GUI)
* Integrate real-time weather APIs
* Add airport database support
* Include machine learning prediction models
* Implement route optimization
* Add emergency severity scoring

---

## 📚 Learning Concepts Used

This project demonstrates:

* Artificial Intelligence
* Expert Systems
* Knowledge Representation
* Rule-Based Systems
* Forward Chaining
* Decision Support Systems

---

## 👨‍💻 Author

Nidhi Goyal

---

## 📄 License

This project is intended for educational and learning purposes.

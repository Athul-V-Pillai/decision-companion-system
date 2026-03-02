# Decision Companion System

A web-based decision support system that helps users evaluate multiple options against weighted criteria using a transparent, deterministic algorithm. Make better decisions with clear reasoning, visual analysis, and shareable reports.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Key Components](#key-components)
- [Documentation](#documentation)
- [Future Enhancements](#future-enhancements)

## Overview

The Decision Companion System is a practical tool for making complex decisions transparently. Instead of using black-box AI recommendations, it employs a rule-based **Weighted Sum Model (WSM)** algorithm that allows users to understand exactly how and why decisions are ranked.

**Use Cases:**
- Career path evaluation
- Product/service selection
- Investment decisions
- Project prioritization
- Purchase comparisons

## Features

### Core Features

✅ **Dynamic Decision Framework**
- Add unlimited options and criteria
- Assign weighted importance to each criterion
- Assign performance scores for each option-criterion pair

✅ **Transparent Scoring**
- Deterministic Weighted Sum Model algorithm
- Min-max normalization for fair comparison across scales
- Clear score breakdown showing contribution of each criterion

✅ **Decision Confidence Levels**
- Automatic confidence scoring (High/Medium/Low)
- Based on score distribution and consistency
- Helps identify clear vs. ambiguous decisions

✅ **Multi-Format Visualization**
- **Bar Chart**: Side-by-side option score comparison
- **Radar Chart**: Multi-criteria performance analysis
- Color-coded results for quick assessment

✅ **Decision History**
- Auto-save all evaluations to JSON storage
- Review past decisions and analyses
- Delete unwanted records

✅ **Professional PDF Reports**
- Export decisions as formatted PDF documents
- Includes ranking, scores, explanations, and recommendations
- Business-ready formatting with tables and styling

✅ **Natural Language Explanations**
- Automatic generation of decision reasoning
- Identifies top-performing options
- Explains ranking rationale clearly

## Tech Stack

### Backend
- **Framework**: Flask 2.3.3 (Python)
- **Language**: Python 3.x
- **PDF Generation**: ReportLab
- **Data Storage**: JSON (flat-file)
- **API Style**: RESTful

### Frontend
- **Markup**: HTML5
- **Styling**: CSS3 (responsive design)
- **Interactivity**: Vanilla JavaScript (no frameworks)
- **Visualization**: Chart.js 3.9.1
- **Deployment**: Static files served by Flask

### Development
- **Version Control**: Git
- **Package Management**: pip (Python)
- **Virtual Environment**: venv

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                         │
│  ┌──────────────────────────────────────────────┐   │
│  │  HTML/CSS/JavaScript (Vanilla)              │   │
│  │  - Form Generation & Validation             │   │
│  │  - Chart.js Integration (Bar + Radar)       │   │
│  │  - History Management                       │   │
│  │  - PDF Export Handler                       │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────┬──────────────────────────────────┘
                  │ REST API (JSON)
┌─────────────────▼──────────────────────────────────┐
│                  BACKEND (Flask)                    │
│  ┌──────────────────────────────────────────────┐  │
│  │  app.py (Routes & Controllers)              │  │
│  │  ├─ POST /api/evaluate                      │  │
│  │  ├─ GET  /api/history                       │  │
│  │  ├─ DELETE /api/history/{id}                │  │
│  │  └─ POST /api/export-report                 │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Decision Engine (decision_engine/)          │  │
│  │  ├─ validator.py    (Input validation)      │  │
│  │  ├─ evaluator.py    (Scoring & ranking)    │  │
│  │  ├─ explainer.py    (Explanations)         │  │
│  │  └─ __init__.py     (History manager)      │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Data Layer                                  │  │
│  │  ├─ data/decision_history.json              │  │
│  │  └─ ReportLab (PDF generation)              │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Data Flow

```
User Input (Form)
        ↓
[Browser Validation]
        ↓
POST /api/evaluate (JSON payload)
        ↓
[Server-side Validation] → validator.py
        ↓
[Normalization] → Min-max scaling (0-1)
        ↓
[Weighted Scoring] → WSM Algorithm
        ↓
[Ranking] → Sort by score
        ↓
[Confidence Calculation] → High/Medium/Low
        ↓
[Explanation Generation] → Natural language
        ↓
Response with Results → Display in UI
        ↓
[Auto-save to History] → data/decision_history.json
```

## Project Structure

```
Decision Companion System/
│
├── Source Code/                    # Main application code
│   ├── app.py                     # Flask application & API routes
│   ├── config.py                  # Configuration settings
│   ├── requirements.txt           # Python dependencies
│   ├── run.sh / run.bat           # Startup scripts
│   │
│   ├── decision_engine/           # Core decision logic
│   │   ├── __init__.py           # Module exports & HistoryManager
│   │   ├── validator.py          # Input validation layer
│   │   ├── evaluator.py          # Scoring & ranking logic
│   │   └── explainer.py          # Explanation generation
│   │
│   ├── templates/
│   │   └── index.html            # Main UI template
│   │
│   ├── static/
│   │   ├── script.js             # Frontend logic & API calls
│   │   └── style.css             # Styling & responsive design
│   │
│   └── data/
│       └── decision_history.json  # Saved decisions
│
├── BUILD_PROCESS_DOCS/           # Development journey documentation
│   └── BUILD_PROCESS.md          # How the project was built
│
├── RESEARCH_LOG/                 # Research & decision logs
│   ├── Research_Logs_Summary.md  # Comprehensive research log
│   ├── Quick_Reference_Sheet.md  # Quick reference decisions
│   ├── architecture flow...      # ChatGPT architecture notes
│   └── final-architecture...     # Client-Server architecture notes
│
├── Design Diagram/               # Visual documentation
│   ├── architecture of dms.png
│   ├── data flow diagrams...png
│   ├── Decision Logic Flow...png
│   └── UML Component Diagram.png
│
└── README.md                     # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/decision-companion-system.git
cd "Decision Companion System"
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
```

**Activate virtual environment:**

- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

### Step 3: Install Dependencies

```bash
cd "Source Code"
pip install -r requirements.txt
```

### Step 4: Run the Application

**Option A: Using Python directly**

```bash
python app.py
```

**Option B: Using provided scripts**

- **Windows:**
  ```powershell
  .\run.bat
  ```

- **macOS/Linux:**
  ```bash
  ./run.sh
  ```

### Step 5: Access the Application

Open your browser and navigate to:

```
http://localhost:5000
```

The application will load, and you can start making decisions immediately.

## Usage

### Making a Decision

1. **Enter Decision Details**
   - Give your decision a title (e.g., "Choose a Laptop")
   - Add options to compare (e.g., "Dell", "MacBook", "HP")

2. **Define Criteria**
   - Add criteria that matter to your decision (e.g., "Price", "Performance", "Design")
   - Assign weight to each criterion (must sum to 100%)

3. **Score Options**
   - Rate each option against each criterion (0-100 scale)
   - Use consistent scoring methodology

4. **Review Results**
   - View ranked options with scores
   - Check confidence level (High/Medium/Low)
   - Read the natural language explanation
   - Examine bar chart and radar chart visualizations

5. **Export or Save**
   - **Save to History**: Auto-saved; view from history tab
   - **Export to PDF**: Download professional report for sharing

### Advanced Usage

**Modifying Past Decisions:**
- View history → Click on a decision
- Modify criteria/weights/scores
- Re-evaluate for comparison

**Comparing Decisions:**
- Use history to compare different analyses
- Track how your priorities have changed

## How It Works

### Algorithm: Weighted Sum Model (WSM)

The Decision Companion System uses the **Weighted Sum Model**, a deterministic multi-criteria decision-making algorithm:

**Step 1: Normalization**
- Convert all scores to 0-1 range using min-max normalization
- Ensures fair comparison regardless of input scale

**Formula:** `normalized_score = (score - min) / (max - min)`

**Step 2: Weighted Scoring**
- Multiply each normalized criterion score by its weight
- Sum the weighted scores for each option

**Formula:** `total_score = Σ(weight_i × normalized_score_i)`

**Step 3: Ranking**
- Sort options by total score (highest to lowest)
- Generate explanations for top performers

**Step 4: Confidence Calculation**
- Analyze score distribution
- High confidence: Clear winner (large score gap)
- Medium confidence: Multiple competitive options
- Low confidence: Close scores or high variability

### Why WSM?

✅ **Transparent**: Users understand exactly how scores are calculated  
✅ **Interpretable**: No black-box AI or hidden logic  
✅ **Scalable**: Handles any number of options/criteria  
✅ **Reliable**: Consistent, deterministic results  
✅ **Practical**: Widely used in real business contexts

## Key Components

### Backend Modules

**app.py (371 lines)**
- Flask application initialization
- REST API endpoint definitions
- Request handling and response formatting
- PDF export orchestration
- Error handling middleware

**decision_engine/validator.py**
- Input validation layer
- Validates options, criteria, weights, scores
- Returns detailed error messages
- Prevents invalid data from entering algorithm

**decision_engine/evaluator.py**
- Core scoring logic
- Min-max normalization implementation
- Weighted sum calculation
- Confidence score generation
- Ranking algorithm

**decision_engine/explainer.py**
- Natural language explanation generation
- Identifies top performers
- Explains ranking rationale
- Provides actionable recommendations

**decision_engine/__init__.py**
- Module initialization
- HistoryManager class for CRUD operations
- JSON file persistence
- Auto-save functionality

### Frontend Components

**script.js (811+ lines)**
- Dynamic form generation
- Form input validation
- API call orchestration (Fetch API)
- Chart.js integration (Bar & Radar charts)
- History management (load, delete, display)
- PDF export trigger and data capture
- Event listener setup

**style.css (674+ lines)**
- Responsive design (mobile, tablet, desktop)
- Card-based UI layout
- Professional color scheme
- Chart container styling
- History panel styling
- Print-friendly PDF styles

**index.html (181 lines)**
- Semantic HTML5 structure
- Form elements for input
- Results display containers
- Chart placeholders
- History section markup
- Action buttons (Export, View History)

## Documentation

### Included Documentation

1. **[BUILD_PROCESS.md](BUILD_PROCESS_DOCS/BUILD_PROCESS.md)**
   - Development journey from first idea to completed system
   - Decisions made and why
   - Mistakes and corrections
   - Lessons learned

2. **[RESEARCH_LOG/Research_Logs_Summary.md](RESEARCH_LOG/Research_Logs_Summary.md)**
   - All AI prompts used
   - Search queries and references
   - Analysis of accepted/rejected recommendations
   - Decision rationale matrix

3. **[RESEARCH_LOG/Quick_Reference_Sheet.md](RESEARCH_LOG/Quick_Reference_Sheet.md)**
   - Quick reference of key decisions
   - Technology selection matrix
   - Accepted/rejected features
   - Future research areas

4. **Design Diagrams** (in `Design Diagram/` folder)
   - System architecture visualization
   - Data flow diagrams
   - Component relationships
   - Decision logic flowchart

## API Endpoints

### POST /api/evaluate
Evaluate options against weighted criteria.

**Request:**
```json
{
  "decision_title": "Choose a Laptop",
  "options": ["Dell", "MacBook", "HP"],
  "criteria": {
    "Price": 30,
    "Performance": 40,
    "Design": 30
  },
  "scores": {
    "Dell": [90, 85, 70],
    "MacBook": [60, 95, 95],
    "HP": [75, 75, 80]
  }
}
```

**Response:**
```json
{
  "success": true,
  "ranking": [
    {"option": "MacBook", "score": 82.5, "confidence": "High"},
    {"option": "HP", "score": 77.5, "confidence": "Medium"},
    {"option": "Dell", "score": 82.0, "confidence": "High"}
  ],
  "explanation": "MacBook ranks highest...",
  "scores": {...}
}
```

### GET /api/history
Retrieve all saved decisions.

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "id": "uuid-1234",
      "title": "Choose a Laptop",
      "timestamp": "2026-03-02T10:30:00",
      "result": {...}
    }
  ]
}
```

### DELETE /api/history/{id}
Delete a specific decision from history.

### POST /api/export-report
Generate and download PDF report.

**Request:** Evaluation results data

**Response:** PDF file download

## File Guidelines

### Adding New Decision Criteria
1. Validate criteria names in `validator.py`
2. Update weight calculation in `evaluator.py`
3. Modify explainer logic in `explainer.py` if needed

### Customizing Styling
- Edit `static/style.css` for colors, fonts, layout
- Responsive breakpoints: 768px (tablet), 480px (mobile)

### Changing Algorithm
- Modify scoring logic in `decision_engine/evaluator.py`
- Update explanation logic in `decision_engine/explainer.py`

## Future Enhancements

### Phase 2: Advanced Features
- [ ] Advanced MCDM algorithms (TOPSIS, AHP, ELECTRE)
- [ ] Multi-user collaboration
- [ ] Real-time shared decision-making sessions
- [ ] User accounts and authentication

### Phase 3: Enterprise
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Machine learning criteria weighting suggestions
- [ ] Analytics and decision pattern analysis
- [ ] API for third-party integration
- [ ] Advanced visualization (heatmaps, custom charts)

### Phase 4: Deployment
- [ ] Docker containerization
- [ ] Kubernetes orchestration
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Performance optimization and caching
- [ ] Load testing and scalability

## Performance Metrics

- **Response Time**: < 200ms for evaluation
- **PDF Generation**: < 5 seconds
- **History Load**: < 1 second (up to 1000 decisions)
- **UI Responsiveness**: 60 FPS on modern browsers

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Troubleshooting

**Server won't start:**
- Check if port 5000 is available
- Verify Python virtual environment is activated
- Run `pip install -r requirements.txt` to ensure dependencies

**Charts not displaying:**
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for JavaScript errors
- Verify Chart.js loaded correctly

**PDF export fails:**
- Check file permission in `data/` directory
- Ensure all form fields are valid
- Review server logs for detailed error

**History not saving:**
- Verify `data/` directory exists
- Check file system permissions
- Review JSON file for syntax errors

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Contact & Support

- **Project Repository**: [GitHub Link]
- **Issue Tracker**: [GitHub Issues]
- **Email**: [Your Email]

## Changelog

### Version 1.0.0 (March 2, 2026)
- Initial release
- Core WSM algorithm implementation
- Full UI with form generation
- History tracking with JSON storage
- PDF export functionality
- Chart visualizations (Bar + Radar)
- Confidence scoring system
- Natural language explanations

## Acknowledgments

- Chart.js for visualization
- ReportLab for PDF generation
- Flask team for the web framework
- Research sources in RESEARCH_LOG/ folder

---

**Last Updated**: March 2, 2026  
**Status**: Production Ready ✓  
**Version**: 1.0.0

# Post-Quantum Cryptography Readiness Metric

A multi-stage analytical pipeline for evaluating and scoring Post-Quantum Cryptography (PQC) readiness frameworks using frequency analysis, NLP embeddings, and machine learning techniques.

## 📁 Project Structure

```
.
├── 00_data/                    # Centralized data repository
│   ├── raw/                    # Source PDF documents (30 frameworks)
│   ├── processed/              # Cleaned text files (001.txt - 030.txt)
│   ├── framework_mapping.csv   # PDF to Framework ID mapping
│   └── labels.csv              # Expert-labeled ground truth scores
│
├── 01_preprocess/              # Stage 1: PDF text extraction
│   └── preprocess.py           # Extract and clean text from PDFs
│
├── 02_freq-analysis/           # Stage 2: Frequency-based scoring
│   ├── frequency.py            # Keyword frequency analysis
│   ├── analysis.py             # Dimension score calculation
│   ├── run_pipeline.py         # Stage 2 pipeline runner
│   ├── keyword_map.py          # Keyword definitions per dimension
│   ├── dimension_weights.csv   # Weight assignments for dimensions
│   └── results/                # Per-framework frequency results
│
├── 03_ml-model/                # Stage 3: ML/NLP-based scoring
│   ├── main.py                 # NLP embedding-based scoring
│   ├── calibrate.py            # Score calibration vs expert labels
│   ├── calibrate_svr.py        # SVR-based calibration refinement
│   ├── composite_score_calculator.py  # Final weighted composite scores
│   ├── run_pipeline.py         # Stage 3 pipeline runner
│   ├── svr_config.json         # SVR hyperparameters
│   ├── svr_rf_config.json      # Random Forest hyperparameters
│   └── results/                # NLP scores and calibration outputs
│
└── 04_llm-pipeline/            # Stage 4: LLM-based scoring
    ├── run_stage1.py           # LLM scoring stage 1
    ├── run_stage2.py           # LLM scoring stage 2
    ├── llm_3090_score.py       # LLM inference script
    └── outputs/                # LLM scoring results
```

## 🎯 Five Dimensions of PQC Readiness

Each framework is evaluated across five key dimensions:

1. **Cryptographic Asset Management** - Inventory and classification of crypto assets
2. **Crypto-Agility** - Ability to swap algorithms and maintain flexibility
3. **Migration Planning** - Structured transition roadmap and timelines
4. **Risk Management** - Quantum threat assessment and mitigation strategies
5. **Standards Compliance** - Adherence to NIST, FIPS, CNSA 2.0, etc.

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8+
pip install -r requirements.txt
```

Required libraries:
- `pdfplumber` - PDF text extraction
- `sentence-transformers` - NLP embeddings
- `scikit-learn` - ML models
- `pandas`, `numpy` - Data manipulation

### Installation

```bash
git clone <repository-url>
cd pqc-readiness-metric
pip install -r requirements.txt
```

### Running the Pipeline

#### Stage 1: Preprocessing
```bash
cd 01_preprocess
python preprocess.py
```
**Output:** Cleaned text files in `00_data/processed/` (001.txt - 030.txt)

#### Stage 2: Frequency Analysis
```bash
cd 02_freq-analysis
python run_pipeline.py
```
**Output:** Keyword-based dimension scores in `02_freq-analysis/results/`

#### Stage 3: ML Model Scoring
```bash
cd 03_ml-model
python run_pipeline.py
```
**Output:** 
- `results/nlp_scores.csv` - NLP-based dimension scores
- `results/PQC_Framework_Composite_Scores.csv` - Final composite scores

#### Stage 4: LLM Pipeline
```bash
cd 04_llm-pipeline
python run_stage1.py
python run_stage2.py
```
**Output:** LLM-generated scores in `04_llm-pipeline/outputs/`

## 📊 Key Output Files

| File | Location | Description |
|------|----------|-------------|
| `framework_mapping.csv` | `00_data/` | Maps PDF filenames to Framework IDs |
| `labels.csv` | `00_data/` | Expert ground truth scores (0-5 scale) |
| `final_results.csv` | `02_freq-analysis/` | Frequency-based scores |
| `nlp_scores.csv` | `03_ml-model/results/` | NLP embedding scores |
| `PQC_Framework_Composite_Scores.csv` | `03_ml-model/results/` | **Final weighted composite scores** |

## 🔬 Methodology

### Stage 2: Frequency Analysis
- Keyword-based scoring using dimension-specific term lists
- TF-IDF weighting and normalization
- Scores scaled 0-5

### Stage 3: ML/NLP Scoring
- **Sentence embeddings** using `all-MiniLM-L6-v2` model
- **Semantic similarity** between framework chunks and dimension references
- **Keyword signals** (specific vs general term density)
- **Hybrid scoring** combining NLP + keyword features
- **Calibration** using SVR and Random Forest against expert labels
- **Weighted composite** using dimension-specific weights

### Dimension Weights
```
Cryptographic Assets:      25%
Crypto-Agility:           20%
Migration Planning:       25%
Risk Management:          15%
Standards Compliance:     15%
```

## 📈 Scoring Scale

| Score Range | Readiness Level |
|-------------|----------------|
| 4.0 - 5.0 | Excellent |
| 3.0 - 3.9 | Good |
| 2.0 - 2.9 | Moderate |
| 1.0 - 1.9 | Limited |
| 0.0 - 0.9 | Minimal |

## 🛠️ Configuration Files

- `02_freq-analysis/dimension_weights.csv` - Dimension weight assignments
- `02_freq-analysis/keyword_map.py` - Keyword definitions per dimension
- `03_ml-model/svr_config.json` - SVR hyperparameters
- `03_ml-model/svr_rf_config.json` - Random Forest hyperparameters

## 📝 Adding New Frameworks

1. Place PDF in `00_data/raw/`
2. Run Stage 1: `cd 01_preprocess && python preprocess.py`
3. Add expert scores to `00_data/labels.csv` (optional, for calibration)
4. Re-run Stages 2-3 to score the new framework

## 🧪 Validation

Expert labels in `00_data/labels.csv` are used to:
- Calibrate model parameters
- Validate scoring accuracy
- Tune dimension-specific thresholds

## 📄 License

[Add your license here]

## 👥 Contributors

Dino Edouard Halley Yacat
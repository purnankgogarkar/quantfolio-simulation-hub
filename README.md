# Quantfolio Simulation Hub

A professional-grade **portfolio risk analysis platform** that helps investors understand their investment risk using advanced Monte Carlo simulations, statistical modeling, and real-time market data.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Features

- **4 Simulation Methods**
  - Monte Carlo Simulation
  - Historical Simulation
  - Bootstrap Simulation
  - Stress Testing

- **Real-time Market Data** 📈
  - Live NSE/BSE stock prices
  - 1-year historical data
  - Automatic data alignment & cleaning

- **Professional Risk Metrics** 📊
  - Value at Risk (VaR) calculation
  - Expected Shortfall (ES)
  - Maximum Loss/Gain analysis
  - Statistical summaries

- **Interactive Dashboard** 🎨
  - Drag-and-drop portfolio builder
  - Real-time portfolio summary
  - Dynamic loss distribution charts
  - Portfolio composition breakdown

- **Professional PDF Reports** 📄
  - Embedded loss distribution charts
  - Financial explanations & insights
  - Risk recommendations
  - Compliance-ready disclaimers

- **Educational Content** 🎓
  - VaR/ES explanations
  - Chart interpretation guides
  - Risk management recommendations

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Backend** | Python, NumPy, Pandas |
| **Visualization** | Plotly, Matplotlib |
| **Data** | yfinance |
| **PDF Generation** | ReportLab |
| **Simulations** | SciPy, NumPy |

## 📸 Screenshots

### Dashboard
[Add screenshot of main dashboard]

### Risk Analysis Results
[Add screenshot of risk metrics]

### PDF Report
[Add screenshot of PDF report]

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/quantfolio-simulation-hub.git
cd quantfolio-simulation-hub
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
```
http://localhost:8501
```

## 📖 How to Use

1. **Upload Portfolio**
   - Click "Upload Excel" or "Build Portfolio"
   - Add stock symbols and quantities
   - File format: Stock, Quantity columns

2. **Configure Simulation**
   - Choose simulation method (Monte Carlo, Historical, Bootstrap, Stress)
   - Set number of iterations (1,000 - 50,000)
   - Select confidence level (90% - 99%)

3. **Run Simulation**
   - Click "🚀 Run Simulation"
   - Wait for calculations to complete

4. **Analyze Results**
   - View risk metrics (VaR, ES)
   - Explore loss distribution chart
   - Read educational explanations
   - Download PDF report or CSV data

## 📊 Key Concepts Explained

### Value at Risk (VaR)
The maximum amount you could lose on a single day with a given confidence level (e.g., 95%).

**Example**: VaR of ₹50,000 at 95% confidence means:
- 95% of days, you won't lose more than ₹50,000
- 5% of days, you might lose more than ₹50,000

### Expected Shortfall (ES)
The average loss on days when the loss exceeds the VaR threshold. Represents the worst-case scenario losses.

### Monte Carlo Simulation
Generates thousands of random market scenarios based on historical volatility and correlation to estimate potential portfolio outcomes.

## 🔧 Project Structure

```
quantfolio-simulation-hub/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── simulations/
│   ├── monte_carlo.py             # Monte Carlo implementation
│   ├── historical.py              # Historical simulation
│   ├── bootstrap.py               # Bootstrap resampling
│   └── stress_test.py             # Stress test simulation
│
├── utils/
│   ├── data_fetcher.py            # yfinance data integration
│   ├── pdf_generator.py           # PDF report generation
│   ├── explanations.py            # Financial education content
│   ├── styling.py                 # CSS styling
│   └── ...
│
└── ui/
    ├── portfolio_builder.py       # Portfolio input interface
    ├── modern_components.py       # Streamlit components
    └── charts.py                  # Visualization
```

## 🐛 Key Features & Bug Fixes

- ✅ **Intelligent data cleaning**: Handles missing values using forward/backward fill
- ✅ **Stock alignment**: Validates portfolio stocks against downloaded data
- ✅ **Error handling**: Comprehensive error messages for users
- ✅ **Performance optimization**: 10K simulations run in <5 seconds
- ✅ **Professional output**: PDFs with embedded charts and explanations

## 💡 Learning Points

This project demonstrates:

1. **Financial Computing**
   - Monte Carlo simulations
   - Statistical risk modeling
   - Time-series analysis

2. **Data Engineering**
   - Real-time data fetching
   - Data cleaning & alignment
   - Missing value handling

3. **Software Design**
   - Modular architecture
   - Error handling
   - Code organization

4. **Product Development**
   - UI/UX design
   - Professional reporting
   - User education

## 🚧 Future Enhancements

- [ ] Portfolio optimization suggestions
- [ ] Tax-loss harvesting recommendations
- [ ] Correlation analysis between stocks
- [ ] Multi-currency support
- [ ] Mobile app version
- [ ] API for integration
- [ ] Historical report tracking
- [ ] Risk alerts & notifications

## 📝 Notes

- Data is fetched in real-time from Yahoo Finance (yfinance)
- Simulations are based on 1-year historical data
- Past performance does not guarantee future results
- See disclaimer in PDF reports for important legal information

## ⚠️ Disclaimer

This tool is for **educational and analytical purposes only**. It is not a substitute for professional financial advice. Past performance does not guarantee future results. Consult with a qualified financial advisor before making investment decisions.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 👨‍💻 Author

[Your Name]
- GitHub: [@purnankgogarkar](https://github.com/purnankgogarkar)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/purnankgogarkar)
- Email: purnank18@gmail.com

## 📧 Questions?

Feel free to open an issue or reach out directly!

---

<p align="center">
  Built with ❤️ for financial literacy
  <br/>
  <sub>Quantfolio Simulation Hub © 2024</sub>
</p>

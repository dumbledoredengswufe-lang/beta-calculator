# Beta Calculator

A Python skill for calculating rolling 100-day beta coefficients for stocks. Uses HS300 index as market benchmark.

## Features

- **Rolling Window Calculation**: Calculates beta based on the past 100 trading days
- **Market Benchmark**: Uses HS300 (Shanghai-Hong Kong Stock Connect 300 Index) as the market benchmark
- **Batch Processing**: Automatically processes all stock data files in the folder
- **Auto Save**: Directly adds Beta column to the original files
- **Statistics**: Provides mean, standard deviation and other statistical information of Beta

## Beta Formula

```
Beta = Cov(Ri, Rm) / Var(Rm)

Where:
- Ri: Stock daily return (simple return)
- Rm: Market (HS300) daily return
- Cov(Ri, Rm): Covariance between stock and market
- Var(Rm): Market variance
```

## Installation

```bash
pip install pandas numpy openpyxl
```

## Usage

```bash
python3 calculate_beta.py
```

## Data Requirements

The input data should contain the following columns:
- **Column 114**: Stock daily return (Simple_Return)
- **Column 38**: HS300 percentage change (PctChange, in %)

Data files should contain 3 header rows, with data starting from row 4.

## Output

After calculation, each stock data file will have a new column added:

| Column Name | Chinese Name | Description |
|-------------|--------------|-------------|
| Rolling_Beta_100d | Rolling 100-day Beta | Rolling Beta based on past 100 trading days |

## Beta Interpretation

| Beta Range | Meaning | Investment Characteristics |
|-----------|---------|---------------------------|
| Beta > 1.5 | High Volatility Stock | Offensive, volatility more than 1.5x the market |
| Beta = 1.0 ~ 1.5 | Medium-High Volatility Stock | Synchronized with market or slightly higher |
| Beta = 1.0 | Market Synchronized Stock | Volatility completely synchronized with market |
| Beta = 0.5 ~ 1.0 | Medium-Low Volatility Stock | Volatility less than market |
| Beta < 0.5 | Low Volatility Stock | Defensive, volatility less than half of market |
| Beta < 0 | Negative Correlation Stock | Negatively correlated with market |

## Mathematical Principles

### CAPM Model
Beta originates from the Capital Asset Pricing Model (CAPM):

```
E(Ri) = Rf + Beta × (E(Rm) - Rf)

Where:
- E(Ri): Expected stock return
- Rf: Risk-free rate
- E(Rm): Market expected return
- E(Rm) - Rf: Market risk premium
```

### Economic Meaning of Beta
- Beta measures systematic risk (market risk)
- Cannot be eliminated through diversification
- Reflects the sensitivity of individual stocks to market fluctuations

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
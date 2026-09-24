<div align="center">

# Predictive Maintenance with Probability

**The alarm went off. Is it really a failure?**

An interactive dashboard that applies probability and statistics to a cyber-physical
maintenance system: vibration and temperature sensors, alarms that can be wrong, and the
decision to stop the machine or keep it running.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?logo=scipy&logoColor=white)](https://scipy.org)

`Every formula is checked against 100,000 Monte Carlo simulations`

[Português](README.md) &nbsp;·&nbsp; **English**

</div>

![Dashboard with the combination of normals tab open](docs/preview.png)

---

## The problem

There are three ways to do maintenance. **Corrective** fixes the machine after it breaks,
and unplanned downtime is expensive. **Preventive** replaces parts on a schedule and throws
away parts that were still good. **Predictive** decides based on the machine's real
condition, measured by sensors.

But sensors are noisy and alarms can be wrong. The project question is:

> With imperfect sensor data, how do we estimate the chance of failure and the best time to intervene?

## The model

```
Machine  →  Sensors (vibration, temperature)  →  IoT network  →  Probabilistic model  →  Decision
```

The model answers four questions, each using part of the course:

| Question | Distribution | Purpose |
|---|---|---|
| How many failures? | Binomial, Poisson | Plan staff and spare parts |
| When does it fail? | Exponential, Normal | Choose when to replace |
| Is the sensor right? | Bayes, joint distribution | Filter false alarms |
| How much to trust the data? | Combination of normals | Reduce measurement noise |

**Assumptions:** machines fail independently, the failure rate is constant over the period
and sensor noise is Normal with zero mean. Parameters are illustrative; in a real plant they
would come from the line's history.

## What each tab shows

| Tab | Formula | Result with default values |
|---|---|---|
| Sets | P(E ∪ M) = P(E) + P(M) − P(E ∩ M) | 17% chance of an electrical or mechanical failure in 1 month |
| Bayes | P(F\|A) = P(A\|F)·P(F) / P(A) | only **28%** of alarms are real failures |
| Binomial | C(n,k)·pᵏ·(1−p)ⁿ⁻ᵏ | 26% chance of 2 or more of 20 machines down within 10 days |
| Poisson | e^(−λ)·λᵏ / k! | 8% chance of a month with 6 or more failures |
| Joint | P(x) = Σ P(x,y), Cov = E[XY] − E[X]E[Y] | high vibration comes with high temperature 60% of the time |
| Exponential | P(T ≤ t) = 1 − e^(−λt) | 39% chance the inverter fails in the next 500 h |
| Normal | Z = (X − μ)/σ | preventive replacement at 3604 h with 1% risk |
| Uniform | (d − c)/(b − a) | 25% of stops last between 20 and 35 min |
| Combination of normals | aX₁ + bX₂ ~ N(aμ₁ + bμ₂, a²σ₁² + b²σ₂²) | two sensors together err only 0.89 °C |

Each tab shows the formula, what every symbol means, when to use it, controls to change
the parameters, and the theoretical result next to the simulated one.

<p align="center">
  <img src="docs/bayes.png" width="45%" alt="True and false alarms">
  <img src="docs/normal.png" width="45%" alt="Bearing life and replacement point">
</p>

## How to run

```bash
git clone https://github.com/caiogadotti/manutencao-preditiva-probabilidade.git
cd manutencao-preditiva-probabilidade
pip install -r requirements.txt
streamlit run app.py
```

### Deploy on Streamlit Community Cloud

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
2. Click **Create app** and pick this repository, branch `main`, file `app.py`.
3. Click **Deploy**. The light theme comes from `.streamlit/config.toml`.

## Structure

```
app.py                  Streamlit dashboard (one tab per topic)
modelos.py              formulas (SciPy) and Monte Carlo simulations (NumPy)
.streamlit/config.toml  visual theme
docs/                   README images
```

## References

- LEE, J.; BAGHERI, B.; KAO, H.-A. A Cyber-Physical Systems architecture for Industry 4.0-based manufacturing systems. *Manufacturing Letters*, v. 3, p. 18-23, 2015.
- JARDINE, A. K. S.; LIN, D.; BANJEVIC, D. A review on machinery diagnostics and prognostics implementing condition-based maintenance. *Mechanical Systems and Signal Processing*, v. 20, n. 7, p. 1483-1510, 2006.
- LEE, J. et al. Prognostics and health management design for rotary machinery systems. *Mechanical Systems and Signal Processing*, v. 42, p. 314-334, 2014.
- KALMAN, R. E. A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, v. 82, n. 1, p. 35-45, 1960.
- MONTGOMERY, D. C.; RUNGER, G. C. *Applied Statistics and Probability for Engineers*. Wiley.

---

Caio Gadotti · Course project for Probability and Statistics, Cyber-Physical Systems Engineering (ESCF) at PUC-SP.

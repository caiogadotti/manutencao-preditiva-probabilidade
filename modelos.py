import numpy as np
from scipy import stats

RNG = np.random.default_rng(42)


def uniao(p_a: float, p_b: float, p_ab: float) -> float:
    return p_a + p_b - p_ab


def bayes_alarme(prev: float, sens: float, fp: float) -> dict:
    p_alarme = sens * prev + fp * (1 - prev)
    return {
        "p_alarme": p_alarme,
        "p_falha_dado_alarme": sens * prev / p_alarme,
        "p_falha_dado_silencio": (1 - sens) * prev / (1 - p_alarme),
    }


def simular_bayes(prev: float, sens: float, fp: float, n: int = 100_000) -> float:
    falha = RNG.random(n) < prev
    alarme = np.where(falha, RNG.random(n) < sens, RNG.random(n) < fp)
    return falha[alarme].mean()


def binomial(n: int, p: float, n_sim: int = 50_000):
    k = np.arange(n + 1)
    return k, stats.binom.pmf(k, n, p), RNG.binomial(n, p, n_sim)


def poisson(lam: float, n_sim: int = 50_000):
    k = np.arange(int(lam + 5 * np.sqrt(lam) + 5))
    return k, stats.poisson.pmf(k, lam), RNG.poisson(lam, n_sim)


def conjunta_padrao() -> np.ndarray:
    """P(X=vibração alta, Y=temperatura alta) — linhas X∈{0,1}, colunas Y∈{0,1}."""
    return np.array([[0.60, 0.10], [0.12, 0.18]])


def analisar_conjunta(tab: np.ndarray) -> dict:
    px, py = tab.sum(1), tab.sum(0)
    ex, ey = px[1], py[1]
    cov = tab[1, 1] - ex * ey
    return {
        "px": px, "py": py,
        "independentes": np.allclose(tab, np.outer(px, py)),
        "cov": cov,
        "corr": cov / np.sqrt(px[1] * px[0] * py[1] * py[0]),
        "p_y1_dado_x1": tab[1, 1] / px[1],
    }


def exponencial(mtbf: float, t: float, s: float, n_sim: int = 100_000):
    lam = 1 / mtbf
    amostras = RNG.exponential(mtbf, n_sim)
    sobrev = amostras[amostras > s]
    return {
        "p_falha_ate_t": 1 - np.exp(-lam * t),
        "sim_p_falha_ate_t": (amostras <= t).mean(),
        "sem_memoria_sim": (sobrev <= s + t).mean(),
        "amostras": amostras,
    }


def normal_vida(mu: float, sigma: float, a: float, b: float, n_sim: int = 100_000):
    am = RNG.normal(mu, sigma, n_sim)
    return {
        "teorico": stats.norm.cdf(b, mu, sigma) - stats.norm.cdf(a, mu, sigma),
        "sim": ((am >= a) & (am <= b)).mean(),
        "amostras": am,
    }


def uniforme(a: float, b: float, c: float, d: float) -> float:
    lo, hi = max(a, c), min(b, d)
    return max(0.0, hi - lo) / (b - a)


def fusao_sensores(s1: float, s2: float):
    """Média ponderada ótima de 2 sensores com ruído Normal independente."""
    w1 = s2**2 / (s1**2 + s2**2)
    return w1, 1 - w1, np.sqrt((s1**2 * s2**2) / (s1**2 + s2**2))


def soma_normais(mus, sigmas, limite: float):
    mu, sd = sum(mus), np.sqrt(sum(s**2 for s in sigmas))
    return mu, sd, stats.norm.cdf(limite, mu, sd)

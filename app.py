import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from scipy import stats

import modelos as m

TEAL, AMB, DARK = "#0F766E", "#F59E0B", "#0B2E2B"
st.set_page_config(page_title="Manutenção Preditiva", page_icon="⚙️", layout="wide")
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.prop_cycle": plt.cycler(color=[TEAL, AMB])})

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;600&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
h1, h2, h3 {{ font-family: 'Instrument Serif', serif !important; font-weight: 400 !important; }}
h1 {{ font-size: 3rem !important; }}
.hero {{ background: {DARK}; color: #fff; padding: 28px 32px; border-radius: 18px; margin-bottom: 18px; }}
.hero h1 {{ color: #fff; margin: 0; }}
.hero p {{ color: #99F6E4; font-size: 1.1rem; margin: 6px 0 0; }}
.box {{ background: #E6F2F1; color: #1E293B; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; }}
.box b {{ color: {TEAL}; }}
.eyebrow {{ color: {TEAL}; font-weight: 600; letter-spacing: .12em; font-size: .78rem; text-transform: uppercase; }}
.result {{ background: {DARK}; color: #fff; border-radius: 14px; padding: 16px 20px; }}
.result .num {{ font-family: 'Instrument Serif', serif; font-size: 2.6rem; color: {AMB}; line-height: 1; }}
div[data-testid="stMetric"] {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 10px 14px; }}
.stTabs [data-baseweb="tab"] {{ font-size: 1rem; padding: 10px 16px; }}
.stTabs [data-baseweb="tab-list"] {{ flex-wrap: wrap; }}
section[data-testid="stSidebar"] h3 {{ font-size: 1.8rem !important; color: {TEAL}; }}
div[data-testid="stSlider"] label p, div[data-testid="stNumberInput"] label p {{ font-size: .95rem; font-weight: 600; }}
.card {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 16px; padding: 18px 20px; height: 100%; }}
.card .n {{ display:inline-block; width:34px; height:34px; border-radius:50%; background:{TEAL}; color:#fff;
           text-align:center; line-height:34px; font-weight:600; margin-bottom:8px; }}
.card h4 {{ font-family: 'Instrument Serif', serif; font-weight:400; font-size:1.5rem; margin:0 0 4px; color:#1E293B; }}
.card p {{ color:#475569; margin:0; }}
.card .use {{ color:#B45309; font-weight:600; margin-top:8px; }}
.flow {{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin:6px 0 18px; }}
.flow span {{ background:#E6F2F1; color:#1E293B; border-radius:12px; padding:12px 16px; font-weight:600; }}
.flow span.on {{ background:{TEAL}; color:#fff; }}
.flow i {{ color:#94A3B8; font-style:normal; font-size:1.3rem; }}
.hint {{ color:#475569; font-size:.95rem; border-left: none; background:#FFF7ED; border-radius:10px; padding:10px 14px; margin-top:10px; }}
</style>""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><h1>⚙️ Manutenção Preditiva com Probabilidade</h1>
<p>Engenharia de Sistemas Ciberfísicos · mexa nos controles e compare a fórmula com 100 mil simulações</p></div>""",
            unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### O modelo")
    st.markdown("""Uma célula de produção com sensores de **vibração** e **temperatura**.
O modelo responde quatro perguntas:

1. **Quantas falhas?** Binomial e Poisson
2. **Quando falha?** Exponencial e Normal
3. **O sensor está certo?** Bayes e distribuição conjunta
4. **Quanto confiar no dado?** Combinação de normais

**Hipóteses:** máquinas independentes, taxa de falha constante, ruído Normal.""")
    st.caption("Teórico = fórmula da aula · Simulado = sorteios Monte Carlo com NumPy")


def explica(formula: str, simbolos: str, quando: str):
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown('<div class="eyebrow">A fórmula</div>', unsafe_allow_html=True)
        st.latex(formula)
        st.markdown(f'<div class="box">{simbolos}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="eyebrow">Quando usar</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box">{quando}</div>', unsafe_allow_html=True)


def resultado(num: str, texto: str):
    st.markdown(f'<div class="result"><div class="num">{num}</div>{texto}</div>', unsafe_allow_html=True)


def fig():
    return plt.subplots(figsize=(7, 3.4))


abas = st.tabs(["Visão geral", "0 · Conjuntos", "1 · Bayes", "2 · Binomial", "2 · Poisson",
                "3 · Bidimensional", "4 · Exponencial", "4 · Normal", "4 · Uniforme", "5 · Normais"])

with abas[0]:
    st.subheader("Como o sistema funciona")
    st.markdown('''<div class="flow"><span>Máquina</span><i>→</i><span>Sensores de vibração e temperatura</span><i>→</i>
<span>Rede IoT</span><i>→</i><span class="on">Modelo probabilístico</span><i>→</i><span>Decisão: parar ou seguir</span></div>''',
                unsafe_allow_html=True)
    cards = [("1", "Quantas falhas?", "Binomial e Poisson contam falhas por turno e por mês.", "Planejar equipe e peças"),
             ("2", "Quando falha?", "Exponencial e Normal modelam o tempo de vida.", "Definir a hora da troca"),
             ("3", "O sensor está certo?", "Bayes e a distribuição conjunta filtram alarme falso.", "Confirmar antes de parar"),
             ("4", "Quanto confiar no dado?", "Combinação de normais funde dois sensores.", "Reduzir o ruído")]
    for col, (n, h, t, u) in zip(st.columns(4), cards):
        col.markdown(f'<div class="card"><div class="n">{n}</div><h4>{h}</h4><p>{t}</p><p class="use">→ {u}</p></div>',
                     unsafe_allow_html=True)
    st.markdown("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Alarmes que são falha real", "28%", help="Aba Bayes")
    c2.metric("Troca preventiva do rolamento", "3604 h", help="Aba Normal, risco de 1%")
    c3.metric("Erro após fundir 2 sensores", "0,89 °C", help="Aba Normais")
    st.markdown('<div class="hint">Como usar: escolha uma aba, leia a fórmula e mexa nos controles. '
                'Os valores teóricos são comparados com 100 mil sorteios Monte Carlo.</div>', unsafe_allow_html=True)

with abas[1]:
    st.subheader("Falha elétrica (E) ou mecânica (M)")
    explica(r"P(E\cup M)=P(E)+P(M)-P(E\cap M)",
            "<b>∪</b> “ou”: pelo menos um · <b>∩</b> “e”: os dois juntos · <b>ᶜ</b> complemento",
            "Chance de “um ou outro” quando os eventos podem ocorrer juntos. A interseção é contada duas vezes, então subtraímos.")
    st.markdown('<div class="eyebrow">Teste</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    pe = c1.slider("P(E)", 0.0, 0.5, 0.08, 0.01)
    pm = c2.slider("P(M)", 0.0, 0.5, 0.12, 0.01)
    pem = c3.slider("P(E ∩ M)", 0.0, float(min(pe, pm)), float(min(0.03, pe, pm)), 0.01)
    pu = m.uniao(pe, pm, pem)
    st.latex(rf"P(E\cup M)={pe}+{pm}-{pem}={pu:.3f}")
    resultado(f"{pu:.0%}", f"de chance de alguma falha · {1-pu:.0%} de seguir sem falha")

with abas[2]:
    st.subheader("O alarme tocou: é falha mesmo?")
    explica(r"P(F|A)=\frac{P(A|F)\,P(F)}{P(A|F)\,P(F)+P(A|\bar F)\,P(\bar F)}",
            "<b>P(F)</b> falha antes de olhar o sensor · <b>P(A|F)</b> sensibilidade · <b>P(A|F̄)</b> falso positivo",
            "Sabemos P(efeito | causa) e queremos P(causa | efeito). Se a falha é rara, os alarmes falsos dominam.")
    c1, c2, c3 = st.columns(3)
    prev = c1.slider("P(falha)", 0.001, 0.30, 0.02, 0.001, format="%.3f")
    sens = c2.slider("Sensibilidade P(A|F)", 0.5, 1.0, 0.95, 0.01)
    fp = c3.slider("Falso positivo P(A|F̄)", 0.0, 0.3, 0.05, 0.01)
    r = m.bayes_alarme(prev, sens, fp)
    sim = m.simular_bayes(prev, sens, fp)
    a, b, c = st.columns(3)
    a.metric("P(alarme)", f"{r['p_alarme']:.4f}")
    b.metric("P(F|A) teórico", f"{r['p_falha_dado_alarme']:.4f}")
    c.metric("P(F|A) simulado", f"{sim:.4f}", f"{sim - r['p_falha_dado_alarme']:+.4f}")
    resultado(f"{r['p_falha_dado_alarme']:.0%}", "dos alarmes são falha real. Dica: aumente P(falha) e veja o número subir.")

with abas[3]:
    st.subheader("Quantas máquinas falham no turno?")
    explica(r"P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}",
            "<b>n</b> máquinas · <b>k</b> quantas falham · <b>p</b> chance de cada uma · E[X] = np",
            "n fixo, tentativas independentes, só dois resultados e p igual para todas.")
    c1, c2 = st.columns(2)
    n = c1.slider("Nº de máquinas (n)", 1, 50, 20)
    p = c2.slider("P(falha de cada) p", 0.01, 0.5, 0.05, 0.01)
    k, pmf, sim = m.binomial(n, p)
    g, ax = fig()
    ax.bar(k, pmf, alpha=.8, label="Teórico")
    ax.plot(k, np.bincount(sim, minlength=n + 1)[: n + 1] / len(sim), "o", c=AMB, label="Simulado")
    ax.set_xlabel("máquinas com falha"); ax.legend()
    c1, c2 = st.columns([3, 2])
    c1.pyplot(g)
    with c2:
        st.metric("E[X] = n·p", f"{n*p:.2f}")
        resultado(f"{1-stats.binom.cdf(1,n,p):.0%}", "de ter 2 ou mais máquinas paradas")

with abas[4]:
    st.subheader("Quantas falhas no mês?")
    explica(r"P(X=k)=\frac{e^{-\lambda}\lambda^k}{k!}",
            "<b>λ</b> média de falhas no período · E[X] = Var[X] = λ",
            "Eventos raros e independentes num intervalo de tempo. É o limite da Binomial com n grande e p pequeno.")
    lam = st.slider("λ (falhas/mês)", 0.5, 15.0, 3.0, 0.5)
    k, pmf, sim = m.poisson(lam)
    g, ax = fig()
    ax.bar(k, pmf, alpha=.8, label="Teórico")
    ax.plot(k, np.bincount(sim, minlength=len(k))[: len(k)] / len(sim), "o", c=AMB, label="Simulado")
    ax.set_xlabel("falhas no mês"); ax.legend()
    c1, c2 = st.columns([3, 2])
    c1.pyplot(g)
    with c2:
        st.metric("P(nenhuma falha)", f"{np.exp(-lam):.4f}")
        resultado(f"{1-stats.poisson.cdf(5,lam):.0%}", "de um mês crítico (6 falhas ou mais)")

with abas[5]:
    st.subheader("Vibração (X) e temperatura (Y) andam juntas?")
    explica(r"P(X=x)=\sum_y P(x,y)\qquad \text{Cov}=E[XY]-E[X]E[Y]",
            "<b>P(x,y)</b> conjunta · <b>P(x)</b> marginal (soma da linha) · independentes se P(x,y)=P(x)P(y)",
            "Dois sensores na mesma máquina: um informa sobre o outro? Se sim, dá para confirmar um alarme com o outro.")
    base = m.conjunta_padrao()
    c = st.columns(4)
    v = [c[i].number_input(lbl, 0.0, 1.0, float(base.flat[i]), 0.01)
         for i, lbl in enumerate(["Vibr. normal · Temp. normal", "Vibr. normal · Temp. alta",
                                  "Vibr. alta · Temp. normal", "Vibr. alta · Temp. alta"])]
    tab = np.array(v).reshape(2, 2)
    if not np.isclose(tab.sum(), 1):
        st.error(f"A soma da tabela deve ser 1 (atual: {tab.sum():.2f})")
    else:
        r = m.analisar_conjunta(tab)
        c1, c2 = st.columns([3, 2])
        c1.table({"": ["Vibr. normal", "Vibr. alta", "P(Y)"], "Temp. normal": [tab[0, 0], tab[1, 0], r["py"][0]],
                  "Temp. alta": [tab[0, 1], tab[1, 1], r["py"][1]], "P(X)": [r["px"][0], r["px"][1], 1.0]})
        with c2:
            st.metric("Cov(X,Y)", f"{r['cov']:.4f}")
            st.metric("Correlação ρ", f"{r['corr']:.3f}")
            st.success("Independentes") if r["independentes"] else st.warning("Dependentes: P(x,y) ≠ P(x)·P(y)")
        resultado(f"{r['p_y1_dado_x1']:.0%}", "de temperatura alta quando a vibração está alta")

with abas[6]:
    st.subheader("Tempo até a falha")
    explica(r"f(t)=\lambda e^{-\lambda t}\qquad P(T\le t)=1-e^{-\lambda t}",
            "<b>λ</b> = 1/MTBF · <b>MTBF</b> tempo médio entre falhas · sem memória: P(T>s+t | T>s) = P(T>t)",
            "Falhas aleatórias, sem desgaste. Uma peça usada tem o mesmo risco de uma nova.")
    c1, c2, c3 = st.columns(3)
    mtbf = c1.slider("MTBF (h)", 100, 5000, 1000, 100)
    t = c2.slider("Janela t (h)", 10, 3000, 500, 10)
    s = c3.slider("Já funcionou s (h)", 0, 3000, 800, 50)
    r = m.exponencial(mtbf, t, s)
    g, ax = fig()
    ax.hist(r["amostras"], 80, density=True, alpha=.35, range=(0, 5 * mtbf), label="Simulado")
    x = np.linspace(0, 5 * mtbf, 300); y = np.exp(-x / mtbf) / mtbf
    ax.plot(x, y, lw=2, label="f(t)"); ax.fill_between(x, y, where=x <= t, color=AMB, alpha=.6)
    ax.set_xlabel("horas"); ax.legend()
    c1, c2 = st.columns([3, 2])
    c1.pyplot(g)
    with c2:
        st.metric("Simulado", f"{r['sim_p_falha_ate_t']:.4f}")
        st.metric(f"Já rodou {s} h (simulado)", f"{r['sem_memoria_sim']:.4f}", help="Quase igual: propriedade sem memória")
        resultado(f"{r['p_falha_ate_t']:.0%}", f"de falhar nas próximas {t} h")

with abas[7]:
    st.subheader("Vida útil do rolamento")
    explica(r"Z=\frac{X-\mu}{\sigma}\qquad P(a\le X\le b)=\Phi(z_b)-\Phi(z_a)",
            "<b>μ</b> vida média · <b>σ</b> espalhamento · <b>Φ(z)</b> área à esquerda na tabela",
            "Desgaste e grandezas que somam muitas pequenas causas. 68% ficam a 1σ da média, 95% a 2σ.")
    c1, c2, c3 = st.columns(3)
    mu = c1.slider("μ (h)", 1000, 10000, 5000, 100)
    sd = c2.slider("σ (h)", 100, 2000, 600, 50)
    risco = c3.slider("Risco aceito na troca", 0.001, 0.2, 0.01, 0.001, format="%.3f")
    a, b = st.slider("Intervalo [a, b]", 0, 15000, (4000, 6000), 100)
    r = m.normal_vida(mu, sd, a, b)
    corte = stats.norm.ppf(risco, mu, sd)
    g, ax = fig()
    x = np.linspace(mu - 4 * sd, mu + 4 * sd, 300); y = stats.norm.pdf(x, mu, sd)
    ax.plot(x, y, lw=2); ax.fill_between(x, y, where=(x >= a) & (x <= b), alpha=.3)
    ax.axvline(corte, c=AMB, lw=2, ls="--", label=f"troca: {corte:.0f} h"); ax.legend()
    c1, c2 = st.columns([3, 2])
    c1.pyplot(g)
    with c2:
        st.metric(f"P({a} ≤ X ≤ {b})", f"{r['teorico']:.4f}", f"sim {r['sim']:.4f}")
        resultado(f"{corte:.0f} h", f"troca preventiva com {risco:.1%} de risco")

with abas[8]:
    st.subheader("Duração de uma parada rápida")
    explica(r"f(x)=\frac{1}{b-a}\qquad P(c\le X\le d)=\frac{d-c}{b-a}",
            "<b>a, b</b> limites · <b>c, d</b> trecho de interesse · E[X] = (a+b)/2",
            "Só sabemos o mínimo e o máximo, sem valor preferido.")
    c1, c2 = st.columns(2)
    a_, b_ = c1.slider("Parada entre (min)", 0, 120, (0, 60))
    c_, d_ = c2.slider("Trecho de interesse (min)", 0, 120, (20, 35))
    pu = m.uniforme(a_, b_, c_, d_) if b_ > a_ else 0
    resultado(f"{pu:.0%}", f"das paradas duram entre {c_} e {d_} min · média {(a_+b_)/2:.0f} min")

with abas[9]:
    st.subheader("Dois sensores valem mais que um")
    explica(r"aX_1+bX_2\sim N(a\mu_1+b\mu_2,\;a^2\sigma_1^2+b^2\sigma_2^2)",
            "<b>a, b</b> pesos · peso ótimo a = σ₂²/(σ₁²+σ₂²) · soma de etapas: μ = Σμᵢ, σ² = Σσᵢ²",
            "Juntar medições com ruído ou somar etapas com tempo incerto. A variância cai com a fusão.")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.slider("σ sensor 1 (°C)", 0.1, 5.0, 2.0, 0.1)
        s2 = st.slider("σ sensor 2 (°C)", 0.1, 5.0, 1.0, 0.1)
        w1, w2, sf = m.fusao_sensores(s1, s2)
        st.latex(rf"\hat T={w1:.2f}\,T_1+{w2:.2f}\,T_2")
        g, ax = fig()
        x = np.linspace(-3 * max(s1, s2), 3 * max(s1, s2), 300)
        for sg, lb in [(s1, "Sensor 1"), (s2, "Sensor 2"), (sf, "Fusão")]:
            ax.plot(x, stats.norm.pdf(x, 0, sg), lw=3 if lb == "Fusão" else 1.5, label=lb)
        ax.legend(); st.pyplot(g)
        resultado(f"{sf:.2f} °C", "de erro após a fusão")
    with col2:
        st.markdown("**Soma das etapas da manutenção**")
        mus = [st.number_input(f"μ etapa {i+1} (min)", 1.0, 200.0, v) for i, v in enumerate([30.0, 45.0, 20.0])]
        sds = [st.number_input(f"σ etapa {i+1}", 0.1, 50.0, v) for i, v in enumerate([5.0, 8.0, 4.0])]
        lim = st.slider("Prazo (min)", 60, 150, 105)
        mu_t, sd_t, p = m.soma_normais(mus, sds, lim)
        st.latex(rf"T\sim N({mu_t:.0f},\;{sd_t:.2f}^2)")
        resultado(f"{p:.0%}", f"de terminar em até {lim} min")

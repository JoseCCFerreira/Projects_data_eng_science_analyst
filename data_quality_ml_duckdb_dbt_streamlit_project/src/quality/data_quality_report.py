import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd
from pathlib import Path
from src.quality.missing_values import missing_value_summary
from src.quality.outlier_detection import detect_iqr_outliers
from src.quality.statistical_profiling import profile_statistics, correlation_matrix
from src.utils.paths import RAW_CSV


REPORT_PATH = Path(__file__).resolve().parents[2] / "reports" / "data_quality_report.md"


def build_report(df: pd.DataFrame) -> str:
    missing = missing_value_summary(df)
    profile = profile_statistics(df)
    outliers = detect_iqr_outliers(df, ["temperature", "humidity", "pressure", "vibration", "energy_consumption", "target_failure_risk"])
    corr = correlation_matrix(df)
    duplicates = df.duplicated().sum()
    lines = [
        "# Data Quality Report",
        "\n",
        "## Resumo Executivo",
        f"- Registos totais: {len(df)}",
        f"- Variáveis: {df.shape[1]}",
        f"- Duplicados detectados: {duplicates}",
        f"- Valores nulos totais: {df.isna().sum().sum()}",
        "\n",
        "## Problemas principais",
        "- Valores nulos e timestamps ausentes podem afetar análises temporais e modelagem.",
        "- Duplicados podem inflar contagens e distorcer médias.",
        "- Outliers em temperatura, pressão e energia podem indicar medições anômalas ou falhas de sensor.",
        "- Categorias inconsistentes em `machine_status` e `location` devem ser normalizadas.",
        "\n",
        "## Estatísticas descritivas",
        profile.to_markdown(index=False),
        "\n",
        "## Valores nulos por coluna",
        missing.to_markdown(index=False),
        "\n",
        "## Outliers detectados (IQR)",
        outliers.to_markdown(index=False),
        "\n",
        "## Correlações principais",
        corr.to_markdown(),
        "\n",
        "## Exemplo de linhas problemáticas",
        "- `timestamp` ausente em algumas linhas;",
        "- `sensor_999` aparece como sensor inválido;",
        "- valores de pressão com +20 ou -30 hPa são fisicamente impossíveis;",
        "- `machine_status` em maiúsculas ou espaços extras são inconsistentes.",
        "\n",
        "## Recomendações",
        "- Limpar duplicados e imputar ou remover registros com timestamps nulos;",
        "- Normalizar categorias antes da modelagem;",
        "- Isolar outliers por equipamento antes de calcular métricas de desempenho;",
        "- Revisar faixas físicas e validar sensores com manutenção preventiva;",
        "- Usar dbt tests para rastrear qualidade de dados após transformações.",
    ]
    return "\n".join(lines)


def main():
    df = pd.read_csv(RAW_CSV, parse_dates=["timestamp"], dayfirst=False)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = build_report(df)
    REPORT_PATH.write_text(report)
    print(f"Relatório de qualidade gerado em {REPORT_PATH}")


if __name__ == "__main__":
    main()

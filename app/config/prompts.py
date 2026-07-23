import json

def build_chart_prompt(question: str, columns: list[str], analysis: dict) -> str:
    return f"""
Sən təcrübəli Data Vizuallaşdırma mütəxəssisisən.

Sənin vəzifən istifadəçi sualına əsasən qrafik yaradılmasının lazım olub-olmadığını müəyyən etməkdir.

Mövcud qrafik növləri:
- bar
- line
- pie
- scatter
- histogram

Mövcud sütunlar:
{json.dumps(columns, indent=2)}

Məlumat analizi:
{json.dumps(analysis, indent=2, default=str)}

İstifadəçi sualı:
{question}

Qaydalar:

- Yalnız etibarlı JSON qaytar.
- Heç vaxt izahat vermə.
- Heç vaxt markdown istifadə etmə.
- Mövcud olmayan sütunlar uydurma.
- Mövcud olmayan qrafik növləri uydurma.
- Yalnız verilmiş sütunlardan istifadə et.
- Əgər vizuallaşdırma faydalı deyilsə, aşağıdakı JSON-u qaytar:

{{"charts":[]}}

Cavab formatı:

{{
    "charts":[
        {{
            "chart_type":"bar",
            "x":"category",
            "y":"total_sales",
            "title":"Kateqoriyaya görə ümumi satışlar"
        }}
    ]
}}
"""


def build_sql_prompt(question: str, schema: str, history: list[str]) -> str:

    history_text = (
        "\n".join(history)
        if history
        else "Əvvəlki söhbət mövcud deyil."
    )

    return f"""
Sən təcrübəli SQLite SQL mühəndisisən.

Yalnız BİR düzgün SQLite sorğusu yarat.

Verilənlər bazasının sxemi:

{schema}

Əvvəlki söhbət:

{history_text}

Cari istifadəçi sualı:

{question}

Qaydalar:

- Yalnız SQL qaytar.
- Heç vaxt izahat vermə.
- Heç vaxt markdown istifadə etmə.
- SQL-i ```sql blokunda yazma.
- Yalnız mövcud cədvəllərdən istifadə et.
- Yalnız mövcud sütunlardan istifadə et.
- Mövcud olmayan cədvəllər uydurma.
- Mövcud olmayan sütunlar uydurma.
- SQLite daxili cədvəllərinə sorğu göndərmə.
- Aşağıdakı cədvəllərdən istifadə etmə:
    sqlite_master
    sqlite_sequence
    sqlite_stat1
    sqlite_*
- İstifadəçi xüsusi olaraq istəmədiyi halda UNION istifadə etmə.
- Əgər verilən sxem əsasında suala cavab vermək mümkün deyilsə, DƏQİQ aşağıdakı mətni qaytar:

CANNOT_GENERATE_SQL
"""

def build_insight_prompt(
    question: str,
    generated_sql: str,
    analysis: dict,
    kpis: dict,
) -> str:
    return f"""
Sən təcrübəli Data Analitiki və Business Intelligence (BI) mütəxəssisisən.

Sənin vəzifən təqdim olunan məlumatları analiz edərək peşəkar biznes insight hesabatı hazırlamaqdır.

=========================
İSTİFADƏÇİ SUALI
=========================
{question}

=========================
İCRA EDİLMİŞ SQL
=========================
{generated_sql}

=========================
MƏLUMAT XÜLASƏSİ
=========================
{json.dumps(analysis, indent=2, default=str)}

=========================
HESABLANMIŞ KPI-LAR
=========================
{json.dumps(kpis, indent=2, default=str)}

=========================
TƏLİMATLAR
=========================

- İstifadəçinin sualını YALNIZ təqdim olunan məlumatlara əsasən cavablandır.
- Heç bir fakt, statistika, trend və ya fərziyyə uydurma.
- Hər bir nəticə təqdim olunan məlumatlarla dəstəklənməlidir.
- Əgər mövcud məlumat cavab vermək üçün kifayət deyilsə, bunu açıq şəkildə bildir.
- Nəticələri şərh edərkən SQL sorğusunun əhatə dairəsini nəzərə al. Gələn nəticələrdən kənar ümumiləşdirmə etmə.
- Insight-ları qısa, aydın və biznes yönümlü yaz.

Cavabı DƏQİQ aşağıdakı JSON formatında qaytar:

{{
  "summary": "1-2 cümləlik qısa rəhbər xülasəsi.",
  "key_findings": [
    "Nəticə 1",
    "Nəticə 2",
    "Nəticə 3"
  ],
  "breakdown": "Hansı kateqoriya, qrup və ya seqmentin seçildiyini və səbəbini izah et.",
  "recommendation": "Məlumatlara əsaslanan praktik biznes tövsiyəsi ver.",
  "caveat": "Nümunə ölçüsü, SQL məhdudiyyəti, çatışmayan dəyərlər, təkrarlanan məlumatlar və ya digər məhdudiyyətləri qeyd et."
}}

Qaydalar:

- Yalnız düzgün JSON qaytar.
- Markdown istifadə etmə.
- JSON-dan əvvəl və ya sonra heç bir izahat yazma.
- JSON sintaktik cəhətdən düzgün olmalıdır.
"""


def build_planner_prompt(question: str) -> str:
    return f"""
Sən AI əsaslı Data Analitika Agenti üçün icra planlaşdırıcısısan.

Sənin vəzifən hansı ƏLAVƏ alətlərin işlədilməli olduğunu müəyyən etməkdir.

Əsas pipeline (həmişə avtomatik işləyir):

1. sql
   - SQL sorğusu yarat.
   - Sorğunu icra et.
   - DataFrame qaytar.

2. pandas
   - DataFrame-i analiz et.

3. kpi
   - KPI göstəricilərini hesabla.

4. insight
   - Biznes insight-ları yarat.

Yeganə əlavə alət:

chart
- Bir və ya bir neçə vizuallaşdırma yarat.

Yalnız istifadəçi açıq şəkildə və ya dolayı yolla vizuallaşdırma istədikdə chart yarat.

Vizuallaşdırma istəklərinə nümunələr:

- chart
- graph
- plot
- visualization
- dashboard
- histogram
- scatter plot
- bar chart
- line chart
- pie chart
- heatmap
- visualize
- compare visually
- show trends

Nümunələr

Sual:
Bütün satışları göstər.

Cavab:
{{"steps":[]}}

Sual:
Ən yüksək satış hansı kateqoriyadadır?

Cavab:
{{"steps":[]}}

Sual:
Kateqoriyalar üzrə satışları bar chart kimi göstər.

Cavab:
{{"steps":["chart"]}}

Sual:
Satışlar üçün dashboard yarat.

Cavab:
{{"steps":["chart"]}}

Qaydalar:

- Yalnız düzgün JSON qaytar.
- Heç vaxt sql, pandas, kpi və ya insight yazma.
- Yalnız əlavə alətləri qaytar.
- Əgər əlavə alət lazım deyilsə, aşağıdakı JSON-u qaytar:

{{"steps":[]}}

İstifadəçi sualı:

{question}
"""

def build_sql_correction_prompt(
    question: str,
    schema: str,
    previous_sql: str,
    error: str,
) -> str:
    return f"""
Sən təcrübəli SQLite SQL mühəndisisən.

Əvvəlki SQL sorğusu icra olunarkən xəta baş verdi.

İstifadəçi sualı:

{question}

Verilənlər bazasının sxemi:

{schema}

Əvvəlki SQL:

{previous_sql}

Xəta:

{error}

Sənin vəzifən düzgün SQL sorğusu yaratmaqdır.

Qaydalar:

- Yalnız SQL qaytar.
- Heç bir izahat vermə.
- Yalnız təqdim olunan sxemdən istifadə et.
- Mövcud olmayan cədvəl və ya sütun uydurma.
- Düzəldilmiş və işlək SQLite sorğusu yarat.
"""
#import "@preview/ilm:1.4.1": *

#set text(lang: "en")

#show: ilm.with(
  title: [QWIM Portfolio Analysis\ Report Using Typst],
  author: "The QWIM Team",
  date: datetime(year: 2025, month: 07, day: 01),
  abstract: [
    This comprehensive report analyzes portfolio allocation and investor information based on data from the QWIM Analytics platform. The analysis includes personal demographics, asset allocation strategies, financial goals assessment, income planning considerations, and detailed portfolio performance comparison against benchmark data. Data is sourced from the "Portfolios" and "Investors" tabs, providing a holistic view for retirement and investment planning strategies.
  ],
  preface: [
    #align(center + horizon)[
      This is placeholder for preface.\ One can use emojis #emoji.face.smile
    ]
  ],
  bibliography: bibliography("sample_refs.bib"),
  figure-index: (enabled: true),
  table-index: (enabled: true),
  listing-index: (enabled: true),
)

// Template documentation sections (keeping for reference)
= Layout
The template uses `A4` as its page size, you can specify a different #link("https://typst.app/docs/reference/layout/page#parameters-paper")[paper size string] using:

```typst
#show: ilm.with(
  paper-size: "us-letter",
)
```

'Ilm display's its content in the following order:
+ Cover page
+ Preface page (if defined)
+ Table of contents (unless disabled)
+ Body (your main content)
+ Appendix (if defined)
+ Bibliography (if defined)
+ Indices (if enabled) --- index of figures (images), tables, or listings (code blocks)

== Cover
The cover/title page has a title, author, date, and abstract which is a short description shown under the author name.

== Template Features
This template provides comprehensive support for financial reporting with professional typography and mathematical notation capabilities.

// Main Report Content Sections
= Investor Information

This section provides comprehensive analysis of investor demographics, financial status, and planning objectives based on data collected through the QWIM Analytics platform.

== Personal Info

// Data placeholders that will be replaced by Python processing
// Primary Investor Information
#let primary_investor_name = "{{PRIMARY_INVESTOR_NAME}}"
#let primary_investor_age_current = "{{PRIMARY_INVESTOR_AGE_CURRENT}}"
#let primary_investor_age_retirement = "{{PRIMARY_INVESTOR_AGE_RETIREMENT}}"
#let primary_investor_age_income_starting = "{{PRIMARY_INVESTOR_AGE_INCOME_STARTING}}"
#let primary_investor_status_marital = "{{PRIMARY_INVESTOR_STATUS_MARITAL}}"
#let primary_investor_gender = "{{PRIMARY_INVESTOR_GENDER}}"
#let primary_investor_tolerance_risk = "{{PRIMARY_INVESTOR_TOLERANCE_RISK}}"
#let primary_investor_state = "{{PRIMARY_INVESTOR_STATE}}"
#let primary_investor_code_zip = "{{PRIMARY_INVESTOR_CODE_ZIP}}"

// Partner Investor Information
#let partner_investor_name = "{{PARTNER_INVESTOR_NAME}}"
#let partner_investor_age_current = "{{PARTNER_INVESTOR_AGE_CURRENT}}"
#let partner_investor_age_retirement = "{{PARTNER_INVESTOR_AGE_RETIREMENT}}"
#let partner_investor_age_income_starting = "{{PARTNER_INVESTOR_AGE_INCOME_STARTING}}"
#let partner_investor_status_marital = "{{PARTNER_INVESTOR_STATUS_MARITAL}}"
#let partner_investor_gender = "{{PARTNER_INVESTOR_GENDER}}"
#let partner_investor_tolerance_risk = "{{PARTNER_INVESTOR_TOLERANCE_RISK}}"
#let partner_investor_state = "{{PARTNER_INVESTOR_STATE}}"
#let partner_investor_code_zip = "{{PARTNER_INVESTOR_CODE_ZIP}}"

Personal demographic information forms the cornerstone of any comprehensive financial planning analysis. This analysis includes detailed information for both investors:

=== Primary Investor: #primary_investor_name

The primary investor profile includes the following key demographics and characteristics:

- *Current Age*: #primary_investor_age_current years
- *Target Retirement Age*: #primary_investor_age_retirement years  
- *Income Starting Age*: #primary_investor_age_income_starting years
- *Marital Status*: #primary_investor_status_marital
- *Gender*: #primary_investor_gender
- *Risk Tolerance*: #primary_investor_tolerance_risk
- *State of Residence*: #primary_investor_state
- *ZIP Code*: #primary_investor_code_zip

=== Partner Investor: #partner_investor_name

The partner investor profile includes the following key demographics and characteristics:

- *Current Age*: #partner_investor_age_current years
- *Target Retirement Age*: #partner_investor_age_retirement years
- *Income Starting Age*: #partner_investor_age_income_starting years  
- *Marital Status*: #partner_investor_status_marital
- *Gender*: #partner_investor_gender
- *Risk Tolerance*: #partner_investor_tolerance_risk
- *State of Residence*: #partner_investor_state
- *ZIP Code*: #partner_investor_code_zip

#blockquote[
  Understanding the personal context of each investor is essential for developing tailored investment strategies that align with individual circumstances and long-term objectives.
]

The personal information analysis provides the demographic foundation that influences all subsequent portfolio allocation decisions and risk management strategies.

== Assets

// Asset data placeholders that will be replaced by Python processing
#let primary_taxable_assets = "{{PRIMARY_TAXABLE_ASSETS}}"
#let primary_tax_deferred_assets = "{{PRIMARY_TAX_DEFERRED_ASSETS}}"
#let primary_tax_free_assets = "{{PRIMARY_TAX_FREE_ASSETS}}"
#let primary_total_assets = "{{PRIMARY_TOTAL_ASSETS}}"

#let partner_taxable_assets = "{{PARTNER_TAXABLE_ASSETS}}"
#let partner_tax_deferred_assets = "{{PARTNER_TAX_DEFERRED_ASSETS}}"
#let partner_tax_free_assets = "{{PARTNER_TAX_FREE_ASSETS}}"
#let partner_total_assets = "{{PARTNER_TOTAL_ASSETS}}"

#let combined_taxable_assets = "{{COMBINED_TAXABLE_ASSETS}}"
#let combined_tax_deferred_assets = "{{COMBINED_TAX_DEFERRED_ASSETS}}"
#let combined_tax_free_assets = "{{COMBINED_TAX_FREE_ASSETS}}"
#let combined_total_assets = "{{COMBINED_TOTAL_ASSETS}}"

Asset allocation analysis represents a critical component of the investment planning process. This subsection examines the current financial position through comprehensive asset categorization:

=== Current Asset Allocation Summary

The following table presents the current asset allocation for both investors, organized by tax treatment:

#figure(
  table(
    columns: 4,
    table.header[*Asset Category*][*Primary Investor*][*Partner Investor*][*Combined Total*],
    [Taxable Assets], [#primary_taxable_assets], [#partner_taxable_assets], [#combined_taxable_assets],
    [Tax Deferred Assets], [#primary_tax_deferred_assets], [#partner_tax_deferred_assets], [#combined_tax_deferred_assets],
    [Tax Free Assets], [#primary_tax_free_assets], [#partner_tax_free_assets], [#combined_tax_free_assets],
    [*Total Assets*], [*#primary_total_assets*], [*#partner_total_assets*], [*#combined_total_assets*],
  ),
  caption: [Current Asset Allocation by Tax Treatment]
)

=== Asset Category Analysis

*Taxable Assets* include cash equivalents, savings accounts, investment accounts, and other assets subject to current taxation on income and capital gains.

*Tax Deferred Assets* encompass traditional retirement accounts such as 401(k) plans, traditional IRAs, and other qualified retirement plans where taxation is deferred until withdrawal.

*Tax Free Assets* include Roth retirement accounts, HSAs (for qualified medical expenses), and other vehicles that provide tax-free growth and distributions.

#blockquote[
  Effective asset allocation across different tax treatments is crucial for optimizing after-tax returns and managing tax liability throughout retirement.
]

The asset analysis provides insights into diversification effectiveness, risk concentration, and alignment with target allocation models for both individual and combined portfolios.

== Goals

// Goals data placeholders that will be replaced by Python processing
#let primary_essential_goals = "{{PRIMARY_ESSENTIAL_GOALS}}"
#let primary_important_goals = "{{PRIMARY_IMPORTANT_GOALS}}"
#let primary_aspirational_goals = "{{PRIMARY_ASPIRATIONAL_GOALS}}"
#let primary_total_goals = "{{PRIMARY_TOTAL_GOALS}}"

#let partner_essential_goals = "{{PARTNER_ESSENTIAL_GOALS}}"
#let partner_important_goals = "{{PARTNER_IMPORTANT_GOALS}}"
#let partner_aspirational_goals = "{{PARTNER_ASPIRATIONAL_GOALS}}"
#let partner_total_goals = "{{PARTNER_TOTAL_GOALS}}"

#let combined_essential_goals = "{{COMBINED_ESSENTIAL_GOALS}}"
#let combined_important_goals = "{{COMBINED_IMPORTANT_GOALS}}"
#let combined_aspirational_goals = "{{COMBINED_ASPIRATIONAL_GOALS}}"
#let combined_total_goals = "{{COMBINED_TOTAL_GOALS}}"

Financial goal analysis translates abstract aspirations into quantifiable targets with specific timelines and funding requirements. This comprehensive assessment examines the financial objectives for both investors across three priority categories:

=== Goal Prioritization Framework

The QWIM goal analysis framework categorizes financial objectives into three distinct priority levels:

- *Essential Goals*: Critical needs that must be funded for basic security and well-being
- *Important Goals*: Significant objectives that enhance quality of life and financial stability  
- *Aspirational Goals*: Desired outcomes that represent optimal financial success

=== Current Financial Goals Summary

The following table presents the current financial goals for both investors, organized by priority level:

#figure(
  table(
    columns: 4,
    table.header[*Goal Category*][*Primary Investor*][*Partner Investor*][*Combined Total*],
    [Essential Goals], [#primary_essential_goals], [#partner_essential_goals], [#combined_essential_goals],
    [Important Goals], [#primary_important_goals], [#partner_important_goals], [#combined_important_goals],
    [Aspirational Goals], [#primary_aspirational_goals], [#partner_aspirational_goals], [#combined_aspirational_goals],
    [*Total Goals*], [*#primary_total_goals*], [*#partner_total_goals*], [*#combined_total_goals*],
  ),
  caption: [Financial Goals by Priority Level]
)

=== Goal Category Analysis

*Essential Goals* represent the foundational financial requirements necessary for maintaining basic living standards and security throughout retirement. These goals typically include housing costs, healthcare expenses, basic living expenses, and minimum lifestyle maintenance.

*Important Goals* encompass financial objectives that significantly enhance quality of life and provide additional security beyond basic needs. These may include travel plans, home improvements, family support, and enhanced lifestyle choices.

*Aspirational Goals* represent the highest level of financial achievement, including luxury lifestyle choices, philanthropic objectives, legacy planning, and optimal lifestyle enhancement opportunities.

#blockquote[
  Effective goal prioritization ensures that essential needs are secured first, while systematically working toward important and aspirational objectives through strategic planning and resource allocation.
]

The goals analysis provides the foundation for determining required portfolio performance, risk tolerance parameters, and strategic asset allocation decisions to achieve targeted financial outcomes.

== Income

// Income data placeholders that will be replaced by Python processing
#let primary_social_security_income = "{{PRIMARY_SOCIAL_SECURITY_INCOME}}"
#let primary_pension_income = "{{PRIMARY_PENSION_INCOME}}"
#let primary_annuity_existing_income = "{{PRIMARY_ANNUITY_EXISTING_INCOME}}"
#let primary_other_income = "{{PRIMARY_OTHER_INCOME}}"
#let primary_total_income = "{{PRIMARY_TOTAL_INCOME}}"

#let partner_social_security_income = "{{PARTNER_SOCIAL_SECURITY_INCOME}}"
#let partner_pension_income = "{{PARTNER_PENSION_INCOME}}"
#let partner_annuity_existing_income = "{{PARTNER_ANNUITY_EXISTING_INCOME}}"
#let partner_other_income = "{{PARTNER_OTHER_INCOME}}"
#let partner_total_income = "{{PARTNER_TOTAL_INCOME}}"

#let combined_social_security_income = "{{COMBINED_SOCIAL_SECURITY_INCOME}}"
#let combined_pension_income = "{{COMBINED_PENSION_INCOME}}"
#let combined_annuity_existing_income = "{{COMBINED_ANNUITY_EXISTING_INCOME}}"
#let combined_other_income = "{{COMBINED_OTHER_INCOME}}"
#let combined_total_income = "{{COMBINED_TOTAL_INCOME}}"

Income analysis encompasses both current earnings and projected future income streams, providing essential data for cash flow planning and retirement readiness assessment. This comprehensive evaluation examines guaranteed and projected income sources for both investors:

=== Income Source Categories

The QWIM income analysis framework evaluates four primary categories of retirement income:

- *Social Security*: Government-provided retirement benefits based on earnings history
- *Pension*: Employer-sponsored defined benefit plans providing guaranteed income
- *Existing Annuities*: Previously purchased annuity contracts providing periodic payments
- *Other Income*: Additional income sources including rental income, business income, and other investments

=== Current Income Projections Summary

The following table presents the projected annual income streams for both investors by source category:

#figure(
  table(
    columns: 4,
    table.header[*Income Source*][*Primary Investor*][*Partner Investor*][*Combined Total*],
    [Social Security], [#primary_social_security_income], [#partner_social_security_income], [#combined_social_security_income],
    [Pension Income], [#primary_pension_income], [#partner_pension_income], [#combined_pension_income],
    [Existing Annuities], [#primary_annuity_existing_income], [#partner_annuity_existing_income], [#combined_annuity_existing_income],
    [Other Income], [#primary_other_income], [#partner_other_income], [#combined_other_income],
    [*Total Income*], [*#primary_total_income*], [*#partner_total_income*], [*#combined_total_income*],
  ),
  caption: [Projected Annual Retirement Income by Source]
)

=== Income Source Analysis

*Social Security Income* provides a foundation of guaranteed inflation-adjusted income throughout retirement. Benefits are calculated based on earnings history and claiming age, with optimization strategies available for married couples.

*Pension Income* represents employer-sponsored defined benefit payments that provide predictable monthly income for life. These benefits may include survivor options and cost-of-living adjustments depending on plan provisions.

*Existing Annuity Income* encompasses previously purchased annuity contracts that provide guaranteed periodic payments. These may include immediate annuities, deferred annuities, or variable annuities with guaranteed withdrawal benefits.

*Other Income Sources* include diverse income streams such as rental property income, business income, part-time employment, and other investment income that contribute to overall cash flow.

#blockquote[
  A comprehensive income strategy combines guaranteed income sources with flexible withdrawals from investment portfolios to create a robust and adaptable retirement income plan.
]

The income analysis serves as the foundation for determining the required portfolio withdrawal rate, identifying income gaps that need to be filled through additional strategies, and optimizing the overall retirement income plan to meet stated financial goals.

= Portfolio Analysis

This section presents detailed analysis of portfolio construction, performance evaluation, and strategic allocation recommendations based on the investor information and market conditions. The analysis incorporates modern portfolio theory principles while considering practical implementation constraints and behavioral finance considerations.

Portfolio analysis represents the synthesis of investor-specific requirements with market opportunities, resulting in customized investment strategies designed to optimize risk-adjusted returns while meeting specified financial objectives.

== Strategic Asset Allocation

Strategic asset allocation forms the foundation of long-term investment success by establishing target allocations across major asset classes based on the current asset base and investor objectives.

== Tactical Positioning

Tactical asset allocation involves short to medium-term adjustments to strategic targets based on market conditions and opportunity identification.

== Portfolios Comparison

// Portfolio comparison data placeholders that will be replaced by Python processing
#let portfolio_comparison_time_period = "{{PORTFOLIO_COMPARISON_TIME_PERIOD}}"
#let portfolio_comparison_start_date = "{{PORTFOLIO_COMPARISON_START_DATE}}"
#let portfolio_comparison_end_date = "{{PORTFOLIO_COMPARISON_END_DATE}}"
#let portfolio_comparison_viz_type = "{{PORTFOLIO_COMPARISON_VIZ_TYPE}}"
#let portfolio_comparison_total_return_portfolio = "{{PORTFOLIO_COMPARISON_TOTAL_RETURN_PORTFOLIO}}"
#let portfolio_comparison_total_return_benchmark = "{{PORTFOLIO_COMPARISON_TOTAL_RETURN_BENCHMARK}}"
#let portfolio_comparison_annualized_return_portfolio = "{{PORTFOLIO_COMPARISON_ANNUALIZED_RETURN_PORTFOLIO}}"
#let portfolio_comparison_annualized_return_benchmark = "{{PORTFOLIO_COMPARISON_ANNUALIZED_RETURN_BENCHMARK}}"
#let portfolio_comparison_volatility_portfolio = "{{PORTFOLIO_COMPARISON_VOLATILITY_PORTFOLIO}}"
#let portfolio_comparison_volatility_benchmark = "{{PORTFOLIO_COMPARISON_VOLATILITY_BENCHMARK}}"
#let portfolio_comparison_max_drawdown_portfolio = "{{PORTFOLIO_COMPARISON_MAX_DRAWDOWN_PORTFOLIO}}"
#let portfolio_comparison_max_drawdown_benchmark = "{{PORTFOLIO_COMPARISON_MAX_DRAWDOWN_BENCHMARK}}"
#let portfolio_comparison_sharpe_ratio_portfolio = "{{PORTFOLIO_COMPARISON_SHARPE_RATIO_PORTFOLIO}}"
#let portfolio_comparison_sharpe_ratio_benchmark = "{{PORTFOLIO_COMPARISON_SHARPE_RATIO_BENCHMARK}}"
#let portfolio_comparison_correlation = "{{PORTFOLIO_COMPARISON_CORRELATION}}"
#let portfolio_comparison_tracking_error = "{{PORTFOLIO_COMPARISON_TRACKING_ERROR}}"
#let portfolio_comparison_information_ratio = "{{PORTFOLIO_COMPARISON_INFORMATION_RATIO}}"

Portfolio vs benchmark comparison analysis provides critical insights into relative performance, risk characteristics, and the effectiveness of active management decisions. This comprehensive evaluation examines performance across multiple dimensions over the selected analysis period.

=== Performance Comparison Overview

The portfolio comparison analysis covers the period from #portfolio_comparison_start_date to #portfolio_comparison_end_date (#portfolio_comparison_time_period), utilizing #portfolio_comparison_viz_type methodology for performance evaluation.

=== Comparative Performance Metrics

The following table presents comprehensive performance statistics comparing the portfolio against its designated benchmark:

#figure(
  table(
    columns: 4,
    table.header[*Performance Metric*][*Portfolio*][*Benchmark*][*Difference*],
    [Total Return], [#portfolio_comparison_total_return_portfolio], [#portfolio_comparison_total_return_benchmark], [{{PORTFOLIO_COMPARISON_TOTAL_RETURN_DIFFERENCE}}],
    [Annualized Return], [#portfolio_comparison_annualized_return_portfolio], [#portfolio_comparison_annualized_return_benchmark], [{{PORTFOLIO_COMPARISON_ANNUALIZED_RETURN_DIFFERENCE}}],
    [Volatility (Std Dev)], [#portfolio_comparison_volatility_portfolio], [#portfolio_comparison_volatility_benchmark], [{{PORTFOLIO_COMPARISON_VOLATILITY_DIFFERENCE}}],
    [Maximum Drawdown], [#portfolio_comparison_max_drawdown_portfolio], [#portfolio_comparison_max_drawdown_benchmark], [{{PORTFOLIO_COMPARISON_MAX_DRAWDOWN_DIFFERENCE}}],
    [Sharpe Ratio], [#portfolio_comparison_sharpe_ratio_portfolio], [#portfolio_comparison_sharpe_ratio_benchmark], [{{PORTFOLIO_COMPARISON_SHARPE_RATIO_DIFFERENCE}}],
    [Correlation], [-], [-], [#portfolio_comparison_correlation],
    [Tracking Error], [-], [-], [#portfolio_comparison_tracking_error],
    [Information Ratio], [-], [-], [#portfolio_comparison_information_ratio],
  ),
  caption: [Portfolio vs Benchmark Performance Comparison (#portfolio_comparison_time_period)]
)

=== Performance Analysis

*Total Return* measures the complete return realized over the analysis period, including both capital appreciation and income distributions. This metric provides the foundation for evaluating absolute performance effectiveness.

*Annualized Return* standardizes performance measurement across different time periods, enabling consistent comparison and projection of long-term performance expectations.

*Volatility (Standard Deviation)* quantifies the degree of performance variability, serving as a primary measure of investment risk and the consistency of returns over time.

*Maximum Drawdown* identifies the largest peak-to-trough decline during the analysis period, highlighting the worst-case scenario investors experienced and portfolio resilience during market stress.

*Sharpe Ratio* measures risk-adjusted returns by comparing excess return over the risk-free rate relative to portfolio volatility, providing insight into compensation received for bearing investment risk.

*Correlation* measures the degree to which portfolio and benchmark returns move together, indicating the level of systematic risk exposure and diversification effectiveness.

*Tracking Error* quantifies the consistency of portfolio performance relative to the benchmark, measuring the standard deviation of return differences between portfolio and benchmark.

*Information Ratio* evaluates the portfolio manager's skill by measuring excess return per unit of tracking error, indicating the effectiveness of active management decisions.

=== Performance Visualization

[Note: Portfolio comparison chart visualization would be inserted here, showing the comparative performance trends over the analysis period using the selected visualization methodology. The chart would display both absolute and relative performance patterns, highlighting periods of outperformance and underperformance.]

#blockquote[
  Portfolio comparison analysis reveals both the effectiveness of investment strategy implementation and the value added through active management decisions relative to passive benchmark exposure.
]

=== Strategic Implications

The portfolio comparison results provide essential guidance for future strategic decisions:

- **Risk Management**: Volatility and drawdown metrics inform appropriate risk budgeting and position sizing decisions
- **Active Management Value**: Information ratio and tracking error analysis validates the effectiveness of active management strategies
- **Benchmark Appropriateness**: Correlation analysis confirms whether the selected benchmark accurately represents the portfolio's risk-return profile
- **Performance Attribution**: Return differentials highlight the sources of outperformance or underperformance for strategic optimization

The comparative analysis serves as a foundation for ongoing portfolio optimization, risk management refinement, and strategic asset allocation adjustments to enhance future performance outcomes.

== Risk Management

Comprehensive risk management encompasses multiple dimensions of portfolio risk through systematic identification, measurement, and mitigation strategies.

== Performance Evaluation

Performance evaluation provides systematic assessment of portfolio results relative to objectives, benchmarks, and peer comparisons.

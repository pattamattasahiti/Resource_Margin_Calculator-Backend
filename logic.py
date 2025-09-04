def calculate_bonus(salary_p_a_inr):
    """Calculate Bonus per annum in INR."""
    return (salary_p_a_inr / 2) * 0.0833

def calculate_india_margin(salary_inr, bonus_inr, overhead_inr):
    """Calculate India Margin (INR)."""
    return (salary_inr + bonus_inr + overhead_inr) * 0.10

def calculate_salary_p_a_usd(amount_inr, conversion_rate):
    """Convert INR to Salary P.A USD."""
    return amount_inr / conversion_rate

def calculate_salary_p_m_usd(salary_p_a_usd):
    """Calculate monthly salary in USD."""
    return salary_p_a_usd / 12

def calculate_billable_p_a_usd(billable_per_hour_usd, occupancy_rate, working_hours_per_year=2080):
    """Calculate annual billable amount in USD."""
    return billable_per_hour_usd * working_hours_per_year * occupancy_rate

def calculate_overhead_bonus_margin_usd(overhead_inr, bonus_inr, india_margin_inr, conversion_rate):
    """Total of Overhead, Bonus, and India Margin converted to USD."""
    return (overhead_inr + bonus_inr + india_margin_inr) / conversion_rate

def calculate_ctc_p_a_usa(salary_p_a_usd, overhead_bonus_margin_usd, overhead_usa_usd):
    """CTC per annum USA."""
    return salary_p_a_usd + overhead_bonus_margin_usd + overhead_usa_usd

def calculate_ctc_p_m_usa(ctc_p_a_usa):
    """CTC per month USA."""
    return ctc_p_a_usa / 12

def calculate_margin_p_a_usd(billable_p_a_usd, ctc_p_a_usa):
    """Margin per annum USD."""
    return billable_p_a_usd - ctc_p_a_usa

def calculate_margin_on_sales(margin_p_a_usd, billable_p_a_usd):
    """Margin on sales %."""
    if billable_p_a_usd == 0:
        return 0.0
    return margin_p_a_usd / billable_p_a_usd

def calculate_cost_per_hour(occupancy_rate, working_hours_per_year=2080):
    """Cost per hour calculation."""
    return working_hours_per_year * occupancy_rate

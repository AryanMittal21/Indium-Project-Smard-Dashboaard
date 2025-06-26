import pandas as pd
from db.db_conn import get_connection

# ============ DASHBOARD 1: Day-wise Fraud Analysis ============

def total_transactions(on_date):
    query = f"""
    SELECT COUNT(*) AS total_txns
    FROM transactions_data
    WHERE date::date = '{on_date}';
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def total_fraud_transactions(on_date):
    query = f"""
    SELECT COUNT(*) AS fraud_txns
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    WHERE f.target = 'Yes' AND t.date::date = '{on_date}';
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def fraud_by_mcc(on_date):
    query = f"""
    SELECT m.description AS mcc_category, COUNT(*) AS frauds
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    JOIN mcc_codes m ON t.mcc::text = m.mcc_code
    WHERE f.target = 'Yes' AND t.date::date = '{on_date}'
    GROUP BY m.description
    ORDER BY frauds DESC
    LIMIT 10;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def fraud_by_hour(on_date):
    query = f"""
    SELECT EXTRACT(HOUR FROM date) AS hour, COUNT(*) AS frauds
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    WHERE f.target = 'Yes' AND date::date = '{on_date}'
    GROUP BY hour
    ORDER BY hour;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def top_fraud_cities(on_date):
    query = f"""
    SELECT merchant_city, COUNT(*) AS frauds
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    WHERE f.target = 'Yes' AND t.date::date = '{on_date}'
    GROUP BY merchant_city
    ORDER BY frauds DESC
    LIMIT 5;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def chip_usage_in_fraud(on_date):
    query = f"""
    SELECT use_chip, COUNT(*) AS frauds
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    WHERE f.target = 'Yes' AND t.date::date = '{on_date}'
    GROUP BY use_chip;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def gender_distribution_fraud(on_date):
    query = f"""
    SELECT u.gender, COUNT(*) AS frauds
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    JOIN users_data u ON t.client_id = u.id
    WHERE f.target = 'Yes' AND t.date::date = '{on_date}'
    GROUP BY u.gender;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def age_group_distribution(on_date):
    query = f"""
    SELECT 
        CASE 
            WHEN u.current_age < 25 THEN '<25'
            WHEN u.current_age BETWEEN 25 AND 35 THEN '25-35'
            WHEN u.current_age BETWEEN 36 AND 50 THEN '36-50'
            ELSE '>50'
        END AS age_group,
        COUNT(*) AS frauds
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    JOIN users_data u ON t.client_id = u.id
    WHERE f.target = 'Yes' AND t.date::date = '{on_date}'
    GROUP BY age_group
    ORDER BY age_group;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def credit_score_distribution(on_date):
    query = f"""
    SELECT 
        CASE 
            WHEN credit_score < 500 THEN '<500'
            WHEN credit_score BETWEEN 500 AND 700 THEN '500-700'
            ELSE '>700'
        END AS score_range,
        COUNT(*) AS frauds
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    JOIN users_data u ON t.client_id = u.id
    WHERE f.target = 'Yes' AND t.date::date = '{on_date}'
    GROUP BY score_range;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def amount_fraud_vs_total(on_date):
    query = f"""
    SELECT 
        SUM(CASE WHEN f.target = 'Yes' THEN amount ELSE 0 END) AS fraud_amount,
        SUM(amount) AS total_amount
    FROM transactions_data t
    LEFT JOIN train_fraud_labels f ON t.id = f.id
    WHERE t.date::date = '{on_date}';
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

# ============ DASHBOARD 2: Card-wise / Account-wise Analysis ============

def account_txn_vs_fraud(client_id):
    query = f"""
    SELECT 
        SUM(CASE WHEN f.target = 'Yes' THEN 1 ELSE 0 END) AS fraud_count,
        COUNT(*) AS total_count
    FROM transactions_data t
    LEFT JOIN train_fraud_labels f ON t.id = f.id
    WHERE t.client_id = '{client_id}';
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def account_txn_trend(client_id):
    query = f"""
    SELECT t.date::date AS txn_date, COUNT(*) AS txns
    FROM transactions_data t
    WHERE t.client_id = '{client_id}'
    GROUP BY txn_date
    ORDER BY txn_date;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def account_fraud_trend(client_id):
    query = f"""
    SELECT t.date::date AS txn_date, COUNT(*) AS frauds
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    WHERE t.client_id = '{client_id}' AND f.target = 'Yes'
    GROUP BY txn_date
    ORDER BY txn_date;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def fraud_by_card_type(client_id):
    query = f"""
    SELECT c.card_type, COUNT(*) AS frauds
    FROM transactions_data t
    JOIN cards_data c ON t.card_id = c.id
    JOIN train_fraud_labels f ON t.id = f.id
    WHERE t.client_id = '{client_id}' AND f.target = 'Yes'
    GROUP BY c.card_type;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def fraud_by_card_brand(client_id):
    query = f"""
    SELECT c.card_brand, COUNT(*) AS frauds
    FROM transactions_data t
    JOIN cards_data c ON t.card_id = c.id
    JOIN train_fraud_labels f ON t.id = f.id
    WHERE t.client_id = '{client_id}' AND f.target = 'Yes'
    GROUP BY c.card_brand
    ORDER BY frauds DESC;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def fraud_vs_spending(client_id):
    query = f"""
    SELECT 
        SUM(CASE WHEN f.target = 'Yes' THEN amount ELSE 0 END) AS fraud_amount,
        SUM(amount) AS total_spent
    FROM transactions_data t
    LEFT JOIN train_fraud_labels f ON t.id = f.id
    WHERE t.client_id = '{client_id}';
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def top_mcc_by_user(client_id):
    query = f"""
    SELECT m.description AS mcc_category, COUNT(*) AS txns
    FROM transactions_data t
    JOIN mcc_codes m ON t.mcc::text = m.mcc_code
    WHERE t.client_id = '{client_id}'
    GROUP BY m.description
    ORDER BY txns DESC
    LIMIT 10;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def chip_vs_no_chip(client_id):
    query = f"""
    SELECT use_chip, COUNT(*) AS txns
    FROM transactions_data
    WHERE client_id = '{client_id}'
    GROUP BY use_chip;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def merchant_states_visited(client_id):
    query = f"""
    SELECT merchant_state, COUNT(*) AS txns
    FROM transactions_data
    WHERE client_id = '{client_id}'
    GROUP BY merchant_state
    ORDER BY txns DESC;
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)

def user_fraud_risk_profile(client_id):
    query = f"""
    SELECT 
        ROUND(AVG(u.credit_score::numeric), 2) AS avg_credit_score,
        ROUND(SUM(REGEXP_REPLACE(u.total_debt, '\\$', '', 'g')::numeric), 2) AS total_debt_fraud_txns
    FROM transactions_data t
    JOIN train_fraud_labels f ON t.id = f.id
    JOIN users_data u ON t.client_id = u.id
    WHERE f.target = 'Yes' AND t.client_id = '{client_id}';
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def dashboard1_daywise_summary(input_date):
    """Run all day-wise queries and return as a dictionary"""
    return {
        "total_txns": total_transactions(input_date),
        "fraud_txns": total_fraud_transactions(input_date),
        "fraud_by_mcc": fraud_by_mcc(input_date),
        "fraud_by_hour": fraud_by_hour(input_date),
        "fraud_by_city": top_fraud_cities(input_date),
        "fraud_chip_split": chip_usage_in_fraud(input_date),
        "fraud_by_gender": gender_distribution_fraud(input_date),
        "fraud_by_age_group": age_group_distribution(input_date),
        "fraud_by_credit_score": credit_score_distribution(input_date),
        "fraud_vs_total_amount": amount_fraud_vs_total(input_date)
    }


def dashboard2_userwise_summary(client_id):
    """Run all account-wise queries and return as a dictionary"""
    return {
        "fraud_vs_total_txns": account_txn_vs_fraud(client_id),
        "txn_trend": account_txn_trend(client_id),
        "fraud_trend": account_fraud_trend(client_id),
        "fraud_by_card_type": fraud_by_card_type(client_id),
        "fraud_by_card_brand": fraud_by_card_brand(client_id),
        "amount_spent_vs_lost": fraud_vs_spending(client_id),
        "mcc_usage": top_mcc_by_user(client_id),
        "chip_usage": chip_vs_no_chip(client_id),
        "merchant_states": merchant_states_visited(client_id),
        "fraud_risk_profile": user_fraud_risk_profile(client_id)
    }

from slack_bot import queries

# Test inputs
sample_date = "2018-06-01"
sample_client_id = "42"

print("========== DASHBOARD 1: Day-wise Fraud Analysis ==========\n")
dash1 = queries.dashboard1_daywise_summary(sample_date)
for k, v in dash1.items():
    print(f"\n🔹 {k}:\n{v}\n")

print("\n\n========== DASHBOARD 2: Card-wise/Account-wise Analysis ==========\n")
dash2 = queries.dashboard2_userwise_summary(sample_client_id)
for k, v in dash2.items():
    print(f"\n🔹 {k}:\n{v}\n")
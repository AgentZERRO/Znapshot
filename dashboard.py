# %%
import os
import json
import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore

# Set base directory relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Shorten wallet address


def shorten(address):
    if not address.startswith("0x") or len(address) < 10:
        return address
    return f"{address[:5]}***{address[-5:]}"


# Load Total.csv
file_path = os.path.join(base_dir, "Total.csv")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ Total.csv not found at {file_path}")

df = pd.read_csv(file_path)
df.sort_values("Holdings", ascending=False, inplace=True)

# Top 10 holders
top_10 = df.head(10).copy()
top_10["Short Address"] = top_10["Address"].apply(shorten)

print("🔝 Top 10 Token Holders:\n")
print(top_10[["Short Address", "Holdings"]].to_string(index=False))

# Plot with Plotly
fig = px.bar(
    top_10,
    x="Short Address",
    y="Holdings",
    title="Top 10 Token Holders by Total Holdings",
    labels={"Short Address": "Wallet", "Holdings": "Total Holdings"},
    text="Holdings"
)
fig.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor="#f8f8f8",
    font=dict(size=14)
)

# Save HTML
# html_output = os.path.join(base_dir, "top_10_holders_chart.html")
# fig.write_html(html_output)
# print(f"\n🌐 Interactive chart saved to: {html_output}")

# Save PNG
png_output = os.path.join(base_dir, "top_10_holders_chart.png")
fig.write_image(png_output)
print(f"🖼️ PNG chart saved to: {png_output}")

# fig.show()  # Uncomment if needed

# Generate Statistics
stats = {}
token_columns = [
    col for col in df.columns if col not in ["Address", "Holdings"]]

for token in token_columns:
    token_data = df[token]
    stats[token] = {
        "total_holders": int((token_data > 0).sum()),
        "total_tokens_held": int(token_data.sum()),
        "average_tokens": float(token_data[token_data > 0].mean()) if (token_data > 0).any() else 0.0,
        "max_tokens": int(token_data.max()),
        "min_tokens": int(token_data[token_data > 0].min()) if (token_data > 0).any() else 0
    }

# Save Statistics
stats_output = os.path.join(base_dir, "Statistics.json")
with open(stats_output, "w") as f:
    json.dump(stats, f, indent=2)
print(f"📊 Statistics saved to: {stats_output}")
# %%
